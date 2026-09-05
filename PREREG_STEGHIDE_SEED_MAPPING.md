# Preregistration: characterize steghide password-to-seed mapping

Date: 2026-09-04. Committed before tracing or comparing any synthetic seed.
The purpose is technical password recovery for the confirmed image07 carrier,
not selection of a puzzle answer.

## Fixed experiment

1. Build a local `LD_PRELOAD` shim that records every unsigned argument passed
   to libc `srand` while leaving behavior unchanged.
2. Using one deterministic synthetic JPEG and one fixed tiny payload, embed with
   exactly these passphrases in this order:
   - empty string
   - `a`
   - `abc`
   - `test`
   - `planet`
   - `8675309`
   - `correcthorsebatterystaple`
3. Repeat `planet` on a second deterministic JPEG to test cover independence.
4. Run StegSeek seed mode on one `planet` control and require its reported seed
   to equal the traced seed before treating the trace as the embedding seed.
5. Compare all seven password/seed pairs against only these preregistered
   transforms: CRC32, Adler-32, FNV-1a-32, DJB2-32, and every contiguous four
   bytes (both endian readings) of MD5, SHA-1, SHA-224, SHA-256, SHA-384,
   SHA-512, and RIPEMD-160 digests of the exact UTF-8 password bytes.

## Decision

A transform is accepted only if it matches every fixed pair and the independent
StegSeek control. Otherwise this simple-mapping hypothesis is killed. A match
would justify a separately preregistered seed-preimage attack; it does not by
itself authorize any password expansion or answer candidate.

No live-site request or submission is involved.

## Attempt A result: libc `srand` is not the path

The preload shim built and all eight synthetic embeddings completed, but no
call to libc `srand` occurred for any registered passphrase or either cover.
The script therefore stopped before its StegSeek control. This is an
instrumentation null result, not a password-family result: steghide's normal
`/dev/urandom`/libmhash path does not expose the embedding selector through
libc `srand`.

## Preregistered follow-up B: trace the dynamically linked libmhash path

Before running it, replace only the failed observation layer as follows:

1. Preload wrappers for the imported `mhash_init`, `mhash`, and
   `mhash_deinit` functions. Record the hash algorithm id, exact input byte
   lengths/bytes, and final digest while forwarding all calls unchanged.
2. Use the same seven fixed passphrases, fixed payload, and two-cover `planet`
   repeat listed above.
3. Complete StegSeek seed mode on the first `planet` carrier and compare that
   reported seed with only the digest-window/endian transforms already frozen
   above.
4. Require identical libmhash traces for `planet` across both covers before
   calling the mapping password-dependent.

If no passphrase-bearing hash/digest can be observed, or no frozen transform
matches the StegSeek seed, this follow-up is killed; no extra hash formula is
introduced post hoc.

## Follow-up B result

The libmhash trace succeeded and left steghide behavior unchanged (the `planet`
control extracted byte-identically). Every passphrase is hashed with MD5
(`mhash` algorithm 1), and the `planet` digest is cover-independent:

`MD5("planet") = 5f295bce38d311f26a96eb811192f391`

StegSeek independently found seed `2c52fe1c` for that carrier. None of the
pre-registered contiguous digest windows/endian readings equals that seed, so
follow-up B's frozen transform set is formally **killed**.

A simple new relation is visible but is not accepted from one sample: XOR the
four 4-byte MD5 quarters bytewise, obtaining `1cfe522c`, then interpret those
four bytes as a little-endian integer, obtaining exactly `2c52fe1c`.

## Preregistered follow-up C: validate MD5 XOR-folding

Define, before any further seed scan:

`H(p) = LE32(MD5(p)[0:4] XOR MD5(p)[4:8] XOR MD5(p)[8:12] XOR MD5(p)[12:16])`

where `p` is the exact UTF-8 passphrase byte string. Compute `H` for the six
other fixed passphrases (empty, `a`, `abc`, `test`, `8675309`, and
`correcthorsebatterystaple`). Run complete StegSeek seed mode on each already
created synthetic carrier. Also scan the second-cover `planet` carrier.

Accept the mapping only if every reported seed equals `H(p)` and both `planet`
carriers give the same seed. One mismatch kills it. A validated mapping permits
a separately preregistered preimage search against target seed `0f58d719`, but
no keyspace is implied by the mapping itself.

## Follow-up C result: mapping validated

The Python implementation of the preregistered formula printed these
predictions before any control scan:

| passphrase | `H(p)` | StegSeek seed |
|---|---:|---:|
| empty | `3b75655e` | `3b75655e` |
| `a` | `927c8494` | `927c8494` |
| `abc` | `275fa452` | `275fa452` |
| `test` | `cb4257a3` | `cb4257a3` |
| `planet` | `2c52fe1c` | `2c52fe1c` |
| `8675309` | `07a3d533` | `07a3d533` |
| `correcthorsebatterystaple` | `cc703c87` | `cc703c87` |

The second-cover `planet` carrier also reported `2c52fe1c`. Thus every fixed
sample and the cover-independence control match exactly: the MD5 XOR-fold
mapping is **validated**.

The validation shell script accidentally hard-coded six different numbers in
its later `predicted=` display fields; those fields consequently printed
`match=no`. They were transcription errors, not outputs of `H`. The formula's
actual pre-scan Python outputs (listed above) equal all seven StegSeek results.

## Consequence

For exact passphrase bytes `p`, steghide's 32-bit selector seed is:

`LE32(MD5(p)[0:4] XOR MD5(p)[4:8] XOR MD5(p)[8:12] XOR MD5(p)[12:16])`.

Therefore target seed `0f58d719` is a fast 32-bit filter for password
candidates. A fold match is only a collision candidate; ordinary steghide
extraction must still authenticate the real password. Candidate keyspaces
remain subject to separate preregistration.
