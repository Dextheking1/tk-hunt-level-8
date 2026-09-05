#!/usr/bin/env python3
"""MAD WORLD analysis: path verification, mask-remainder T9, lyric Boggle."""
import sys
from collections import defaultdict

GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
# swap variant: (1,4)<->(2,3) zero-based = R2C5(7) <-> R3C4(6)
SWAP = [row[:] for row in GRID]
SWAP[1][4], SWAP[2][3] = SWAP[2][3], SWAP[1][4]

KEY = {2:"abc",3:"def",4:"ghi",5:"jkl",6:"mno",7:"pqrs",8:"tuv",9:"wxyz"}
def letters(d):
    return KEY.get(d, "")

DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

dict_words = set()
with open('words.txt') as f:
    for line in f:
        w = line.strip().lower()
        if w.isalpha() and 3 <= len(w) <= 9:
            dict_words.add(w)
print("dict words 3-9:", len(dict_words))

def boggle_words(grid, removed=frozenset(), minlen=3):
    """All dict words spellable on grid (8-dir, no reuse), skipping removed cells."""
    prefix = defaultdict(set)
    for w in dict_words:
        for i in range(1, len(w)):
            prefix[w[:i]].add(w[:i+1])
    results = defaultdict(set)
    # also keep full words by length for reporting
    def dfs(r, c, used, s):
        if s in dict_words and len(s) >= minlen:
            results[len(s)].add(s)
        nxt = prefix.get(s)
        if not nxt:
            return
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 6 and 0 <= nc < 7 and (nr, nc) not in used and (nr, nc) not in removed:
                for L in letters(grid[nr][nc]):
                    ns = s + L
                    if ns in nxt:
                        used.add((nr, nc))
                        dfs(nr, nc, used, ns)
                        used.discard((nr, nc))
    for r in range(6):
        for c in range(7):
            if (r, c) in removed:
                continue
            for L in letters(grid[r][c]):
                if L in prefix:
                    dfs(r, c, {(r, c)}, L)
    return results

def path_count(grid, word):
    """Count distinct cell-paths spelling word (8-dir, no reuse)."""
    count = 0
    paths = []
    def dfs(r, c, i, used):
        nonlocal count
        if i == len(word):
            count += 1
            paths.append(tuple(used))
            return
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 6 and 0 <= nc < 7 and (nr, nc) not in used:
                if word[i] in letters(grid[nr][nc]):
                    dfs(nr, nc, i+1, used | {(nr, nc)})
    for r in range(6):
        for c in range(7):
            if word[0] in letters(grid[r][c]):
                dfs(r, c, 1, {(r, c)})
    return count, paths

print("== path uniqueness (original grid) ==")
for w in ["mad","wrod","word","world","kelli","smelt","tills"]:
    n, p = path_count(GRID, w)
    print(f"{w}: {n} path(s)", p[:3])
print("== path uniqueness (swapped grid) ==")
for w in ["mad","wrod","word","world"]:
    n, p = path_count(SWAP, w)
    print(f"{w}: {n} path(s)", p[:3])

print("== mask-remainder T9 (original grid) ==")
mask_wrod = frozenset([(0,6),(1,5),(0,4),(2,5),(1,4),(2,3),(3,2)])
mask_world = frozenset([(0,6),(1,5),(0,4),(2,5),(1,4),(2,3),(3,4),(4,3)])
for name, mask, g in [("WROD-mask(7)", mask_wrod, GRID),
                      ("WORLD-mask(8)", mask_world, SWAP)]:
    res = boggle_words(g, mask, minlen=4)
    total = sum(len(v) for v in res.values())
    print(f"-- {name}: {total} words len>=4")
    for L in sorted(res):
        ws = sorted(res[L])
        print(f"   len{L} ({len(ws)}):", " ".join(ws)[:400])

print("== full T9 inventory len3/len4 (original) ==")
res = boggle_words(GRID, minlen=3)
for L in (3,4):
    print(f"len{L}:", " ".join(sorted(res.get(L, []))))
print("== full T9 inventory len3/len4 (swapped) ==")
ress = boggle_words(SWAP, minlen=3)
for L in (3,4):
    print(f"len{L}:", " ".join(sorted(ress.get(L, []))))
print("len5 swapped:", " ".join(sorted(ress.get(5, []))))

print("== lyric dictionary Boggle ==")
LYRIC_WORDS = set("""
i know a world where everyone can hear me no ones free to speak and theres
no one to blame nothing to gain feels the beat and when my heart beats
fast it so can like im a fool in this mad
personal jesus reaching out in faith im in the deep im in trouble i need
your working im in the deep im in trouble and i cant be saved without you
personal jesus youre the only one i see save me from the dark outside
no im on my knees ill be on my knees ill be on my knees hold on hang on
la isla bonita where the sun shines bright the people are all so nice i
feel like im in a paradise i love you i love you love you
papa don preach to me papa don preach ive been to the altar and ive seen
your kind its a lonely place and the devils in it youve been a good man
all of your life you cant turn back you can only go forward
ghostbusters if theres anything out there im ready for it im ready for it
im ready for it i got you i believe in you i got you i believe in you
i just called to say i love you to tell you how im feeling gotta tell
you right now nothing gonna change my love for you you know that i still
love you i need you you know that i still need you months go by and my
longing just keeps growing and its only getting stronger im thinking of
you all the time my love for you
dreams are made of this what do they consist of its hard to say
""".split())
LYRIC_WORDS = {w.strip(",'?!.").lower() for w in LYRIC_WORDS if w.strip(",'?!.").isalpha()}
# also check as T9-spellable
res_l = boggle_words(GRID, minlen=3)
hits = {}
for L in range(3, 10):
    for w in res_l.get(L, ()):
        if w in LYRIC_WORDS:
            hits.setdefault(L, set()).add(w)
print("lyric hits original:", {L: sorted(v) for L, v in hits.items()})
ress_l = boggle_words(SWAP, minlen=3)
hits2 = {}
for L in range(3, 10):
    for w in ress_l.get(L, ()):
        if w in LYRIC_WORDS:
            hits2.setdefault(L, set()).add(w)
print("lyric hits swapped:", {L: sorted(v) for L, v in hits2.items()})
