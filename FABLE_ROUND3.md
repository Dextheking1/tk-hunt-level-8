# Fable round 3 (2026-09-04) -- grid-only, all DEAD (verified by code)

Operator ruling: Level 8 is standalone. No cross-level calibration. Dropped.

Tests run this round (nltk words, 234k):
1. 1-as-separator T9 on row/col/boustrophedon/reversed streams (7 segments
   each): only noise (gonid, dol, thy, hub, wit, bug...). Duplicate of
   earlier '1=space segmentation' entry -- confirmed dead, do not redo.
2. Old-SMS multi-tap (run-length = letter index, 1 = space): gibberish in
   all 6 orders (e.g. 'gngd mtjw pajadwmjwt ...').
3. Hitori: strict = 0 solutions. Drop-adjacency = 0 (row3 '5 3 9 5 1 3'
   forces adjacent shading). Drop-connectivity = 200+ non-unique. DEAD in
   every variant (matches earlier UNSAT).
4. Whole-line T9 with 1 = wildcard / 1 = deleted, fwd+rev, all 13 lines:
   hits IMOGEN (row1, 1 dropped), TIMOTHY (row6, 1=O), MEZZO (col3 rev),
   GLOWER/GROWER (col4, 1 wild), GROWAN (col6 rev). Names/at-chance for
   6-7 letter T9 strings (~15% per line). Not a mechanism.
5. Digit pairs as (key, press-count) SMS encoding: 16 variants (row/col,
   offset, swap, 0/1-based) -> all gibberish.
6. Digits as numpad direction pointers (8up 2dn 4lt 6rt diag 7/9/1/3,
   5 = stop) tracing paths from every start cell: longest path 5 cells.
   No structure. DEAD.

Still-open (none evidenced): the SELECTION rule for keypad->3 words.
Everything grid-internal tested to date is at chance level.
