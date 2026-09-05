# Preregistration: vectorized Hashcat MD5-fold masks for image07

Date: 2026-09-05. Committed before patching/running the control kernel or
calculating any target-family collision.

## Technical method

Use the installed Hashcat 6.2.6 optimized raw-MD5 attack-mode-3 OpenCL kernel
as a vectorized enumerator. Copy it to `/tmp` and alter only the final
multi-hash comparison:

1. calculate the validated steghide selector value
   `(A+MD5_IV_A) XOR (B+MD5_IV_B) XOR (C+MD5_IV_C) XOR (D+MD5_IV_D)`;
2. compare it with one hard-coded registered fold target;
3. for matching vector lanes only, substitute the internal MD5 state of
   Hashcat's documented sentinel digest
   `8743b52063cd84097a65d1633f5c74f5`, then invoke the stock comparison macro.

Supply that sentinel plus a second dummy MD5 hash so the multi-hash kernel is
used. Use `--keep-guessing`, disable potfile/restore/self-test, and emit all
plaintexts. Mount the copied kernel over the stock path only inside an
unprivileged user+mount namespace; the installed file stays unchanged.

## Implementation control

Hard-code control fold `H("test") = cb4257a3` and exhaust built-in lowercase
mask `?l?l?l?l` (456,976 candidates). In parallel, run the previously validated
scalar C fold scanner over the identical alphabet/keyspace. The complete sets
of fold-collision plaintexts must match exactly and must include `test`.
Independent Python must verify `H` for every emitted plaintext. Any mismatch
kills the vectorized implementation before a target run.

## Frozen target families

After the control passes, rebuild only the hard-coded fold constant to target
seed `0f58d719` and run these complete, disjoint masks:

1. built-in printable `?a`, exact length 5: `95^5 = 7,737,809,375`;
2. custom `?1=?l?u?d`, exact length 6:
   `62^6 = 56,800,235,584`;
3. custom `?1=?l?d`, exact length 7:
   `36^7 = 78,364,164,096`;
4. built-in lowercase `?l`, exact length 8:
   `26^8 = 208,827,064,576`.

Total: **351,729,273,631** password candidates. Record Hashcat's reported
keyspace/completion, kernel-source hashes, runtime, and every emitted plaintext.
No increment mode, preferred prefix, semantic word, or adaptive extension.

## Decision rule

The null expectation is approximately **81.893** 32-bit fold collisions, so
collision count and uniqueness carry no clue value. Independently verify every
output's fold, then run ordinary `steghide extract` twice with exact password
bytes. Only two successful hash-identical outputs recover the password. If all
collisions fail, close exactly these masks without extension.

No live-site request or submission is involved.
