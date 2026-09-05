#!/usr/bin/env python3
"""Baseline JPEG decoder producing exact integer DCT coefficients,
ordered exactly like libjpeg's jpeg_read_coefficients (component order,
block row-major, natural coefficient order).

Optimized: int-keyed Huffman tables, byte-cursor bit reader.
DC-only fast path available for validation (dc_only()).
"""

# natural index -> zigzag step
ZIGZAG = [
    0, 1, 8, 16, 9, 2, 3, 10,
    17, 24, 32, 25, 18, 11, 4, 5,
    12, 19, 26, 33, 40, 48, 41, 34,
    27, 20, 13, 6, 7, 14, 21, 28,
    35, 42, 49, 56, 57, 50, 43, 36,
    29, 22, 15, 23, 30, 37, 44, 51,
    58, 59, 52, 45, 38, 31, 39, 46,
    53, 60, 61, 54, 47, 55, 62, 63,
]
NAT_BY_ZZ = [0] * 64
for _n, _z in enumerate(ZIGZAG):
    NAT_BY_ZZ[_z] = _n


class Huff:
    def __init__(self, counts, syms):
        tab = {}
        code = 0
        k = 0
        for length in range(1, 17):
            for _ in range(counts[length - 1]):
                tab[code | (length << 16)] = syms[k]
                k += 1
                code += 1
            code <<= 1
        self.tab = tab


class BitReader:
    __slots__ = ("data", "pos", "n")

    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.n = len(data)


def decode_mcus(jd, dc_only=False, raw=False):
    """Decode all blocks. Returns (grids, W, H, maxh, maxv).
    grids: {comp_id: [[64-int list]]}; if dc_only, blocks hold [dc, 0..0]."""
    d = jd.data
    sof = jd.sof
    W, H = sof["w"], sof["h"]
    maxh = max(c["h"] for c in sof["comps"])
    maxv = max(c["v"] for c in sof["comps"])
    ent = jd.entropy
    pos = 0
    n = len(ent)

    compmap = {c["id"]: c for c in sof["comps"]}
    grids = {}
    for c in sof["comps"]:
        hb = -(-(H * c["v"]) // (8 * maxv))
        wb = -(-(W * c["h"]) // (8 * maxh))
        grids[c["id"]] = [[None] * wb for _ in range(hb)]

    n_mcu_w = -(-W // (8 * maxh))
    n_mcu_h = -(-H // (8 * maxv))

    dc_pred = {c["id"]: 0 for c in sof["comps"]}

    # per-component decoded tables / qtables
    dc_tabs = {}
    ac_tabs = {}
    qtabs = {}
    for cid, dc_t, ac_t in jd.sos_comps:
        c = compmap[cid]
        dc_tabs[cid] = jd.dctabs[dc_t].tab
        qtabs[cid] = jd.qtables[c["qid"]]
        if not dc_only:
            ac_tabs[cid] = jd.actabs[ac_t].tab

    cur = 0
    nbits = 0

    def getbit():
        nonlocal cur, nbits, pos
        if nbits == 0:
            if pos >= n:
                return 0
            byte = ent[pos]
            pos += 1
            if byte == 0xFF:
                if pos >= n:
                    return 0
                nb = ent[pos]
                pos += 1
                if nb != 0x00:
                    return 0  # marker mid-scan: data over
                cur = 0xFF
            else:
                cur = byte
            nbits = 8
        nbits -= 1
        return (cur >> nbits) & 1

    def huff(tab):
        code = 0
        length = 0
        while True:
            code = (code << 1) | getbit()
            length += 1
            sym = tab.get(code | (length << 16))
            if sym is not None:
                return sym
            if length > 16:
                raise ValueError(f"invalid huffman code @block {mrow},{mcol},{cid} pos={pos}/{n}")

    def getbits(k):
        v = 0
        for _ in range(k):
            v = (v << 1) | getbit()
        return v

    def ext(v, k):
        if v < (1 << (k - 1)):
            v -= (1 << k) - 1
        return v

    nat_by_zz = NAT_BY_ZZ
    for mrow in range(n_mcu_h):
        for mcol in range(n_mcu_w):
            for cid, _dc_t, _ac_t in jd.sos_comps:
                c = compmap[cid]
                dtab = dc_tabs[cid]
                atab = ac_tabs.get(cid)
                qt = qtabs.get(cid)
                for r in range(c["v"]):
                    for s in range(c["h"]):
                        cat = huff(dtab)
                        if cat:
                            v = getbits(cat)
                            dc = dc_pred[cid] + ext(v, cat)
                        else:
                            dc = dc_pred[cid]
                        dc_pred[cid] = dc
                        if dc_only:
                            blk = [dc * qt[0]] + [0] * 63
                        else:
                            coeff = [0] * 64
                            coeff[0] = dc
                            k = 1
                            while k < 64:
                                rs = huff(atab)
                                run = rs >> 4
                                size = rs & 0xF
                                if size == 0:
                                    if run == 0xF:
                                        k += 16
                                        continue
                                    break
                                k += run
                                if k > 63:
                                    raise ValueError("AC overrun")
                                v = getbits(size)
                                coeff[k] = ext(v, size)
                                k += 1
                            blk = [0] * 64
                            for z in range(64):
                                # raw=True: keep quantized values (what libjpeg's
                                # coefficient array / StegSeek sees); else dequantize
                                blk[ZIGZAG[z]] = coeff[z] * (1 if raw else qt[z])  # natural = ZIGZAG[step]
                        rr = mrow * maxv + r
                        cc = mcol * maxh + s
                        if rr < len(grids[cid]) and cc < len(grids[cid][0]):
                            grids[cid][rr][cc] = blk
    return grids, W, H, maxh, maxv


class JpegDct:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        if data[0] != 0xFF or data[1] != 0xD8:
            raise ValueError("not a JPEG")
        self.pos = 2
        self.qtables = {}
        self.sof = None
        self.dctabs = {}
        self.actabs = {}
        self.sos = None
        self.entropy = None
        self.sos_comps = None
        self._parse()

    def _marker(self):
        d = self.data
        if d[self.pos] != 0xFF:
            raise ValueError(f"expected marker at {self.pos}")
        while d[self.pos] == 0xFF:
            self.pos += 1
        m = d[self.pos]
        self.pos += 1
        return m

    def _parse(self):
        d = self.data
        while True:
            m = self._marker()
            if m == 0xD8:
                continue
            if m == 0xD9:
                return
            if m == 0xDA:  # SOS
                (seglen,) = __import__("struct").unpack(">H", d[self.pos:self.pos + 2])
                self.pos += 2
                ncomp = d[self.pos]
                self.sos_comps = []
                self.pos += 1
                for _ in range(ncomp):
                    cid, ta = d[self.pos], d[self.pos + 1]
                    self.sos_comps.append((cid, ta >> 4, ta & 0xF))
                    self.pos += 2
                self.pos += 3
                start = self.pos
                i = start
                while i < len(d) - 1:
                    if d[i] == 0xFF and d[i + 1] != 0x00:
                        if d[i + 1] == 0xFF:
                            i += 1
                            continue
                        break
                    i += 1
                self.entropy = d[start:i + 1]
                self.pos = i + 1
                return
            if m == 0x01:
                continue
            if 0xD0 <= m <= 0xD7:
                continue
            (seglen,) = __import__("struct").unpack(">H", d[self.pos:self.pos + 2])
            body = d[self.pos + 2:self.pos + seglen]
            self.pos += seglen
            if m == 0xDB:  # DQT — libjpeg convention: prec=upper nibble, idx=lower
                p = 0
                while p < len(body):
                    prec = body[p] >> 4
                    qid = body[p] & 0xF
                    p += 1
                    if prec:
                        vals = list(__import__("struct").unpack(">64H", body[p:p + 128]))
                        p += 128
                    else:
                        vals = list(body[p:p + 64])
                        p += 64
                    self.qtables[qid] = vals
            elif m == 0xC0:  # SOF0
                precision = body[0]
                h, w = __import__("struct").unpack(">HH", body[1:5])
                ncomp = body[5]
                comps = []
                p = 6
                for _ in range(ncomp):
                    cid, sampling, qid = body[p], body[p + 1], body[p + 2]
                    comps.append(dict(id=cid, h=(sampling >> 4) & 0xF,
                                      v=(sampling & 0xF), qid=qid))
                    p += 3
                self.sof = dict(precision=precision, h=h, w=w, comps=comps)
            elif m == 0xC2:
                raise ValueError("progressive JPEG not supported")
            elif m == 0xC4:  # DHT
                p = 0
                while p < len(body):
                    tc = body[p] >> 4
                    tid = body[p] & 0xF
                    p += 1
                    counts = list(body[p:p + 16])
                    p += 16
                    nsym = sum(counts)
                    syms = list(body[p:p + nsym])
                    p += nsym
                    tab = Huff(counts, syms)
                    if tc == 0:
                        self.dctabs[tid] = tab
                    else:
                        self.actabs[tid] = tab

    def decode(self, dc_only=False, raw=False):
        return decode_mcus(self, dc_only=dc_only, raw=raw)

    def flat_coeffs(self, raw=False):
        """Coefficients in JpegFile.cc order (component, block row-major,
        icoeff 0..63). raw=True = quantized values, exactly as
        jpeg_read_coefficients returns them (what StegSeek sees);
        raw=False = dequantized."""
        grids, W, H, maxh, maxv = self.decode(raw=raw)
        out = []
        for c in self.sof["comps"]:
            g = grids[c["id"]]
            for row in g:
                for blk in row:
                    if blk is not None:  # 4:2:0 edge padding rows (JpegFile only reads
                        out.extend(blk)  # HeightInBlocks/WidthInBlocks rows)
        return out, (W, H), (maxh, maxv), grids
