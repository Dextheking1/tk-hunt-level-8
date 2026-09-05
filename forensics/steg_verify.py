#!/usr/bin/env python3
"""Independent steghide payload-header verifier (no steghide binary).

Calibrates LSB/bit-order/offset conventions on image04.jpg (known seed
0x3b75655e = H(blank password), known payload steg04.jpg), then applies the
validated reader to image07.jpg at seed 0x0f58d719 (the claimed payload) and
to image02/06/12 at the same seed (specificity control).
"""
from PIL import Image
import hashlib, struct, sys

CHAN_ORDERS = {
    1: [((0, 0),)],
    2: [((0, 0), (1, 0))],
    3: [((0, 0), (1, 0), (2, 0))],
    4: [
        ((0, 0), (1, 0), (2, 0), (0, 1)),  # R0 G0 B0 R1
        ((0, 0), (1, 0), (2, 0), (2, 1)),  # R0 G0 B0 B1
        ((0, 0), (1, 0), (2, 0), (1, 1)),  # R0 G0 B0 G1
    ],
}

class Bits:
    def __init__(self, img, bpp, order):
        W, H = img.size
        self.cap = W * H * bpp
        self.bpp = bpp
        self.order = order
        self.px = img.load()
        W, H = img.size
        # build a bytearray of bits
        buf = bytearray(self.cap)
        i = 0
        for y in range(H):
            for x in range(W):
                r, g, b = self.px[x, y][:3]
                ch = (r, g, b)
                for (c, k) in order:
                    buf[i] = (ch[c] >> k) & 1
                    i += 1
        self.buf = buf

    def read_bytes(self, off, n):
        buf = self.buf
        out = bytearray(n)
        i = off
        for o in range(n):
            v = 0
            for _ in range(8):
                v = (v << 1) | buf[i]
                i += 1
            out[o] = v
        return bytes(out)

def find_header(bits, seed):
    off = seed % bits.cap
    hdr = bits.read_bytes(off, 14)
    if hdr[:8] != b"Steghide":
        return None
    ver, meth, bppf = hdr[8], hdr[9], hdr[10]
    size_le = struct.unpack("<H", hdr[11:13])[0]
    size_be = struct.unpack(">H", hdr[11:13])[0]
    return dict(off=off, ver=ver, meth=meth, bppf=bppf, size_le=size_le, size_be=size_be)

def calibrate():
    img4 = Image.open("image04.jpg").convert("RGB")
    seed = 0x3b75655e
    for bpp in (4, 3, 2, 1):
        for order in CHAN_ORDERS[bpp]:
            bits = Bits(img4, bpp, order)
            h = find_header(bits, seed)
            if h:
                print(f"[calib] image04 MAGIC bpp={bpp} order={order} off={h['off']} "
                      f"ver={h['ver']} meth={h['meth']} bppfield={h['bppf']} "
                      f"sizeLE={h['size_le']} sizeBE={h['size_be']}")
                return bits, h
    return None, None

def main():
    bits4, h4 = calibrate()
    if not h4:
        print("CALIBRATION FAILED: no steghide header on image04 at known seed")
        sys.exit(1)
    print("[calib] conventions validated on image04 header")
    # size field: compressed payload of steg04.jpg (48,807 B raw) -> expect ~47.7KB
    size = h4["size_le"] if 40000 < h4["size_le"] < 65000 else (h4["size_be"] if 40000 < h4["size_be"] < 65000 else None)
    print(f"[calib] image04 compressed size = {size}")
    if size:
        blob = bits4.read_bytes(h4["off"], 14 + size)
        data = blob[17:]
        key = hashlib.md5(b"").digest()
        # single-block IV probe
        good_iv = None
        for iv, label in [(b"\x00"*16, "IV=0"),
                          (key, "IV=key"),
                          (struct.pack("<I", 0x3b75655e) * 4, "IV=seed*4"),
                          (struct.pack(">I", 0x3b75655e) * 4, "IV=seedBE*4")]:
            first = aes_cbc_decrypt(data[:16], key, iv)
            if first[:2] in (b"\x78\x9c", b"\x78\xda", b"\x78\x01", b"\x78\x5e"):
                print(f"[calib] IV probe: {label} -> {first[:4].hex()} (zlib magic!)")
                good_iv = iv
                break
            else:
                print(f"[calib] IV probe: {label} -> {first[:4].hex()} (no)")
        if good_iv is not None:
            pt = aes_cbc_decrypt(data, key, good_iv)
            import zlib
            try:
                raw = zlib.decompress(pt)
                ref = open("steg04.jpg", "rb").read()
                print(f"[calib] FULL DECRYPT: len={len(raw)} match_steg04={raw == ref} "
                      f"sha256={hashlib.sha256(raw).hexdigest()[:16]}")
            except Exception as e:
                print(f"[calib] zlib failed: {e}; pt head {pt[:16].hex()}")
    # --- image07 claim ---
    img7 = Image.open("image07.jpg").convert("RGB")
    seed7 = 0x0f58d719
    print("\n[image07] checking seed 0f58d719 ...")
    for bpp in (4, 3, 2, 1):
        for order in CHAN_ORDERS[bpp]:
            bits = Bits(img7, bpp, order)
            h = find_header(bits, seed7)
            if h:
                print(f"[image07] *** MAGIC at bpp={bpp} order={order} off={h['off']} "
                      f"ver={h['ver']} meth={h['meth']} bppfield={h['bppf']} "
                      f"sizeLE={h['size_le']} sizeBE={h['size_be']}")
    # specificity control: other carriers at same seed
    for f in ("image02.jpg", "image06.jpg", "image12.jpg"):
        im = Image.open(f).convert("RGB")
        hits = []
        for bpp in (4, 3, 2, 1):
            for order in CHAN_ORDERS[bpp]:
                bits = Bits(im, bpp, order)
                if find_header(bits, seed7):
                    hits.append((bpp, order))
        print(f"[control] {f} at seed 0f58d719: {'MAGIC ' + str(hits) if hits else 'no header'}")

# ---------- pure-python AES (FIPS-197) ----------
SBOX = bytes.fromhex("637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0"
                     "b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b275"
                     "09832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cf"
                     "d0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2"
                     "cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdb"
                     "e0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08"
                     "ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9e"
                     "e1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16")
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36,0x6c,0xd8,0xab,0x4d]

def xtime(a): return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff

def gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        a = xtime(a)
        b >>= 1
    return p

def aes_expand(key):
    Nk, Nr = 4, 10
    w = [list(key[4*i:4*i+4]) for i in range(Nk)]
    for i in range(Nk, 4*(Nr+1)):
        t = list(w[i-1])
        if i % Nk == 0:
            t = t[1:] + t[:1]
            t = [SBOX[x] for x in t]
            t[0] ^= RCON[i//Nk - 1]
        elif i % Nk == 4:
            t = [SBOX[x] for x in t]
        w.append([w[i-Nk][j] ^ t[j] for j in range(4)])
    return w, Nr

def aes_block_encrypt(block, w, Nr):
    st = [list(block[4*i:4*i+4]) for i in range(4)]  # columns
    def add_round_key(r):
        for c in range(4):
            for j in range(4):
                st[c][j] ^= w[r*4+c][j]
    def sub_bytes():
        for c in range(4):
            for j in range(4):
                st[c][j] = SBOX[st[c][j]]
    def shift_rows():
        for r in range(1, 4):
            col = [st[c][r] for c in range(4)]
            col = col[r:] + col[:r]
            for c in range(4):
                st[c][r] = col[c]
    def mix_columns():
        for c in range(4):
            a = st[c]
            st[c] = [gmul(a[0],2)^gmul(a[1],3)^a[2]^a[3],
                     a[0]^gmul(a[1],2)^gmul(a[2],3)^a[3],
                     a[0]^a[1]^gmul(a[2],2)^gmul(a[3],3),
                     gmul(a[0],3)^a[1]^a[2]^gmul(a[3],2)]
    add_round_key(0)
    for r in range(1, Nr):
        sub_bytes(); shift_rows(); mix_columns(); add_round_key(r)
    sub_bytes(); shift_rows(); add_round_key(Nr)
    out = bytearray(16)
    for c in range(4):
        for j in range(4):
            out[4*c+j] = st[c][j]
    return bytes(out)

def aes_cbc_decrypt(data, key, iv):
    w, Nr = aes_expand(key)
    out = bytearray()
    prev = iv
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        dec = aes_block_decrypt(blk, w, Nr)
        out += bytes(a ^ b for a, b in zip(dec, prev))
        prev = blk
    return bytes(out)

def aes_block_decrypt(block, w, Nr):
    inv_w, _ = aes_expand_inv(key_from_w(w)) if False else (None, None)
    # use forward keys with inverse cipher
    st = [list(block[4*i:4*i+4]) for i in range(4)]
    def add_round_key(r):
        for c in range(4):
            for j in range(4):
                st[c][j] ^= w[r*4+c][j]
    ISBOX = [0] * 256
    for i in range(256): ISBOX[SBOX[i]] = i
    def inv_sub_bytes():
        for c in range(4):
            for j in range(4):
                st[c][j] = ISBOX[st[c][j]]
    def inv_shift_rows():
        for r in range(1, 4):
            col = [st[c][r] for c in range(4)]
            col = col[-r:] + col[:-r]
            for c in range(4):
                st[c][r] = col[c]
    def inv_mix_columns():
        for c in range(4):
            a = st[c]
            st[c] = [gmul(a[0],14)^gmul(a[1],11)^gmul(a[2],13)^gmul(a[3],9),
                     gmul(a[0],9)^gmul(a[1],14)^gmul(a[2],11)^gmul(a[3],13),
                     gmul(a[0],13)^gmul(a[1],9)^gmul(a[2],14)^gmul(a[3],11),
                     gmul(a[0],11)^gmul(a[1],13)^gmul(a[2],9)^gmul(a[3],14)]
    add_round_key(Nr)
    for r in range(Nr-1, 0, -1):
        inv_shift_rows(); inv_sub_bytes(); add_round_key(r); inv_mix_columns()
    inv_shift_rows(); inv_sub_bytes(); add_round_key(0)
    out = bytearray(16)
    for c in range(4):
        for j in range(4):
            out[4*c+j] = st[c][j]
    return bytes(out)

def key_from_w(w):
    return bytes(w[0][0], w[1][0], w[2][0], w[3][0])

def decrypt_cbc(data, key):
    return None

if __name__ == "__main__":
    main()
