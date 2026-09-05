# My solve pass (2026-09-04) — convergence falsified, Boggle closed

## Inputs checked
- `grid_hidden_image.png` (operator's file): viewed — it is the Depeche Mode
  "Personal Jesus" single cover (DM/PERSONAL JESUS, 300x300), i.e. a PNG
  re-export of the already-banked eXIf layer, not a new layer. Spotify links
  resolve to Depeche Mode / "Personal Jesus - Original Single Version". No new
  content from either pointer.
- WORLD re-verified: 0 Boggle paths under pure T9 (needs the unevidenced 7/6
  swap). TEARS: 0 paths. MAD WORLD TEARS is dead independent of letter counts.
- Full cover/phone vocabulary swept for exact T9 Boggle path counts (cap 3),
  pure-T9, 1-cells dead (~80 words: titles, artists, lyric hooks, phone theme,
  site words). Theme words are overwhelmingly ABSENT: personal, jesus, reach,
  touch, faith, called, call, ghost, hotline, payphone, phone, dial, ring,
  voice, stevie, depeche, mode, preach, bonita, bloco/thigy ALL zero paths.
  Present-with-unique-path commons: say, love, you, who, dan, loud, mad, hear,
  cell, hello, line, ray, owen (+isla/keypad non-common).

## Decisive background test (kills the whole Boggle family)
Exhaustive trie-DFS over 27,308 common words (POP+G10K), path counts capped
at 2. Unique-path words are the NORM, not the exception:

len 3: 269/563 unique | len 4: 365/651 | len 5: 243/430 | len 6: 134/236
len 7: 41/58 | len 8: 13/17 | len 9: 2/4 | len 10: 0/1

190 unique-path words at len>=6, no triple among them. SAY/LOVE/YOU (and MAD,
WHO, etc.) uniqueness is exactly chance-level. No selection rule can be built
on Boggle presence, uniqueness, or longest-tier. The convergence design
(covers name the words, grid confirms them) is FALSIFIED: the grid does not
contain the cover vocabulary at all.

## Honest state
No answer is derivable by me from Level-8-internal material. Grid mechanisms:
all at chance. Covers: theme only, no selection. Page: exhausted
(page-render.md + banana video dead). Remaining surfaces all need live reads:
Level 0 hint page, TOOL decoder, /qa text, retro's Discord claim.
Best guess-shape on record remains violation/injection/election (shared TION
tail + 10 distinct letters are real; the pick rule is not). UPDATE: the
violation/injection/election orders, TSH/SIT/STI/TIS/TSI, `i just called` and
no-apostrophe Papa all came back INVALID on the live gate. I did not submit
anything and did not touch the live gate.

## Addendum: steghide + metadata sweep (all dead)
- EXIF on image02/04/06/07/12: stripped except image12 (empty UserComment /
  Image Description, Windows Photo Editor, 2018-07-28 — all known). No
  base64-length blobs in any JPG via strings.
- 56 fresh cover/grid passwords x image02/06/07/12 (madworld, tearsforfears,
  banana(s), kylewood, hotlinebling, payphone, ghostbusters, whogonnacall,
  personaljesus, reachoutandtouchfaith, blockgridthingy, level8,
  treasurekracken, loveloud, orianthi, reynolds, imaginedragons, drake,
  wizkhalifa, maroon5, rayparker, madonna, islabonita, papadontpreach, stevie,
  wonder, ijustcalled, depechemode, violation/injection/election, plus spaced
  and apostrophe variants): 224 attempts, 0 hits. Steganography is closed.

## Addendum 2: layer-4 forensics closure (personally verified)
- grid.png chunk walk: IHDR / eXIf(62220) / 9xIDAT / IEND, then appended ZIP.
  No other chunks. Nothing else to carve.
- image01.png: IHDR / tEXt(Artist, 20141) / iTXt(437) / 2xIDAT / IEND. The
  iTXt chunk dumped in full: keyword `XML:com.adobe.xmp`, content is ONLY the
  XMP packet with `dc:date 1987-02-25` (La Isla Bonita release). No payload.
- eXIf TIFF walked IFD by IFD: IFD0 = X/YResolution + ResolutionUnit +
  YCbCrPositioning; IFD1 = Compression(6=JPEG) + resolutions + JPEG offset
  172 / length 62047. No ImageDescription/Artist/EXIF-subIFD/GPS/second image.
  The chunk is fully accounted for.
- All 9 JPEGs (6 ZIP + 3 nested): EOI at EOF-2, zero trailing bytes, no COM
  segments, no nonstandard APPn. Terminal, every one.
- ZIP: entries in numeric order, no comments, stock 24-byte UT/ux extras.
  Only anomaly: image01.png stamped 2s after the other five (assembly order,
  consistent with it carrying the Artist payload). No signal.
- CONCLUSION: the forensics chain is closed. There is no layer 4. Every
  extractable byte has been extracted; every cover answer tried is dead.

## Addendum 3: multi-tool carrier sweep (2026-09-04)
- `steghide info image04.jpg -p ""` reports the embedded file's TRUE name:
  **`image11.jpg`** (47.7 KB, rijndael-128/CBC, compressed). Re-extraction
  hash-matches steg04.jpg (7643d732...). So missing slot 11 = the Stevie
  cover itself; still missing: 03, 05, 08, 09, 10. (One payload per carrier;
  image04 holds nothing else via steghide.)
- outguess (now found at /usr/bin/outguess): nokey "extraction" from
  image04 (45,864 B) and image07 (8,869 B) PROVEN FALSE POSITIVE — outputs
  are ~8.0-entropy noise, wrong keys change the output length, and a fresh
  synthetic PIL JPEG "extracts" 37 KB too. No outguess payload anywhere.
  (`/usr/local/bin/jsteg` is a saved HTML page, i.e. broken install.)
- stegseek 0.6 + 167-word targeted list (covers, lyrics, hunt words, numbers,
  filenames, classics) on image02/06/07/12: no passphrase on any. Capacities
  remain (02: 23.6 KB, 07: 55.6 KB, 12: 9.1 KB, 06: 540 B) but no key found;
  rockyou-scale brute force not available offline.

## Review: PIC_DIGIT / NKOTB / `widow droid cop` (requested, repo-only)
- Raw path facts verified: the PICDIGITWORD digit string, its 12-cell
  adjacency chain, and the TWO/OLD/KIDS/THE/RIGHT digit paths all check out
  against the transcribed grid.
- Not endorsed as derived. Load-bearing problems:
  1. The picture alphabet gives 1-7 initials per digit; the PICDIGITWORD path
     shape alone can produce 230,496 strings. ~12 candidate theme strings were
     tested against ~0.15% per-string controls, so the family-wise chance is
     ~1.8%, not 0.15%. Multiple comparisons were not accounted for.
  2. Labels were uncertain in-repo at the time (image02's Kendrick second
  face was unknowable to AI; image04 carried a Wiz-vs-Wayne dispute, since
  resolved visually in Wiz Khalifa's favor: dreadlocks, backwards cap,
  face/hand ink, nose ring). Either flip would have collapsed the
  alphabet and every downstream word.
  3. The stencil invokes "unnumbered hidden pictures" and an "image11" that
     does not exist in inventory; positions 08-10 spell TWO only via flexible
     multi-initial choices, then get declared "missing files".
  4. Uniqueness carries no weight per my background test above (len-3/5 unique
     rates ~48%/57%): unique THE, RIGHT, TWO, OLD, KIDS is chance-level.
  5. The chain needs a band recognition (NKOTB), a synonym jump
     (THINGY=STUFF), and Nth-word layers whose rules (one-word labels keep
     their initial) are stipulated, not derived. The author admits COP is not
     formally unique (COB/BOD/DOC/COD/GOD/DOG/ODD exist).
## Addendum 4: Bananagrams theory (dead, all three readings)
Idea: title-links-banana-video -> Bananagrams (interlocking word-grid game),
"banana grid, but with numbers". Checked against the real rules/distribution
(wiki: 144 tiles, J/K/Q/X/Z x2 ... E x18).
1. Tile-set reading: Bananagrams distribution via T9 =
   {2:19, 3:27, 4:19, 5:9, 6:22, 7:20, 8:18, 9:10}. Grid =
   {2:2, 3:5, 4:5, 5:7, 6:6, 7:2, 8:4, 9:5} (+six 1s). Nowhere close
   (5: 7 vs ~2.6 expected; 7: 2 vs ~5.8; 2: 2 vs ~5.5), with or without
   counting 1s as wildcards. The grid is NOT a Bananagrams tile set. DEAD.
2. Interlock reading (every row/col run a T9 word): already proven UNSAT in
   repo (crossword-block CSP, minlen 2 and 3, all block digits). DEAD.
3. Win-shout reading ("Bananas!"): BANANAS needs three T9-2 cells; the grid
   has two ((1,5),(2,0)). Unformable in any reading, and one word anyway. DEAD.
The banana video stays a joke placeholder.

## Addendum 5: musician-letters (dead, both versions)
Idea: the hidden musicians' letters must connect to the solve.
1. Initials-as-T9-paths (pre-registered, 8 orders: outer zip-order first/last
   names MDWROD/MDKPOR, nested byte-order DMS/MMW, all-nine, nested/outside
   song initials PPI/LHPG): ZERO adjacent paths for every one. The musicians
   do not sign the grid.
2. Initials-as-anagrams: partial common words exist (word/worm/dorm;
   pork/drop/prom; words/sword/worms) but none consumes any set cleanly, and
   no principle picks the set, the order, or the split. Textbook sharpshooter.
Covers stand as theme/instructions only (phone keypad + look-inside-files);
no tested connection yields answer words.

## Addendum 6: off-grid surfaces closed by operator (2026-09-04)
Operator read all three live: Q&A full text, Level-6/Level-7 page JSONs, TOOL
page content. Verdict: nothing burger on all three — no hint text beyond the
known Level-0 snippet, no calibratable convention, TOOL effectively empty.
Every known surface is now exhausted: grid, images, forensics, page, video,
TOOL, QA, L6/L7, retro (joke). Residuals only: steghide passphrases on
image02/06/07/12, missing slots 03/05/08/09/10, TEST/twilio/winner stubs.

## Addendum 7: complete StegSeek seed scan finds image07 payload
A preregistered full 2^32 seed-mode test, with known-positive image04 and a
fresh negative JPEG, closed the interrupted earlier seed scans. Controls passed.
image02/image06/image12 completed with no seed. **image07 reproducibly reports
seed `0f58d719`, 19.3 KB compressed plaintext, rijndael-128/CBC.** This is new
hard evidence of another encrypted steghide payload; it is not an outguess
false positive. Seed mode cannot extract encrypted bytes without the password.
The repo-corpus 1,758,842-password sweep also missed, so cracking image07 is now
the sole high-value forensic lead.

## Addendum 8: image07 finite short-key families dead
Preregistered controls and full scans passed. Seed-derived forms (594), every
lowercase a-z string of length 1–6 (321,272,406), and every decimal string of
length 1–8 including leading zeroes (111,111,110) all failed on image07. The
controls independently recovered `planet` and `8675309` byte-perfectly. Thus
the confirmed payload remains encrypted; its key is longer, mixed-character,
or otherwise outside every mechanically justified key family tested so far.

## Addendum 9: generic image07 passwords and common pairs dead
Two more preregistered families completed with byte-perfect controls. A
7,140,015-entry union of local generic passwords/dictionary/word-frequency
forms missed. So did all 100,000,000 ordered pairs of the top 5,000 lowercase
English words with empty/space/hyphen/underscore separators. This does not
weaken the seed-mode carrier detection; it narrows the unresolved password.

## Addendum 10: image07 seed becomes a password oracle
Synthetic tracing and seven independent StegSeek controls establish the exact
selector mapping: bytewise XOR the four 4-byte quarters of `MD5(passphrase)`
and read the result little-endian. All seven passwords match, and `planet`
matches across two covers. Target seed `0f58d719` can now reject passwords with
one MD5 plus a 32-bit comparison; only fold collisions need full extraction.

## Addendum 11: common three-word image07 passwords dead
The validated MD5-fold oracle scanned all four billion ordered triples from the
top 1,000 lowercase English words under empty/space/hyphen/underscore joining.
The control recovered `thetimeyou`; independent C/Python fold samples matched.
The target produced zero fold collisions, so this complete family cannot hold
the image07 password.

## Addendum 12: bounded masks and best64 image07 passwords dead
Controlled MD5-fold scans completed 11,207,042,464 disjoint bounded-mask keys
and 162,505,112 generic best64 mutations. Three mask fold collisions
(`ketoxe`, `smzqagh`, `ovxqfiu`) all failed extraction twice; best64 had no
collision. The confirmed image07 payload remains encrypted.

## Addendum 13: vectorized image07 masks dead
The preregistered copied-kernel control passed: scalar and vectorized complete
lowercase-length-4 collision sets were both exactly `{test}`. Four target masks
then completed all 351,729,273,631 candidates and emitted 88 random 32-bit fold
collisions (null expectation 81.893). Every collision independently matched
seed `0f58d719`; every one failed normal steghide extraction twice. Complete
bytes and outcomes are in `image07_fast_fold_matches.tsv`. No candidate or
answer was recovered. The image07 carrier remains real, but its password is
outside every finite family tested; without a new clue, extending brute force
would violate the preregistered stopping rule.

## Addendum 14: image07 payload independently verified (2026-09-05)
- `stegseek --seed` on image04 (positive control) reports seed `3b75655e`
  = the MD5-XOR-fold of the blank passphrase, 47.7 KB / rijndael-128 / CBC:
  method validated end to end.
- Same command on image07 reports seed `0f58d719`, 19.3 KB compressed /
  rijndael-128 / CBC. The encrypted payload is REAL (not an outguess-class
  artifact). Fold formula re-derived independently: 7/7 doc samples plus all
  88 TSV collisions match (an initial "mismatch" was my own endianness bug,
  corrected to little-endian).
- Local dictionary fold-filter (~105k words from top-1m/NCSC/common, x4 case
  variants): zero hits. The 88 known collisions all fail extraction, so the
  true passphrase is still unknown. Per the stopping rule, no further brute
force without a new clue; the last unopened live surface remains the
Twilio member bodies.

## Addendum 15: two password families miss image07 (2026-09-05)
Agent-supplied lists never arrived, so both families were regenerated here
and committed (`fam_boggle_unique5_mine.txt`: 426 unique-path len-5 words
from american-english; `fam_madworld_mine.txt`: 91 cover/feud words).
Fold oracle: zero hits. `stegseek --crack` on image07 with both: no
passphrase. Families exhausted. NOTE: /tmp was wiped mid-hunt (g10k,
popular, enable1 gone); future runs must use /usr/share/dict or repo-pinned
lists. The kinky/plate/shied and smelt/fishy/ninja triples verified
structurally (unique paths, mutually disjoint) but endorsed by no puzzle
principle — not answers, not passwords.
- Dispute adjudication (2026-09-05): a counter-claim argued the seed hit is
  capacity-conflation. Decisive negatives run by me: full 2^32 `stegseek
  --seed` on image02 and on a fresh synthetic JPEG both return "Could not
  find a valid seed" (exit 1, no output). Scorecard: image04 HIT (correct
  seed+metadata), image07 HIT (seed+metadata), image02/synth MISS. The
  counter-agent's controls tested `steghide info` capacity, never seed mode
  — strawman. The 88-vs-81.893 collision count was never payload evidence
  (it was the failed crack); payload evidence is the seed+metadata, which
  clean files do not produce. Prior note: image04's payload is ALSO
  rijndael-128/CBC, so encryption-per-se is already author behavior; only a
  non-empty passphrase would be new.

## Addendum 16: known-seed raw ciphertext recovered, still opaque
A locally patched StegSeek build passed all preregistered controls: the image04
stream decoded with the blank passphrase to the exact known `image11.jpg`; a
fresh `planet` carrier decoded byte-for-byte; and a fresh clean JPEG completed
2^32 seeds with no hit or dump. Image07 then yielded a 19,760-byte stream:
16-byte IV `e5777082fda3b3ff0054e56b6ce096f1` plus 19,744 bytes of aligned
Rijndael-128/CBC ciphertext, SHA-256
`dd8bd04b408b1d64e9801f37835b16cc7af54549c9d735f26942985dd67e856d`.
Entropy is 7.991366954418 bits/byte and no field after the public 65-bit header
is readable without the passphrase. This validates exact byte recovery but
provides no cryptographic shortcut; password recovery remains the blocker.

## Addendum 17: Orianthi title-capitalization family dead
The established Orianthi identification motivated one narrow omission from the
old lowercase searches: 13 conventional case/joiner forms of *According to
You*. This family was preregistered before hashing. The `planet` fold and exact
synthetic decode controls passed; all 13 target folds missed `0f58d719`.
No extraction was attempted and no candidate survives.

## Addendum 18: phrase-shaped passwords exhausted (2026-09-05)
Steelmanning the combinator suggestion into its complete form: all ordered
pairs and triples of the 426 unique-5 grid words (77.3M triples) and the 91
madworld words, under empty/space/hyphen/underscore joining — full space,
not a head-truncated sample — fold-scanned against `0f58d719`: zero
collisions. (The proposed hashcat one-liner as written mangles single words
only and cannot emit triples; this run is the correct implementation of its
intent.) Phrase-shaped passwords from grid/cover vocabulary are closed. The
image07 password is outside every tested family; parked per stopping rule
pending a new clue (Twilio member bodies remain the last unopened surface).

## Addendum 19: independent 3.4M-fold sweep blank (2026-09-05)
Second agent, fold oracle only (no binaries in its env): ~700 themed
passphrases, 370k singletons x3 cases (~1.11M), core+year/suffix forms
(~50k), ~7k themed pairs, 1,500x1,500 sampled pairs (2.25M), 27-themed
triples (19,683). Arithmetic checks (~3.44M total), zero collisions.
Converges with all prior misses. Park stands.

## Addendum 20: from-scratch re-verification (2026-09-05)
Hashes of all four carriers match originals (no tampering). Fresh full-2^32
`stegseek --seed` scans from this box: image02 miss, image06 miss (first
independent check), image07 HIT `0f58d719` + 19.3 KB / rijndael-128 / CBC,
image12 miss (first independent check). Combined with prior image04 HIT and
fresh-JPEG miss, the map is confirmed without trusting any log. (The 19.3 KB
figure comes from seed-mode metadata output, never from `steghide info` —
no other source was ever claimed.)

## Addendum 21: fresh password batch blank (2026-09-05)
268 previously untested candidates via fold oracle, zero hits: full grid
digit strings (rows/cols/flat/forwards/reversed), full dates (1987-02-25,
2016-12-19, 2018-07-28, 2018-08-19, 2026-09-03, times), site-operation words
(dve99, c217b5, 0d5510, q10kp, rfoq0, jyh0e, gpf1n, uxf2s, kraken spelling,
level9, gulag, tetris, Cor), Discord/Twilio names, Orianthi deep cuts
(believe, heaveninthishell, michaeljackson, alicecooper, sambora, bonjovi),
feud deep cuts (pulitzer, euphoria, meetthegrahams, notlikeus, garyjules,
donniedarko). Nothing left in this vein.

## Addendum 22: image-depth password sweep blank (2026-09-05)
687 fresh candidates via fold oracle, zero hits, across previously untested
image-derived classes: artists' real names (ciccone, aubrey, duckworth,
thomaz, stevland, gahan, panagaris), lyric singles (flesh, celebrate,
upset, stupid, familiar, cellphone, bustin, demons), B-sides (dangerous),
Spanish lyrics (sanpedro), track lengths (347, 427, 412, 405, 401),
phone numbers (5552368 Ghostbusters, 8675309 Jenny), area codes (416, 310,
412, 313), word-form years, feud specifics (aminor, certified, pulitzer,
overseer), meta-tool words (rijndael, steghide, seed, payload), seed/IV
strings, Twilio/Discord names. Images mined dry at password depth.

## Addendum 23: scattershot password batch blank (2026-09-05)
2,908 fresh candidates via fold oracle, zero hits: page IDs, Velo strings,
Utah/sea/mythology vocab, file sizes, missing-slot numbers, prior answers
concatenated, common wordlists, keyboard walks, classics. Well dry.

## Addendum 24: composite image strings blank (2026-09-05)
197 full titles, lyric lines, initial-chains (mdwrod/mdkpor/dms/mmw),
image filenames with extensions, games/movies (tetris/boggle/bananagrams),
call phrases — zero fold hits. Passphrase-from-images now fails at singles,
pairs, triples, full titles, lyric lines, and composites.

## Addendum 25: full rockyou exhausted (2026-09-05)
Downloaded SecLists rockyou (14,344,391 passwords) and MD5-fold-filtered all
of them against `0f58d719` (12-core pool): zero hits. Largest single
untested family is now closed. Password space status: every motivated
family exhausted; only unmotivated brute force (random masks beyond tested
bounds) remains, parked per stopping rule.

## Addendum 26: post-easifier leftovers dead (2026-09-05)
Sudoku-shape readings die on dimensions (6x7 with repeats, not 9x9).
A1Z26 straight lines rerun on the REDUCED grid: zero words len>=5.
Digit-order strings (rows/cols/boustrophedons/spiral/diagonals + reverses,
22 candidates) as image07 passwords: zero fold hits. Cipher key-squares
(Playfair/Polybius/tap need 5x5; no ciphertext exists anywhere): no fit.

## Addendum 27: easier-grid surfaces closed (2026-09-05, goal work)
- `grid3_easier.webp` forensics: single VP8L chunk, zero trailing bytes, no
  EXIF/XMP/ICCP. Clean (Discord re-encodes uploads anyway). No hidden layer.
- 289 easifier-derived passwords via fold oracle (easier/grid3/removed,
  removed-cell digits, kept stub, clue words, all six K-order concatenations,
  discord IDs, webp): zero hits.

## Addendum 28: broad vocabulary sweep blank (2026-09-05)
7,590 additional candidates via fold oracle (games, anime/VN titles,
wrestling/magic-adjacent vocab, extended music terms, keyboard walks,
classic passwords with mutations, months/days/colors): zero hits.

## Addendum 29: visual check of remaining carriers (2026-09-05)
Viewed image06 (Ghostbusters single cover: "Ray Parker Jr. GHOSTBUSTERS
From the Soundtrack LP" + "Original No. 1 Hit in USA" badge) and image07
(Orianthi visual-confirmed: white PRS with swirl decal, hat, no text).
55 password candidates from the new cover text (numberone, soundtrack,
rayparkerjr, hat, purple…): zero fold hits. Submit-order audit: all 18
principled straight-line orders confirmed burned; only unprincipled
remnants (HKT/HKST/mixed-family) never fired — left unfired deliberately.

## Addendum 30: carrier visuals closed + top-2000 triples launched (2026-09-05)
All carriers now eyeballed: image12 = Reynolds/LOVELOUD stage (no text
beyond shirt), steg04 and artist_hidden = standard single covers, no
hidden text. 113-fold micro-batch (first-letters, solver names, weekdays):
zero hits. Top-2000-English triples scan (8B x empty/space joinings, closes
the necklace/popcorn-depth gap) launched in background; hyphen/underscore
remainder deferred. Result pending — see cache scan2000.done.

## Addendum 31: first triples collision fails auth (2026-09-05)
Scan emitted `hits answers might` (fold match, as expected ~4 random
collisions over 16B candidates). `steghide extract` with it failed
("invalid length", no output): random collision, not the password. Scan
still running; further random collisions expected and meaningless without
extraction.
