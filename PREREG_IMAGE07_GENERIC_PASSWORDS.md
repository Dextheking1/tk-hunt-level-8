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

## Results

### Stage D — generic local single strings

- Frozen list: **7,140,015** candidates; **62,220,747 bytes**.
- SHA-256:
  `7ad3b00f75124fe641277175f8722acbcf9b3953e5f4f0d569020abfd1fdfe45`
- Positive control recovered exact passphrase `correcthorsebatterystaple` and
  the extracted bytes matched the source payload SHA-256.
- `image07.jpg`: complete scan, no valid passphrase (exit 1).

### Stage E — common ordered two-word strings

- Frozen base: 5,000 words; `yellow` rank 2,045 and `planet` rank 2,070.
- Base-list SHA-256:
  `8e740b9c5e5c05b9cac19219e05e181cc4115c477f63bff9e26b878ed162282f`
- Generated exactly **100,000,000** pair/separator candidates;
  **1,447,080,000 bytes**.
- Pair-list SHA-256:
  `b189e0e54da48a9a58ed43e6760ce4f88922a8fbe9ed315e87d52abc89707e98`
- Positive control recovered exact passphrase `yellowplanet` and the extracted
  bytes matched the source payload SHA-256.
- `image07.jpg`: complete scan, no valid passphrase (exit 1).

## Decision

Both frozen families are **killed**. The confirmed image07 payload remains
unextracted. Its key is not any tested generic local single-string variant and
not any ordered pair among the top 5,000 lowercase English words under the four
registered separators. No semantic or artist/title candidates were added.
