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

## Results

Controls behaved correctly:

- Positive `image04.jpg`: seed `3b75655e` found at 71.78% of the seed space;
  reported 47.7 KB compressed plaintext, rijndael-128/CBC. This agrees with the
  independently known steghide payload.
- Deterministic flat-JPEG negative control: complete scan, no valid seed
  (exit 1, 16.56 s).

Residual complete scans:

| carrier | result | elapsed |
|---|---|---:|
| `image02.jpg` | no valid seed | 44.38 s |
| `image06.jpg` | no valid seed | 43.73 s |
| `image07.jpg` | **possible seed `0f58d719` found** | 35.86 s quiet / 38.22 s repeated |
| `image12.jpg` | no valid seed | 44.16 s |

The non-quiet independent repeat on `image07.jpg` stopped at 80.07% and
reported, reproducibly:

- seed: `0f58d719`
- plain size: **19.3 KB (compressed)**
- encryption: **rijndael-128, CBC**

No output file is expected from seed mode for an encrypted payload. The first
quiet scan exited 0; the independent non-quiet scan also exited 0 and exposed
the same deterministic embedding metadata. All no-hit scans exited 1 after
exhausting the seed space.

## Decision

**New validated carrier found.** `image07.jpg` contains a steghide-compatible
encrypted embedding. The other three residual carriers are now closed for
steghide presence, not merely for known passphrases. The immediate blocker is
the passphrase for `image07.jpg`; prior targeted and 1,758,842-entry
repository-corpus wordlists did not contain it.
