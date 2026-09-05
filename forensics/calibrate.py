#!/usr/bin/env python3
"""Known-plaintext calibration. Usage:
  python3 calibrate.py "<r1 c1 ... r6 c7 space-separated 42 digits>" "word1 word2 word3"
Tests a battery of pick-3 rules; prints which rules reproduce the known answer
(as a set and in exact order). Run on L6 and L7 to identify THE mechanism,
then apply to L8 (digits in rule_hunter.py GRID)."""
import sys
from collections import defaultdict
import wordfreq

def freq(w):
    try: return wordfreq.word_frequency(w, 'en')
    except Exception: return 0.0

dict_words = set()
with open('words.txt') as f:
    for line in f:
        w = line.strip().lower()
        if w.isalpha() and 1 <= len(w) <= 15:
            dict_words.add(w)

KEY = {2:"abc",3:"def",4:"ghi",5:"jkl",6:"mno",7:"pqrs",8:"tuv",9:"wxyz"}
DIRS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def collect(digits, minlen=3, block1=False):
    R, C = len(digits), len(digits[0])
    prefix = defaultdict(set)
    for w in dict_words:
        for i in range(1, len(w)-1):
            prefix[w[:i]].add(w[:i+1])
    found = defaultdict(list)
    def dfs(r, c, used, s):
        if s in dict_words and len(s) >= minlen:
            found[s].append(frozenset(used))
        nxt = prefix.get(s)
        if not nxt:
            return
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in used:
                continue
            nd = digits[nr][nc]
            if block1 and nd == 1:
                continue
            for L in KEY.get(nd, ""):
                ns = s + L
                if ns in nxt:
                    used.add((nr, nc))
                    dfs(nr, nc, used, ns)
                    used.discard((nr, nc))
    for r in range(R):
        for c in range(C):
            d = digits[r][c]
            if block1 and d == 1:
                continue
            for L in KEY.get(d, ""):
                if L in prefix:
                    dfs(r, c, {(r,c)}, L)
    return {w: list(dict.fromkeys(ps)) for w, ps in found.items()}

def first_cell(paths, digits):
    """(row, col) of the reading-order first cell of the earliest path."""
    best = None
    for p in paths:
        fs = min(p)  # sorted tuple; min = top-leftmost
        if best is None or fs < best:
            best = fs
    return best

def main():
    toks = sys.argv[1].split()
    assert len(toks) == 42, f"need 42 digits, got {len(toks)}"
    digits = [[int(t) for t in toks[r*7:(r+1)*7]] for r in range(6)]
    answer = sys.argv[2].lower().split()
    assert len(answer) == 3
    aset = set(answer)
    print(f"answer: {answer}")
    print(f"grid: {digits}")
    print(f"distinct letters in answer: {len(''.join(answer)) and len(set(''.join(answer)))}")
    print()

    wp = collect(digits)
    wp2 = collect(digits, block1=True)
    print(f"words: {len(wp)} (1=passable) / {len(wp2)} (1=wall)")

    scored = sorted(((len(w), freq(w), len(ps), w) for w, ps in wp.items() if freq(w) >= 3e-6),
                    key=lambda t: (-t[0], -t[1], t[2], t[3]))
    top3 = [t[3] for t in scored[:3]]
    top3_set = set(top3)
    allwords = sorted(((len(w), len(ps), w) for w, ps in wp.items()), key=lambda t: (-t[0], -t[1], t[1]))
    top3raw = [t[2] for t in allwords[:3]]
    uniq = [w for w, ps in wp.items() if len(ps) == 1]
    uniq_sorted = sorted(uniq, key=lambda w: (-len(w), -freq(w)))

    results = []
    def chk(name, cond_set, cond_order=False):
        ok_set = cond_set == aset
        ok_ord = False
        if cond_order:
            ok_ord = list(cond_set) == answer if isinstance(cond_set, list) else None
        results.append((name, ok_set, ok_ord))

    chk("R1 top3 longest common (set)", top3_set)
    chk("R2 top3 longest dict (set)", set(top3raw))
    chk("R3 unique-path words == answer (set)", set(uniq_sorted[:3]) if len(uniq) >= 3 else None, )
    chk("R4 answer words all unique-path", aset <= set(uniq))
    # order variants of R1
    r1o1 = top3
    r1o2 = sorted(top3, key=lambda w: first_cell(wp[w], digits) or (9,9))
    r1o3 = sorted(top3)
    for nm, seq in (("R1-order: len-desc", r1o1),
                    ("R1-order: start-cell reading", r1o2),
                    ("R1-order: alpha", r1o3)):
        results.append((nm, set(seq) == aset, seq == answer))
    # disjoint greedy
    def greedy():
        out = []
        used = set()
        for w in [t[3] for t in scored]:
            if any(not (p & used) for p in wp[w]):
                out.append(w)
                used |= min(wp[w], key=lambda p: (len(p), min(p)))
                if len(out) == 3:
                    return out
        return out
    g = greedy()
    results.append(("R6 greedy longest disjoint (set)", set(g) == aset, g == answer))
    # 1-anchored: longest word touching each of 3 chosen 1s? (needs L6 shape; just report)
    ones = [(r,c) for r in range(6) for c in range(7) if digits[r][c] == 1]
    print(f"1-cells ({len(ones)}): {ones}")
    print()

    print(f"{'rule':38s} {'set':>5s}  order")
    print("-"*52)
    for name, ok_set, ok_ord in results:
        s = "?" if ok_set is None else ("YES" if ok_set else "no")
        o = "" if ok_ord is None else ("YES" if ok_ord else "no")
        print(f"{name:38s} {s:>5s}  {o}")
    print()
    print("answer present on board:", aset <= set(wp))
    print("answer lengths:", {w: len(w) for w in answer})
    for w in answer:
        if w in wp:
            print(f"  {w}: {len(wp[w])} path(s), len {len(w)}, freq {freq(w):.1e}")
        else:
            print(f"  {w}: NOT ON BOARD")

if __name__ == '__main__':
    main()
