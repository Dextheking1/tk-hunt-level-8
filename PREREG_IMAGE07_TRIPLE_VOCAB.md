# Preregistration: image07 puzzle-vocabulary triple-key family

Date: 2026-09-05. Committed BEFORE any candidate of this family is checked.
Target: `image07.jpg` seed `0f58d719`, checked with the swarm-validated MD5
XOR-fold oracle (7/7 fixed samples matched; `PREREG_STEGHIDE_SEED_MAPPING.md`).
Every fold collision still requires two successful ordinary steghide
extractions before it counts.

## Why this family is new ground

- Stage A–E + corpus + semantic (~145M): single words, seed literals, short
  lowercase, decimals, top-5000 two-word pairs.
- Swarm 4B kill: **all ordered triples from the wordfreq top-1,000 English
  words** under empty/space/hyphen/underscore joining (MY_SOLVE_PASS addendum
  11) — zero fold collisions.
- Stages F/G (preregistered `PREREG_IMAGE07_MASKS_AND_RULES.md`): short
  bounded masks and best64 single-word mutations — neither generates
  three-word joined strings of length 8–15.
- The residual class is therefore: three-word joined strings containing at
  least one word OUTSIDE the wordfreq top 1,000, drawn from the puzzle's own
  vocabulary (the board's words, the cover titles, the artist names).

## Frozen rule

V1: the 300 most frequent words on the board — Boggle 8-direction king-move
paths (len ≥ 3) over the verified 7×6 grid (digit 1 = no letter), dictionary
`forensics/words.txt` (73,062 entries), ranked by `wordfreq.word_frequency(w,
'en')` descending, ties alphabetical. (Census reproduced exactly: 1,650
board words, matching the swarm's `rule_hunter.py` count.)

V2: all cover-title words (lowercase, apostrophes removed): personal jesus
la isla bonita papa dont preach hotline bling payphone who you gonna call
ring my bell i just called to say love ghostbusters ghost busters.

V3: all artist-name words (lowercase): depeche mode madonna drake wiz khalifa
ray parker jr orianthi dan reynolds stevie wonder.

V = V1 ∪ V2 ∪ V3, deduplicated, sorted: **335 words**, SHA-256
`492af997a173d00f03b5a9aba6cb2e8e6f93c6de6ef2b3423c26a2837842197f`
(`V_words.txt` committed alongside). 160 of the 335 are outside the wordfreq
top 1,000 (includes all 27 cover/artist-specific words), so the family
covers every triple of the puzzle's own vocabulary, including pure-cover
triples.

Candidates: all ordered triples (a, b, c) from V, repetition allowed, under
joining {empty, space, hyphen, underscore} = 4 × 335³ = **150,381,500**
strings, each MD5-folded and compared to `0f58d719`.

## Canary (pipeline integrity)

`H("the for you") = 87503672` (independent precomputation). The execution
loop must first be run with target `87503672` and report exactly that
collision; a canary failure invalidates the run.

## Decision rule

- Canary passes + zero collisions vs `0f58d719`: the puzzle-vocabulary
  triple family is KILLED. Combined with the 4B top-1000 triple kill, every
  three-word password built from words the puzzle itself surfaces (top-1000
  or exotic) is closed. Remaining image07 key space: words from the unknown
  10th image's content, author-personal strings, or non-vocabulary long
  strings (outside finite sweep scope, subject to Stage F/G completion).
- Any collision: hand to the swarm for dual steghide extraction.

No live-site request or submission is involved.

## Results (2026-09-05, executed after commit d5dc7c7)

- Canary: target `87503672` run returned exactly `["the for you"]` (142.6 s
  over all four joinings) — pipeline valid.
- Target: all **150,381,500** candidates (335³ × 4 joinings) checked in 152.2 s
  with the same loop; **zero fold collisions** vs `0f58d719`.

## Decision: KILLED

The puzzle-vocabulary triple family is dead. Combined with the swarm's 4B
top-1,000-word triple kill, every three-word password whose words are drawn
from the wordfreq top 1,000 **or** the puzzle's own vocabulary (board words,
cover titles, artist names — including all 27 exotic cover/artist words) is
closed under all four joinings. Residual three-word key space: words the
puzzle never surfaces (unknown 10th image content, author-personal). This run
also cross-validates the swarm's 4B null with an independent loop and
vocabulary construction.
