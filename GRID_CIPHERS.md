# dcode Grid Cipher sweep (2026-09-05, goal work)

dcode "Grid Cipher" family enumerated from tools-list: ADFGX, Bazeries,
Bifid, Collon, Delastelle Trifid, Grandpre, Nihilist, PlayFair, Polybius,
Swagman, Tap Code, Three Squares, Turning Grille, Two-square, VIC.
Adjacent: Route/Path, Spiral, Caesar Box, Columnar, Cardan Grille,
Monome-Dinome, T9/Phone/Multi-tap/A1Z26, DTMF, Dice, Grid Coordinates.

## Executed: straddling checkerboard (Monome-Dinome)
Only family with all inputs available (digit stream + image-word keys).
Sweep: 46 keys x 72 marker pairs = 3,240 combos (I/J merged, 7+10+8 layout).
1,080 decodable; top score 8 substring hits, best words `brawn/sears/meals`
scattered across keys/markers with junk outputs — chance-level noise, no
convergence, no coherent text. DEAD.

## Killed on missing inputs (definitional, not hand-wave)
- Pigpen/Tic-Tac-Toe, Tap Code, DTMF, Dice, semaphore shapes: need symbols,
  taps, audio, or faces. None exist anywhere on the level.
- PlayFair/Two-square/Three-Squares/Polybius/Bifid/Trifid/ADFGX/Collon/
  Grandpre/Swagman: need 5x5+ key squares and/or alpha text. We have 6x7
  digits and zero text.
- Nihilist/VIC/Bazeries: need numeric/key inputs that were never given.
- Route/Spiral/Caesar Box/Columnar: need ciphertext text. None exists.
- Cardan/Turning grille: already tested dead in repo.
- T9/Phone/Multi-tap/A1Z26/Grid-coordinates-as-pairs: done to exhaustion
  in repo (straight lines, Boggle, pairs-mod-26 all dead).

## Images-as-keys
Tested inside the sweep (46 image-derived keys: artists, titles, surnames,
lyric hooks, hunt words). Dead with it. No image functions as a cipher key
under any grid-cipher family with available inputs.
