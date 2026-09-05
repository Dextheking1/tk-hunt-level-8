# Preregistration: image07 Orianthi title-capitalization family

Date: 2026-09-05. This file is committed before calculating any target fold
for the candidates below.

## Motivation

Repository evidence identifies the visible guitarist in `image07.jpg` as
Orianthi from the white PRS guitar and ornate O emblem. The canonical hit title
*According to You* is a direct artist-shaped password hypothesis that earlier
one-word lists omitted. Its four all-lowercase empty/space/hyphen/underscore
forms already fall inside the completed top-1,000 common-three-word search, so
those dead forms will not be retested. This experiment tests only conventional
capitalization variants not covered by that family.

A local vision model associated the outfit with the video, but gave mutually
contradictory artist and instrument labels in other prompts. That association
is therefore motivation only, not evidence and not an answer endorsement.
No background-person, Michael Jackson, Richie Sambora, or discography grab-bag
candidate is admitted in this family.

## Frozen candidates

Apply exactly four joiners (`""`, one ASCII space, `-`, `_`) to each of these
three word-case rows, retaining byte case exactly:

1. `According`, `to`, `You`
2. `According`, `To`, `You`
3. `ACCORDING`, `TO`, `YOU`

Then add exactly one lower-camel form: `accordingToYou`.
Deduplicate while preserving this order. The family has 13 UTF-8/ASCII byte
strings. No punctuation, digits, artist prefixes, suffixes, alternate titles,
or post-result additions are allowed.

## Control and decision rule

First verify the existing fold implementation still returns `2c52fe1c` for
`planet`, and that `planet` decodes the synthetic positive byte-for-byte. Then
calculate every candidate's selector fold

`LE32(MD5[0:4] XOR MD5[4:8] XOR MD5[8:12] XOR MD5[12:16])`.

- If no fold equals `0f58d719`, kill the family without invoking extraction.
- If a fold matches, a 32-bit collision alone is not evidence: run ordinary
  Steghide extraction twice and require successful, hash-identical outputs.
- Only a valid decoded object can motivate a later answer-derivation rule.

No live-site request or submission is involved.

## Results

The `planet` fold control returned `2c52fe1c`, and the synthetic raw stream
again decoded byte-for-byte to the registered 59-byte plaintext. All 13 frozen
candidate byte strings were enumerated in the registered order. **Zero** had
selector fold `0f58d719`, so extraction was correctly skipped.

**Decision:** this exact title-capitalization family is killed. It does not
weaken the Orianthi identification, but *According to You* is not the image07
passphrase in any registered conventional case/joiner form.
