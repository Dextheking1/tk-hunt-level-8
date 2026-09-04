# Level 8 working notes

## Grid (verified)

```
r0: 4 6 6 4 3 1 6
r1: 8 5 9 1 7 2 5
r2: 2 3 9 6 5 9 8
r3: 1 5 3 9 5 1 3
r4: 6 5 1 3 4 7 5
r5: 8 4 6 1 8 4 9
```

OCR: tesseract per-cell (inverted + border, psm 8). Six cells read as "15"
were proven to be single-component glyphs of matching pixel sizes
(1260/1293 px pairs at (1,1)/(4,1) and (1,6)/(4,6)) — all are 5.

Image forensics: backgrounds all 255, ink all 0, uniform grid spacing
(129px cols, ~133px rows), RGBA alpha all 255, no EXIF/text chunks.
The image carries nothing but the digits.

## Arithmetic tests (all gibberish)

- A1Z26 rows: DFFDCAF / HEIAGBE / BCIFEIH / AECIEAC / FEACDGE / HDFAHDI
- A1Z26 cols: DHBAFH / FECEED / FIICAF / DAFICA / CGEEDH / ABIAGD / FEHCEI
- Row-major pairs mod 26 (A=0): UMFQHRZXSHDBRNNNV GUSX (21 letters, no words)
- Col-major pairs mod 26: only 3 valid (U, P, L)
- Row sums mod 26: CKPAEM. Col sums mod 26: CBHXFXJ.
- Row-product digital roots: all 9 (coincidence — most rows contain 9 or 3x3).
- Adjacent-pair sums (row-major): J,J,D,N,N,H,G,E,O,N,I,H,N,D,K,D,K,M,J,I,M.

## Visual-pattern tests (ASCII renderings, no letters found)

odd/even, prime/composite, >=5, ==d for each digit 1-9, 4-bit-per-cell
expanded bitmap (14x12). The `==5` cells: (1,1),(1,6),(2,4),(3,1),(4,1),(4,6).
The `==1` cells: (0,5),(1,3),(3,0),(3,5),(4,2),(5,3) — six 1s.
None of the binnings draw letters or QR-like structure at this scale.

## Word search (A=1..I=9, 8 directions, len 4-7, system wordlist)

Only 6 hits, all length 4, scattered, no theme:
FIFE, GEED, FICA, ACID, CHEF, FAHD. Ruled out as solve path
(a 3-word answer would need long/thematic hits).

## Killed by grid logic

- Minesweeper: corners (0,0)=4, (0,6)=6, (5,0)=8 exceed max 3 neighbors.
- Shikaku: digit sum is 205, grid area is 42.
- Nurikabe: every cell numbered, no room for the sea.
- Fillomino: isolated cells with value != 1 violate region sizes.
- QR: 7x6 cells far below minimum QR dimensions.

## Untested leads (for parallel agents)

1. Hitori solve (shade dupes, no adjacent shade, connectivity) -> shaded
   pattern or unshaded A-I letters. Needs a real solver + payoff theory.
2. T9/phone words on rows/cols that avoid digit 1 (only r2 and c1 qualify).
3. Guitar-tab reading (6 strings x 7 frets 1-9) -> pitches -> note names.
4. "BLOCK" = calendar (6 weeks x 7 days)? Numbers 1-9 only — weak.
5. 2x2 block stats (sums/products mod 26) over the 30 overlapping windows.
6. Snake/spiral/boustrophedon reading orders + pair mod-26.
7. Atbash A-I -> R-Z then word search.
8. Nonogram-style: use row/col sums as run-lengths? (Sums 24-42 too big.)
9. KenKen/Kakuro-style arithmetic with hidden cages — needs cage theory.
10. The title itself: "BLOCK GRID THINGY" — anagram? B-L-O-C-K... (15 letters).
    Anagram of the title has never been checked.
11. 42 cells — check pairs/positions against external constants (periodic
    table? US states? book cipher needs a book — none given).
12. Username "BORIS" appeared in a solver's screenshot OCR (likely a Discord
    username, probably noise — flagging so nobody chases it twice).

## SOLVED 2026-09-04 — T9 phone-keypad word search

Mechanism: each digit maps to telephone-keypad letters
(2=ABC 3=DEF 4=GHI 5=JKL 6=MNO 7=PQRS 8=TUV 9=WXYZ, 1=break).
Four English words hidden in straight lines (8 directions), each reading
as a word in exactly one direction (all reverses gibberish):

- HOMIE: row 0, cols 0-4, left-to-right [4,6,6,4,3]
- KELLI: col 1, rows 1-5, top-to-bottom [5,3,5,5,4]
- SMELT: diagonal (1,4)->(5,0) [7,6,3,5,8]
- TILLS: col 4, rows 5-1, bottom-to-top [8,4,5,5,7]

Cross-confirmation (classic planted-word-search design):
KELLI x SMELT share (4,1)=5 (L/L); TILLS x SMELT share (1,4)=7 (S/S).

Why exactly these (background test): 60 random 6x7 grids average 9.4
len-5+ T9 words; this grid has 4 -> filler curated, survivors deliberate.
KELLI is a proper name, unusable as a password word (precedent L6 uses
common words) -> accident/decoy. Answer triple: HOMIE SMELT TILLS
(reading order = alphabetical order).

Phantoms excluded: with speculative 1=I mapping, IDIOM/TAINT/SHEIK
(+junk CLXII/JILIN) also appear — but every one contains a literal 1-cell,
which breaks decoding under the puzzle's own mapping, so the author (working
in T9, where 1 maps to nothing) could never have planted them. Proof: the
1=I theory yields 7 plants for a 3-word password (diverges); pure-T9 theory
converges to exactly 3 after name exclusion.

## Submit log
- 2026-09-04 ~07:00 UTC: `homie smelt tills` (reading order) -> INVALID.
  Triple {HOMIE,SMELT,TILLS} kept (name-exclusion of KELLI); order suspect.
  Next: `homie tills smelt` (end-cell reading order).
- Intel: tk-clues official rules (Kracken 8/30): "Letters and numbers are
  fair game. Nothing is case-sensitive. Punctuation matters. Try not to
  overthink it." No official L8 hint exists. tk-lvl-8 chat: waffle jokes,
  unexplained "video" confusion, "are you Kyle Wood" (KYLE is grid noise,
  len-4 diag). tk-lvl-9: only "First" claim (WifeElect, Sep 3), no mechanism.

## Pivot 2026-09-04: HST triple dead, Y triple leads
- `homie smelt tills` INVALID, `homie tills smelt` INVALID.
- Accident math: TAINT needs 4 free cells ((1,0),(2,0),(3,0),(4,0) given
  SMELT's (5,0)=8): P~1/6561 as filler chance. SHEIK likewise 1/6561.
  Both MUST be deliberate plants => author endorses 1=I (digit 1 as letter I).
- New theory: pure-phone finds (HOMIE/SMELT/TILLS) are DECOYS; real triple is
  the three common words requiring the twist: IDIOM / TAINT / SHEIK
  (CLXII dropped as non-word, JILIN as name - same filter shape).
- Supporting: official rule "Letters and numbers are fair game" licenses
  using the number 1 as a letter. Each Y word uses exactly one 1-cell.
- Y orders: start-cell reading = IDIOM(0,5),TAINT(1,0),SHEIK(4,5);
  end-cell reading = alphabetical = IDIOM,SHEIK,TAINT.

## Transcription audit (passed)
Glyph-identity NCC + row-level TSV OCR + split-pattern analysis confirm
EVERY cell. Key resolutions: six ambiguous cells = 5 (NCC-identical to
certain (3,4)); five "9" cells really are 9 (exact row reads rows 3,5);
both "7" cells really are 7; (2,1)=3 ("13" split), (2,0)=2, (1,5)=2.
Grid as transcribed is CORRECT. T9 word inventory stands:
len5 pure-phone HOMIE/KELLI/SMELT/TILLS; len5 1=I IDIOM/TAINT/SHEIK;
len4 incl KYLE/MELT/TILL + 28 noise words (expected accidents).

## Submit log (all INVALID)
1. `homie smelt tills` (X triple, start-cell order)
2. `homie tills smelt` (X triple, end-cell order)
3. `idiom taint sheik` (Y triple, start-cell order)

## Structural facts for next theories
- Chain joints: TILLS[4]=S=SMELT[0]; SMELT[3]=L=KELLI[3].
  Chain order TILLS->SMELT->KELLI ("tills smelt kelli") or reverse.
- HOMIE isolated (no shared cells). IDIOM shares 4 cells with HOMIE.
- TAINT shares (5,0)=T with SMELT. SHEIK shares (4,1) with KELLI/SMELT.
- Crossword-direction filter (across->/down-v only): HOMIE, KELLI, TAINT.

## Unifying theory (2026-09-04): alphabetical convention + decoy triple
- If author's order convention is ALPHABETICAL: X-triple submits as HST
  (failed #1), Y-triple submits as IST. Y-start-order ITS (failed #3) is
  then EXPECTED to fail. All three failures consistent with: answer=Y,
  order=alphabetical => `idiom sheik taint`.
- Design parses: pure-phone finds (HOMIE/SMELT/TILLS) are the obvious
  decoys; the 1=I twist reveals the real triple; KELLI punishes
  include-everything (4-word) attempts.
- Queue if IST fails: `tills smelt kelli`, `kelli smelt tills`,
  X-remnants (SHT/STH/THS/TSH), `homie kelli taint`, 4-word HKST.

## Auto-queue (2026-09-04 ~07:44 UTC)
Driving submits via CDP (trusted-key typing, UI-rate-limited, same 60s
countdown as manual). 8 candidates: X-remnants SHT/STH/THS/TSH, then
Y-remnants SIT/STI/TIS/TSI.
- `smelt homie tills`, `smelt tills homie`, `tills homie smelt`,
  `tills smelt homie`, `sheik idiom taint`, `sheik taint idiom`,
  `taint idiom sheik`, `taint sheik idiom`
DO NOT submit manually while the bot runs (state interleaving).
