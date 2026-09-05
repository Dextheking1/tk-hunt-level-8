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

## Results (run after preregistration)

Run date: 2026-09-05. The unprivileged namespace bind left the installed
Hashcat kernel unchanged.

### Implementation control

- stock optimized-kernel SHA-256:
  `05eaf3083bc1cbed4b1f1531412134793722835b48cdd0154080420dd76ddf58`
- copied control-kernel SHA-256:
  `b0131e6fd56c3ccfb8f1f2949b7100ba637caf0a7fcdfd6cd7209d875c1e1620`
- sentinel internal-state words:
  `b9702086 19b721da cb16887c e54207c9`
- complete scalar lowercase-length-4 collision set: `{test}`
- complete vectorized lowercase-length-4 collision set: `{test}`
- independently recomputed fold: `H("test") = cb4257a3`

Both enumerators completed all 456,976 candidates and their complete sets
matched exactly, so the frozen acceptance control passed. The synthetic
sentinel technique writes matching lanes to the outfile but leaves Hashcat's
real-MD5 recovery counter at zero; consequently an exhausted run returns 1.
This observed status behavior was handled explicitly. Candidate-set equality
and independent fold recomputation, not the recovery counter, were the
registered implementation checks.

### Target run

Target-kernel SHA-256:
`1d365c03cc9c6bf412322ef42f25cbf4ebf1a781e7d76461dc1ce1c7b12bcb3d`.
All four logs report `Status: Exhausted`, exact full progress, and zero rejected
candidates.

| Frozen mask | Candidates / progress | Runtime | Final speed | Fold hits |
|---|---:|---:|---:|---:|
| printable `?a`, length 5 | 7,737,809,375 | 44 s | 293.0 MH/s | 0 |
| `?l?u?d`, length 6 | 56,800,235,584 | 135 s | 462.6 MH/s | 15 |
| `?l?d`, length 7 | 78,364,164,096 | 184 s | 359.6 MH/s | 16 |
| lowercase `?l`, length 8 | 208,827,064,576 | 469 s | 445.9 MH/s | 57 |
| **Total** | **351,729,273,631** | **832 s** | — | **88** |

The 88 observed hits are consistent with the preregistered random expectation
of about 81.893. Python independently recomputed `H(p) = 0f58d719` for every
exact password byte string. Three hits (`ketoxe`, `smzqagh`, `ovxqfiu`) repeat
earlier narrower scans because the new length-6/7 masks overlap those prior
families; 85 are newly observed random fold collisions. The complete set is in
`image07_fast_fold_matches.tsv`.

Ordinary `steghide extract` was then run twice for each of the 88 exact
passwords. All 176 attempts returned 1 and created no output. Therefore none
is the image07 password. Per the decision rule, these masks are closed with no
adaptive extension. The confirmed payload remains encrypted; the unresolved
blocker is its unknown passphrase outside all preregistered families tested.
