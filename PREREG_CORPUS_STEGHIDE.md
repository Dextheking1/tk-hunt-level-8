# Preregistration: repository-corpus steghide key sweep

Date: 2026-09-04. This file is committed **before** generating the wordlist or
running any residual carrier. It is a finite residual test, not a new reading
of the digit grid.

## Question

Do any of the still-open JPEG carriers (`image02.jpg`, `image06.jpg`,
`image07.jpg`, `image12.jpg`) contain a steghide payload whose passphrase is
present mechanically in the repository rather than guessed semantically?

## Frozen candidate-generation rule

Source corpus: bytes of every Git-tracked file at this commit. Do not add web
material, inferred musician labels, synonyms, or words after seeing results.
Generate and deduplicate these UTF-8 passphrase candidates:

1. Every printable `strings -n 4` line, stripped, length 4–80.
2. Every whitespace-delimited token of length 1–64 from printable repository
   text, plus every contiguous 2-, 3-, and 4-token sequence that stays within
   one source line and is at most 80 characters.
3. For every candidate from 1–2, exactly these normalizations: verbatim;
   lowercase; uppercase; whitespace collapsed to one space; spaces changed to
   `_`; spaces changed to `-`; and ASCII alphanumeric-only.
4. Every tracked basename and relative path, with and without its final
   extension, under the same normalizations.
5. For every tracked regular file: decimal byte size, lowercase hexadecimal
   byte size with and without `0x`, CRC32 (8 hex digits), MD5, SHA-1, and
   SHA-256; for each digest include lowercase, uppercase, first 8, last 8,
   first 16, and last 16 characters.
6. For every ZIP entry: exact entry name, basename, stem, CRC32, compressed
   size, uncompressed size, and timestamp rendered as `YYYYMMDDHHMMSS` and
   `YYYY-MM-DD HH:MM:SS`.
7. Cross-file key forms are limited to `<stem><fact>`, `<fact><stem>`,
   `<stem>-<fact>`, `<fact>-<stem>`, `<stem>_<fact>`, and `<fact>_<stem>`, where
   `fact` is one of that same file's size/digest/CRC variants. No pairwise
   combinations between unrelated prose tokens are allowed.

Sort candidates bytewise before use. Empty passphrase is excluded because it
has already been tested on all four carriers.

## Execution and controls

- Use the identical frozen wordlist with `stegseek` against each of the four
  residual carriers.
- Positive control: confirm `steghide extract -p ''` still extracts the known
  `image11.jpg` payload from `image04.jpg` and hash-matches the banked copy.
- Negative control: create a fresh deterministic Pillow JPEG containing a flat
  RGB field and run the same wordlist against it.
- A hit counts only if the cracker reports a passphrase and extraction yields a
  nonempty file whose bytes are stable on a second extraction. Console noise or
  outguess-style random output does not count.

## Decision rule

- One validated hit: inspect only that extracted payload and continue the chain.
- Zero validated hits on all four, with controls behaving correctly: mark this
  corpus-key family dead. Do not expand it post hoc.

## Results

Wordlist generation obeyed the frozen rule over 53 tracked files:

- candidates: **1,758,842**
- UTF-8 wordlist size: **37,113,179 bytes**
- SHA-256: `5c78c22d962454642ca85a5d0f9b89b803a4f2f2ae8046b4c0992a425ebf9619`

Controls:

- Positive: blank-password extraction from `image04.jpg` reproduced the banked
  `image11.jpg`/Stevie payload byte-for-byte, SHA-256
  `7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0`.
- Negative: the full wordlist against a freshly generated deterministic flat
  Pillow JPEG returned `Could not find a valid passphrase` (exit 1) and wrote
  no output file.

Residual carriers, each tested against the entire identical wordlist:

| carrier | stegseek result | output |
|---|---|---|
| `image02.jpg` | no valid passphrase, exit 1 | none |
| `image06.jpg` | no valid passphrase, exit 1 | none |
| `image07.jpg` | no valid passphrase, exit 1 | none |
| `image12.jpg` | no valid passphrase, exit 1 | none |

The first shell driver reached and cleared `image02.jpg` but then stopped on a
non-POSIX `PIPESTATUS` expression. A corrected no-pipeline loop reran all four
carriers from scratch and produced the table above.

## Decision

**Killed.** None of the four residual JPEGs uses a passphrase mechanically
available through the preregistered repository-corpus, filename, ZIP-fact, or
same-file fingerprint family. Per the decision rule, this family will not be
expanded post hoc.
