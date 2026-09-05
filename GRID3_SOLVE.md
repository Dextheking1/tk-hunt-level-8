# EASIER grid solve (official clue 2026-09-05)

Official: "Level #8 — We removed some of the numbers you don't need."
`grid3_easier.png` (banked) vs original: rows 0-4 IDENTICAL, row 5 truncated
to `8 4`. Removed cells: (5,2)=6, (5,3)=1, (5,4)=8, (5,5)=4, (5,6)=9.

## What the removal does
- KILLS `TILLS` (needed (5,4)). All other old straight-line words survive:
  HOMIE (row 0), KELLI (col 1), SMELT (diag), IDIOM/TAINT/SHEIK (1=I).
- Full subsegment enumeration (every straight run, every len>=5 window,
  dict-matched): the ONLY pure-T9 English words left are
  **HOMIE, KELLI, SMELT**. Exactly three. No dict artifact (all decodings
  enumerated; TILLS is structurally gone).
- Boggle tiers UNCHANGED (violation/injection/election/MAD/SAY/LOVE/YOU paths
  avoid removed cells) — but straight-line exactly-3 now dominates by
  authorial intent: the easifier deleted precisely the 4th word.
- Retroactive verdict: pure-T9 was the intended mechanism all along. The 1=I
  "twist" (TAINT/SHEIK accident math) was our apophenia — under it the grid
  holds 8 words and the author's deletion makes no sense.

## Answer: an ordering of HOMIE / KELLI / SMELT
Six orders, NONE ever tried (every old submit used T, never K):
1. `homie kelli smelt`
2. `homie smelt kelli`
3. `kelli homie smelt`
4. `kelli smelt homie`
5. `smelt homie kelli`
6. `smelt kelli homie`
Fire all six at 1/min. KELLI-as-name objection noted and overruled by
exactly-3 structure. No principled order — alphabetical first is as good
as anything.
