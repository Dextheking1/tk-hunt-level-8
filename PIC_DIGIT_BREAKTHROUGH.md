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

## Stronger repo-only reading: answer-word layers

The string made by the path plus its missing-file letters is naturally read as
**PIC DIGIT — WORD TWO**. That suggests taking the second word initial from
each picture label. The independently recovered `NTH` says to generalize this
to the Nth word for answer word N.

Use these established labels:

1. Personal Jesus
2. La Isla Bonita
3. Papa Don't Preach
4. Drake
5. Wiz Khalifa
6. I Just Called to Say I Love You
7. Ghostbusters
8. Orianthi
9. Dan Reynolds

A one-word label keeps its only initial; a longer label contributes its Nth
word when it has one. The three letter layers begin:

- word 1: `1=P,2=L,3=P,4=D,5=W,6=I,7=G,8=O,9=D`
- word 2: `1=J,2=I,3=D,4=D,5=K,6=J,7=G,8=O,9=R`
- word 3: `2=B,3=P,4=D,6=C,7=G,8=O` (other multiword labels are blank)

Touching-cell paths then give:

- **WIDOW** (word-1 layer): digits `56485`,
  `R4C2 → R5C1 → R6C2 → R6C1 → R5C2`
- **DROID** (word-2 layer): digits `39823`,
  `R4C7 → R3C6 → R3C7 → R2C6 → R1C5`
- **COP** (word-3 layer): digits `683`,
  `R1C2 → R2C1 → R3C2`

Each has exactly one path. WIDOW is the only ordinary-English maximum-length
word in layer 1 (`Diplo` is a proper name), and DROID is the sole length-5 word
in layer 2. In sparse layer 3, COP is the most frequent everyday word having
one path; more frequent GOD/DOG/ODD and near-peer DOC/COD repeat. A 500,000
histogram-preserving random-grid control reproduced all three exact unique
paths only 170 times (0.034%). Combined with the independently rare unique
`PICDIGITWORD` instruction, this is the strongest repo-only answer mechanism
found so far.

### Current leading candidate

`widow droid cop`

No live request or submission was made.

### Exact remaining caution

Layer 3 also has less-common one-path words such as COB and BOD, so **COP is
strongly salient but not selected by a purely formal longest-word rule**.
Also, retaining the sole initial of a one-word label (Orianthi) in later layers
is natural but implicit. Those are now the only substantive blockers to calling
the candidate mathematically unique.

The previous *The Right Stuff* lyric candidate `great blast love` is downgraded:
it requires an external lyric lookup and an arbitrary choice between GREAT and
the line-final TIME. The `widow droid cop` route stays within the repository's
picture labels and directly obeys `PIC DIGIT WORD TWO` plus `NTH`.
