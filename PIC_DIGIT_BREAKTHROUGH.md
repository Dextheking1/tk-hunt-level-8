# PIC DIGIT WORD breakthrough (repo-only, unsubmitted)

## Picture alphabet

Use the nine meaningful images in physical recursive discovery order. Each
digit can stand for the initials of the words identifying that picture:

| digit | picture | usable initials |
|---|---|---|
| 1 | Personal Jesus | P/J |
| 2 | La Isla Bonita | L/I/B |
| 3 | Papa Don’t Preach | P/D |
| 4 | Drake | D |
| 5 | Wiz Khalifa | W/K |
| 6 | I Just Called to Say I Love You | I/J/C/T/S/L/Y |
| 7 | Ghostbusters | G |
| 8 | Orianthi | O |
| 9 | Dan Reynolds | D/R |

This is not ordinary T9.

## Exact path message

The original, unmodified 6x7 grid has exactly one adjacent, non-reusing path
for `PICDIGITWORD` under that alphabet:

`166967265893`

`R2C4 → R1C3 → R1C2 → R2C3 → R3C4 → R2C5 → R2C6 → R1C7 → R2C7 → R3C7 → R3C6 → R4C7`

A 500,000-grid random permutation control preserving the digit histogram found
this word at all in 3.35% and found it uniquely in 0.1544%.

Apply the numbered-picture stencil to the 12 path positions:

| position | file state | path letter |
|---:|---|:---:|
| 1 | image01 | P |
| 2 | image02 | I |
| 3 | unnumbered hidden picture | C |
| 4 | image04 | D |
| 5 | unnumbered hidden picture | I |
| 6 | image06 | G |
| 7 | image07 | I |
| 8 | missing | T |
| 9 | missing | W |
| 10 | missing | O |
| 11 | embedded filename image11 | R |
| 12 | image12 | D |

The two unnumbered hidden pictures fill the two internal gaps, and the three
actual missing positions are therefore 08–10. Their letters are **TWO**. This
is direct evidence for the previously unproved 03/05 gap fill.

## Three planted straight words

Under the same picture alphabet, the conspicuous straight-line words are:

- `TWO`: `658`, `R1C7 → R2C7 → R3C7` (one straight path)
- `OLD`: `823`, `R3C7 → R2C6 → R1C5` (one straight path)
- `KIDS`: `5696`, `R4C5 → R3C4 → R2C3 → R1C2` (one straight path)

Top-to-bottom they read **TWO OLD KIDS**. The next high-frequency alternative,
`TRY`, has two paths; these three are the highest-frequency words with exactly
one straight path. Combined with **BLOCK** in the page title and the music
payload, this points to **New Kids on the Block**, not to a final password.

## THE RIGHT STUFF

Using ordinary telephone T9 plus the already-observed literal `1 = I` rule,
the grid contains exactly one adjacent non-reusing `THE` path and exactly one
`RIGHT` path:

- `THE`: `843`, `R6C5 → R5C5 → R5C4`
- `RIGHT`: `71448`, `R5C6 → R4C6 → R5C5 → R6C6 → R6C5`

`THINGY` in the page title supplies the synonym **STUFF**. New Kids on the
Block + THE RIGHT + STUFF identifies their song **The Right Stuff**.

A 20,000-grid histogram-preserving control found the joint condition “unique
straight TWO/OLD/KIDS in top-to-bottom order plus unique T9 THE and RIGHT” only
2 times (0.01%). Together with unique PICDIGITWORD and the independent NTH
self-check, the chain is overwhelmingly structural rather than a word-search
coincidence.

## Candidate final extraction (not live-tested)

The opening verse of *The Right Stuff* explicitly enumerates first, second,
and third times. The changing result words are:

- first time: **great**
- second time: **blast**
- third time: **love**

This gives the strongest current password candidate:

`great blast love`

No live request or submission was made. Remaining caution: a mechanical
line-final reading would be `time blast love`; the changing-result reading is
preferred because repeated `time` is scaffolding, while GREAT / BLAST / LOVE
are the three semantic payloads. This final choice is the only unresolved
micro-ambiguity in an otherwise deterministic chain.
