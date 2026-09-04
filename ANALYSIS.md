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

## UI finding: stuck "Checking..." is cosmetic
After any wrong guess, the Velo countdown re-enables the input and
re-attaches onClick, but the button LABEL stays "Checking..." (the reset to
"Submit" only runs at countdown start). The button remains fully clickable
(and Enter in the input works). Bots must gate on INPUT-ENABLED, not label.
- Submit #6 `smelt tills homie` -> INVALID (countdown restarted after it).
- Bot v3 (input-gated) running remaining 6: THS/TSH + SIT/STI/TIS/TSI.

## Status: 7 misses, guessing HALTED by operator
Failed submits: HST, HTS, ITS, IST (manual) + SHT, STH, THS (bot, all
confirmed-wrong via countdown-restart / no-redirect).
Remaining Kung-fu: TSH/SIT/STI/TIS/TSI, K-chain (TSK/KST), HKT, 4-word HKST,
X/Y-remnant orders. NO more blind submits without a derived rule.
Partials established: transcription audited 3 ways; Hitori UNSAT x2;
Minesweeper/Shikaku/Nurikabe/Fillomino/Mosaic killed by constraints;
arithmetic/anagrams/Caesar/Boggle/bitmaps/paint/segments/title-anagram/
grille-concat/whole-lines/spiral all dead; background-rate analysis shows
pure-T9 finds (4) AND 1=I finds are both at/below chance (9.4 / 12.15) --
word sets may be filler noise, mechanism unconfirmed.
Next: ask retro (claimed L8 knowledge in tk-lvl-8 7:29 AM). Await parallel agents.

## Hidden-file solve path (2026-09-04)
grid.png = 132KB PNG + 3.1MB appended ZIP (after IEND). ZIP: 6 music
images (all 2026-09-03 23:35). image01 (Madonna La Isla Bonita) EXIF Artist
= 20KB base64 data-URL -> Madonna Papa Don't Preach cover. Others: OVO-shirt
man (Drake?), Wiz Khalifa, Ghostbusters cover, blonde guitarist, Dan Reynolds.
No thumbnails/payloads/trailing data elsewhere. Row<->image T9 links all
dead (rows lack required letters positionally). Grid & images independent.
Submits: `papa don't preach` (ASCII) INVALID.
Queue: `la isla bonita` (surface, typable, island-themed) >
`papa don\u2019t preach` (curly U+2019: Wikipedia/smart-quote theory) >
`papa dont preach` (normalization theory).

## Steghide layer (2026-09-04): Stevie Wonder cover in image04
`steghide extract -sf image04.jpg -p ""` -> 300x300 JPEG = Stevie Wonder
"I Just Called To Say I Love You" single cover (steg04.jpg). No recursion
(nested covers terminal; 100+ passphrases fail on 02/06/07/12; no LSB/
thumbnails/markers elsewhere).
Cover-text candidates: "la isla bonita" (surface) / "papa don't preach"
variants incl curly U+2019 (deep) / "i love you" + "i just called" (Stevie
hook vs setup). Photos yield no text. Grid rows cannot spell image words.

## Third cover (2026-09-04, via parallel agent tip, verified)
grid.png has an eXIf chunk (62KB) = TIFF with JPEG thumbnail =
Depeche Mode "Personal Jesus" (1989) single cover (exif_personaljesus.jpg,
paint.net/Photoshop CS, 2016-12-19 dates). "Reach out and touch faith" lyric
reads as method-hint (look inside files). 2 words: not the answer itself.
image07 = Orianthi (blonde rock guitarist) per parallel agent, plausible.
No Spotify link found anywhere in repo (agent referenced unknown context).
Inventory now: covers Isla/Papa/Ghostbusters/Stevie-8wds/PersonalJesus(2w)
+ 4 textless photos. Photos yield no text; rows cannot spell image words.
New candidates from Stevie cover: `i love you` (hook), `i just called`.
Queue: i-love-you > i-just-called > curly-Papa > noapos-Papa > isla.

## Solo-track findings (2026-09-04, re-logged after merge)
- Submit #6 `smelt tills homie` INVALID. UI quirk: after a wrong guess the
  button label sticks at "Checking..." while staying enabled+clickable.
  Bots must gate on INPUT-ENABLED, not label. Enter key always submits.
- Bot queue fired SHT/STH/THS (all wrong via countdown-restart/no-redirect).
  Manual+bot misses total 7: HST,HTS,ITS,IST,SHT,STH,THS.
- Background rates: pure-T9 finds 4/grid vs 9.4 random avg; 1=I finds 9 vs
  12.15 avg. Both at/below chance: word sets may be filler noise.
- Dead: Hitori UNSAT (own solver), Caesar sweep (only EGGED), Boggle-T9
  (718 noise), Boggle-AI (20, FACADE-family), bitmaps+OCR (garbage),
  paint-by-numbers (blank), title anagram (junk), whole-grid anagram
  (0 covers), grille-concat masks x16 (no covers), spiral/snake A-I
  (CHEF/FAHD/CHIEF/EACH only), seven-seg letters (only BEEF),
  2x2/3x3 blocks (noise), spiral/snake T9 (LOWELL only),
  1=space segmentation (HOMIE-unique + SALAD + THY/VIZ, rest dead),
  row/col anagrams (none), phone-column words (none), guitar-tab (no zeros
  kill it), calendar (dates don't repeat), Minesweeper/Shikaku/Nurikabe/
  Fillomino/Mosaic (corner/sum/blank kills), Braille, stereogram (no period),
  pairs-ASCII (gibberish), mediants/modes/ranges (gibberish), ASCII rows
  (0x7F), 6-bit cols (out of range), knight paths (385 noise).
- Transcription audited 3 ways (NCC glyph identity, row TSV, split patterns).
- Boggle-presence (T9 king-move): LOVE, YOU, ISLA, RAY, DAN, MAD, KYLE present;
  MADONNA/DRAKE/WIZ/ORIANTHI/STEVIE/WONDER/DEPECHE/MODE/WORLD/GHOST/PAPA/
  PREACH/BONITA/JESUS absent. LOVE+YOU share cells (overlap ok for separate
  finds). "I LOVE YOU" convergent: Boggle-present + Stevie hook + phrase.
- MAD/WORLD caution: WORLD needs unevidenced 7/6 swap at (1,4)/(2,3)
  (glyphs confirmed as-is); without swap it's WROD (nonsense). Outer
  initials MDWROD + placed-A = sharpshooter. Downgraded.

## Swarm transcript intake (2026-09-04): spiral/diceware/knight/mosaic dead
- Spiral A1Z26 string verified exact (DFFDCAF...FEEIC). Hits with system
  dict: CW CAFE/FEE (+EEC junk; FAB absent from dict), CCW ICE/DIE/CHEF
  (+CHE/FAHD junk). Random 42-perm background averages 5.25 hits vs our
  3-5: AT CHANCE. "Exactly 3" needs a curated wordlist. REJECTED.
- Diceware mappings verified in EFF-large (46643 reexamine, 16512 concrete,
  52365 rope, 16535 confiding, 41646 napping). REJECTED anyway: arbitrary
  "first 15 rolls" cutoff (remaining 16 valid dice ignored), and EFF-large
  lacks necklace/love/ducks/pump so it contradicts the hunt wordlist.
- Knight's-tour DICE opener verified as existing path (0,0)->(1,2)->(0,4)->
  (1,6)->(3,5)->(5,6)->(4,4)->(3,2) = DICEAIDC, but flexible knight paths can
  open with almost any short word: apophenia. REJECTED.
- Mosaic (digits 1-9 -> 9 thumbnails) unmappable: relayed digit->image
  assignments incoherent, no principled alternative. PARKED.
- OPERATIONAL: submissions are FREE, 1/minute, case-insensitive;
  spaces+spelling matter. (Relaxes earlier strike-fear; queue viable.)

## Notion-agent transcript intake (2026-09-04)
- Covers-as-instructions framing: Ghostbusters ("who you gonna call"),
  Stevie ("I just called"), Personal Jesus ("reach out and touch faith"),
  Papa ("don't P-reach" -> REACH). Converges on phone+Boggle method, not
  on an answer triple. Contact-theme words (reach/call/touch) noted but
  orderless: NOT a submittable candidate without a derived order.
- Years (1984/86/87/89/2018) as touching-cell paths: tested, all fail.
- MAD WORLD downgraded independently (WORLD needs unsupported swap).
- No new payloads; inventory matches repo.

## Notion-agent intake 2 (2026-09-04): decisive constraints + new leads
- DISTINCT-LETTER PROOF: L6 (necklace popcorn love) and L7 (ducks pump
  premium) each use 10 distinct letters. One digit (1-9) carries <=9 values,
  so one-digit-to-one-letter schemes (A1Z26/Caesar/QWERTY/Atbash/note-names)
  are IMPOSSIBLE as a class. T9/multi-letter cells survive (draw from 26).
- PLURALS KILL WORDLISTS: "ducks" absent from BIP-39/EFF-large/EFF-short/
  Diceware (all exclude plurals by design). Author uses no curated list;
  digits do NOT index into a wordlist.
- House format (operator-confirmed): 3 UNCONNECTED common English words
  (cf necklace/popcorn/love, ducks/pump/premium). Phrases/titles excluded
  as answers (kills Papa/Isla/I-love-you as literal answers).
- Title hyperlink = "Fun Facts About Bananas" joke video (placeholder).
  Conceal/Reveal = stock Wix menu animation. Site bg = Gird_Background.jpg.
  Page has no instructions (title + grid + "." + Submit only).
- Guitar-tab (all tunings), Nashville/jianpu (all keys), digit-index into
  artist/song titles (rows+cols, both offsets), all-names-concat 2-digit
  tokens (both dirs), Connect-Four lines (none exist): ALL DEAD (verified).
- what3words hypothesis (3 uncorrelated incl plurals = w3w address shape):
  grid would have to encode a location; images have no GPS (stub only).
  UNTESTED (needs w3w list/API).
- LEADS (need live-site reads, NOT yet authorized): Level 0 page (admin-
  confirmed hint for later levels), TOOL page (possible author decoder),
  /qa page, Level 6 grid image (known-plaintext calibration vs known answer).

## Covers-as-instructions framing (Notion agent, banked 2026-09-04)
Covers read as method hints, not answers: Ghostbusters ("who you gonna
call") + Stevie ("I just called") -> CALL = phone keypad; Personal Jesus
("reach out and touch faith") -> TOUCH = adjacent/Boggle cells; Papa
("don't P-reach" -> REACH) consistent with touch-traversal. Since `i love
you` failed, Stevie title likely tells HOW to traverse, not what to submit.
Falsified under this framing: year-paths (1984/86/87/89/2018 as
touching-cell paths all fail). MAD WORLD stays downgraded (WORLD needs the
unsupported 7/6 swap). Open: what the traversal SELECTS (Boggle alone gives
hundreds of words; still needs a pick-3 rule).

## Boggle-unique-paths correction (2026-09-04, verified by exhaustive DFS)
Claim was "only 3 long Boggle words with unique paths (beached/acacia/
cicada)". Full count over the 20 known len6+ A-I words: unique paths also
for CHAFED, DECIDE, GAFFED (1 each). So SIX unique-path words, not three;
the triple is cherry-picked and its order (not alphabetical, not reading,
not length) is unprincipled. NOT recommended.
Counts: ACACIA 1, BEACHED 1, CHAFED 1, CICADA 1, DECIDE 1, GAFFED 1,
ACHEBE/CADDIE/CADGED/DECADE/DIFFED/EDIFIED/FACADE 2, CICADAE/DEFACED/
DEICED 3, DEIFIED 4, DEFACE/EDIFICE 5.
## Dates-as-mod42-coords (2026-09-04): dead
1987-02-25 -> (19,87,02,25) mod42 = cells give IDFE (0-based) / EFFI
(1-based). 2016-12-19 -> HIBI / IDPJ. No words either indexing. The
Personal-Jesus file dates carry no grid selection.

## Coordinate splits falsified (2026-09-04, reverse-geocoded)
Row pairs as DD.DDDDD + D[D].DDDDDD: (46.64316,8.591725) = Gotthardstrasse,
Andermatt, Switzerland; (23.96598,15.39513) = Murzuq, Libya; (65.13475,
84.61849) = Turukhansky, Siberia. Three random remote spots, zero connection
to Utah/music/Kracken/artists' origins. Splits arbitrary anyway. DEAD.
what3words rejected outright (operator: passwords are 3 unconnected random
English words, not addresses).
## Fable transcript intake (2026-09-04)
Row/col T9-separator segment lists match repo exactly (cross-validated).
Knight DICE opener + spiral/diceware/mosaic claims already falsified here.
No new payloads. Open leads still Only: Level 0 hint page, TOOL page, /qa,
L6 grid calibration (all need live-site reads, awaiting operator OK).

## Fable round 2 intake (2026-09-04, verified by code)
- Straight-line T9 search (8 dirs) for ALL image-derived words (artists,
  titles, phone-theme: hotline/bling/payphone/call/touch/reach/faith/
  receiver/believer/ghost/isla/papa/preach/madonna/stevie/depeche...):
  only LA (x4) and UP (x1). Images are NOT a word-search key. DEAD.
- Filename numbers as cell selectors: cells 1,2,4,6,7,12 (row-major) =
  4,6,4,1,6,7; as column picks per row = junk. DEAD.
- Theme-word Boggle presence (king-move): hotline(1=i) 1, bling 3, dial 4,
  wire 3, line 1, key 10 -- all at chance for a 42-cell grid. Not evidence.
- Digit histogram: 1:6 2:2 3:5 4:5 5:7 6:6 7:2 8:4 9:5 (no signal).
- Song-ID note for the 4 textless photos (phone theme fits): Drake =
  Hotline Bling, Wiz Khalifa = Payphone (Maroon 5 feat.), Ghostbusters =
  "who you gonna call", Stevie = "I just called". Theme => KEYPAD is the
  intended mechanism; the missing piece is the SELECTION rule, which no
  grid-internal test has produced.
- Recommendation: obtain Level 6 + Level 7 puzzle assets (already-solved
  pages, known plaintexts necklace/popcorn/love + ducks/pump/premium) and
  the Level 0 hint page into the repo. Calibrating the author's mechanism
  on a known answer is the only lead that is not a blind guess.
