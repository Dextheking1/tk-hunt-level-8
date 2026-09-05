#!/usr/bin/env python3
"""Validate the DCT coefficient decoder (full decode): the DC coeff equals
the sum of the 64 sample values, so c0/8 == block sample mean. The JPEG
components are Y/Cb/Cr; compare against PIL's RGB converted with the exact
IJG YCbCr formulas."""
import sys, time
sys.path.insert(0, "forensics")
from jpeg_dct import JpegDct
from PIL import Image


def ijjg_rgb2ycbcr(r, g, b):
    # IJG int formula (jsamplecol / rgb.ycc)
    y = 98 * r + 192 * g + 38 * b + 32768
    cb = -38 * r - 74 * g + 112 * b + 32768 + 8388608
    cr = 112 * r - 94 * g - 18 * b + 32768 + 8388608
    return (y >> 16), (cb >> 16), (cr >> 16)


def dc_check(fn):
    t0 = time.time()
    d = JpegDct(open(fn, "rb").read())
    W, H = d.sof["w"], d.sof["h"]
    grids, _, _, _, _ = d.decode()  # full decode: AC bits must be consumed
    pil = Image.open(fn).convert("RGB")
    raw = pil.tobytes()
    stride = W * 3
    ids = [c["id"] for c in d.sof["comps"]]
    res = {}
    for c in d.sof["comps"]:
        cid = c["id"]
        g = grids[cid]
        hb, wb = len(g), len(g[0])
        comp_idx = ids.index(cid)  # 0=Y, 1=Cb, 2=Cr
        worst = 0.0
        bad = 0
        n = 0
        for r in range(hb):
            for cc in range(wb):
                c0 = g[r][cc][0]
                expected_mean = c0 / 8.0
                x0, y0 = cc * 8, r * 8
                s = 0
                for u in range(8):
                    yy = min(y0 + u, H - 1)
                    row_off = yy * stride + x0 * 3
                    for v in range(8):
                        xx = min(v, W - 1 - x0)
                        off = row_off + xx * 3
                        if comp_idx == 0:
                            val = ijjg_rgb2ycbcr(raw[off], raw[off + 1], raw[off + 2])[0]
                        elif comp_idx == 1:
                            val = ijjg_rgb2ycbcr(raw[off], raw[off + 1], raw[off + 2])[1]
                        else:
                            val = ijjg_rgb2ycbcr(raw[off], raw[off + 1], raw[off + 2])[2]
                        s += val
                actual_mean = s / 64
                diff = abs(expected_mean - actual_mean)
                n += 1
                if diff > worst:
                    worst = diff
                if diff > 2.0:
                    bad += 1
        res[cid] = (n, worst, bad)
    dt = time.time() - t0
    return res, dt


if __name__ == "__main__":
    for fn in sys.argv[1:] or ["image04.jpg", "image07.jpg"]:
        res, dt = dc_check(fn)
        parts = [f"comp{cid}: n={n} worst={w:.3f} bad={b}" for cid, (n, w, b) in res.items()]
        print(f"{fn}: {' '.join(parts)} ({dt:.1f}s)")
