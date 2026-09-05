#!/usr/bin/env python3
"""Stronger decoder validation: float IDCT on a random sample of blocks,
compare reconstructed Y (and Cb/Cr) against PIL pixels. If the coefficient
decoder is wrong, the IDCT output won't match the visible image."""
import sys, time, random
sys.path.insert(0, "forensics")
from jpeg_dct import JpegDct
from PIL import Image


def idct8(a):
    """a: flat 64 natural-order coefficients -> flat 64 float samples (row-major)."""
    # 1D IDCT: out[n] = sum_k C(k) a[k] cos((2n+1)k pi/16), C(0)=1/sqrt(2)
    import math
    COS = [[math.cos((2 * n + 1) * k * math.pi / 16) for k in range(8)] for n in range(8)]
    C = [math.cos(math.pi / 16)] * 8  # placeholder
    CK = [1 / math.sqrt(2)] + [1.0] * 7
    def idct1d(x):
        return [sum(CK[k] * COS[n][k] * x[k] for k in range(8)) for n in range(8)]
    # rows
    rows = []
    for u in range(8):
        row = a[u * 8:(u + 1) * 8]
        rows.append(idct1d(row))
    # columns
    out = [0.0] * 64
    for v in range(8):
        col = [rows[u][v] for u in range(8)]
        dc = idct1d(col)
        for u in range(8):
            out[u * 8 + v] = 0.25 * dc[u]
    return out


def check(fn, seed=42, nblocks=200):
    t0 = time.time()
    jd = JpegDct(open(fn, "rb").read())
    grids, W, H, maxh, maxv = jd.decode()
    pil = Image.open(fn).convert("RGB")
    raw = pil.tobytes()
    stride = W * 3
    ids = [c["id"] for c in jd.sof["comps"]]
    rng = random.Random(seed)
    all_diffs = {}
    for cid, (n, worst, bad) in {c["id"]: (None, 0, 0) for c in jd.sof["comps"]}.items():
        all_diffs[cid] = []
    for cid in ids:
        c = next(cc for cc in jd.sof["comps"] if cc["id"] == cid)
        g = grids[cid]
        hb, wb = len(g), len(g[0])
        comp_idx = ids.index(cid)
        for _ in range(nblocks):
            r = rng.randrange(hb)
            cc = rng.randrange(wb)
            rec = idct8(g[r][cc])
            x0, y0 = cc * 8, r * 8
            worst = 0.0
            for u in range(8):
                for v in range(8):
                    yy = min(y0 + u, H - 1)
                    xx = min(x0 + v, W - 1)
                    off = yy * stride + xx * 3
                    R, G, B = raw[off], raw[off + 1], raw[off + 2]
                    if comp_idx == 0:
                        ref = 0.299 * R + 0.587 * G + 0.114 * B
                    elif comp_idx == 1:
                        ref = 128 - 0.168736 * R - 0.331264 * G + 0.5 * B
                    else:
                        ref = 0.5 * R - 0.418688 * G - 0.081312 * B
                    d = abs(rec[u * 8 + v] - ref)
                    if d > worst:
                        worst = d
            all_diffs[cid].append(worst)
    out = {}
    for cid in ids:
        ds = all_diffs[cid]
        out[cid] = (sum(ds) / len(ds), max(ds))
    return out, time.time() - t0


if __name__ == "__main__":
    for fn in sys.argv[1:] or ["image04.jpg"]:
        out, dt = check(fn)
        parts = [f"comp{cid}: mean={m:.2f} worst={w:.2f}" for cid, (m, w) in out.items()]
        print(f"{fn}: {' '.join(parts)} ({dt:.1f}s)")
