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
