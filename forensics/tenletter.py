#!/usr/bin/env python3
"""Census: which triples of common board words have EXACTLY 10 distinct letters in union?
House pattern: L6 and L7 answers both have exactly 10 distinct letters total."""
import pickle
from itertools import combinations
import wordfreq

wp = pickle.load(open('/tmp/wp_orig.pkl','rb'))

def freq(w):
    try: return wordfreq.word_frequency(w, 'en')
    except Exception: return 0.0

common = {}
for w, paths in wp.items():
    f = freq(w)
    if f >= 3e-6 and len(w) >= 4:
        common[w] = f

words = sorted(common, key=lambda w: (-len(w), -common[w], w))
print(f"common words len>=4: {len(words)}")

sets = {w: set(w) for w in words}
lens = {w: len(w) for w in words}

# 1) top-3 longest
t3 = words[:3]
print("top3 longest:", t3, "union distinct:", len(union_sets := set().union(*[sets[w] for w in t3])))

# 2) among top-15 longest words: which triples hit exactly 10?
top15 = words[:15]
hits15 = []
for a,b,c in combinations(top15, 3):
    u = sets[a] | sets[b] | sets[c]
    if len(u) == 10:
        hits15.append((a,b,c))
print(f"triples within top15 with 10 distinct: {len(hits15)}")
for h in hits15[:20]: print("   ", h)

# 3) among ALL common words: count triples with exactly 10 distinct letters (any 3)
n10 = 0
examples = []
for a,b,c in combinations(words, 3):
    u = sets[a] | sets[b] | sets[c]
    if len(u) == 10:
        n10 += 1
        if len(examples) < 12: examples.append((a,b,c))
print(f"ALL triples of common words with exactly 10 distinct: {n10}")
print("   examples:", examples)

# 4) among the longest triples: max total length per distinct-count
best = {}
for a,b,c in combinations(words, 3):
    u = sets[a] | sets[b] | sets[c]
    key = len(u)
    tot = lens[a]+lens[b]+lens[c]
    if key not in best or tot > best[key][0]:
        best[key] = (tot, a, b, c)
for key in sorted(best, reverse=True):
    tot, a, b, c = best[key]
    print(f"  max-total-len triple with {key} distinct: {tot} = {a} {b} {c}")
