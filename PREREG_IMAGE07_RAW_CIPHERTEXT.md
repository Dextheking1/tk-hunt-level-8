# Preregistration: known-seed raw ciphertext recovery

Date: 2026-09-05

## Question

Can the independently validated image07 selector seed `0f58d719` recover the
exact encrypted steghide bitstream without the passphrase, and does that
bitstream expose any clue or permit any passphrase-independent attack?

This is a format-analysis experiment, not a new password brute force. It will
not touch the live hunt site.

## Frozen method

Use StegSeek source revision `ff677b9` only as a local decoder implementation.
Add a diagnostic seed-mode path that, after a seed passes the ordinary header
checks, follows that exact `Selector` stream, extracts the full declared
embedding, removes the 65-bit public steghide header (24-bit magic, one version
terminator bit, five algorithm bits, three mode bits, and 32 plain-size bits),
and writes the remaining encrypted bits byte-for-byte.

For rijndael-128/CBC, the raw result should consist of a 16-byte IV followed by
whole 16-byte ciphertext blocks. No interpretation will be made from random
ciphertext strings.

## Controls

1. **Known positive:** `image04.jpg`, detected seed `3b75655e`, blank
   passphrase. The direct-seed dump must have a valid 16-byte IV plus block-
   aligned ciphertext. Decrypting/parsing it with the known blank passphrase
   must reproduce `hidden/steg04.jpg` exactly (expected SHA-256
   `7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0`).
2. **Synthetic encrypted positive:** embed a fixed local text file in a fresh
   JPEG using passphrase `planet`. Its detected seed must be `2c52fe1c`; the
   direct-seed dump, when decrypted with `planet`, must reproduce the fixed
   input exactly.
3. **Negative:** a fresh never-embedded JPEG must produce no valid seed and no
   raw dump.

A target dump is accepted only if all three controls behave as specified.

## Target checks

For `image07.jpg`, record the exact public header fields, encrypted-byte count,
IV, SHA-256, entropy, and ordinary `file`, `strings`, and `binwalk` results.
Then inspect whether any filename, magic, compression header, checksum, or
other bytes lie outside encryption.

## Decision rule

- If the control-valid dump contains only IV plus semantically opaque CBC
  ciphertext, log that the selector seed does not recover the filename or
  plaintext and that key recovery still requires the exact passphrase.
- If a deterministic unencrypted field exists, use only the field explicitly
  established by the format/control; do not infer clues from chance strings.
- Do not extend generic password masks as a consequence of this experiment.
