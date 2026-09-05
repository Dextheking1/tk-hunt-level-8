# ADJUDICATION: swarm GRID3_SOLVE.md "fire all six homie/kelli/smelt" plan

Date: 2026-09-05. After union-merging swarm master 97a61fb. Adjudicated
against the frozen hunt standards before any action; NO submission made.

## The swarm claim (GRID3_SOLVE.md, their master)

- grid3_easier.png vs original: rows 0-4 identical, row 5 truncated to
  `8 4`; removed (5,2)=6 (5,3)=1 (5,4)=8 (5,5)=4 (5,6)=9. (Matches my
  verified reading exactly.)
- "Full subsegment enumeration (every straight run, every len>=5 window,
  dict-matched): the ONLY pure-T9 English words left are HOMIE, KELLI,
  SMELT. Exactly three."
- "The easifier deleted precisely the 4th word (TILLS, needed (5,4))."
- "Straight-line exactly-3 now dominates by authorial intent" → answer =
  an ordering of HOMIE/KELLI/SMELT → **"Fire all six at 1/min."**

## My verification (frozen dict = steghide_dictionary.txt ∪
forensics/words.txt = 72,870 words; T9 first-letter/full-key mapping;
straight runs, 8 dirs, digit-1 cells letter-incapable)

- KELLI verified: col 1 vertical (1,1)→(5,1) = 5 3 5 5 4.
- SMELT verified: anti-diagonal (1,4)→(5,0) = 7 6 3 5 8.
- TILLS verified on the 42-board: col 4 vertical (5,4)→(1,4) =
  8 4 5 5 7 — the T sits on (5,4), a REMOVED cell. The deletion does
  structurally kill TILLS. (Their structural claim is correct.)
- HOMIE: a valid T9 reading of row 0 prefix 4 6 6 4 3 — **but HOMIE is
  NOT in the frozen 72,870-word dictionary** (absent from both
  steghide_dictionary.txt and forensics/words.txt). It is an artifact of
  the swarm's larger wordlist.
- Consequence under the frozen dictionary:
  - 42-board len-5 straight T9 words = {KELLI, SMELT, TILLS} — **3, not 4**.
  - Canonical 37-board len-5 words = {KELLI, SMELT} — **2, not 3**.
  - "Exactly three remain" does not exist on the frozen dict. Creating it
    requires adding HOMIE post hoc = forbidden dictionary expansion
    (operator standard: "dictionary = common words; curated wordlists
    out"; no post-hoc label choices).
- Noise census (record only): 4-letter = 26 words (DEFT DINO … MELT
  PLOW …); 3-letter = 85 (HUB IVA …). Chance-level, no structure.

## Background control (1,000 random boards, same 42-digit multiset,
seeds 42/7)

- 42-board len-5 count: mean 4.70, P(>=4) = 0.626, max 18.
  (Observed 3 on the frozen dict = unremarkable.)
- 37-board (same 5 cells removed) len-5 count: mean 3.40, P(>=3) = 0.583.
- P(before==4 AND after==3 on random boards, same 5 cells) = 0.055 —
  and the observed pair is (3, 2), not (4, 3).
- No statistical signal in the "deleted the 4th word" structure under
  the frozen dictionary.

## RULING

1. **Evidence standard — KILLED.** The "exactly 3 remaining" authorial
   structure is a dictionary artifact (HOMIE). On the frozen common
   dictionary the canonical board holds exactly 2 len-5 straight T9
   words, and random-board controls put the observed counts at chance.
   No derivation is endorsed.
2. **Class standard — DEAD regardless.** Even if the structure were
   real, HOMIE/KELLI/SMELT orderings are grid-word orderings. Standing
   rulings (2026-09-05): operator T7 "word-search/grid-word class DEAD";
   user cumulative rejects "ALL grid-word orders" (prior submissions
   used TILLS-based orders and were rejected). The swarm's "fire all six
   at 1/min" instruction conflicts with those rulings.
3. **Action taken: none.** No live request, no submission. The swarm's
   submit-order audit (MY_SOLVE_PASS.md Add.29: "all 18 principled
   straight-line orders confirmed burned; only unprincipled remnants
   (HKT/HKST/mixed-family) never fired — left unfired deliberately")
   confirms the six homie/kelli/smelt orders were never submitted — the
   class is closed by ruling, not by exhaustion of submissions.
4. **Reopening:** only the user/operator may lift the grid-word class
   ruling. If they do, the six orders are the unfired set (KELLI, SMELT,
   and HOMIE — noting HOMIE's dictionary status is contested under the
   frozen standard). Until then this family stays unfired.
