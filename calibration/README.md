# Calibration pack: solved levels + Level 0 pointer

Purpose: give the Level 8 keypad/selection-rule work a known-plaintext calibration
target. Known solved passwords are `necklace popcorn love` (Level 6) and
`ducks pump premium` (Level 7).

Important limitation: the local workspace does **not** contain the full Level 6 /
Level 7 puzzle bodies. The HTML shells below are generic Wix page shells; the
actual puzzle content lives in external Wix page JSON / media that was not
present locally. No live site was fetched for this pack.

## Files

- `level-6/level-6.html`
  - Source: `/tmp/tk8/site/level-6.html`
  - Size: 698499 bytes
  - SHA256: `a46a3dd2cf60472297cffd40e6a3df27f741a5965373e2c7b1ceaaa5e6c1d128`
  - Notes: `<title>Level-6</title>`, canonical
    `https://www.treasurekracken.com/level-6`; otherwise a generic Wix shell.
    No Level 6 puzzle image or page-data JSON is present locally.

- `level-7/level-7.html`
  - Source: `/tmp/tk8/site/level-7.html`
  - Size: 697032 bytes
  - SHA256: `cd2b85e4160d0192c12239f7ded90ca0b629b6f9c6a232eef21f92dc2b063cc5`
  - Notes: `<title>Level-7</title>`, canonical
    `https://www.treasurekracken.com/level-7`; otherwise a generic Wix shell.
    No Level 7 puzzle image or page-data JSON is present locally.

- `level-7/level7_q1.png`
  - Source: `/home/beni/level7_q1.png`
  - Size: 220901 bytes, PNG 627x627 RGB
  - SHA256: `8a10f726de9717afe0b11b4085d7af3f9fc64f8be6c76c6befb193e196dc1ea4`
  - Notes: filename suggests a Level 7 question-1 screenshot; image content was
    not visually verified in this pass.

- `level-7/level7_q4.png`
  - Source: `/home/beni/level7_q4.png`
  - Size: 205236 bytes, PNG 627x627 RGB
  - SHA256: `88f1907aad8509dc335714b0be618b31d7205055b713676e2eb22af29b1e0e09`
  - Notes: filename suggests a Level 7 question-4 screenshot; image content was
    not visually verified in this pass.

- `level-0/qa-level0-snippet.md`
  - The actual Level 0 page was not present locally, so it could not be added.
  - This file preserves the exact local Q&A statement about Level 0 plus its
    source path.

## Still missing for true calibration

- Level 6 puzzle body: room/secret-room/torch/checkpoint layout or page media.
- Level 7 puzzle body: labyrinth/fork assets, board state, page-data JSON, media.
- Actual Level 0 hint page.
- Any author-side keypad→word convention example tied to a solved answer.

If those exist anywhere else locally, point to the paths and they can be added
without touching the live site.
