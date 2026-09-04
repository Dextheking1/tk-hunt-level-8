# Level 8 rendered-page inventory (from local `page_dve99.json`, no live fetch)

This is everything the Level 8 page renders beyond `grid.png` and the Velo
gate file. Source of truth is `page_dve99.json` (`props/render/compProps`);
`level8.html` is only the generic Wix shell (`<title>Level-8</title>`, no puzzle
content, no img alt text).

## Visible elements, in order

1. Heading (h2, underlined): **BLOCK GRID THINGY** — it is a link:
   `https://www.youtube.com/watch?v=jZcrSUhonBk` (new tab).
   Component: `comp-mdq6p6yh`. The video itself was not fetched here.
2. Grid image (`comp-mt4nmrcx`): `0d5510_2edf85d9a3374cc2b99661a8384a96ae~mv2.png`,
   1176x1056, alt/name `level8.png`. Clicking it opens the full-size image in a
   new tab (ExternalLink to the same static URL).
3. Heading (h5): `.` — a literal single period, nothing else.
   Component: `comp-msm3k8y81`.
4. Text input (`comp-msm3k8yb1`): empty value, empty label, empty placeholder.
5. Button (`comp-msm3k8yf`): label `Submit`, no link (Velo-handled).
6. Footer (h6): `TREASURE KRACKEN 2026` (`comp-mdq6p6yn1_r_comp-me5swrmj`).
7. Footer icons linking out: Discord (`https://discord.gg/5gF9X6zkWs`),
   Instagram (`https://www.instagram.com/utah_treasure_hunters/`),
   Reddit (`https://www.reddit.com/r/utahtreasurehunt/`).

## What is NOT on the page

- No other text, hints, alt text, placeholders, aria labels, or hidden
  components exist in the page JSON. The nav-vector alt texts are stock
  ("Open/Close Site Navigation").
- SEO is locked down: `noarchive, nofollow, noimageindex, nosnippet`.
- The countdown/validation/redirect behavior lives in `velo_dve99.js`
  (60s timer, `validatePasswordAndAssignRole(8, …)`, redirect `/level-9`).

## Unexamined pointer

The only rendered-page element whose content is not in this repo is the linked
YouTube video `jZcrSUhonBk`. Everything else on the page is above.
