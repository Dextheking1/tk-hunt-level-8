#!/usr/bin/env python3
"""Rule hunter: evaluate candidate 'pick-3' selection rules on the L8 T9-Boggle board.
Run: python3 rule_hunter.py   (writes /tmp/wp_orig.pkl, /tmp/wp_wall.pkl)"""
import pickle
from collections import defaultdict

GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
KEY = {2:"abc",3:"def",4:"ghi",5:"jkl",6:"mno",7:"pqrs",8:"tuv",9:"wxyz"}
def letters(d): return KEY.get(d,"")
DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
R, C = 6, 7

dict_words = set()
with open('words.txt') as f:
    for line in f:
        w = line.strip().lower()
        if w.isalpha() and 1 <= len(w) <= 15:
            dict_words.add(w)

import wordfreq
def freq(w):
    try: return wordfreq.word_frequency(w, 'en')
    except Exception: return 0.0

def collect(grid, minlen=3, block1=False):
    prefix = defaultdict(set)
    for w in dict_words:
        for i in range(1, len(w)-1):
            prefix[w[:i]].add(w[:i+1])
    found = defaultdict(set)
    def dfs(r, c, used, s):
        if s in dict_words and len(s) >= minlen:
            found[s].add(frozenset(used))
        nxt = prefix.get(s)
        if not nxt:
            return
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in used:
                continue
            nd = grid[nr][nc]
            if block1 and nd == 1:
                continue
            for L in letters(nd):
                ns = s + L
                if ns in nxt:
                    used.add((nr, nc))
                    dfs(nr, nc, used, ns)
                    used.discard((nr, nc))
    for r in range(R):
        for c in range(C):
            d = grid[r][c]
            if block1 and d == 1:
                continue
            for L in letters(d):
                if L in prefix:
                    dfs(r, c, {(r,c)}, L)
    return {w: list(ps) for w, ps in found.items()}

def straight_lines(grid):
    out = []
    for r in range(R):
        for c in range(C):
            for dr, dc in DIRS:
                if dr < 0 or (dr == 0 and dc < 0):
                    continue
                pr, pc = r-dr, c-dc
                if 0 <= pr < R and 0 <= pc < C:
                    continue
                cells = []
                rr, cc = r, c
                while 0 <= rr < R and 0 <= cc < C:
                    cells.append((rr, cc)); rr, cc = rr+dr, cc+dc
                if len(cells) >= 3:
                    out.append(cells)
    return out

def line_words(lines):
    hits = defaultdict(set)
    for cells in lines:
        digits = [GRID[r][c] for (r,c) in cells]
        if any(d == 1 for d in digits):
            continue
        opts = [letters(d) for d in digits]
        def rec(i, s):
            if len(s) >= 3 and s in dict_words:
                hits[s].add(tuple(digits))
            if i == len(opts): return
            for L in opts[i]:
                rec(i+1, s+L)
        rec(0, "")
    return hits

def top3(scored): return [t[3] for t in scored[:3]]

def report(tag, words_paths, thr=3e-6, topn=30):
    scored = []
    for w, paths in words_paths.items():
        f = freq(w)
        if f < thr: continue
        scored.append((len(w), f, len(paths), w))
    scored.sort(key=lambda t: (-t[0], -t[1], t[2], t[3]))
    print(f"== {tag} ==  ({len(scored)} common words)")
    for t in scored[:topn]:
        print(f"   len={t[0]:2d} freq={t[1]:.1e} paths={t[2]:3d}  {t[3]}")
    print("  top3 ->", top3(scored))
    print()
    return scored

def disjoint3(words_paths, thr=5e-6, minlen=4, maxlen=9, cap=160):
    cands = []
    for w, paths in words_paths.items():
        if not (minlen <= len(w) <= maxlen): continue
        f = freq(w)
        if f < thr: continue
        cands.append((w, f, list(paths)[:4]))
    cands.sort(key=lambda t: (-t[1], t[0]))
    cands = cands[:cap]
    n = len(cands)
    found = {}
    for i in range(n):
        for j in range(i+1, n):
            a, fa, pa = cands[i]
            b, fb, pb = cands[j]
            for k in range(j+1, n):
                c, fc, pc = cands[k]
                for xa in pa:
                    for xb in pb:
                        if xa & xb: continue
                        blocked = xa | xb
                        for xc in pc:
                            if not (xc & blocked):
                                key = tuple(sorted((a,b,c)))
                                found[key] = len(a)+len(b)+len(c)
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
    items = sorted(found.items(), key=lambda kv: (-kv[1], kv[0]))
    return items

def main():
    try:
        wp = pickle.load(open('/tmp/wp_orig.pkl','rb'))
        wp2 = pickle.load(open('/tmp/wp_wall.pkl','rb'))
        print("loaded cached word sets")
    except Exception:
        print("collecting board words (1 = no letters, passable)...")
        wp = collect(GRID, minlen=3)
        pickle.dump(wp, open('/tmp/wp_orig.pkl','wb'))
        print("collecting with 1 as wall...")
        wp2 = collect(GRID, minlen=3, block1=True)
        pickle.dump(wp2, open('/tmp/wp_wall.pkl','wb'))
    print(f"total words (1 passable): {len(wp)}   (1 wall): {len(wp2)}")
    print()

    scored = report("RULE A: all common words (1 passable)", wp)
    scored2 = report("RULE B: common words (1 = wall)", wp2)

    print("== RULE D: straight lines, digit->one letter ==")
    lw = line_words(straight_lines(GRID))
    for w, d in sorted(lw.items(), key=lambda t: (-len(t[0]), t[0])):
        print(f"   {len(w):2d} {w}  <- digits {list(d)}")
    print()

    ones = [(r,c) for r in range(R) for c in range(C) if GRID[r][c] == 1]
    print("1-cells:", ones)
    print()

    print("== RULE A3: 3 pairwise cell-disjoint common words (max total len) ==")
    items = disjoint3(wp)
    for key, tot in items[:15]:
        print(f"   total={tot:2d}  {' / '.join(key)}")
    print(f"   ({len(items)} disjoint triples total)")
    print()

    # tiling check: 3 disjoint paths covering all 42 cells
    allcells = frozenset((r,c) for r in range(R) for c in range(C))
    print("== TILING: 3 disjoint words whose paths cover all 42 cells ==")
    ntile = 0
    for key, tot in items:
        if tot == 42:
            ntile += 1
            print("   TILING:", key)
    print(f"   ({ntile} tiling triples)")

if __name__ == '__main__':
    main()
