# Preregistration: image07 finite seed forms and short-key brute force

Date: 2026-09-04. Committed before any password in these families is tried.
Target is only the newly validated encrypted steghide carrier `image07.jpg`
(seed `0f58d719`, reported plaintext 19.3 KB compressed).

## Stage A — seed-derived literal family

Generate from the 32-bit seed, without adding semantic words:

1. Big-endian hex, uppercase/lowercase, with and without leading zero and `0x`.
2. Byte-reversed hex under the same forms.
3. Unsigned decimal and signed 32-bit decimal of both endian readings.
4. Binary and base-36 representations, uppercase/lowercase where applicable.
5. Each representation alone and concatenated before/after exactly one of
   `image07`, `image07.jpg`, `07`, or `seed`, using separators empty, hyphen,
   underscore, or one space.

Deduplicate and byte-sort. Test once with StegSeek. No additions after results.

## Stage B — exhaustive lowercase short keys

Generate every string over ASCII `abcdefghijklmnopqrstuvwxyz` of lengths 1
through 6, ordered first by length and then lexicographically. There are exactly
`sum(26^1..26^6) = 321,272,406` candidates. No capitalization, digits,
mutations, or dictionary additions belong to this stage.

Positive control: make a deterministic local JPEG with a tiny steghide payload
and password `planet`, which is inside the frozen keyspace. Run the same file
and wordlist through StegSeek before the target.

## Stage C — exhaustive numeric short keys

Generate every ASCII decimal string of lengths 1 through 8, including leading
zeros, ordered first by length and then lexicographically. There are exactly
`111,111,110` candidates. No dates or preferred ranges.

Positive control: a deterministic local steghide JPEG with password `8675309`.

## Validation and stopping

A target hit counts only if normal `steghide extract` using the reported
passphrase succeeds twice and the extracted files hash-identically. Controls
must crack to their exact registered passwords. If a stage misses, mark only
that finite family dead; do not extend it post hoc. If all three miss, the open
space is longer, mixed-character, or non-mechanical passwords.

No live-site request or submission is involved.
