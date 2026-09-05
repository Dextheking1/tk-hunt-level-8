# VERDICT — "image07.jpg contains an encrypted steghide payload"

**Date:** 2026-09-05 · **Requested by:** user ("Verify that payload claim")
**Verdict: CONFIRMED — strongest form possible, and now independently
re-confirmed by a full 2^32 seed-space scan with proper controls.**

## Claim under test

Swarm finding: `image07.jpg` carries an encrypted steghide payload (~19.3 KB),
originally reported with magic `0xb3eb88`.

## Confirmed facts (two independent pipelines, bit-exact)

| fact | value |
|---|---|
| carrier | `image07.jpg` (1200×900, 4:4:4, 956,205 B) |
| seed | `0f58d719` |
| magic | **`0x73688d`** (real steghide magic; the original `0xb3eb88` was an artifact — see below) |
| version | 0 |
| algo / mode | rijndael-128 / CBC |
| nplainbits | **157,865** (plaintext 19,733.1 B) |
| encrypted stream | 158,080 bits = **19,760 B** (IV 16 B + 19,744 B ciphertext) |

Pipeline (a) — **C + libjpeg.so.62**: `forensics/jpegmini.h` +
`forensics/crosscheck.c` / `forensics/streamdump.c` / `forensics/dumpcoef.c`.
Real libjpeg coefficient table, StegSeek LCG (A=1367208549, C=1).

Pipeline (b) — **pure Python**: `forensics/jpeg_dct.py` (RAW mode: reads
quantized DCT coefficients exactly as libjpeg sees them — the original
`0xb3eb88` claim came from a dequantization bug in this file, since fixed) +
`forensics/verify_steg.py`.

**Stream bit-identity C vs Python:** image07 = **158,079 bits identical**;
image04 (positive control) = **390,527 bits identical**. Extraction is proven
exact, not merely plausible.

**Independent confirmation (swarm, 2026-09-05, commit f02ddfa):** full 2^32
`stegseek --seed` scans — image04 HIT (seed 3b75655e + metadata), image07 HIT
(seed 0f58d719 + metadata), image02 MISS, fresh synthetic JPEG MISS.
Scorecard: payload files produce seed+metadata, clean files demonstrably do
not. This is the exact control my single-seed negatives (image07@3b75655e →
0x863f82; image02/06/12@0f58d719 → no magic) approximated.

## Format facts established (source + arithmetic, 2026-09-05)

1. **Steghide JPEG = 3 samples per vertex** (stegseek fork `JpegFile.h`:
   `SamplesPerVertex = 3`; each embedded bit written redundantly into 3
   non-zero DCT coefficients; vertex bit = parity of the 3). Capacity =
   numSamples/3 bits — matches swarm-reported capacities exactly (image07:
   1,367,317/3/8 = 56,971 B = 55.6 KB ✓).
2. **Seed↔passphrase mapping**: `seed = LE32(MD5(p)[0:4] ⊕ MD5(p)[4:8] ⊕
   MD5(p)[8:12] ⊕ MD5(p)[12:16])`. Validated by the swarm on 7 synthetic
   embeddings (empty, a, abc, test, planet, 8675309,
   correcthorsebatterystaple) + cover-independence control
   (`PREREG_STEGHIDE_SEED_MAPPING.md`). StegSeek 0.6's own `-p` mode
   implements exactly this (`Cracker.cc::verifyMagic(Passphrase)`).
3. **image04 passphrase = "" — my earlier "refutation" is WITHDRAWN.**
   Arithmetic: `MD5("") = d41d8cd9 8f00b204 e9800998 ecf8427e`;
   LE-quarter XOR fold = `3b75655e` = image04's seed exactly. Under the
   validated mapping the passphrase is the empty string, matching the swarm's
   documented `steghide extract -sf image04.jpg -p ""` extraction of
   `hidden/steg04.jpg` (48,807 B, sha256 7643d732…).

## Decryption sub-thread (OPEN — bug localized to my side or the author's build)

- AES-128-CBC verified vs pycryptodome (pre-reset; FIPS C.1 re-checked post-
  reset). Key derivation for *vanilla* steghide proven from mhash source:
  MD5(passphrase).
- image04 stream facts (proven): IV `9bb27b71cea8de6d8f829c14b12dcc58`,
  C0 `e37d80f56244a9981416fb60e44060d8`.
- A 49-bit decrypt-prefix oracle (nuncobits variants × zlib levels;
  false-positive ≈ 2⁻⁴⁸/candidate) rejects key = MD5("") at every stream
  offset 33–73, ECB, reversed-IV, and 20+ alternate key derivations
  (fold bytes padded/repeated, MD5 of fold hex, SHA1/256 prefixes, …).
- Since ground truth says passphrase = "" (seed arithmetic + successful
  extraction with the swarm's build), the failure is NOT a wrong passphrase.
  It is either (a) **the author's steghide build uses non-standard key
  derivation** (the swarm's build — which did the extraction and the
  LD_PRELOAD mhash traces — is not vanilla 0.5.1: it also hardwires
  seed = H(pw)), or (b) a subtle bug in my coefficient/evs pipeline that
  only a known-answer test can expose.
- **To close:** one of the swarm's 8 synthetic carriers (known passphrase +
  payload, e.g. `test` → seed `cb4257a3`) or the author's steghide binary.
  A known-answer run through `forensics/verify_steg.py` + decrypt settles
  (a) vs (b) in one shot.

**Consequence for the payload verdict: none.** The claim stands on the
bit-exact two-pipeline extraction + the swarm's full-scan controls,
independent of the decryption bug. image07's passphrase (unknown, H(p) =
0f58d719) is out of reach per the swarm's preregistered stopping rule
(~145k³ 3-word space; 4B triple scan + 11.2B masks + 351.7B vectorized masks
all dead).

## Files

- `forensics/verify_steg.py` — Python extractor/verifier (both seeds + controls)
- `forensics/jpeg_dct.py` — RAW-mode JPEG coefficient reader (bug fixed)
- `forensics/crosscheck.c`, `forensics/jpegmini.h`, `forensics/streamdump.c`,
  `forensics/dumpcoef.c` — C/libjpeg pipeline
- `forensics/full_decrypt.py` — AES-128-CBC (verified vs pycryptodome + FIPS C.1)
- `forensics/streams/image07_0f58d719_stream_lsb.bin` (19,768 B) and
  `image04_3b75655e_stream_lsb.bin` (48,824 B) — full embedded streams,
  LSB-packed from bit 0; encrypted stream starts at bit 65 (24 magic + 1
  version + 5 algo + 3 mode + 32 nplainbits, source-verified).

## Method notes (operator standards)

- Both pipelines pre-registered before crosscheck; no post-hoc label choices.
- Every "proven" step has a named control (image04 positive; 3 negatives;
  pycryptodome + FIPS reference; mhash/stegseek source for keygen/selector;
  swarm's full 2^32 scan as independent confirmation).
- My one overreach (calling the swarm's blank-password claim "refuted") is
  corrected in this revision with the seed arithmetic that disproves it.
- No live-site interaction; no submissions; repo-only forensics.

## Repo-state note (2026-09-05)

- origin/master is a **single-commit** rewritten history, tip `f02ddfa`
  ("adjudicate seed dispute: negatives miss, payload stands").
- `7ff5f1b` exists nowhere on the server (verified by fetch + cat-file) —
  never pushed. `d69ca74` was an earlier fabrication. Both are treated as
  untrusted-source artifacts.
- Local sandbox was re-cloned between turns, resetting this branch to
  `b06b34a` and dropping local objects for `6188fb4`; recovered via
  `git fetch origin <arena branch>` + `git reset --mixed 6188fb4` (working
  tree was intact).
