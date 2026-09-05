# Level 8 working notes

## Official clue grid3_easier (2026-09-05) — see PREREG_GRID3_EASIER.md

Author: "We removed some of the numbers you don't need." Verified reading:
official 7×6 grid minus 5 cells (last row, cols 2–6) = digits `6 1 8 4 9`
removed, 37 remain.

- **KEY FINDING:** the removed 4-cell run `6 1 8 4` = **FAHD** (A=1..I=9) —
  the UNIQUE position of that word-search junk hit. The author removed
  precisely FAHD's cells (+adjacent 9) → the A=1..I=9 word search is the
  author-relevant grid reading (P≈4.5e-5 for arbitrary removal; 1/7 if
  last-row targeting).
- KILLS (all controlled): T1 survivors = ACID CHEF FICA FIFE GEED = 5 junk
  (≠3, no len≥5) — word-search refinement dead as answer producer. T2
  37-digit multi-tap = chance (control 461/1000). T3 removed 61849 = no
  word/phrase (61849=127×487). T4 removed digits = exactly the 5
  non-primes, p=0.00423; prime-cell follow-up barren (0/1000 control).
  T5 repo-wordlist survivors = 4 words ≠ 3 (frequency cut forbidden).
  T6 no planted glyph markers (1/5 size-outlier; true outliers remain).
- **OPERATOR RULING:** word-search survivor class DEAD — grid-word
  answers already rejected in prior rounds (all orders killed); no survivor
  or combo will be submitted. Clue residual value: canonical 37-cell grid +
  removed-cell exclusion for any future non-word-search mechanism.
- **No new answer candidate.** Queue unchanged: `call touch reach` ×6 →
  `two zero seven`. Only remaining lock: image07 passphrase.

## COMPLETE MAP (2026-09-05) — see COMPLETE_MAP.md

Consolidated inventory: grid.png (XMP/eXIf + 6-file ZIP, verified), image01
(artist/XMP, readable), image02/06/12 (proven empty by full 2^32 scans),
image04 (Stevie cover, embedded name image11.jpg, blank passphrase),
image07 (19.3 KB payload — **the only remaining lock**, unknown passphrase),
3 nested covers terminal with zero trailing bytes.

## VERDICT 2026-09-05 — image07 payload claim VERIFIED (see VERDICT_PAYLOAD_CLAIM.md)

- `image07.jpg @ 0f58d719` → steghide magic **0x73688d**, version 0,
  rijndael-128/CBC, nplainbits 157,865 (19,733.1 B plain), enc stream 19,760 B.
  Two independent pipelines (C/libjpeg.so.62 + pure Python) with the FULL
  encrypted streams **bit-identical** (image07 158,079 b; image04 390,527 b).
- **INDEPENDENTLY CONFIRMED (f02ddfa, 2026-09-05):** full 2^32 `stegseek
  --seed` scans — image04 HIT (3b75655e+metadata), image07 HIT
  (0f58d719+metadata), image02 MISS, fresh synthetic MISS. The counter-claim
  (capacity-conflation) is dead: its controls tested `steghide info` capacity,
  never seed mode. The 88-vs-81.893 count was a failed crack (random fold
  collisions), never payload evidence.
- Original "0xb3eb88" claim was a jpeg_dct.py dequantization bug — fixed (RAW
  mode reads quantized coefficients, exactly what libjpeg/StegSeek see).
- Format: steghide JPEG = 3 samples/vertex (fork JpegFile.h), capacity =
  numSamples/3 bits (matches swarm 55.6 KB for image07 exactly).
- **seed = LE32(XOR-fold(MD5(pw)))** (validated 7/7 + cover control; StegSeek
  -p mode implements it). ARITHMETIC: H("") = 3b75655e = image04's seed →
  **image04 passphrase = "" (my earlier "refuted" claim WITHDRAWN — overreach
  corrected in VERDICT_PAYLOAD_CLAIM.md)**.
- OPEN (my side): image04 stream does NOT decrypt under key=MD5("") at any
  offset 33–73 / 20+ key variants (49-bit oracle, AES re-verified FIPS C.1).
  Ground truth (H("") seed + swarm's successful `-p ""` extraction) says the
  passphrase IS blank → the author's steghide build (which the swarm runs)
  must derive the AES key non-standardly, or my evs pipeline has a subtle
  bug. Close with one synthetic carrier (known-answer) or the author's
  binary. Does NOT affect the payload verdict.
- Operational: origin/master = single-commit rewrite, tip f02ddfa. 7ff5f1b
  does not exist on the server — never pushed (like d69ca74 before it; treat
  that source as untrusted until verified). Local re-clone dropped 6188fb4
  objects; branch recovered via fetch + reset --mixed.

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
(129px cols, ~133px rows), RGBA alpha all 255. (CORRECTION 2026-09-05: the
old "no EXIF/text chunks" line was wrong/incomplete — grid.png carries an
XMP/eXIf chunk at 0x1ce and an embedded ZIP at 0x2059e containing all six
carrier files byte-identical to top level. See COMPLETE_MAP.md.)

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

--- (agent-2 sections merged back) ---

## 2026-09-04 (agent-2): steghide verification, Artist keyword, census correction, FINAL RANKED CANDIDATES
Verified against force-pushed master (a0a9fd2..071d0bf):
- image04.jpg blob identical to swarm's; steg04.jpg sha256 == 7643d732... ==
  swarm's documented extraction; artist_hidden.jpg sha256 == 83431008...;
  both covers viewed: Stevie Wonder "I Just Called To Say I Love You"
  single cover; DM "Personal Jesus" cover. FULL INVENTORY now 5 covers +
  4 photos, all verified on disk.
- image12 EXIF: DateTimeOriginal 2018:07:28 20:05:53, Modify 2018:08:19
  00:25:37 (Windows Photo Editor). 2018-07-28 20:05 = "LoveLoud 2018"
  (Imagine Dragons/Zedd/Mike Shinoda), Rice-Eccles Stadium, Salt Lake
  City, UT — matches the LOVELOUD shirt. Photo identity/date confirmed.
- image01 tEXt keyword CORRECTED: it is "Artist" (7 chars + NUL), NOT
  "st" — earlier off-by-4 chunk parse (data starts at 41, not 45).
  "Artist" is a standard EXIF tag name. Swarm's A-insertion is REAL:
  M D W R O D + A (keyword "Artist") = M A D W R O D.
- image01 XMP date 1987-02-25: US #1 song that day = "Livin' on a
  Prayer" (Bon Jovi, 4 words); "Who's That Girl" single released June
  1987 (not Feb 25). Date-as-key thread: no clean 3-word hit. Likely
  decorative mid-80s Madonna-era date.
- Mad World background (searched): original 1982 T4F single (B-side
  "Ideas as Opiates"), 1998 reissue, Donnie Darko version by Michael
  Andrews feat. Gary Jules (B-side "No Poetry"), 1967 TV film "Mad
  World" starring Lane Morrison. 3-word next-steps: "lane morrison",
  "ideas as opiates", "mad mad world" (lyric). "tears for fears"
  (2-word-style band name) already INVALID; gary numan / donnie darko /
  gary jules / michael andrews are 2 words (format mismatch).

### METHODOLOGY CORRECTIONS (do not re-rely on old numbers)
- The old "exactly 3 words len>=5" T9 census was STRAIGHT-LINE-ONLY
  (itertools over fixed lines after the DFS timeout). Full 8-dir Boggle
  census: original grid has ~3024 dict words (hundreds len>=5); swapped
  ~3106. Background sparsity stats (10.22/4.78/4.55 means) are invalid —
  grid is a normal T9-Boggle board, no curation in the word COUNT.
- Path-UNIQUness is NOT a signal: 1,590 len>=3 words have exactly one
  path on the original grid. MAD/WROD uniqueness is generic noise; only
  the artist-initial coincidence is designed.
- Mask-remainder (remove MAD+WROD or MAD+WORLD cells, T9-search the rest):
  813/750 words len>=4 = noise. Dead.
- Lyric trigrams (all 3 words present as Boggle words): ~57+ per grid —
  too many to select (devils in it / on my knees / tell you how /
  still love you / i got you / mad mad world...). Grid presence alone
  cannot discriminate.

### SWAPPED-GRID EFFECT (7/6 at R2C5/R3C4)
Gains: world, knees, myself, see, man, seen, and, two.
Losses: say, save, dark, hear, her, saw.
Gain/loss sets are both lyric-meaningful (PJ "on my knees"/"see", PDP
"a good man"/"seen your kind", Mad World "world", PDP "save me from
the dark", MW "can hear me", Stevie "to say i love you"). The swap is
the transposition-motif completion (WROD->WORD/WORLD) but remains
unevidenced as the "true" grid.

### GRID PRESENCE OF CONTENT WORDS (for reference)
orig: mad know hear this feels love you say still tell need time
  devils kind life been got only save dark move la island? (isla
  spellable, not in dict) god plan yellow (Drake/Wiz photo songs!)
swap-only: world knees man seen see myself
absent: isla(in dict) loud prayer livin shine faith jesus called
  just believe ready again black ghost preach papa bonita

### FINAL RANKED CANDIDATES (for user submission, in order)
1. `i just called` — ONLY untried 3-word cover candidate. Stevie cover
   (steghide, empty password = author's simplest layer) title is 8
   words; natural 3-word ends: last3 "i love you" (REJECTED) vs
   first3 "i just called" (untried). Swarm's own queue had exactly this
   order. Clean rule: "opening of the steghide cover's title".
2. `mad mad world` — the lyric fragment of the MAD WORLD intermediate
   ("...in this mad, mad world"); all 3 words Boggle-present on the
   swapped grid; "mad" is the designed acrostic word. Needs the swap.
3. `i got you` — B-side of the Ghostbusters single ("I Got You (I
   Believe in You)"); 3 words; i/got/you all present on ORIGINAL grid;
   image06 is the odd cover (200x199, not 300x300).
Rejected/avoid: every grid T9 word order (incl KST), la isla bonita,
papa don't preach (all 3 forms), i love you, tears for fears,
personal jesus (2w), ghostbusters (1w), lane morrison, ideas as
opiates (too obscure vs "try not to overthink it").
## 2026-09-04 (agent-2): repo-upload verification + FINAL RECOMMENDATION [SUPERSEDED by later sections — kept for record]
Repo gained commits c184a00 (hidden/ + HIDDEN_FINDINGS.md), 2afbb10 (this
section's predecessor), 417348c (Dex upload: 2059E.zip, F341, F341.zlib,
6 images, tk-hunt-grid_original.png). Verified:
- tk-hunt-grid_original.png md5 == grid.png (same file).
- 2059E.zip == grid's trailing ZIP, byte-identical 6 entries. DEAD.
- F341.zlib = zlib(raw IDAT scanlines of grid.png, corrupted ~row 204 +
  adler mismatch) + IEND + same trailing ZIP. Tooling byproduct. DEAD.
- F341 = empty placeholder.
- Artist-field cover (hidden/artist_hidden.jpg == forensics/view/
  artist_embed.jpg, md5 f20d52aa) VIEWED: it is Madonna "PAPA DON'T PREACH"
  single cover (B&W portrait, leather jacket, vertical "MADONNA PAPADON'T
  PREACH" text). Earlier "Ray of Light" label (mine and user's screenshot
  caption) is a MISID. HIDDEN_FINDINGS.md is right.
- image01.png structure: IHDR + tEXt kw "st" (20141 B) = base64 data-URL
  (claims image/png, payload is JPEG /9j/), trailing "\n" before CRC;
  iTXt com.adobe.xmp (dc:date 1987-02-25, ExifTool 12.76); IDAT = cover.
- Exhaustive payload scan of ALL 8 images (b64 blobs >=200ch, ASCII runs
  >=40ch, data-after-EOI, EXIF/XMP strings): NO other hidden payloads.
  eXIf-chunk "Personal Jesus" JPEG: Photoshop CS Windows XMP 2016-12-19,
  1000x1000, ICC, 1 trailing 0x00 byte only. Nesting TERMINATES at
  Papa Don't Preach.
- Photo IDs (viewed full-size): image02 = R. Kelly per user (previous
  agent guessed Drake; cap has clover+MLB-ish patches — unconfirmed);
  image04 = dreadlocked rapper, teardrop tattoo, nose ring, hand pendant
  (previous: Wiz Khalifa; likely Lil Wayne — unconfirmed); image07 =
  blonde guitarist, black wide-brim hat + leopard band, orange aviators,
  white blouse + leather skirt + OTC boots, PURPLE-wound mic, white
  single-cutaway w/ black scroll inlay, red stage, male bandmate in flat
  cap (Paramore/Rearviewmirror-era look; unconfirmed); image12 = white
  male stadium singer, rainbow "…OUD" tee, heart pendant, Canon SX410
  EXIF 2018-08-19 00:25:37, no GPS (previous: Dan Reynolds 2018-07-28).
- Wix files contain no answer string; velo_dve99.js = stock
  validatePasswordAndAssignRole gate (server-side). "don't" hits in
  tb8_0.json/page JSON are boilerplate.

### THE NESTING (verified, hand-redoable)
grid.png
 ├─ eXIf chunk (62,220 B after IEND region) → 300x300 "Personal Jesus"
 │   (Depeche Mode) cover [depth 2]
 └─ trailing ZIP → 6 images [depth 2]
     ├─ image01.png = 300x300 Madonna "La Isla Bonita" cover
     │   └─ tEXt "st" base64 → 300x300 Madonna "PAPA DON'T PREACH" cover
     │       [depth 3 — unique deepest layer]
     ├─ image02/04/07/12 = performer photos (decoys)
     └─ image06 = "Ghostbusters" (Ray Parker Jr.) cover [depth 2]
Exactly THREE images are 300x300: Personal Jesus, La Isla Bonita, Papa
Don't Preach — one per depth of the chain. Rule: "the 300x300 cover hidden
INSIDE another image is the answer."

### FINAL RECOMMENDATION (do NOT auto-submit; user constraint)
1. `papa don’t preach` — curly apostrophe U+2019 (straight-U+0027
   already REJECTED as submit #9). Rationale: unique deepest layer;
   only 3-word title with punctuation (official rule: "Punctuation
   matters"); English (vs Spanish "la isla bonita"); "Try not to
   overthink it" = just find the deepest hidden image.
2. `papa dont preach` — if the author dropped the apostrophe.
3. `la isla bonita` — layer-2 decoy candidate (island theme), weakest:
   no punctuation, Spanish, and the author nested a deeper cover inside
   it (treasure is never shallower than the bait).
Grid T9 (kelli smelt tills etc.) is DEAD per user rejection; grid is a
decoy ("BLOCK GRID THINGY" misdirection, banana-video T9 bait).
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

## 2026-09-04 (agent-2, post-442f5cc): Wix model mining, live reads, rule hunt, 10-letter hit

### Wix page model (page_dve99.json) fully mined
- L8 grid image = `static.wixstatic.com/media/0d5510_2edf85d9a3374cc2b99661a8384a96ae~mv2.png`
  (1176x1056, file name/alt = "level8.png"). L6/L7 grids are therefore
  almost certainly "level6.png"/"level7.png" on Wix media — member pages only.
- **UNSEEN ASSET ON L8 PAGE: ChatGPT-generated image, 1254x1254**, file name
  "ChatGPT Image Aug 8, 2026, 02_09_44 PM.png", linked to Home.
  PUBLIC url (no login): `static.wixstatic.com/media/c217b5_fa5946b9ac6647d08322089d4a4680b5~mv2.png`
  Never viewed by anyone in the swarm so far. NEEDS OPERATOR EYES.
- Full L8 member-page text content = "BLOCK GRID THINGY" (h2, underlined
  link -> youtube jZcrSUhonBk), a lone ".", and footer "TREASURE KRACKEN 2026".
  Nothing else. No form placeholders, no hidden labels.
- "BLOCK GRID THINGY" video ("Fun Facts About Bananas", Kyle Wood, 2025-09-17,
  11:28) transcript mined in full: generic banana trivia, no numbers/grid/
  puzzle content. Joke/decoy, or "block grid" = Boggle-board metaphor
  (Boggle = grid of letter blocks). Either way no answer content inside.
- pagesMap: L6=q10kp, L7=rfoq0, L8=dve99, TOOL=jyh0e — none have
  pageJsonFileName (member-fetched models only). COWLAZARS page = giveaway
  background only. /blog, /post, /tool, /template all member-gated.
- Guest HTML of level pages contains NO level content (Wix member-only pages
  serve the sign-up prompt only) -> even a working raw-HTML proxy could not
  yield L6/L7 grids. All CORS proxies failed anyway (allorigins 522,
  codetabs 522, corsproxy API-key, thingproxy dead).
- **Only path to L6/L7 grids: operator's member browser** (open level-6/7,
  screenshot or transcribe the 42 digits, or copy the image URL).

### Public leaderboard (first public view)
- 24 members tied at top label "Level 7" (Dave, Logan, Noah, BlueElvis,
  Candy, FireGypsy, Darkslyde11, SikBeatz, Anne, Cyndia, Echoless, Caden,
  Kn'uthin, Tanya, Abbie, Julie, Shrodinger's Gold, Cor, retro, Stormy,
  Tawny, Brute_Forcing, Horse Adams, Michael), then Level 6 x3, Level 5 x7,
  Level 4 x5, Level 3 x11, Level 2 x13, Level 1 x14+.
- Interpretation consistent with operator being on L8: label = highest level
  CLEARED -> "Level 7" = on L8. **NO ONE on the board has cleared L8.**
  L8 is the live frontier (24+ members racing).
- retro (#19, hence on L8) asked in Q&A 10h ago: "Tell me labyrinth trick.
  But tell no one else." -> "labyrinth" plausibly = L8 grid path puzzle;
  admin did not answer publicly.

### Q&A feed (guest-rendered subset of 27)
- Admin: "Level 0 does not need to be solved to reach level 1. Level 1 just
  unlocks on Halloween at noon. Level 0 does give a little hint for later on
  in the game though." + "part 2 from 0" / "3 of 0" = L0 has parts.
- Q&A list is JS-paginated; the question "What does the number 1 represent?"
  (and any admin answer to it) is NOT in the guest render. ASK OPERATOR:
  scroll the full Q&A — an admin answer about digit 1 would be decisive.

### Rule hunt on L8 board (forensics/rule_hunter.py, /tmp/wp_orig.pkl)
- Board word set: 1650 dict words; 892 "common" (wordfreq >= 3e-6).
  1=wall vs 1=passable: identical top lists.
- Longest common words: violation(9) injection(9) election(8) | florida(7)
  helpful(7) swallow(7) testify(7) explode(7) whiskey(7) violate(7)
  isolate(7) playful(7) shuffle(7) | really(6) before(6) player(6)
  figure(6) listen(6) expect(6) broken(6) ...
- No 3-word tiling of all 42 cells. 191,494 pairwise-disjoint common triples
  -> "disjoint" alone is NOT a pick rule. No common word whose every path
  touches a 1-adjacent cell. Straight-line one-letter-per-digit dead
  (only kyle/lyle/teed/adz/eat/fat/ola/old/own/ted/tee).
- Labyrinth direction hypothesis (digit = numpad/phone direction, 5=stop,
  fwd+rev): max chain length 5. DEAD (forensics/labyrinth.py).

### KEY HIT: top-3 longest common words = exactly 10 distinct letters
- violation + injection + election -> union {v,i,o,l,a,t,n,j,e,c} = 10.
  Same as BOTH known answers (L6 10, L7 10). (forensics/tenletter.py)
- But census: 9,559,321 of C(589,3)=33.6M common triples also have exactly
  10 distinct letters (~28%) -> 10-distinct is a weak filter by itself.
  The "top-3 longest common words" rule is what selects them; the 10-letter
  hit is a consistency check that matches the house pattern.
- Max-total-length triple for each distinct-count (10..17): 10-distinct is
  the max-length bucket (26 = violation+injection+election), unique.
- wordfreq scale (for calibration): love 6.6e-4, premium 2.1e-5, pump
  1.9e-5, ducks 7.9e-6, popcorn 5.4e-6, necklace 7.1e-6; artifacts beached
  4e-7, cicada 3e-7, gaaffed 0. Threshold 3e-6 separates answer-class words
  from unique-path artifacts cleanly.

### CURRENT LEAD (pending L6/L7 calibration)
- Mechanism: T9 keypad + Boggle 8-dir traversal (survives distinct-letter
  proof; matches covers-as-instructions + "BLOCK GRID THINGY" = Boggle).
- Pick-3 candidate rule: the THREE LONGEST common words on the board.
- L8 candidate answer: **violation injection election**
  (order unknown — house order not length-sorted: L6 8,7,4 desc but L7 5,4,7
  not; order rule = open; 6 permutations submittable).
- MUST VERIFY on L6 grid (top-3 longest common = necklace popcorn love?)
  and L7 grid (= ducks pump premium?). If both check out, submit orderings.
- Fallback leads if top-3-longest fails calibration: unique-path words
  (6 known, but not "common"), disjoint-triples with 10-letter union,
  1-cell-anchored rules, ChatGPT-image content.

### Asks to operator (unblock the hard solve)
1. L6 grid: 42 digits (7 cols x 6 rows) or screenshot / image URL.
2. L7 grid: same.
3. Open the ChatGPT image URL above (public, no login) and describe/save it
   (suggest: hidden/chatgpt.png in repo).
4. Full Q&A feed: is there an admin answer to "What does the number 1
   represent?" (or any digit-1 / format question)?
5. (optional) L0/TOOL page content — "little hint for later in the game".

### Calibration harness + structure details (forensics/calibrate.py)
- calibrate.py "<42 digits>" "w1 w2 w3" tests the rule battery (R1 top3
  longest common, R2 top3 longest dict, R3/R4 unique-path, R6 greedy
  disjoint, order variants) against a known answer. Ready for L6/L7.
- L8 structure (canonical grid): max board word length = 9. ONLY two
  9-letter words exist: violation, injection (both unique-path). 16
  8-letter words: election goldfish firewall deletion hologram ejection
  valkyrie forklift flywheel glycerin workweek disallow milkweed
  wildfowl lifework oilcloth — election is the most common by 60x
  (1.2e-4 vs next 1.9e-6). So "top-3 longest common" = forced pair +
  clear 3rd.
- R3 check: top-3 longest UNIQUE-PATH words also = {violation, injection,
  election} (4th: firewall). Two independent selection rules converge.
- All three words' paths start in the top-left corner region (all include
  cells (0,0),(0,1),(0,2),(1,0),(2,0)). Order tie (violation/injection,
  both len 9): freq says violation first; alpha says injection first.
  Six permutations are submittable; 1/min free.
- Swapped-grid variant (1,4)<->(2,3) for reference: top-3 longest common =
  selection violation injection; 9-letter words there: selection,
  violation, injection, rejection, culminate, fulminate. (The
  "-ection" cluster is a tempting decoy of the wrong grid.)
- ChatGPT image: OCR'd via ocr.space (demo key) — NO TEXT detected;
  pure illustration. Visual ID still unknown (operator eyes).
  Gird_Background.jpg: OCR clean, no text (pure background).

### L8-STANDALONE derivation (per operator: no cross-level dependency)
- 8-letter tier profile (len, #paths, digit-set, corner(0,0)): election
  {2,3,4,5,6,8} corner; deletion {3,4,5,6,8} corner; ejection
  {2,3,4,5,6,8} corner; oilcloth {2,4,5,6,8} corner; goldfish {3,4,5,6,7};
  firewall/hologram/valkyrie/forklift/glycerin/disallow/milkweed/wildfowl/
  lifework use 7 and/or 9; flywheel/workweek lack corner.
- 10-distinct check on the -ection family: violation+injection+ELECTION =
  10 distinct; violation+injection+EJECTION = 10 distinct (ejection has the
  same digit set); DELETION = 11; OILCLOTH = 11. So 10-distinct does NOT
  break the election/ejection tie; COMMONNESS does (election 1.2e-4 vs
  ejection 1.2e-6; house format demands common words).
- FINAL L8-ONLY CASE: board max = 9, exactly two 9-letter words
  (violation, injection — forced); 3rd = commonest 8-letter word = election.
  Triple = unique-path, corner-anchored, 10 distinct letters, zero letters
  from keypad 7 (pqrs) or 9 (wxyz) — the board's 7s/9s are decoys.
- Submit order (user, 1/min free): violation injection election ->
  injection violation election -> violation election injection ->
  injection election violation -> election violation injection ->
  election injection violation.

### 2026-09-04 (agent-2): cover-keyword board test RETRACTED + new untried queue
- BUG RETRACTION: earlier "boggle_hits" (love/papa/jesus/isla = 1 each) was
  FLAWED (no visited-cell tracking; cell revisits allowed). True Boggle DFS:
  only LOVE is on the board. Cover-keyword-on-board hypothesis DEAD.
- 1=letter sweep (all 26, straight segments len>=5): no mapping yields a
  clean 3-word set. 1=i -> known IDIOM/TAINT/SHEIK set (tried, dead);
  1=r -> 9 junk words; others 0-4 noise.
- Row/col runs with 1=separator (T9 1-letter-per-digit): only hub, iva, owe,
  sal, pal, dirk, fisk, disk, tin, vim, tho, tim, thy. No triple.
- T9 codes of CALL(2255)/TOUCH(86824)/REACH(73224): NOT in grid (no straight
  line, no Boggle path). Grid does not confirm the cover-verb triple.
- Planted-word chain (structural): TILLS->SMELT->KELLI share cells
  ("labyrinth" per retro); HOMIE isolated. "tills smelt kelli" (TSK) never
  submitted (bot halted before K-chain).
- UNTRIED QUEUE (all L8-standalone, all never submitted):
  1. `block grid thingy` — the page's only multi-word text (link anchor);
     3 unrelated common words; "try not to overthink it"; banana video =
     click-bait decoy; grid self-describes as the "block grid thingy"
     (board contains GRID; site bg literally named Gird_Background.jpg;
     board contains GIRD too).
  2. `call touch reach` + 5 perms — cover-lyric contact verbs (GB "who you
     gonna call", PJ "reach out and touch faith", Papa "P-reach"); the
     covers-as-instructions words taken literally; no order rule -> try all.
  3. `two zero seven` — grid digit sum = 207; "letters and numbers are fair
     game"; trivial hand derivation. (Weak: 207 unremarkable vs mean 210.)
  4. `see you again` — hidden Wiz Khalifa photo (image04 zip layer); 3-word
     title. (Phrase-shaped; lowest priority.)
  5. `tills smelt kelli` — the planted-word chain order (the "labyrinth").
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

## 2026-09-04 (agent-2) THE DERIVATION: corner -TION braid = the planted answer

### New intake (7 swarm commits, 442f5cc..ab63ca5)
- L6/L7 are DIFFERENT puzzle types (L6 rooms/torch/checkpoint, L7 neon
  labyrinth-fork — level7_q1/q4.png are neon corridor assets, NOT digit
  grids) -> NO shared grid convention exists -> cross-level calibration is
  impossible; operator's "standalone" ruling confirmed by evidence.
- ChatGPT image located: it lives in the MASTER-PAGE (site header) section
  of the model (comp-mdq6p6xf_r_*, links Home) -> site-wide decorative art,
  NOT L8 page content. Red herring cleared.
- Swarm background test (60+ random grids): Boggle uniqueness/longest-tier
  all at chance; cover vocabulary ABSENT from board (convergence falsified);
- Phone theme locked at 8/8 music items: GB "who you gonna CALL", Stevie
  "I just CALLED", PJ "REACH out and TOUCH faith", Papa "don't P-REACH",
  Drake=HOTLINE BLING, Wiz Khalifa=PAYPHONE, Orianthi=RING MY BELL,
  Dan Reynolds=CALLING. Mechanism = phone keypad; open item = selection rule.

### The structure (code-verified, the only non-chance feature on the board)
Three single-path words share the board's top-left corridor and all end on
the same 4 cells (1,0)->(0,0)->(0,1)->(0,2) = T-I-O-N:
- violation : (5,0)v (5,1)i (4,0)o (3,1)l (2,0)a | t i o n   [9, unique path]
- injection : (5,1)i (4,0)n (3,1)j (2,1)e (2,0)c | t i o n   [9, unique path]
- election  : (3,2)e (3,1)l (2,1)e (2,0)c | t i o n         [8, unique path]
Facts: only two 9-letter words on the whole board (violation, injection);
election = most common of 16 eight-letter words (60x gap); union = exactly
10 distinct letters (house style); no letter from keypad 7 (pqrs) or 9
(wxyz) — the board's 7s/9s are decoys; branches weave through the same
cells (5,0)/(5,1)/(4,0)/(3,1)/(2,1)/(3,2) = a 3-strand braid into -TION.
The planted straight-line words form a connected labyrinth — TILLS (up
col 4) -> SMELT (diagonal) — which passes (3,2)=election's E and ENDS at
(5,0)=violation's V (retro's "labyrinth trick").
NEVER SUBMITTED (swarm log: "I did not submit anything").

### SUBMIT (user, 1/min, free) — set is derived; order is the only unknown
1. violation injection election   (labyrinth endpoint; length order)
2. election violation injection   (start-cell reading order)
3. injection violation election
4. violation election injection
5. election injection violation
6. injection election violation

## 2026-09-04 (agent-2) SOLVED: the grid is a T9 keypad of the puzzle's own vocabulary

### The misread that held us up
steg04.jpg (steghide "Stevie" stash in image04) is the STEVIE WONDER "I Just
Called To Say I Love You" LP cover — NOT a second DM cover. exif_personaljesus.jpg
(grid eXIf) is the DM "Personal Jesus" single cover. Nine songs total, all
phone-themed: Personal Jesus, La Isla Bonita, Papa Don't Preach, Hotline Bling,
Payphone, Who You Gonna Call, Ring My Bell, (Dan Reynolds/LoveLoud 2018 photo),
I Just Called To Say I Love You.

### The grid's own vocabulary (code-verified, full 73k-word census)
Only TWO non-common words exist on the board: **keypad** (539723, unique path,
(4,6)->(3,6)->(2,5)->(1,4)->(1,5)->(0,4)) and **isla** (4752, unique path,
(0,3)->(1,4)->(2,4)->(1,5)) — braided through the same top-right cells.
keypad = the mechanism (T9 phone keypad). isla = pointer into the image set
(La Isla Bonita = image01). Common-word fragments are chance (swarm baseline)
EXCEPT the title-fragment set, which is structural:

### THE RULE (the decisive test)
Test every one of the 9 song titles against the keypad board, counting
len>=3 title words that have a path:
- I Just Called To Say I Love You -> say(729,1p) love(5683,1p) you(968,1p) = **3**
- Who You Gonna Call -> who, you = 2 (call/gonna absent)
- Ring My Bell -> bell = 1 | La Isla Bonita -> isla = 1
- Hotline Bling, Payphone, Papa Don't Preach, Personal Jesus -> 0
ONLY ONE title yields exactly three words: the steghide-hidden Stevie cover.
just(5878) and called(225533) are deliberately ABSENT — the grid excludes
"i love you" (already rejected by user) and forces "say love you".
Geometry: love & you share the O-U cells (0,1)=6,(1,0)=8 (braided pair);
say sits at (1,4)(1,5)(2,5) — the planted cluster.

### ANSWER (title order, derived): `say love you`
Fallbacks only if order is the sole miss: love say you / love you say /
say you love / you say love / you love say

## 2026-09-04 (agent-2, post-ce43069) residual pass: kills + final steghide package

### New intake (00e9cfe, ce43069)
- Corpus steghide sweep KILLED per swarm (1,758,842 candidates, 4/4 no
  passphrase, controls clean). image04 = BLANK-password steghide, payload
  named image11.jpg internally.
- PICDIGIT chain (picture-alphabet Boggle): widow-droid-cop RETIRED;
  MAD WORLD dead (WORLD unformable); tears-for-fears submitted INVALID.

### New kills this pass
1. **F341.zlib (3,216,754B) = swarm byproduct, not a puzzle artifact.**
   zlib header 78da but stream breaks within the first 64KB ("incorrect data
   check"); inflates to ~4.15MB of mostly-zero bytes. No match to
   zlib(grid variants) at levels 6/9, raw/stored. F341 = 0-byte failed
   extraction. Logged as forensics detritus.
2. **Public page surface CLOSED.** sitemap.xml mined: pages-sitemap =
   leaderboard/qa/terms/cowlazars/ig/pasthunts/home/gulag only (all read:
   pasthunts = 3 past winners, no puzzle content; gulag = tetris-escape text,
   "You are NOT in timeout"). /twilio and /twilio-page = soft-404; /test ->
   gated "Endless Art" signup wall; /winner gated.
3. **/twilio/{Ash,Aiden,Jess,Morgan} = the only fresh surface found.**
   dynamic-twilio-sitemap.xml (dated 2026-09-04) lists four member Twilio
   pages: Ash Stowe, Aiden Johnson, Jess White, Morgan James. Guest view =
   name only, zero content. Member-gated. These four names are the only
   public artifacts on them; testing names against the grid is forbidden
   post-hoc label selection (standards). Actionable only by a member: open
   these four URLs logged in; if any shows SMS-thread content, that is new
   puzzle material.
4. **KILL: "say love you" title-fragment rule — background control FAILED.**
   Pre-registered event: "IJC title contributes exactly 3 len>=3 words to the
   board and no other title does." 1,000 histogram-preserving random grids:
   P(any title = 3) = 26.3%, P(IJC = 3, others <= 2) = 25.9%, P(exact
   say/love/you present + just/called absent) = 13.7%. The rule is chance
   (1 in 4 grids). The title-fragment pattern on the grid is NOT planted.
   "say love you" joins the burn pile as a killed theory (never submitted).

### Final steghide residual packaged (for swarm/user machine)
- PREREG_DICTIONARY_STEGHIDE.md + steghide_dictionary.txt (145,406 frozen
  entries: words.txt 3-normalization) + run_dictionary_sweep.sh with
  positive/negative controls. Completes the steghide key space (corpus +
  dictionary). After this, forensics on the four carriers is COMPLETE either
  way — no further steghide work is legitimate.

### State of the well (honest)
Every label-dependent scheme is dead (artist disputes), every grid-reading
scheme dead, all forensics closed or about to be, content-derived triples
submitted 4x (tears for fears / widow droid cop / i love you / papa x2) and
invalid. Remaining surfaces: the four member-gated /twilio pages (user
action), and genuinely-new-mechanism search, which this pass found no
pre-registerable candidate for.
