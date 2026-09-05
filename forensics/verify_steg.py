#!/usr/bin/env python3
"""Verify the steghide payload claim by replicating StegSeek's seed attack
from the real source (RickdeJager/stegseek, a steghide 0.5.1 fork):

  - JPEG embedding domain: non-zero DCT coefficients (libjpeg linear order:
    component order, block row-major, natural coefficient order)
  - EValue = |coef| % 2 ; 3 samples per vertex ; vertex bit = (sum ev) % 2
  - LCG: seed = seed * 1367208549 + 1 (mod 2^32), one step per sample
  - valIdx = sv_idx + (double)seed / 2^32 * (double)(numSamples - sv_idx)
  - header bits (LSB-first values): magic 24b = 0x73688D ("shm"),
    version unary, encalgo 5b (EncryptionAlgorithm::IRep_size=5; RIJNDAEL128=2),
    encmode 3b (EncryptionMode::IRep_size=3; CBC=1), nplainbits 32b
  - encrypted size (MCryptPP::getEncryptedSize): 128b IV + ceil(nplainbits/128)*128
    for CBC/rijndael; stream layout = [16B IV][AES-128-CBC ciphertext]
    key = MD5(passphrase) (MHashKeyGen KEYGEN_MCRYPT, MHASH_MD5, keysize 16)

Decoder validation: forensics/dc_check / per-block IDCT vs PIL: median
error 0.036 px, max 0.45 px (this file family stores components with a
-128 signed-space bias; +1024 DC-bias variants are parity-preserving, so
the embedding bits are unaffected).
"""
import sys, time
sys.path.insert(0, "forensics")
from jpeg_dct import JpegDct

A, C = 1367208549, 1
M32 = (1 << 32) - 1
MAGIC = 0x73688D
ALGOS = {0: "none", 1: "twofish", 2: "rijndael-128", 3: "rijndael-192",
         4: "rijndael-256", 5: "saferplus", 6: "rc2", 7: "xtea"}
MODES = {0: "ECB", 1: "CBC", 2: "OFB", 3: "CFB", 4: "NOFB", 5: "NCFB", 6: "CTR", 7: "STREAM"}


class BitStream:
    def __init__(self, evs, seed):
        self.evs = evs
        self.n = len(evs)
        self.seed = seed & M32
        self.sv_idx = 0
        self._bit = None

    def next_bit(self):
        if self._bit is None:
            ev = 0
            for _ in range(3):
                self.seed = (self.seed * A + C) & M32
                valIdx = self.sv_idx + int((self.seed / 4294967296.0) * (self.n - self.sv_idx))
                if valIdx >= self.n:
                    raise RuntimeError("selector past sample space")
                ev = (ev + self.evs[valIdx]) % 2
                self.sv_idx += 1
            self._bit = ev
        b = self._bit
        self._bit = None
        return b

    def read_value(self, n):
        v = 0
        for i in range(n):
            v |= self.next_bit() << i
        return v


def read_header(bs):
    magic = bs.read_value(24)
    out = dict(magic=magic, ok=(magic == MAGIC))
    if not out["ok"]:
        return out
    ver = 0
    while bs.next_bit() == 1:
        ver += 1
    out["version"] = ver
    out["algo"] = bs.read_value(5)  # EncryptionAlgorithm::IRep_size = 5; RIJNDAEL128 = 2
    out["mode"] = bs.read_value(3)  # EncryptionMode::IRep_size = 3; CBC = 1
    out["nplainbits"] = bs.read_value(32)
    return out


def analyze(fn, seed):
    t0 = time.time()
    jd = JpegDct(open(fn, "rb").read())
    # raw=True: quantized coefficients, exactly as jpeg_read_coefficients
    # returns them and as StegSeek's JpegFile.cc reads them (calcEValue =
    # |quantized coef| % 2). Dequantizing first is WRONG when the DQT has
    # values != 1 (image07's DQT is {1,2}).
    coeffs, (W, H), (maxh, maxv), _ = jd.flat_coeffs(raw=True)
    evs = [abs(c) & 1 for c in coeffs if c != 0]
    decode_t = time.time() - t0
    bs = BitStream(evs, seed)
    hdr = read_header(bs)
    hdr.update(dict(file=fn, seed=seed, num_samples=len(evs),
                    size=f"{W}x{H}", decode_s=round(decode_t, 1)))
    if hdr["ok"]:
        a, m, p = hdr["algo"], hdr["mode"], hdr["nplainbits"]
        hdr["algo_name"] = ALGOS.get(a, f"algo#{a}")
        hdr["mode_name"] = MODES.get(m, f"mode#{m}")
        if a == 0:
            hdr["enc_bits"] = p
        else:  # MCryptPP::getEncryptedSize: IV (128b for AES) + ceil(bits/128)*128
            hdr["enc_bits"] = 128 + ((p + 127) // 128) * 128
    return hdr


def main():
    targets = [
        # NOTE: image04 seed 3b75655e = H("") (XOR-fold of MD5("")) → pw "".
        # My decrypt sub-thread still fails under key=MD5("") (open bug:
        # author's build keygen or my evs pipeline). See VERDICT_PAYLOAD_CLAIM.md.
        ("image04.jpg", 0x3B75655E, "known-good: payload=steg04.jpg, pw='' (H-mapping)"),
        ("image07.jpg", 0x0F58D719, "THE CLAIM: encrypted payload, 19.3KB"),
        ("image02.jpg", 0x0F58D719, "control"),
        ("image06.jpg", 0x0F58D719, "control"),
        ("image12.jpg", 0x0F58D719, "control"),
    ]
    for fn, seed, label in targets:
        h = analyze(fn, seed)
        print(f"\n== {fn} ({label}) {h['size']} samples={h['num_samples']} [{h['decode_s']}s]")
        print(f"   seed {seed:08x}: magic=0x{h['magic']:06x} "
              f"{'*** VALID STEGHIDE PAYLOAD ***' if h['ok'] else 'no magic -> no payload'}")
        if h["ok"]:
            print(f"   version={h['version']} algo={h['algo_name']} mode={h['mode_name']} "
                  f"nplainbits={h['nplainbits']} ({h['nplainbits']/8:.1f} B plaintext)")
            print(f"   encrypted stream = {h['enc_bits']} bits = {h['enc_bits']/8:.1f} B")


if __name__ == "__main__":
    main()
