# COMPLETE MAP — level-8 hunt inventory (2026-09-05)

Consolidated state from the swarm's full-scan adjudication (f02ddfa) +
arena-branch forensics. Every row verified against repo files where
possible (verification noted).

| file | deeper content | lock | status |
|---|---|---|---|
| `grid.png` (3,279,027 B) | PNG (7×6 digit grid) + **XMP/eXIf** (offset 0x1ce, `ns.adobe.com/exif/1.0`) + **ZIP** (offset 0x2059e → EOF, 6 entries) | none — carve and read | **VERIFIED this pass**: ZIP = all six carriers, each **byte-identical** (sha256) to the top-level repo files; entry dates 2026-09-03 21:35. NOTE: supersedes the old "no EXIF/text chunks" line in ANALYSIS.md (Grid section) — that check was incomplete. |
| `image01.png` (89,480 B) | **Artist-field cover** + **XMP dates** (XMP at 0x4efa) | none — base64 decode | **VERIFIED**: XMP present; decoded payload already banked (`hidden/artist_b64.txt` 20,134 B → `hidden/artist_hidden.jpg`); terminal PNG (clean IEND tail, zero trailing bytes). |
| `image02.jpg` (421,058 B) | nothing | — | swarm full 2^32 `stegseek --seed`: **MISS**; arena single-seed control: 0x93347a (no magic). |
| `image04.jpg` (1,519,450 B) | Stevie Wonder "I Just Called…" cover (48,807 B); **embedded filename `image11.jpg`** (authoritative: steghide extraction report) | none — **blank passphrase** | **VERIFIED**: seed 3b75655e = H("") arithmetically (arena, this pass); payload banked `hidden/steg04.jpg` (sha256 7643d732…); two-pipeline stream bit-exact (390,527 b). Arena's decryption sub-thread still has an open local bug (MD5("") key fails the 49-bit oracle at every offset 33–73) — does not affect the map: extraction ground truth + H("") both say blank. |
| `image06.jpg` (18,494 B) | nothing | — | swarm full 2^32 scan: **MISS**; arena control: 0x0567d2 (no magic). |
| `image07.jpg` (956,205 B) | **19.3 KB encrypted payload** (rijndael-128/CBC, nplainbits 157,865, enc 19,760 B) at seed 0f58d719 | **unknown passphrase** — the ONLY remaining lock in the hunt | **VERIFIED** (arena two-pipeline bit-exact + swarm full scan HIT); H(p) = 0f58d719 filter; per preregistered stopping rule all finite families dead (4B triples, 11.2B masks, 351.7B vectorized, 145k dictionary, puzzle triples). |
| `image12.jpg` (183,346 B) | nothing | — | swarm full 2^32 scan: **MISS**; arena control: 0x37cd2f (no magic). |
| 3 nested covers (artist in image01, Stevie in image04, +1) | terminal | **zero trailing bytes** (nothing appended after any nested payload) | terminal = no further steganography inside (outguess false-positives already killed, swarm MY_SOLVE_PASS addenda). |

## Net state

- **Solved/readable:** grid, image01 (artist + XMP dates), image04 (blank
  passphrase), the grid.png bundle (XMP/eXIf + 6-file ZIP).
- **Proven empty:** image02, image06, image12 (full seed space scanned).
- **Locked (sole remaining lock):** image07 passphrase.
- Open local items (do not change the map): arena's image04 AES
  sub-thread bug (needs one synthetic carrier or the author's steghide
  binary — see VERDICT_PAYLOAD_CLAIM.md).

## Verification log (this pass)

- grid.png: ZIP@0x2059e + EOCD at EOF, 6 entries; XMP with exif namespace
  at 0x1ce; sha256 of all 6 extracted entries == top-level files.
- image01.png: XMP@0x4efa; clean IEND tail.
- All file sizes cross-checked vs this file's table.
