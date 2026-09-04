# TK Level 8 — BLOCK GRID THINGY

Treasure Kracken prize treasure hunt, Level 8 of 10.
Page: https://www.treasurekracken.com/level-8 (login required, members only)
Password page: 60s countdown, then a text box + Submit. Password is validated
server-side via `validatePasswordAndAssignRole(8, password, memberId)`
(`backend/levelSystem.jsw.ajax`). No brute-forcing (rate-limited, strike system).

## The puzzle

Title on page: **BLOCK GRID THINGY**. One static image appears to be a plain
7-wide x 6-tall digit grid. Its rendered pixels are uniform, but the original
file is a PNG/ZIP polyglot: a six-image music archive begins immediately after
the PNG `IEND`. See `HIDDEN_FINDINGS.md`.

Image: `grid.png` (original, 1176x1056)
Source URL: https://static.wixstatic.com/media/0d5510_2edf85d9a3374cc2b99661a8384a96ae~mv2.png

## Transcription (OCR-verified, ambiguous cells resolved by glyph analysis)

```
4 6 6 4 3 1 6
8 5 9 1 7 2 5
2 3 9 6 5 9 8
1 5 3 9 5 1 3
6 5 1 3 4 7 5
8 4 6 1 8 4 9
```

Also in `grid_digits.txt`.

## Answer format

**3 random English words, space-separated, lowercase, spelling matters, case does not.**
(Precedent: L6 = `necklace popcorn love`. L7 was a QR-code visual.)
The words are random and uncorrelated — derived from solving, not guessable.
Do NOT submit guesses to the live page (strike system). Bring candidate answers
back with reasoning instead.

## Rules / facts

- Nothing hidden in site code. Velo (`velo_dve99.js`) is a stock password gate:
  60s countdown -> enable input -> server-side check -> redirect `/level-9`.
  The Level-8 variant also resolves display name via
  `currentMember.getMember({fieldsets:["FULL"]})` -> nickname -> loginEmail prefix.
- The rendered grid pixels contain no extra marks, but `grid.png` has a valid
  ZIP appended after `IEND`; the earlier no-steganography conclusion was false.
- Digits present: 1-9 (no 0). Corners are 4, 6, 8, 9 (kills Minesweeper:
  corner clues 4/6/8 exceed 3 neighbors).
- Row sums: 29, 37, 42, 27, 31, 39. Col sums: 29, 28, 34, 24, 32, 24, 36.

## Current strongest intermediate (not solved)

The six hidden artists in filename order give `MDWROD`; the nested PNG field
name `Artist` supplies `A`, producing `MAD WROD`. Under phone-keypad and
Boggle adjacency, `MAD` and `WROD` each have a unique path in the original
grid. Swapping the R/O blocks gives a unique `WORLD` path. This strongly
derives **MAD WORLD**, but `tears for fears` was submitted and is **INVALID**,
so a further extraction remains. In addition, blank-password `steghide` on
`image04.jpg` reveals a Stevie Wonder *I Just Called to Say I Love You* cover;
that second nested clue is not yet reconciled with MAD WORLD.

## Ruled out (with evidence in ANALYSIS.md)

- Direct A1Z26 (rows/cols gibberish), row/col-pair mod-26 (gibberish),
  row/col sums mod-26 (gibberish), row-product digital roots (all 9, coincidence),
  word search on A-I letters (only 6 scattered 4-letter words),
  Minesweeper (corner clues impossible), Shikaku (sums to 205, not 42),
  Nurikabe (no sea possible), Fillomino (inconsistent), QR (grid far too small),
  T9/phone words (digit 1 breaks every line), binary pixel-fonts of digits.

## Files

| file | what |
|---|---|
| `grid.png` | original puzzle image |
| `grid_digits.txt` | transcription |
| `velo_dve99.js` | Level-8 page code (stock gate, nothing hidden) |
| `page_dve99.json` | Level-8 page structure (171KB) |
| `tb8_0.json` | site pages map |
| `level8.html` | page shell (697KB) |
| `2059E.zip` | carved six-image archive appended to the PNG |
| `image01.png` through `image12.jpg` | six original hidden ZIP entries |
| `image01_artist_hidden.jpg` | JPEG decoded from `image01.png` metadata |
| `hidden/steg04.jpg` | Stevie Wonder JPEG extracted from `image04.jpg` |
| `HIDDEN_FINDINGS.md` | extraction, confirmed identities, and MAD WORLD path |
| `ANALYSIS.md` | full working notes: tested hypotheses + evidence |
| `AGENT_PROMPT.md` | paste-ready brief for parallel solver agents |
