# PREREG: grid3_easier — official "removed numbers you don't need" clue

Date: 2026-09-05. Clue (author, via user): "Level #8 We removed some of the
numbers you don't need" + grid3_easier.png (Discord media, fetched inline).
**Verified reading:** identical to the OCR-verified official 7×6 grid with
exactly 5 cells removed — last row (r5, 0-indexed), cols 2–6 — digits
`6 1 8 4 9`. Remaining: 37 cells, last row `8 4`.

Pre-registered BEFORE any test run. Decision rules fixed in advance.

## T1 — word-search refinement (primary)

Same reading as the killed full-grid run (A=1..I=9, 8 directions, len 4–7)
with the 5 removed cells as walls; dictionary =
steghide_dictionary.txt ∪ forensics/words.txt (superset approximation of the
original "system wordlist"; the 6 known full-grid hits are included as
anchor checks regardless of dict).

- T1a: full hit list on the 37-cell grid.
- T1b: positions of each full-grid hit (FIFE, GEED, FICA, ACID, CHEF, FAHD);
  which positions survive the removal.
- DECISION: if the surviving set is exactly 3 words → candidate answer
  family (log + whole-chain review; no submission without operator OK).
  If ≤5 scattered junk remains → word-search refinement KILLED (the clue
  prunes noise but doesn't produce the answer).

## T1c — background control

1,000 random 7×6 grids with the 37-digit histogram preserved, same 5 cells
removed → distribution of hit counts. Report P(count ≤ observed).

## T2 — 37-digit sequence readings (variant of killed mechanisms — flagged)

Row-major 37 digits: `4664316 8591725 2396598 1539513 6513475 84`
(col-major too). Tests: multi-tap T9 (1 = separator), A1Z26 pairs.
Flag: full-grid multi-tap already killed (0 hits, control 0.207/grid);
running only because the author-selected subsequence is new data.
Control: 1,000 shuffles of the same 37-multiset → baseline hit counts.
DECISION: accept a hit only if the full-grid version would NOT have shown
it and the control rate makes it unlikely (P < 0.01).

## T3 — removed digits `61849` as a message

Enumerate: T9 one-tap combos (1 = separator: 3×3×3×4 = 108 two-word
combinations), A1Z26 single (F A H D I) + valid pairings, number 61849
(factor/date), coordinates. DECISION: accept only a real dictionary
word/phrase that a control random-5-digit-draw (same histogram) does not
produce at ≥1% rate.

## T4 — structural observation + control

Removed digits = exactly the 5 non-prime digits {1,4,6,8,9}, one each.
Control: probability a random 5-cell draw from the 42-multiset
(1:6 2:2 3:5 4:5 5:7 6:6 7:2 8:4 9:5) yields exactly one of each of
{1,4,6,8,9} (any order). Report P. If P < 1%: follow-up reading of the
16 prime cells (row-major: 3 5 7 2 5 2 3 5 5 3 5 3 5 3 7 5) with the same
controls as T2. If P ≥ 1%: log as chance, no follow-up.

## Standing rules

No live submission. No post-hoc label choices. Every kill logged with
method + evidence. Corroboration-only claims (distinct letters, etc.)
marked as such.

## RESULTS (2026-09-05, run after pre-registration)

### T1 — KILLED (with a key finding)

- Full-grid hits (145,766-word dict): ACID, CHEF, FAHD, FIFE, GEED (+FICA in
  the original system wordlist). FAHD has exactly ONE position: the removed
  4-cell run r5c2–r5c5 = 6,1,8,4 (F-A-H-D in A=1..I=9). **The author
  removed precisely the cells of the FAHD junk hit** (+adjacent 9).
- Two-branch inference (author rule unknown): if removal = 5 arbitrary
  cells of 42, P(contain a specific 4-run) ≈ 4.5e-5 → author knew the
  word search; if removal = "5 of last row", P(FAHD hit) = C(3,1)/C(7,5)
  = 1/7 → coincidence branch. Either way: **the A=1..I=9 word search is
  the author-relevant grid reading** (author pruned one of its junk hits).
- Easy-grid survivors: ACID, CHEF, FIFE, GEED (+FICA, survives — its
  positions are in rows 0–3). 5 scattered junk ≠ exactly-3 acceptance →
  word-search refinement KILLED as answer producer. No len≥5 hits exist in
  either grid (full-grid run had zero).

### T2 — KILLED

Row-major 37-digit multi-tap: 0 hits. Col-major: HUB, IVA — but control:
461/1000 shuffles of the same multiset yield ≥1 hit → chance-level. A1Z26
pairs: "?"-garbage both orders.

### T3 — KILLED

61849: T9 (1=sep) combos → no two-word phrase (isolates: THY, MT, MU, NU);
A1Z26 single → FAHDI (not a word); 61849 = 127×487 (both prime); no
date match to the music/artist corpus.

### T4 — OBSERVATION + follow-up barren

P(a 5-cell draw from the 42-multiset = exactly one of each of
{1,4,6,8,9}) = **0.00423** (<1% → pre-registered follow-up ran): the 16
prime cells (3 5 7 2 5 2 3 5 5 3 5 3 5 3 7 5) multi-tap = 0 hits, control
0/1000 shuffles — the reading is barren (no information either way).
Logged as controlled observation only.

### T5 — KILLED (pre-registered post-hoc, dictionary fixed BEFORE run)

Hypothesis: the survivors filtered to the repo-canonical wordlist
(forensics/words.txt, used all-hunt) are the 3 password words. Fixed
dict → survivors = ACID, CHEF, FIFE, GEED = **4 words ≠ 3** (operator
format). Reaching 3 requires a post-hoc frequency cut (excluding GEED) —
forbidden by standards. KILLED.

### T6 — KILLED (glyph subtlety in grid.png)

Per-cell glyph bbox comparison (same-digit twins): each digit has one
exact-twin "main" family + variants; only 1 of 5 removed cells is a
size-outlier (the 1 at r5c3: 67px vs 66px for its digit); genuine
outliers (4@r4c4, 3@r4c3, 6s@r0c1/r2c3/r4c0, 2s, 8s, 5s) all REMAIN.
No planted glyph marker in the removed set.

### Status

The clue confirms the word-search reading is author-relevant and pins the
author's canonical grid (37 cells), but produces NO new answer candidate.
Answer queue unchanged (`call touch reach` ×6 perms → `two zero seven`);
no live submission. The only remaining puzzle lock stays image07's
passphrase.

### T7 — OPERATOR RULING (2026-09-05): word-search survivor class DEAD

Operator: the answer is not the word-search direction ("I dont think its
gonna be that"); the grid-word class was already submitted and rejected in
prior rounds (all grid-word orders killed), so none of the five survivors
(ACID CHEF FICA FIFE GEED) or any combo of them will be submitted.
No live interaction. The clue's residual value: the 37-cell canonical
grid + removed-cell exclusion remain valid constraints for any future
non-word-search mechanism.
