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
