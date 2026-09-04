# Agent brief: solve TK Level 8 (paste this to a fresh agent)

You are helping solve Level 8 of the Treasure Kracken prize treasure hunt
(10 levels, armchair creative puzzles). Work ONLY from the files in this repo.
Do not touch the live site (strike system bans guessing).

## The puzzle

Page title: **BLOCK GRID THINGY**. One static image: a plain 7-wide x 6-tall
grid, one digit 1-9 per cell (`grid.png`). Transcription (verified):

```
4 6 6 4 3 1 6
8 5 9 1 7 2 5
2 3 9 6 5 9 8
1 5 3 9 5 1 3
6 5 1 3 4 7 5
8 4 6 1 8 4 9
```

## The answer

**Exactly 3 random English words** (lowercase, space-separated). Precedent:
Level 6 was `necklace popcorn love`. The words are uncorrelated and NOT
guessable — they must be DERIVED from the grid by a clean mechanism
(A1Z26, phone keypad, solvent pattern, arithmetic, word search, etc.).
Report back: the 3 words + the exact derivation. Never submit to the live page.

## Constraints (proven, don't re-do)

- Velo code (`velo_dve99.js`) is a stock gate: 60s countdown, server-side
  password check, redirect to `/level-9`. Nothing hidden in it.
- Image forensics clean: uniform white bg, black ink, no metadata/stego.
- Digits 1-9 only. Corners 4/6/8/9 kill Minesweeper. Digit sum 205 kills
  Shikaku. No blanks kills Nurikabe/Fillomino-as-given. 7x6 too small for QR.
- Direct A1Z26 (rows, cols, pairs, sums, products) = gibberish (see ANALYSIS.md).
- Word search on A-I letters found only 6 scattered 4-letter words (no theme).
- Digit 1 appears in almost every row/col, which breaks naive T9/phone reads.

## Your task

Find a mechanism that converts this grid into 3 English words. Untried leads
(Hitori solve, T9 on the two lines without 1s, guitar-tab reading, 2x2-block
stats, alternate reading orders, Atbash + word search, title anagram) are
listed in ANALYSIS.md — start there or bring your own idea. If you use vision,
look at `grid.png` yourself; do not trust OCR blindly (positions above are
verified, but check any cell you build a theory on).

Output format: (1) the 3 words, (2) step-by-step derivation anyone can redo
by hand in under 5 minutes, (3) why alternatives were rejected. If you fail,
report which leads you exhausted so the next agent doesn't repeat them.
