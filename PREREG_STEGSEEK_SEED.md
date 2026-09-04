# Preregistration: complete StegSeek seed scans

Date: 2026-09-04. Committed before starting these scans.

## Question

Do any of the four residual JPEGs contain a steghide embedding at all, even if
the passphrase is absent from every tested wordlist? Earlier seed-mode attempts
were interrupted and covered only a small, unquantified fraction, so they did
not answer this question.

## Frozen method

Run StegSeek 0.6 in `--seed` mode to normal completion, with no seed range,
wordlist, semantic key, file-label interpretation, or post-hoc variant, on:

- positive control: `image04.jpg` (known steghide payload, blank passphrase)
- negative control: a deterministic 640x480 flat RGB `(73,109,151)` Pillow JPEG,
  quality 93, subsampling 2, non-progressive, non-optimized
- residuals: `image02.jpg`, `image06.jpg`, `image07.jpg`, `image12.jpg`

Each process gets a separate log and output path. A completed no-hit scan must
reach the end of seed space and report no embedded data. A hit counts only if:

1. StegSeek explicitly reports an embedding/seed;
2. an output file is produced or the reported metadata can be independently
   reproduced; and
3. a second extraction/detection agrees.

## Controls and decision rule

- Positive hit + negative no-hit: the experiment is valid.
- Positive miss or negative hit: stop and diagnose; do not interpret residuals.
- Valid controls + residual hit: inspect only the hit's extracted payload.
- Valid controls + all four complete no-hits: close steghide-presence itself on
  these carriers, not merely the tested passphrase families.

No live Treasure Kracken request or submission is part of this test.
