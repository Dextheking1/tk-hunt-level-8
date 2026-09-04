# Site map + strike safety (mined offline from `level8.html`, 2026-09-04)

## Strike safety (code-proven, read the embeds before running bots)
- Wrong-password submits NEVER create strikes. The only strike sources are:
  1. assigning `window.currentLevel` / `window.userLevel` in devtools
     (setter traps, `__tkWrappedV33` block), and
  2. posting `{type:'tk-giveStrikes'}` on window (second embed, page q10kp) —
     nothing in normal play sends this; do not send it yourself.
- 3 strikes (1-hour TTL, localStorage `__tk_strikes`) -> `/gulag` redirect.
- Skip environments install nothing: in-app browsers (FB/IG/Discord/TikTok
  UA) or social referrers. Normal submit bots are gulag-safe; keep the 60s
  Velo countdown discipline (1/min) and never touch the two globals above.

## Page IDs (from `pageIdToTitle`, 48 pages)
No Level-0 page exists. Levels run 1-11, and Level-9 (`uxf2s`) already exists
as the redirect target.

| Page | ID | URI |
|---|---|---|
| Level-1 | k09pq | level-1 |
| Level-2 | ajm1g | level-2 |
| Level-3 | rodw8 | level-3 |
| Level-4 | emmbm | level-4 |
| Level-5 | hht8w | level-5 |
| Level-6 | q10kp | level-6 |
| Level-7 | rfoq0 | level-7 |
| Level-8 | dve99 | level-8 |
| Level-9 | uxf2s | level-9 |
| Level-10 | j47cf | level-10 |
| Level-11 | n235y | level-11 |
| TOOL | jyh0e | tool |
| Q&A | gpf1n | qa |
| Gulag | odibg | gulag |
| TEST | vriho | (test) |
| strike-logger | v9mz6 | strike-logger |
| twilio-page | b0tok | twilio-page |
| winner | ngfw4 | winner |
| hunt-success | m1ayi | hunt-success |
| COWLAZARS | jzuls | cowlazars |
| IG | k5les | ig |
| Leaderboard | ru248 | leaderboard |

Calibration lead is now addressable: Level-6 (`q10kp`) and Level-7 (`rfoq0`)
page JSON + Velo can be pulled from the static CDN the same way `tb8_0.json`
and `velo_dve99.js` were obtained. Compare the author's keypad/selection
convention against known `necklace popcorn love` / `ducks pump premium`.
