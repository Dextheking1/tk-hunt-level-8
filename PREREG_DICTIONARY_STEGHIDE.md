# Preregistration: general-dictionary steghide sweep (final residual)

Date: 2026-09-04. Committed **before** running any carrier. This closes the
last untested steghide key family: single dictionary words not present
mechanically in the repository. The repository-corpus family (1,758,842
candidates) is already KILLED (PREREG_CORPUS_STEGHIDE.md); this is its final
complement, not an expansion of it.

## Why this family only

- image04.jpg payload: blank password, validated, banked (hidden/steg04.jpg).
- image02/06/07/12: zsteg/outguess/stegseek closed for non-steghide; 380
  semantic passwords + full repository-corpus wordlist found nothing.
- Remaining key space for a steghide container = single words absent from the
  repo corpus (general dictionary) or personal words (unknowable, out of scope
  for a finite sweep).

## Frozen wordlist

- Source: `forensics/words.txt` (73,062-line common/scrabble list, tracked).
- Filter: 3 <= len <= 20, ASCII alpha only -> 72,703 words.
- Normalizations (frozen): verbatim; lowercase; uppercase.
- Deduplicated, bytewise-sorted -> **145,406 entries**.
- `steghide_dictionary.txt` is the frozen artifact, SHA-256
  `bef24002824580ce209e9353...` (full hash in the committed file's first run
  log). Do not edit after the run starts.

## Execution (on a machine with steghide/stegseek)

    for c in image02.jpg image06.jpg image07.jpg image12.jpg; do
      steghide extract -sf "$c" -f /dev/null -p "" -x /dev/null 2>/dev/null  # sanity
      stegseek "$c" -w steghide_dictionary.txt -o /dev/null || true
    done

or the bundled `run_dictionary_sweep.sh`.

## Controls

- Positive: `steghide extract -p '' -sf image04.jpg` must still reproduce
  `hidden/steg04.jpg` byte-for-byte (SHA-256
  7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0).
- Negative: run the identical wordlist against a fresh deterministic flat
  Pillow JPEG; expect "Could not find a valid passphrase", no output file.

## Decision rule

- One validated hit (passphrase reported + stable nonempty extraction on a
  second run): inspect only that payload; the chain continues.
- Zero validated hits on all four with controls correct: the steghide key
  space is fully closed (corpus + dictionary). Any further steghide attempt
  requires out-of-repo semantic knowledge (author personal words) — mark the
  carrier forensics COMPLETE, not merely "no key found".
