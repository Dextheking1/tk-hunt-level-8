#!/usr/bin/env python3
"""Convention brute-force: find the steghide bit layout that yields the
"Steghide" magic at image04's known seed 0x3b75655e."""
from PIL import Image
import struct

img4 = Image.open("image04.jpg").convert("RGB")
W, H = img4.size
px = img4.load()
print("image04", W, H)
SEED = 0x3b75655e
MD5_BLANK = bytes.fromhex("d41d8cd98f00b204e9800998ecf8427e")
BLOCKS = [0x3b75655e] + [struct.unpack(">I", MD5_BLANK[4*i:4*i+4])[0] for i in range(4)]
BLOCKS_LE = [0x3b75655e] + [struct.unpack("<I", MD5_BLANK[4*i:4*i+4])[0] for i in range(4)]
print("offset candidates:", [hex(b) for b in BLOCKS + BLOCKS_LE])

def ch_bit(x, y, ch, k):
    r, g, b = px[x, y][:3]
    return ((r, g, b)[ch] >> k) & 1

# candidate per-pixel bit patterns (channel, bit-index) for j=0..bpp-1
PATTERNS = {
    1: [((0, 0),)],
    2: [((0, 0), (1, 0)), ((0, 0), (2, 0)), ((1, 0), (0, 0))],
    3: [((0, 0), (1, 0), (2, 0)), ((2, 0), (1, 0), (0, 0)),
        ((0, 0), (2, 0), (1, 0)), ((1, 0), (0, 0), (2, 0))],
    4: [((0, 0), (1, 0), (2, 0), (0, 1)),
        ((0, 0), (1, 0), (2, 0), (2, 1)),
        ((0, 0), (1, 0), (2, 0), (1, 1)),
        ((2, 0), (2, 1), (1, 0), (1, 1)),   # 24-bit-LE: B0 B1 G0 G1
        ((0, 0), (0, 1), (1, 0), (1, 1)),   # R0 R1 G0 G1
        ((2, 0), (1, 0), (0, 0), (2, 1)),   # B0 G0 R0 B1
        ((1, 0), (0, 0), (2, 0), (1, 1)),   # G0 R0 B0 G1
        ((0, 0), (2, 0), (1, 0), (0, 1)),   # R0 B0 G0 R1
        ((2, 0), (0, 0), (1, 0), (2, 1)),   # B0 R0 G0 B1
    ],
}

def check(bpp, pattern, layout, lsb_first, off):
    cap = W * H * bpp
    def bit_at(i):
        if layout == "pix":
            p = i // bpp
            j = i % bpp
            x = p % W
            y = p // W
            c, k = pattern[j]
            b = ch_bit(x, y, c, k)
        else:  # plane-major: plane = j, position within plane = i//bpp... 
            # plane p contains W*H bits; bit i: plane = i // (W*H)?? no:
            # layout: for j in 0..bpp-1: for p in 0..W*H-1: bit(pattern[j] of pixel p)
            plane = i // (W * H)
            pos = i % (W * H)
            x = pos % W
            y = pos // W
            c, k = pattern[plane]
            b = ch_bit(x, y, c, k)
        return b
    out = bytearray()
    for o in range(14):
        v = 0
        for bidx in range(8):
            bit = bit_at(off + o * 8 + (7 - bidx if lsb_first else bidx))
            v = (v << 1) | bit
        out.append(v)
    return bytes(out)

hits = []
offsets = []
for bpp in (4, 3, 2, 1):
    cap = W * H * bpp
    for b in BLOCKS + BLOCKS_LE:
        offsets.append((b % cap, b))
seen = set()
for bpp in (4, 3, 2, 1):
    for pat in PATTERNS[bpp]:
        for layout in ("pix", "plane"):
            for lsb_first in (False, True):
                cap = W * H * bpp
                for off, raw in offsets:
                    if (off, bpp, layout, lsb_first) in seen: continue
                    seen.add((off, bpp, layout, lsb_first))
                    try:
                        hdr = check(bpp, pat, layout, lsb_first, off)
                    except IndexError:
                        continue
                    if hdr[:8] == b"Steghide":
                        hits.append((bpp, pat, layout, lsb_first, raw, off, hdr))
                        print(f"MAGIC: bpp={bpp} pat={pat} layout={layout} lsbfirst={lsb_first} "
                              f"rawseed={raw:08x} off={off}")
                        print(f"  ver={hdr[8]} meth={hdr[9]} bppf={hdr[10]} "
                              f"sizeLE={struct.unpack('<H',hdr[11:13])[0]} sizeBE={struct.unpack('>H',hdr[11:13])[0]}")
if not hits:
    print("no magic found in convention x offset space")
