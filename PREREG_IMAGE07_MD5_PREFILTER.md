# Preregistration: image07 MD5-fold common three-word search

Date: 2026-09-05. Committed before generating the base, calculating any target
fold match, or trying any candidate password.

## Motivation

The validated steghide selector mapping makes a large mechanical search
possible without billions of JPEG extraction attempts. The puzzle's required
output is exactly three common lowercase English words, so the next finite
password family is registered as common lowercase triples rather than any
artist-, title-, or image-label-derived guesses.

## Frozen family

1. Take the first 1,000 distinct strings from
   `wordfreq.top_n_list('en', 500000)` that are ASCII alphabetic after
   lowercasing. Preserve rank order.
2. Enumerate every ordered triple `(a,b,c)`.
3. For each triple, emit exactly four password bytes in this order:
   `abc`, `a b c`, `a-b-c`, `a_b_c`.
4. This is exactly `1000^3 × 4 = 4,000,000,000` candidates. No case changes,
   plural expansion, digits, synonyms, proper-name injection, or later
   additions.
5. Calculate
   `H(p) = LE32(MD5(p)[0:4] XOR MD5(p)[4:8] XOR MD5(p)[8:12] XOR MD5(p)[12:16])`
   and retain every candidate equal to target seed `0f58d719`. Do not stop at
   the first match.

## Controls

- Run the same compiled scanner first over the first 100 base words and the
  registered password `thetimeyou`, after asserting all three component words
  are in that 100-word base. Its independently computed Python `H` must be
  returned by the scanner.
- Compare the C and Python fold values for the first, middle, and last generated
  control candidates.
- Record base-list SHA-256, exact count, throughput, and every target fold
  collision.

## Decision rule

A 32-bit collision alone is expected by chance: the target run's null
expectation is `4,000,000,000 / 2^32 = 0.9313` collisions. Therefore neither a
match nor uniqueness is answer evidence. Every fold collision must be tried
with ordinary `steghide extract` twice. Only two successful, hash-identical
extractions count as a recovered password. Otherwise the entire frozen triple
family is dead and will not be expanded post hoc.

No live-site request or submission is involved.

## Results

- Frozen 1,000-word base SHA-256:
  `46adcbb0e99aa158faeda262a909f7aa40abf865c6666bb8c54001ac6c10698f`
- The 100-word control enumerated exactly 4,000,000 candidates and returned
  the registered password `thetimeyou` at indices `(0,58,10)`, separator 0.
- C/Python sample folds matched directly:
  - first `thethethe`: `7a6026fb`
  - middle `nothethe`: `3b0fa0b5`
  - last `much_much_much`: `4422e416`
- A later regex-only assertion in the shell wrapper malformed its capture and
  printed a Python traceback. This did not alter the scanner or target run;
  the values above are present identically in the independent Python and C
  output, and the exact registered control match was recovered.
- Target enumeration completed all **4,000,000,000** candidates in 89.023 s
  at 44.932 million MD5 folds/s on 12 threads.
- Target fold collisions: **0**. Therefore there were no passwords to send to
  steghide extraction.

## Decision

The entire preregistered top-1,000 common three-word family under empty, space,
hyphen, and underscore joining is **killed**. Zero collisions is compatible
with the predeclared null expectation (Poisson mean 0.9313); it is not itself a
rare clue. No base expansion or semantic term was added.
