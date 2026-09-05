# Preregistration: image07 dark-hatted background / This Is It family

Date: 2026-09-05. Committed before calculating any candidate fold.

## Motivation

A fresh visual audit confirms that `image07.jpg` shows a second dark-clothed
person at a microphone around the Orianthi foreground. One small local vision
model selected “Michael Jackson during This Is It rehearsal” from explicit
options; another model instead described a gray-bearded band member and was
internally unreliable about artists and guitar brands. The identity is thus a
falsifiable visual hypothesis, not an established fact.

If it is Michael Jackson with Orianthi, the two nearest clean password labels
are the rehearsal film/event *This Is It* and the guitar-feature song *Beat
It*; the person-name itself is a third direct label. Their all-lowercase
space/empty/hyphen/underscore forms were either included in completed common
pair/triple work or are not to be inferred as new evidence. This experiment
only checks conventional capitalization forms that those lowercase families
did not cover. It does not treat any phrase as the required random-word answer.

## Frozen candidates

For each word-case row below, join its words with exactly `""`, one ASCII
space, `-`, and `_`, in that order:

1. `This`, `Is`, `It`
2. `This`, `is`, `It`
3. `THIS`, `IS`, `IT`
4. `Beat`, `It`
5. `BEAT`, `IT`
6. `Michael`, `Jackson`
7. `MICHAEL`, `JACKSON`

Then append exactly these lower-camel forms:

- `thisIsIt`
- `beatIt`
- `michaelJackson`

Deduplicate while preserving order. This yields exactly 31 ASCII strings. No
years, punctuation, possessives, song-list expansion, partner names, prefix,
suffix, leetspeak, or post-result additions are allowed.

## Control and decision rule

First require the existing `planet -> 2c52fe1c` fold control and byte-identical
synthetic `planet` decode. Calculate all 31 selector folds. If none equals
`0f58d719`, kill the family without extraction. Any 32-bit fold match must be
tried with ordinary Steghide twice; only successful, hash-identical extraction
counts. No live-site request or submission is involved.
