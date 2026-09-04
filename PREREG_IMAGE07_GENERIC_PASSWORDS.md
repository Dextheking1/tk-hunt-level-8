# Preregistration: image07 generic local-password families

Date: 2026-09-04. Committed before either frozen wordlist is generated or tried.
This is password recovery for a cryptographically detected payload, not a
wordlist-based answer theory.

## Stage D — generic local single strings

Union these three already-installed, non-puzzle-specific sources:

1. `/snap/john-the-ripper/current/bin/password.lst`, excluding lines beginning
   `#!comment:`;
2. `/usr/share/dict/words`;
3. every item returned by `wordfreq.top_n_list('en', 500000)` (the installed
   model currently returns 319,938 items).

Keep only printable ASCII candidates of length 1–80 after stripping line ends.
For every source candidate emit exactly: verbatim, lowercase, uppercase,
Python `capitalize()`, Python `title()`, and full character reversal. Deduplicate
and byte-sort. No puzzle terms or post-result additions.

Positive control: a deterministic local steghide JPEG with passphrase
`correcthorsebatterystaple`, added verbatim to a separate copy of the frozen
wordlist solely for the control. The target receives the unaugmented list.

## Stage E — common ordered two-word strings

Take the first 5,000 distinct ASCII-alphabetic lowercase items, in rank order,
from `wordfreq.top_n_list('en', 500000)`. Emit every ordered pair `(a,b)` once
for each separator in this exact order: empty, one space, hyphen, underscore.
This creates exactly `5000 × 5000 × 4 = 100,000,000` lines before any accidental
identical-line deduplication; no case changes, digits, or other mutations.
Generation order is `a`, then `b`, then separator order above.

Positive control: deterministic local steghide JPEG with password
`yellowplanet`, after asserting both component words occur in the frozen 5,000.

## Decision rule

Controls must recover the exact registered passwords and byte-identical payload.
A target hit must be reproduced twice with ordinary `steghide extract`. If both
stages miss, only these generic one- and two-string families are closed; no
semantic title or artist candidates are added after the fact. Cryptographic
extraction is the hit validator, so random-grid rates are inapplicable.

No live-site request or submission is involved.
