# Hidden content in `grid.png`

## Container and extraction facts

Found 2026-09-04 with `binwalk` and ZIP carving.

- The 3,279,027-byte `grid.png` is a PNG/ZIP polyglot.
- The visible PNG ends at byte 132,510 (`0x2059e`).
- A valid 3,146,517-byte ZIP begins at that offset and ends exactly at EOF.
- The ZIP has no comment and contains exactly six files, in this order:
  `image01.png`, `image02.jpg`, `image04.jpg`, `image06.jpg`,
  `image07.jpg`, `image12.jpg`.
- Recursive carving and metadata inspection found no further archive layer.

The visible pixel layer itself is clean. The earlier conclusion that the whole
file had no hidden content was wrong because it examined only PNG pixels and
chunks and missed the archive appended after `IEND`.

## Confirmed image inventory

| file | identification | useful detail |
|---|---|---|
| `image01.png` | Madonna, *La Isla Bonita* cover | PNG `Artist` text field contains a base64 data URI |
| nested payload | Madonna, *Papa Don’t Preach* cover | URI claims PNG, but decoded magic is JPEG (`FFD8FFE0`), 300x300 |
| `image02.jpg` | Drake | OVO shirt and OVO-style cap |
| `image04.jpg` | Wiz Khalifa | empty-password `steghide` payload |
| nested `image04` payload | Stevie Wonder, *I Just Called to Say I Love You* cover | tracked as `hidden/steg04.jpg` |
| `image06.jpg` | Ray Parker Jr., *Ghostbusters* cover | 200x199 cover image |
| `image07.jpg` | Orianthi | white PRS guitar with the ornate O emblem |
| `image12.jpg` | Dan Reynolds (Imagine Dragons) | LOVELOUD shirt; EXIF date 2018-07-28 |

The user-provided `thumb.png` and `artist_thumb.jpg` are helper copies of the
same nested Madonna image, and `img02_small.png` is a helper copy of
`image02.jpg`; they are not additional ZIP entries.

The `image01` nested JPEG has SHA-256
`83431008255b5c4bccf2604e9db407579ef4d67c824af7f3d4fdb12e39d1c12b`.

A second nested image is extracted with:

```bash
steghide extract -sf image04.jpg -p ""
```

It is a 300x300 Stevie Wonder *I Just Called to Say I Love You* cover with
SHA-256 `7643d7326d34fe2671a545f0443c2f0e40536c3ea450959103f90dc8771ac7a0`.
No recursive payload was found in either nested cover. Tests of more than 100
candidate passwords on images 02, 06, 07, and 12 did not establish another
`steghide` layer.

## Artist-initial intermediate

Taking the six principal artists in numeric filename order gives:

```text
01 Madonna       M
02 Drake         D
04 Wiz Khalifa   W
06 Ray Parker Jr R
07 Orianthi      O
12 Dan Reynolds  D
                 MDWROD
```

The literal metadata key `Artist` supplies an `A` inside the `image01` step,
so the strongest reading is:

```text
M A D / W R O D
MAD WROD
```

This is an intermediate hypothesis, not the password. The nested Stevie
Wonder cover supplies additional content that this outer-artist acrostic does
not yet explain, so `MAD WROD` must not be treated as a complete extraction.

## Exact phone-keypad/Boggle fit

Use ordinary phone-keypad groups (`2=ABC`, `3=DEF`, `5=JKL`, `6=MNO`,
`7=PQRS`, `9=WXYZ`) and allow movement to any of the eight adjacent cells.
Coordinates below are one-based.

In the original grid there is exactly one non-reusing path for `MAD`:

```text
R1C7 6=M -> R2C6 2=A -> R1C5 3=D
```

There is also exactly one non-reusing path for `WROD`:

```text
R3C6 9=W -> R2C5 7=R -> R3C4 6=O -> R4C3 3=D
```

Swap the two R/O blocks at R2C5 and R3C4, exchanging the 7 and 6. The same
opening cells now read `WOR`, and the modified grid contains exactly one
non-reusing `WORLD` path:

```text
R3C6 9=W -> R2C5 6=O -> R3C4 7=R -> R4C5 5=L -> R5C4 3=D
```

This tightly supports **MAD WORLD** as an intended intermediate. A 50,000-grid
same-size random simulation found unique `MAD` and unique `WROD` paths together
in about 2.46% of grids; the meaningful R/O swap and unique `WORLD` continuation
make the full coincidence substantially more specific.

## Rejected conclusions

These have been tried on the live gate and returned invalid:

- `papa don’t preach`
- `tears for fears` (the tempting original artist of *Mad World*)

Therefore **MAD WORLD is not sufficient as a final solve**, and the last step
cannot simply be to name the original performer. `la isla bonita` is also a
weak endpoint because it ignores the rest of the payload and is not three
English words.

## Open questions

1. What operation should follow the `MAD WORLD` intermediate?
2. What is the exact role of filenames `01, 02, 04, 06, 07, 12` beyond order?
3. Does the eight-cell `MAD` plus `WORLD` mask select, block, rotate, or reorder
   other grid cells?
4. Does *Mad World* identify lyrics, a particular recording or video, or
   another music-related key rather than its artist?
5. What roles do the nested *Papa Don’t Preach* and *I Just Called to Say I
   Love You* covers play? Candidate fragments `i love you` and `i just called`
   are unvalidated and do not yet connect cleanly to the grid.

## Third nested cover: Depeche Mode "Personal Jesus" (solo track)
`grid.png` also carries a 62,220-byte `eXIf` chunk (offset 0x21, right after
`IHDR`, before the first `IDAT`). It holds a TIFF header plus one complete
embedded 300x300 JPEG (offset 172 in the chunk) = Depeche Mode "Personal
Jesus" (1989) single cover, tracked as `hidden/exif_personaljesus.jpg`.
Its own metadata: Photoshop CS Windows, created 2016-12-19, original
1000x1000, paint.net 4.3.11. Same 300x300 cover-art format as the two
Madonna singles: deliberately planted. Lyric read ("reach out and touch
faith") = look inside the files. Two words, so not the password itself.
Extract: `python -c "d=open('grid.png','rb').read();open('pj.jpg','wb').write(d[0x21+8+172:0x21+8+62220])"`
(or `exiftool -b -ThumbnailImage` on the chunk).

## Further rejections (live gate, INVALID)
- `la isla bonita`
- `i love you`
- `homie smelt tills`, `homie tills smelt`, `idiom taint sheik`,
  `idiom sheik taint`, `smelt homie tills`, `smelt tills homie`,
  `tills homie smelt` (grid T9-word orders)
- `widow droid cop` (PICDIGIT Nth-layer candidate — INVALID, chain retired)

### Burn: image07 bounded masks and generic best64 rules (2026-09-05)
With the validated MD5-fold seed oracle, full controlled searches killed:
printable ASCII length <=4, mixed-case alphanumeric length 5, lowercase
alphanumeric length 6, lowercase alphabetic length 7, and 162,505,112 outputs
from installed best64 rules over local generic sources. Mask fold collisions
`ketoxe`, `smzqagh`, and `ovxqfiu` each failed extraction twice. These are hash
collisions, not answer candidates; never submit or revive them.

### Burn: image07 puzzle-vocabulary triple keys (2026-09-05)
335-word V (top-300 common board words ∪ 24 cover-title words ∪ 14
artist-name words) × ordered triples × 4 joinings = 150,381,500 candidates,
canary-validated, zero fold collisions vs 0f58d719 (PREREG_IMAGE07_TRIPLE_
VOCAB.md). Together with the 4B top-1000 triple kill, no three-word password
composed of puzzle-surfaced words can hold the image07 payload. Do not
revive with reordered V or extra joinings; only words outside the puzzle
surface (unknown 10th image, personal) remain.
