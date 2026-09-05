#!/usr/bin/env python3
"""Find 3-word lyric sequences (and title words) fully present as Boggle/T9 words on the grid."""
from collections import defaultdict

GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
SWAP = [row[:] for row in GRID]
SWAP[1][4], SWAP[2][3] = SWAP[2][3], SWAP[1][4]
KEY = {2:"abc",3:"def",4:"ghi",5:"jkl",6:"mno",7:"pqrs",8:"tuv",9:"wxyz"}
def letters(d): return KEY.get(d,"")
DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

dict_words = set()
with open('words.txt') as f:
    for line in f:
        w = line.strip().lower()
        if w.isalpha() and 1 <= len(w) <= 12:
            dict_words.add(w)

def grid_wordset(grid):
    prefix = defaultdict(set)
    for w in dict_words:
        for i in range(1, len(w)):
            prefix[w[:i]].add(w[:i+1])
    found = set()
    def dfs(r, c, used, s):
        if s in dict_words and len(s) >= 1:
            found.add(s)
        nxt = prefix.get(s)
        if not nxt:
            return
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0 <= nr < 6 and 0 <= nc < 7 and (nr, nc) not in used:
                for L in letters(grid[nr][nc]):
                    ns = s + L
                    if ns in nxt:
                        used.add((nr, nc))
                        dfs(nr, nc, used, ns)
                        used.discard((nr, nc))
    for r in range(6):
        for c in range(7):
            for L in letters(grid[r][c]):
                if L in prefix:
                    dfs(r, c, {(r, c)}, L)
    return found

print("computing original...")
WS = grid_wordset(GRID)
print("orig words:", len(WS))
print("computing swapped...")
WS2 = grid_wordset(SWAP)
print("swap words:", len(WS2))

SONGS = {
 "mad_world": """i know a world where everyone can hear me i know a world where no ones free to speak
 and theres no one to blame theres nothing to gain i know a world where no one feels the beat
 and when my heart beats fast it beats so fast i can feel it i feel it i feel like im a fool in this mad mad world""",
 "personal_jesus": """personal jesus reaching out in faith im in the deep im in trouble i need your working
 im in the deep im in trouble and i cant be saved without you personal jesus youre the only one i see
 ill be down on my knees ill be down on my knees ill be down on my knees personal jesus youre the only one i see
 save me from myself save me from myself save me from myself save me from myself personal jesus i need your working
 i can feel you reaching out in faith personal jesus i cant be alone hold on hang on
 personal jesus youre the only one i see save me from the dark outside no no no
 save me from the dark outside no no no i need your working i can feel you reaching out in faith
 personal jesus reaching out in faith i need your working i can feel you reaching out in faith
 i need your working i can feel you reaching out in faith i need your working i can feel you reaching out in faith""",
 "la_isla_bonita": """la isla bonita where the sun shines bright the people are all so nice i feel like im in a paradise
 i love you i love you love you la isla bonita i would like to stay the people are all so nice
 i feel like im in a paradise i love you i love you love you when the night begins i see your silhouette
 moving to the music the music and you and i love the way you move you i love the way you move
 i want you i want you want you la isla bonita i would like to stay""",
 "papa_dont_preach": """papa dont preach to me papa dont preach ive been to the altar and ive seen your kind
 its a lonely place and the devils in it youve been a good man all of your life you cant turn back
 you can only go forward so dont try so hard to make me change my mind i know what im doing
 and dont you dare try to change my mind papa dont preach to me papa dont preach ive been to the altar
 and ive seen your kind its a lonely place and the devils in it so dont try so hard to make me change my mind
 i know what im doing and dont you dare try to change my mind papa dont preach to me papa dont preach
 i know what im doing and dont you dare try to change my mind you can try you can try you can try
 but you can never make me change my mind""",
 "ghostbusters": """ghostbusters if theres anything out there im ready for it im ready for it im ready for it
 i got you i believe in you i got you i believe in you i got you i believe in you ghostbusters""",
 "i_just_called": """i just called to say i love you i just called to say i love you to tell you how im feeling
 gotta tell you right now nothing gonna change my love for you you know that i still love you i need you
 you know that i still need you months go by and my longing just keeps growing and its only getting stronger
 im thinking of you all the time my love for you i just called to say i love you i just called to say i love you
 to tell you how im feeling gotta tell you right now nothing gonna change my love for you you know that i still love you
 i need you you know that i still need you""",
}
TITLES = {
 "mad_world": "mad world",
 "personal_jesus": "personal jesus",
 "la_isla_bonita": "la isla bonita",
 "papa_dont_preach": "papa dont preach",
 "ghostbusters": "ghostbusters",
 "i_just_called": "i just called to say i love you",
}

def trigram_hits(WS, min_present=2):
    hits = []
    for song, text in SONGS.items():
        words = [w for w in text.split() if w.isalpha()]
        for i in range(len(words)-2):
            t = tuple(words[i:i+3])
            n = sum(1 for w in t if w in WS)
            if n == 3:
                hits.append(t)
    return sorted(set(hits))

for name, ws in [("ORIGINAL", WS), ("SWAPPED", WS2)]:
    print(f"\n===== {name}: title words present =====")
    for song, t in TITLES.items():
        tw = t.split()
        mark = [w for w in tw if w in ws]
        if mark:
            print(f"  {song}: {mark}")
    print(f"===== {name}: full lyric trigrams (all 3 words present) =====")
    for t in trigram_hits(ws):
        print("  ", " ".join(t))

# 2-word and 1-word lyric presence per song (for selection-rule analysis)
print("\n===== per-song lyric-word presence =====")
for name, ws in [("ORIGINAL", WS), ("SWAPPED", WS2)]:
    print(f"-- {name}")
    for song, text in SONGS.items():
        words = [w for w in text.split() if w.isalpha()]
        uniq = sorted(set(w for w in words if len(w) >= 2 and w in ws))
        print(f"  {song}: {uniq}")

# check specific words
probe = ["isla","bonita","la","papa","preach","dont","just","called","say","love","you","to","faith","reach","touch","out","work","ready","believe","got","ghost","shine","paradise","nice","sun","knees","save","dark","only","see","devils","kind","man","life","lonely","altar","hear","know","world","mad","fool","feel","feels","still","need","tell","how","time","thinking","longing","growing","stronger","beats","fast","heart","beat","blame","gain","speak","free","everyone","me"]
print("\n===== probes =====")
for w in probe:
    a, b = w in WS, w in WS2
    if a or b:
        print(f"  {w}: orig={a} swap={b}")
