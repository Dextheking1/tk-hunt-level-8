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
