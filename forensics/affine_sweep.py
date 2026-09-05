#!/usr/bin/env python3
"""Affine/substitution sweep: digit->letter maps, find mappings with few clean words."""
import itertools

GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
R,C = 6,7
WORDS = set(w.strip() for w in open('words.txt') if w.strip())
WORDS4PLUS = {w for w in WORDS if len(w)>=4}

def words_2d(L, minlen=4, maxlen=8):
    hits = set()
    for r in range(R):
        for c in range(C):
            for dr,dc in [(0,1),(1,0),(1,1),(-1,1)]:
                s=''
                rr,cc=r,c
                while 0<=rr<R and 0<=cc<C and len(s)<maxlen:
                    s += L[rr][cc]
                    if len(s)>=minlen and s in WORDS4PLUS:
                        hits.add(s)
                    rr+=dr; cc+=dc
    return hits

def orders():
    y=[]
    y.append([(r,c) for r in range(R) for c in range(C)])
    y.append([(r,c) for c in range(C) for r in range(R)])
    out=[]
    for r in range(R):
        row=[(r,c) for c in range(C)]
        if r%2: row.reverse()
        y.append(y and None) if False else None
    # snake rows
    s=[]
    for r in range(R):
        row=[(r,c) for c in range(C)]
        if r%2: row.reverse()
        s+=row
    y.append(s)
    # snake cols
    s=[]
    for c in range(C):
        col=[(r,c) for r in range(R)]
        if c%2: col.reverse()
        s+=col
    y.append(s)
    # spiral
    s=[]; top,bot,left,ri=0,R-1,0,C-1
    while top<=bot and left<=ri:
        for c in range(left,ri+1): s.append((top,c))
        for r in range(top+1,bot+1): s.append((r,ri))
        if top+1<=bot:
            for c in range(ri-1,left-1,-1): s.append((bot,c))
        if left<=ri-1:
            for r in range(bot-1,top,-1): s.append((r,left))
        top+=1;bot-=1;left+=1;ri-=1
    y.append(s)
    # diagonals
    s=[]
    for k in range(R+C-1):
        for r in range(max(0,k-C+1), min(R,k+1)):
            s.append((r,k-r))
    y.append(s)
    # row-major reversed
    y.append(list(reversed(y[0])))
    return y

ORDERS = orders()

def n2l(n): return chr(64+((n-1)%26)+1)

results = []
# affine maps d -> (a*d+b) mod 26 (1-26)
for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
    for b in range(26):
        L = [[n2l((a*d+b)%26 or 26) for d in row] for row in GRID]
        h = words_2d(L)
        if 0 < len(h) <= 6:
            results.append((len(h), f"affine a={a},b={b}", sorted(h)))
        # 1D row-major string substrings
        s = ''.join(L[r][c] for r in range(R) for c in range(C))
        sub = set()
        for i in range(len(s)):
            for j in range(i+4, min(len(s), i+9)+1):
                w = s[i:j]
                if w in WORDS4PLUS: sub.add(w)
        if 0 < len(sub) <= 4:
            results.append((len(sub), f"affine a={a},b={b} 1D", sorted(sub)))

results.sort(key=lambda t: (t[0], t[1]))
print("candidates with <=6 words (2D) or <=4 (1D):")
for n, name, h in results[:80]:
    print(f"  {n} {name}: {h}")
