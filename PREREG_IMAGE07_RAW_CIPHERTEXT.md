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

## Results

The diagnostic build and every frozen control completed successfully.

1. `image04.jpg` produced seed `3b75655e`, `390393` declared plaintext bits,
   and a 48,816-byte raw stream. Its first 16 bytes are the IV; the remaining
   48,800 bytes are block-aligned ciphertext. Reconstructing and parsing the
   stream with the known blank passphrase produced embedded filename
   `image11.jpg`, 48,807 bytes, checksum OK, and exact SHA-256
   `7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0`.
   It byte-matched `hidden/steg04.jpg`.
2. The fixed synthetic plaintext had SHA-256
   `41f1895f67c4dd704156b9555bcd8f81d970815979e9e8dff09c0b4bacf75b03`.
   Its `planet` carrier produced the required seed `2c52fe1c`, a 112-byte raw
   stream, and decoded back to `fixed.txt`, 59 bytes, checksum OK, with the
   same SHA-256 and an exact byte comparison.
3. The never-embedded JPEG completed all 2^32 seeds, exited 1 with `Could not
   find a valid seed`, and created zero `.raw` or `.meta` files.

Only after those controls passed, `image07.jpg` produced:

```text
seed=0f58d719
plain_bits=157865
enc_algo=2            # rijndael-128
enc_mode=1            # CBC
raw_bits=158080
raw_bytes=19760
IV=e5777082fda3b3ff0054e56b6ce096f1
raw_sha256=dd8bd04b408b1d64e9801f37835b16cc7af54549c9d735f26942985dd67e856d
```

The 19,760 bytes are exactly a 16-byte IV plus 19,744 bytes of block-aligned
ciphertext. `file` reports only `data`; all 256 byte values occur; measured
Shannon entropy is 7.991366954418 bits/byte. Three eight-byte printable runs
were present, at the rate expected in random ciphertext, and are not treated
as clues. The local `binwalk` launcher remains broken (`binwalk.__main__`
missing), so it provided no result; this does not affect the byte, alignment,
or entropy checks.

The implementation uses a 32-byte password-derived key for 16-byte-block
Rijndael/CBC. The selector fold constrains only 32 bits derived from the first
MD5 digest; the encrypted metadata and payload remain opaque. The known seed
therefore exposes no filename, compression flag, checksum, magic, or practical
passphrase-independent decryption route.

**Decision:** the control-valid raw recovery succeeds, but it leaves the exact
passphrase as the blocker. Generic mask expansion remains disallowed.
