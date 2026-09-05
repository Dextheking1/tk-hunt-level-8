#!/usr/bin/env python3
"""Labyrinth test: do the grid digits encode directions (numpad/phone layout)?
If a chain starting somewhere visits all 42 cells exactly once -> the grid is a maze."""
GRID = [
    [4,6,6,4,3,1,6],
    [8,5,9,1,7,2,5],
    [2,3,9,6,5,9,8],
    [1,5,3,9,5,1,3],
    [6,5,1,3,4,7,5],
    [8,4,6,1,8,4,9],
]
R, C = 6, 7
KEY = {2:"abc",3:"def",4:"ghi",5:"jkl",6:"mno",7:"pqrs",8:"tuv",9:"wxyz"}

MAPPINGS = {
    "numpad": {7:(-1,-1),8:(-1,0),9:(-1,1),4:(0,-1),6:(0,1),1:(1,-1),3:(1,1)},
    "phone":  {1:(-1,-1),2:(-1,0),3:(-1,1),4:(0,-1),6:(0,1),7:(1,-1),8:(1,0),9:(1,1)},
}

def follow(mapping, start, rev=False):
    path = [start]
    used = {start}
    r, c = start
    while True:
        d = GRID[r][c]
        if d == 5:
            break
        vec = mapping.get(d)
        if vec is None:
            break
        dr, dc = vec
        if rev:
            dr, dc = -dr, -dc
        nr, nc = r+dr, c+dc
        if not (0 <= nr < R and 0 <= nc < C) or (nr, nc) in used:
            break
        path.append((nr, nc))
        used.add((nr, nc))
        r, c = nr, nc
    return path

def main():
    results = []
    for mname, mp in MAPPINGS.items():
        for start in [(r,c) for r in range(R) for c in range(C)]:
            for rev in (False, True):
                p = follow(mp, start, rev=rev)
                results.append((len(p), mname, rev, start, p))
    results.sort(key=lambda t: -t[0])
    print("top 10 chains:")
    for L, m, rvs, s, p in results[:10]:
        print(f"  len={L:2d} mapping={m} rev={rvs} start={s}")
    print()
    print("HAMILTONIAN (len>=40):")
    for L, m, rvs, s, p in results:
        if L >= 40:
            print(f"  mapping={m} rev={rvs} start={s} len={L}")
            print("   cells:", p)
            print("   digits:", [GRID[r][c] for (r,c) in p])

if __name__ == '__main__':
    main()
