# Preregistration: image07 mechanically-derived string family (seed-checked)

Date: 2026-09-04. The family below was defined, frozen, and seed-checked in a
single script run (no candidate was seen before checking). Target: the
confirmed steghide carrier `image07.jpg`, StegSeek-reported seed
`0f58d719` (19.3 KB compressed payload — sized like a 300x300 cover, i.e.
almost certainly a tenth image from the missing slots 03/05/08/09/10).

## Why this family is new ground

All prior keyspaces are corpus-derived (repo text tokens/sequences), generic
dictionaries, or exhaustive short strings:
- corpus 1,758,842 / generic 7,140,015 / pairs 100,000,000 /
  lowercase-1-6 321,272,406 / decimal-1-8 111,111,110 / 56 cover-grid words /
  380 semantic — all zero (see their prereg files).
- None of them contains **contiguous concatenations of structured facts**
  (file slots, digit rows/cols, page strings, T9 codes, dates with separators)
  because the corpus rule only emits whitespace tokens and within-line
  sequences. Verified: `image03/05/08/09/10` occur **zero times** in the repo.

## Seed-check method

`H(p) = LE32(MD5(p)[0:4] ^ MD5(p)[4:8] ^ MD5(p)[8:12] ^ MD5(p)[12:16])`
(byte-wise XOR of the four MD5 quarters, little-endian). Implementation
validated: `H("planet") = 2c52fe1c` — exactly the StegSeek-reported seed for
the swarm's `planet` control carrier (PREREG_STEGHIDE_SEED_MAPPING.md).

## Frozen family (1,000 candidates, bytewise-sorted)

- F1: `imageNN` / `imageNN.jpg` for NN = 00..99, x {verbatim, upper,
  capitalize} — **includes the missing slots 03/05/08/09/10, absent from
  every prior keyspace and the entire repository** — plus ZIP-start-offset
  names `2059E`/`0x2059E`/`132510`.
- F2: grid digit rows (6), columns (7), full 42-digit string, each reversed
  (28 contiguous digit strings — prior decimal stage only covered 1-8 digits).
- F3: page-title concatenations `blockgridthingy`/`blockgrid`/`gridthingy`/
  `blockthingy` x 3 cases (spaced forms tested; contiguous forms not).
- F4: file-number concatenations (present set 01020406071112 etc., missing
  set 0305080910, full 01..12, leading-zero and bare, each reversed).
- F5: non-pure-digit date/datetime forms (1987-02-25, 2016-12-19T21:25:36,
  ZIP timestamps with T/space; pure decimals already covered by Stage C).
- F6: T9 digit codes of all 9 titles, 8 artists, 20 title words, 17
  board-vocabulary words (contiguous digit strings).
- F7: container facts (`19.3kb`, `19300`, seed literals).
- F8: contiguous no-space/underscore/hyphen forms of all title/artist/lyric
  entities x 3 cases (incl. `ringmybell` — in no prior keyspace).
- F10: album names as resolved facts (Violator, True Blue, Khalifa, Orianthi,
  Believe, Hot Rocks Vol. 2, If You're Reading This It's Too Late, More Life,
  Ghostbusters OST, Imagine Dragons, It's Time, Night Visions, Evolve) x 5 forms.

Artifact: `image07_mech_strings.txt`, 1,000 lines, SHA-256
`718da3576b788610cbf01dbc51cff2c23ca1c0c01b42189633ce649a30a941d3`.

## Result

**0 of 1,000 candidates satisfies `H(p) = 0f58d719`** (computed locally with
the validated H; no steghide execution involved).

## Expected StegSeek seeds for follow-up C validation

Independent precomputation for the swarm's seven fixed synthetic carriers —
if the reported seeds match these, the mapping is confirmed and the no-hit
above becomes a tool-validated kill of this family:

| passphrase | expected seed |
|---|---|
| `` (empty) | `3b75655e` |
| `a` | `927c8494` |
| `abc` | `275fa452` |
| `test` | `cb4257a3` |
| `planet` | `2c52fe1c` (already matched) |
| `8675309` | `07a3d533` |
| `correcthorsebatterystaple` | `cc703c87` |

## Decision rule

- If follow-up C confirms H (all seven seeds match): the swarm runs
  `stegseek image07.jpg -w image07_mech_strings.txt` (1,000 lines, seconds)
  for the tool-validated verdict; a miss kills the mechanically-derived
  string family. The remaining key space is then only the unknown payload's
  own content or author-personal strings — outside finite sweep scope.
- If follow-up C rejects H: this no-hit is an instrumentation null (as
  attempt A), and the family reopens under the corrected mapping.
