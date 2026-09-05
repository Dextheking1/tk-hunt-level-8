#!/usr/bin/env python3
"""Full end-to-end proof: extract the ENTIRE embedded bitstream from image04
(seed 3b75655e = H('')), decrypt AES-128-CBC with key = MD5('') and verify the
payload is the known steghide envelope (zlib -> JPEG).

If this decrypts to a valid zlib stream, the extraction pipeline is bit-exact
and the image07 'no magic' result is a genuine refutation of the claim.
"""
import sys, time, hashlib, zlib
sys.path.insert(0, "forensics")
from jpeg_dct import JpegDct
from verify_steg import BitStream, read_header, MAGIC

# ---------- pure-python AES-128 (FIPS-197) ----------
SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]

def _xtime(a):
    a <<= 1
    if a & 0x100:
        a ^= 0x11b
    return a & 0xFF

def _gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        a = _xtime(a)
        b >>= 1
    return p & 0xFF

def _expand_key(key):
    Nk, Nr = 4, 10
    w = [key[4*i:4*i+4] for i in range(Nk)]
    for i in range(Nk, 4*(Nr+1)):
        temp = w[i-1][:]
        if i % Nk == 0:
            temp = temp[1:] + temp[:1]
            temp = bytes(SBOX[b] for b in temp)
            temp = bytes([temp[0] ^ RCON[i//Nk - 1]] + list(temp[1:]))
        w.append(bytes(a ^ b for a, b in zip(w[i-Nk], temp)))
    return w

def _add_round_key(st, w, rnd):
    return [row[:4] and bytes(st[r+c*4] ^ w[rnd*4+c][r] for c in range(4))
            for r in range(4)] if False else None

INV_SBOX = [0] * 256
for _i, _v in enumerate(SBOX):
    INV_SBOX[_v] = _i


def _inv_block(block, w):
    # equivalent inverse cipher (FIPS-197 section 5.3.5): same structure,
    # inverse S-box, inverse mix-columns, reversed round keys.
    st = [[block[r + 4*c] for c in range(4)] for r in range(4)]

    def add_rk(round_):
        for c in range(4):
            for r in range(4):
                st[r][c] ^= w[round_*4 + c][r]

    def inv_sub_bytes():
        for r in range(4):
            for c in range(4):
                st[r][c] = INV_SBOX[st[r][c]]

    def inv_shift_rows():
        for r in range(1, 4):
            st[r] = st[r][-r:] + st[r][:-r]

    def inv_mix_cols():
        for c in range(4):
            col = [st[r][c] for r in range(4)]
            out = [
                _gmul(col[0],14) ^ _gmul(col[1],11) ^ _gmul(col[2],13) ^ _gmul(col[3],9),
                _gmul(col[0],9)  ^ _gmul(col[1],14) ^ _gmul(col[2],11) ^ _gmul(col[3],13),
                _gmul(col[0],13) ^ _gmul(col[1],9)  ^ _gmul(col[2],14) ^ _gmul(col[3],11),
                _gmul(col[0],11) ^ _gmul(col[1],13) ^ _gmul(col[2],9)  ^ _gmul(col[3],14),
            ]
            for r in range(4):
                st[r][c] = out[r]

    add_rk(10)
    for rnd in range(9, 0, -1):
        inv_sub_bytes(); inv_shift_rows(); add_rk(rnd); inv_mix_cols()
    inv_sub_bytes(); inv_shift_rows(); add_rk(0)
    return bytes(st[r][c] for c in range(4) for r in range(4))


def _aes_block(block, w):
    # state: 4x4 column-major from 16-byte block
    st = [[block[r + 4*c] for c in range(4)] for r in range(4)]

    def add_rk(round_):
        for c in range(4):
            for r in range(4):
                st[r][c] ^= w[round_*4 + c][r]

    def sub_bytes():
        for r in range(4):
            for c in range(4):
                st[r][c] = SBOX[st[r][c]]

    def shift_rows():
        for r in range(1, 4):
            st[r] = st[r][r:] + st[r][:r]

    def mix_cols():
        for c in range(4):
            col = [st[r][c] for r in range(4)]
            out = [
                _gmul(col[0],2) ^ _gmul(col[1],3) ^ col[2] ^ col[3],
                col[0] ^ _gmul(col[1],2) ^ _gmul(col[2],3) ^ col[3],
                col[0] ^ col[1] ^ _gmul(col[2],2) ^ _gmul(col[3],3),
                _gmul(col[0],3) ^ col[1] ^ col[2] ^ _gmul(col[3],2),
            ]
            for r in range(4):
                st[r][c] = out[r]

    add_rk(0)
    for rnd in range(1, 10):
        sub_bytes(); shift_rows(); mix_cols(); add_rk(rnd)
    sub_bytes(); shift_rows(); add_rk(10)
    return bytes(st[r][c] for c in range(4) for r in range(4))

def aes_cbc_decrypt(ciphertext, key, iv):
    w = _expand_key(key)
    out = b""
    prev = iv
    for i in range(0, len(ciphertext), 16):
        blk = ciphertext[i:i+16]
        dec = _inv_block(blk, w)
        out += bytes(a ^ b for a, b in zip(dec, prev))
        prev = blk
    return out

# ---------- main ----------
def main():
    fn, seed, expected_pw = "image04.jpg", 0x3B75655E, ""
    t0 = time.time()
    jd = JpegDct(open(fn, "rb").read())
    coeffs, (W, H), (maxh, maxv), _ = jd.flat_coeffs(raw=True)
    evs = [abs(c) & 1 for c in coeffs if c != 0]
    n = len(evs)
    bs = BitStream(evs, seed)
    hdr = read_header(bs)
    print(f"magic=0x{hdr['magic']:06x} valid={hdr['ok']}")
    assert hdr["ok"], "magic failed"
    a, m, p = hdr["algo"], hdr["mode"], hdr["nplainbits"]
    print(f"algo={a} mode={m} nplainbits={p} version={hdr['version']}")
    enc_bits = 128 + ((p + 127) // 128) * 128
    total = 24 + hdr["version"] * 0 + 1 + 5 + 3 + 32 + enc_bits  # header + stream
    # version unary cost = version+1 bits
    total = 24 + (hdr["version"] + 1) + 5 + 3 + 32 + enc_bits
    print(f"encrypted stream: {enc_bits/8:.1f} B; total bits to read: {total}")

    def bits_to_bytes(kbits):
        v = 0
        sh = 0
        out = bytearray()
        for _ in range(kbits):
            v |= bs.next_bit() << sh
            sh += 1
            if sh == 8:
                out.append(v & 0xFF)
                v = 0; sh = 0
        return bytes(out)

    stream = bits_to_bytes(enc_bits)
    print(f"stream extracted: {len(stream)} B; first 16B (IV): {stream[:16].hex()}")
    key = hashlib.md5(expected_pw.encode()).digest()
    print(f"key MD5({expected_pw!r}) = {key.hex()}")
    pt = aes_cbc_decrypt(stream[16:], key, stream[:16])
    print(f"plaintext: {len(pt)} B; first 16B: {pt[:16].hex()}")
    open("/tmp/steg04_plain.bin", "wb").write(pt)

    # steghide plaintext layout: 1-bit compression flag (LSB), then if 1:
    # 31-bit nuncobits, 1-bit checksum, 32-bit crc32, then data...
    # LSB-first bit string -> take first bit
    b0 = pt[0] & 1
    print(f"compression flag bit = {b0}")
    if b0:
        # next 31 bits LSB-first = nuncobits
        val = 0
        sh = 1
        nuncobits = 0
        for i in range(31):
            v = (pt[sh >> 3] >> (sh & 7)) & 1
            nuncobits |= v << i
            sh += 1
        print(f"nuncobits = {nuncobits} ({nuncobits/8:.1f} B data field)")
        rest_bits = sh
        checksum = (pt[rest_bits >> 3] >> (rest_bits & 7)) & 1
        rest_bits += 1
        crcv = 0
        for i in range(32):
            v = (pt[rest_bits >> 3] >> (rest_bits & 7)) & 1
            crcv |= v << i
            rest_bits += 1
        print(f"checksum bit = {checksum}, crc32 field = 0x{crcv:08x}")
        data = bytearray()
        b = rest_bits
        while b + 8 <= len(pt) * 8:
            byte = 0
            for i in range(8):
                byte |= (pt[b >> 3] >> (b & 7)) & 1 << i
                b += 1
            data.append(byte)
        data = bytes(data)
        print(f"payload field: {len(data)} B, magic: {data[:4].hex()}")
        if data[:1] == b"\x78":
            dec = zlib.decompress(data)
            print(f"ZLIB DECOMPRESSED: {len(dec)} B, magic: {dec[:4].hex()}")
            open("/tmp/steg04_extracted.jpg", "wb").write(dec)
            ok = dec[:2] == b"\xff\xd8" and dec[-2:] == b"\xff\xd9"
            print(f"*** VALID JPEG: {ok} ***")
        else:
            print("payload does not start with zlib 0x78")

if __name__ == "__main__":
    main()
