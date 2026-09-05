#!/usr/bin/env python3
"""Systematic explorer: grid -> letter mechanisms -> dictionary hits."""
import itertools, re

GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
R, C = 6, 7
WORDS = set(w.strip() for w in open('words.txt') if w.strip())

def is_word(s):
    return s in WORDS

# ---------- reading orders over the 42 cells ----------
def cells_rowmajor():  return [(r,c) for r in range(R) for c in range(C)]
def cells_colmajor():  return [(r,c) for c in range(C) for r in range(R)]
def cells_snake():     # serpentine rows
    out=[]
    for r in range(R):
        row=[(r,c) for c in range(C)]
        if r%2: row.reverse()
        out+=row
    return out
def cells_snakec():    # serpentine cols
    out=[]
    for c in range(C):
        col=[(r,c) for r in range(R)]
        if c%2: col.reverse()
        out+=col
    return col_out if False else out
def cells_spiral():    # spiral inward
    out=[]; seen=set(); top,bot,left,ri=0,R-1,0,C-1
    while top<=bot and left<=ri:
        for c in range(left,ri+1): out.append((top,c))
        for r in range(top+1,bot+1): out.append((r,ri))
        if top+1<=bot:
            for c in range(ri-1,left-1,-1): out.append((bot,c))
        if left<=ri-1:
            for r in range(bot-1,top,-1): out.append((r,left))
        top+=1;bot-=1;left+=1;ri-=1
    return out
def cells_diag():      # diagonal sweep
    out=[]
    for s in range(R+C-1):
        for r in range(max(0,s-C+1), min(R,s+1)):
            out.append((r,s-r))
    return out

ORDERS = {
 'row': cells_rowmajor(), 'col': cells_colmajor(), 'snake': cells_snake(),
 'snakec': cells_snakec(), 'spiral': cells_spiral(), 'diag': cells_diag(),
}

# ---------- mechanisms ----------
def seq_digits(order):
    return [GRID[r][c] for (r,c) in order]

def a1z26_single(d):   # 1-9 -> A-I
    return ''.join(chr(64+d) for d in d)

def a1z26_pairs(d):    # consecutive 2-digit numbers 10..99 -> mod 26 or direct
    out=[]
    for i in range(0,len(d)-1,2):
        n = d[i]*10+d[i+1]
        out.append(n)
    return out

def a1z26_pairs_mod26(d):
    return [ (n-1)%26+1 for n in a1z26_pairs(d) ]

def keypad_letter_map():  # single press, ambiguous; return sets
    K = {2:'abc',3:'def',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:'wxyz',1:'1',0:'0'}
    return K

def multtap(d):  # runs of same digit; count mod 3 +1 within group 1-9
    K = {1:'1', 2:'abc',3:'def',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:'wxyz'}
    out=[]
    i=0
    while i < len(d):
        j=i
        while j+1<len(d) and d[j+1]==d[i]: j+=1
        cnt = (j-i) % 3 + 1
        g = K[d[i]]
        if d[i]==1:
            out.append('1')
        else:
            out.append(g[(cnt-1) % len(g)] if len(g)>1 else g[0])
        i=j+1
    return ''.join(out)

def atbash(s):
    return ''.join(chr(72-ord(c)) if c!='1' else '1' for c in s)  # A<->I ... E->E

def diffs(d, mod=26):
    return [ (d[i+1]-d[i])%mod if (d[i+1]-d[i])%mod else 26 for i in range(len(d)-1) ]

def sums(d):
    return [ (d[i]+d[i+1]) for i in range(len(d)-1) ]

def n2letter(n):
    return chr(64 + ((n-1)%26)+1)

def report(name, letters):
    """letters: string. Find dictionary words length>=4 inside (contiguous)."""
    hits = []
    L = letters
    for i in range(len(L)):
        for j in range(i+4, min(len(L), i+9)+1):
            w = L[i:j].lower()
            if is_word(w):
                hits.append(w)
    uniq = sorted(set(hits))
    if uniq:
        print(f"[{name}] {L}")
        print(f"   words: {uniq[:40]}")
    return uniq

print("=== 1. A1Z26 single (1-9 -> A-I) per reading order ===")
for on, cells in ORDERS.items():
    s = a1z26_single(seq_digits(cells))
    report(f"a1z1_{on}", s)

print("\n=== 2. A1Z26 pairs (direct & mod26) per reading order ===")
for on, cells in ORDERS.items():
    d = seq_digits(cells)
    ps = a1z26_pairs_mod26(d)
    s = ''.join(n2letter(n) for n in ps)
    report(f"a1zp_{on}", s)

print("\n=== 3. Multi-tap (runs) per reading order ===")
for on, cells in ORDERS.items():
    s = multtap(seq_digits(cells))
    report(f"mt_{on}", s)

print("\n=== 4. Atbash on A-I per reading order ===")
for on, cells in ORDERS.items():
    s = atbash(a1z26_single(seq_digits(cells)))
    report(f"atb_{on}", s)

print("\n=== 5. Diffs & sums mod26 per reading order ===")
for on, cells in ORDERS.items():
    d = seq_digits(cells)
    s1 = ''.join(n2letter(n) for n in diffs(d))
    s2 = ''.join(n2letter(n) for n in [ (x-1)%26+1 for x in sums(d)])
    report(f"diff_{on}", s1)
    report(f"sums_{on}", s2)

print("\n=== 6. Row-wise & col-wise independent (each row = word?) ===")
# A1Z26 pairs within each row (7 digits -> 3 pairs + 1 leftover)
for ri,row in enumerate(GRID):
    for mod in (False,True):
        ps = a1z26_pairs(row)
        if mod: ps=[(n-1)%26+1 for n in ps]
        s=''.join(n2letter(n) for n in ps)
        report(f"row{ri+1}_{'mod' if mod else 'raw'}", s)
for ci in range(C):
    col=[GRID[r][ci] for r in range(R)]
    ps=a1z26_pairs(col)
    s=''.join(n2letter(n) for n in [(n-1)%26+1 for n in ps])
    report(f"col{ci+1}_mod", s)

print("\n=== 7. Row as base-10 number -> letters (mod tricks) ===")
for ri,row in enumerate(GRID):
    n = 0
    for d in row: n = n*10+d
    print(f"row{ri+1} = {n}  mod26={n%26}  mod9={n%9}  digit sum={sum(row)}")

print("\n=== 8. keypad single-press word search (each digit -> its 3 letters) ===")
K = {2:'abc',3:'def',4:'ghi',5:'jkl',6:'mno',7:'pqrs',8:'tuv',9:'wxyz'}
def kp_search(cells, dirs, minlen=4):
    pos = {c:i for i,c in enumerate(cells)}
    seq = [K[GRID[r][c]] for (r,c) in cells]
    hits=set()
    L=len(cells)
    for i in range(L):
        cur=[seq[i][0]]
        for ch in cur:
            if len(ch)>=minlen and ch.lower() in WORDS: hits.add(ch.lower())
        cur=[ch+seq[i+1][0] for ch in cur] if i+1<L else []
    return hits
# row-major 2D word search with keypad letters
hits=set()
gridL = [[K[x] for x in row] for row in GRID]
for r in range(R):
    for c in range(C):
        for dr,dc in [(0,1),(1,0),(1,1),(-1,1),(0,-1),(-1,0),(-1,-1),(1,-1)]:
            s=''
            rr,cc=r,c
            while 0<=rr<R and 0<=cc<C:
                for ch in gridL[rr][cc]:
                    s2=s+ch
                    if len(s2)>=4 and s2 in WORDS: hits.add(s2)
                s = s + gridL[rr][cc][0]  # placeholder
                rr+=dr; cc+=dc
                # do proper DFS below instead
# proper DFS
hits=set()
def dfs(r,c,dr,dc,s):
    if not (0<=r<R and 0<=c<C): return
    for ch in gridL[r][c]:
        s2=s+ch
        if len(s2)>=4 and s2 in WORDS: hits.add(s2)
        dfs(r+dr,c+dc,dr,dc,s2)
for r in range(R):
    for c in range(C):
        for dr,dc in [(0,1),(1,0),(1,1),(-1,1)]:
            dfs(r,c,dr,dc,'')
print("keypad 2D word search:", sorted(hits))
