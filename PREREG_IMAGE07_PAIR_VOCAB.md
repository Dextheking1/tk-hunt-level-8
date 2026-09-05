# Preregistration: image07 puzzle-vocabulary pair-key family

Date: 2026-09-05. Committed BEFORE any candidate is checked. Target:
`image07.jpg` seed `0f58d719`, validated MD5 XOR-fold oracle.

## Why new ground

The 100M two-word kill covered top-5,000 x top-5,000 (4 joinings); the corpus
kill covered within-repo sequences. The residual: two-word strings where at
least one word is a puzzle-surfaced word OUTSIDE the top 5,000 (exotic cover/
artist/board words: khalifa, orianthi, reynolds, bonita, payphone, hotline,
ghostbusters, jesus, madonna, stevie, wonder, depeche, mode, parker, reynolds,
whiskey, shuffle, florida, …). Cross-pairs like "khalifa reynolds" or
"payphone hotline" appear in neither keyspace.

## Frozen rule

Same V as the triple family (335 words, SHA-256
`492af997a173d00f03b5a9aba6cb2e8e6f93c6de6ef2b3423c26a2837842197f`,
`V_words.txt`). Candidates: all ordered pairs (a, b) from V, repetition
allowed, under {empty, space, hyphen, underscore} joining = 4 x 335² =
**448,900** strings, MD5-folded vs `0f58d719`.

## Canary

`H("love you") = c0adf94b` — the loop must find exactly that
collision first.

## Decision rule

Canary pass + zero collisions: the puzzle-vocabulary pair family is KILLED.
Together with top-5000² (swarm) and the triple kills (swarm 4B + this repo
150M), every 1-, 2-, and 3-word password composed of puzzle-surfaced words
(closed by Stage D/corpus/56-words for 1-word, this family for 2-word, the
two triple kills for 3-word) is exhausted. Only 4+ word or non-surface
passwords remain (outside finite sweep scope).

## Results (2026-09-05, executed after commit 6852abd)

- Canary: `love you` (c0adf94b) found exactly once (0.4 s).
- Target: all **448,900** candidates checked; **zero fold collisions** vs
  `0f58d719`.

## Decision: KILLED

Every two-word password built from puzzle-surfaced words is now closed (this
family ∪ top-5,000² swarm kill ∪ corpus sequences).
