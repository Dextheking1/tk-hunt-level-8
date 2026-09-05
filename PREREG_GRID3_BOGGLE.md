# PREREG: grid3_easier x Boggle board-embedding layer

Date: 2026-09-05. The clue (5 removed cells: r5c2–r5c6) was first applied to
the A=1..I=9 word-search layer (FAHD finding). This pre-registration applies
it to the BOGGLE layer (king moves) — the layer that produced the top
candidate `block grid thingy` (GRID/GIRD unique-path plantings,
Gird_Background.jpg corroboration) before its operator rejection.

## Fixed setup (CORRECTED after null run on the wrong layer)

First run used the A=1..I=9 mapping by mistake — that layer is the dead
word-search layer (reproduced its FAHD-only diff; no new info). The live
Boggle layer is the swarm's board-planting layer: **keypad mapping** —
each cell with digit d (2-9) may be ANY letter of T9L[d]
(2=ABC 3=DEF 4=GHI 5=JKL 6=MNO 7=PQRS 8=TUV 9=WXYZ); digit-1 cells are
letter-incapable (excluded from paths, pre-registered).

- Baseline = 42-cell grid; Easy = 37-cell grid (removed cells blocked).
- King moves (8-dir), no cell reuse, len 3+, dictionary =
  steghide_dictionary.txt ∪ forensics/words.txt (72,870 words len≥3).
- Removed cells R = {(5,2),(5,3),(5,4),(5,5),(5,6)} = digits 6,1,8,4,9.

## Experiments (run in order, decision rules fixed)

- E1: recount GRID (4,7,4,3) and GIRD (4,4,7,3) path counts on the 42-cell
  grid; verify the swarm's "exactly 1 path" claims; record the exact
  cell paths.
- E2: do the GRID / GIRD paths touch R? (any path cell in R = the author's
  removal prunes that planting).
- E3: full Boggle word-set diff baseline → easy. Report every word that
  dies; flag: (a) GRID/GIRD, (b) any song/artist/phone-theme word,
  (c) len≥6 words, (d) words with unique paths.
- DECISION: any flagged embedding pruned by the author = logged as
  author-removed (dead as answer material). GIRD surviving intact =
  author-corroborated planting (Gird_Background.jpg consistency).
  No submission either way; this test only sorts the planting record.

## Standing rules

No live submission. Controls: the Boggle word-set diff itself is the
control (words that survive = not targeted). No post-hoc label choices on
which words "matter" — the flag list above is the whole list.

## Results E1-E3 (2026-09-05)

- E1 VERIFIED: keypad-Boggle (cell = any T9L[d] letter, digit-1 cells
  letter-incapable, king moves, dict 72,870) → GRID = 4743 exactly 1
  ordered path: (5,5)G→(4,5)R→(4,4)I→(4,3)D. GIRD = 4473 exactly 1:
  (4,4)G→(5,5)I→(4,5)R→(3,6)D. Swarm claims confirmed.
- E2: **both plantings pass through (5,5) — a removed cell.** GRID and
  GIRD are ABSENT from the canonical 37-cell board. The author's own
  "easier" grid prunes both unique-path plantings (and FAHD in the
  A-I layer). block-grid-thingy is now doubly dead (operator reject +
  author pruning).
- E3: 607 of 2,843 baseline Boggle words die; theme-flagged: only LINE
  (phone-adjacent) dies; HOT/KEY/BELL/PAY/VINYL/LOVE/MAD survive.
  CALL/TOUCH/REACH were never board-embeddable (no adjacent 2-2 for
  CALL; no T-O-U-C-H / R-E-A-C-H paths) — clue changes nothing there.

## E4 — surviving unique-path plantings (pre-registered before run)

Census on the canonical 37-cell board: words with exactly 1 ordered path
(len≥4, path count capped at 50). Report survivors; flag: (a) theme words
(phone/music/artist list), (b) len≥6, (c) words whose path-digit
sequence is monotone/palindromic/prime. DECISION: surviving unique-path
words = author-LEFT plantings = the only board-derived answer material
that remains legitimate (no submission without full chain + operator OK).
Random-board control pre-registered: 1,000 boards with the same 37-digit
multiset and the same 5 blocked cells (seed 9); the theme-flagged
unique-path survivor count must beat the control at p<0.01 or the list is
chance and dead.

## E4 RESULTS (2026-09-05) — KILL (chance)

Census (len≥4, dict 72,870): 42-board = 2,386 words / 1,373 unique-path;
canonical 37-board = 1,843 words / 1,091 unique-path (total vs control:
mean 970, P(≥1091) = 0.307 n.s. — no global planting signal).

Theme-list unique-path survivors on the canonical board (ordered digit
sequences, extracted):

```
BELL  2355   cells (2,0)→(2,1)→(3,1)→(4,1)
BLUES 25837  (1,5)→(1,6)→(2,6)→(3,6)→(4,5)
DISCO 34726  (0,4)→(0,3)→(1,4)→(1,5)→(0,6)
FIRE  3473   (4,3)→(4,4)→(4,5)→(3,6)
FUNK  3865   (2,1)→(1,0)→(0,1)→(1,1)
LOVE  5683   (1,1)→(0,1)→(1,0)→(2,1)
VINYL 84695  (1,0)→(0,0)→(0,1)→(1,2)→(1,1)
WATER 92837  (2,5)→(1,5)→(2,6)→(3,6)→(4,5)
WAVE  9283   (2,5)→(1,5)→(2,6)→(3,6)
```

Control (1,000 boards, same multiset + blocked cells, seed 9): theme
unique-path survivor count mean 3.99, max 17; observed = 9 → P(≥9) = 0.044.
p > 0.01 → **not significant under the "uniqueness needs a random-grid
background control" standard → the 9-word list is chance, not a planted
set.** Digit strings logged for the record only; no further derivation
authorized. (Monotone/palindromic/prime flag: none of the 9 sequences
qualifies — 2355 no, 25837 no, 34726 no, 3473 no, 3865 no, 5683 no,
84695 no, 92837 no, 9283 no.)

## FINAL VERDICT — board-planting line DEAD (doubly)

1. Both keypad-Boggle plantings (GRID=4743, GIRD=4473) pass through the
   cell the author removed → the author pruned them (plus the operator's
   reject of `block grid thingy`).
2. Surviving unique-path theme words on the canonical board are at chance
   level (p=0.044).
No board-derived candidate is endorsed. The Boggle layer exhausts the
grid3_easier clue. The clue's remaining value is the canonical 37-cell
grid itself (digit sum 179 — see PREREG_GRID3_EASIER.md, T8) and the
removed-cell exclusion rule.
