#!/usr/bin/env python3
# 2026-09-05: H-preimage wordlist scan for image07 passphrase.
# H(p) = LE32(MD5(p)[0:4]^[4:8]^[8:12]^[12:16]); target seed 0x0f58d719.
# Families NOT covered by earlier closed scans (732 catalog, 1.76M corpus,
# 7.14M generic/dict, 100M pairs, 594 seed forms, a-z<=6, dec<=8):
#  - PRS / Paul Reed Smith orbit and broader musician collaborators
#  - full legal names incl. middle parts, record labels
#  - cover titles WITH articles + alternates
#  - image07 visual vocabulary, puzzle vocabulary, grid word triples
#  - odd external tokens (questiclesdotnet, banana/kyle wood, etc.)
#  - L6/L7 known answers (author reuse hypothesis)
# Case forms + separators + short numeric affixes. Bounded ~ few 100k.
import hashlib, itertools, sys, os, time

TARGET = bytes([0x19, 0xd7, 0x58, 0x0f])
HITS = []

def check(p: bytes) -> bool:
    h = hashlib.md5(p).digest()
    return ((h[0]^h[4]^h[8]^h[12]) == TARGET[0] and
            (h[1]^h[5]^h[9]^h[13]) == TARGET[1] and
            (h[2]^h[6]^h[10]^h[14]) == TARGET[2] and
            (h[3]^h[7]^h[11]^h[15]) == TARGET[3])

BASES = []
def add(*ws):
    for w in ws:
        w = w.strip()
        if w: BASES.append(w)

# --- person / band names (legal + stage) ---
add("orianthi panagaris", "orianthi", "orianthi panagaris adelaide", "orianthi adelaide",
    "paul reed smith", "paul smith", "prs guitars", "prs", "paulreedsmith",
    "alice cooper", "alicecooper", "michael jackson", "michaeljackson", "this is it",
    "madonna louise ciccone", "madonna ciccone", "madonna", "aubrey drake graham", "drake",
    "cameron jibril thomaz", "cameron thomaz", "wiz khalifa", "wizkhalifa",
    "raymond parker", "ray parker jr", "ray parker", "rayparkerjr",
    "stevie wonder", "stevland morris", "stevland hardaway judkins", "stevland",
    "dan reynolds", "daniel coulter reynolds", "imagine dragons", "wayne sermon",
    "ben mckee", "daniel platzman", "depeche mode", "dave gahan", "martin gore",
    "andrew fletcher", "vince clarke", "alan wilder", "kyle wood", "kylewood",
    "carlos santana", "richie sambora", "steve vai", "zakk wylde", "slash",
    "saul hudson", "gary moore", "joe satriani", "eddie van halen", "jimmy page",
    "carrie underwood", "kelly clarkson", "joss stone", "michael bolton",
    "zakk wylde black label", "black label society", "john 5", "nita strauss",
    "lita ford", "joan jett", "nancy wilson", "jennifer batten", "taylor swift",
    "prince", "beyonce", "rihanna", "katy perry", "lady gaga", "pink", "gwen stefani")
# --- record labels / industry ---
add("geffen records", "interscope", "island records", "republic records", "motown",
    "polydor", "mute records", "sire records", "atlantic records", "rcm",
    "19 recordings", "rob cavallo", "dave stewart")
# --- Orianthi song/album catalog incl. articles and alternates (re-cheap) ---
add("violet journey", "believe", "believe ii", "heaven in this hell", "rock candy",
    "some kind of feeling", "live from hollywood", "according to you",
    "shut up and kiss me", "shut up & kiss me", "courage", "frozen", "sex e bizarre",
    "better with you", "impulsive", "sinners hymn", "attention", "dark days are gone",
    "highly strung", "bad news", "whats it gonna be", "what's it gonna be",
    "missing you", "think like a girl", "now or never", "light it up",
    "where did your heart go", "sorry", "radio free america", "livin on a prayer",
    "living on a prayer", "girl in a catsuit", "we are the world", "usa for africa")
# --- other artists' key songs with articles ---
add("la isla bonita", "papa don't preach", "papa dont preach", "personal jesus",
    "i just called to say i love you", "ghostbusters", "who you gonna call",
    "hotline bling", "see you again", "black and yellow", "young wild and free",
    "radioactive", "believer", "thunder", "whatever it takes", "demons", "on top of the world",
    "reach out and touch faith", "never let me down again", "enjoy the silence",
    "just can't get enough", "somebody", "stripped", "i feel you", "world in my eyes",
    "the right stuff", "hangin tough", "step by step", "cover girl", "please don't go girl",
    "you got it", "i'll be loving you", "dirty dawg", "this one's for the children")
# --- cover/hidden-image visual vocabulary ---
add("white prs", "prs white", "signature prs", "orianthi signature", "custom 24",
    "custom24", "silver sky", "mccarty", "sculpted", "blonde guitarist", "blonde",
    "guitar", "guitarist", "rock guitar", "shred", "solo", "vintage", "stage",
    "les paul", "stratocaster", "telecaster", "headstock", "amplifier", "band",
    "rock star", "rockstar", "loveloud", "love loud", "utah", "salt lake city",
    "slc", "usana", "mega pass", "festival", "charity")
# --- level-8 vocabulary ---
add("block grid thingy", "blockgridthingy", "grid thingy", "level 8", "level8",
    "kracken", "kraken", "treasure kracken", "treasurekracken", "tk", "level 8 kracken",
    "tk level 8", "8 kracken", "eight", "the kracken", "captain kracken", "kracken 8")
add("mad world", "madworld", "tears for fears", "tearsforfears", "tears",
    "homie", "smelt", "tills", "kelli", "idiom", "taint", "sheik", "homie smelt tills",
    "homie tills smelt", "smelt homie tills", "smelt tills homie", "tills homie smelt",
    "tills smelt homie", "idiom sheik taint", "sheik idiom taint", "taint sheik idiom",
    "necklace popcorn love", "necklacepopcornlove", "ducks pump premium", "duckspumppremium",
    "necklace", "popcorn", "love", "ducks", "pump", "premium")
add("questiclesdotnet", "questicles", "questicles dot net", "dotnet", "gulag",
    "boris", "banana", "bananas", "fun facts about bananas", "funfactsdaily",
    "orange", "red", "blue", "green", "yellow", "purple", "pink", "black", "white")
add("orianthi hotline", "orianthi payphone", "hotline", "payphone", "telephone",
    "phone", "dial", "ring ring", "ring", "call", "called", "i love you",
    "love you", "you", "planet", "8675309", "jenny", "jenny i got your number")
# --- years / dates relevant ---
add("1984", "1986", "1987", "1989", "2015", "2016", "2018", "2019", "2025",
    "2026", "1025", "1031", "halloween", "october", "october 31", "oct 31", "christmas",
    "xmas", "valentine", "summer", "winter", "fall", "spring")
# --- seed/hex literals (mostly covered by 594; cheap to include) ---
add("0f58d719", "of58d719", "0F58D719", "0xf58d719", "f58d719", "0f58d71", "0f58d7",
    "3b75655e", "2c52fe1c", "2059e", "f341", "132510", "0x2059e", "2059E")

SEPS = ["", "-", "_", " "]
DIGS = ["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "07", "8",
        "2025", "2026", "69", "88", "96", "x", "xx", "007", "11"]
def case_forms(s):
    forms = {s.lower(), s.upper(), s.capitalize(), s.title()}
    forms.add(s.lower().replace(" ", ""))
    if "'" in s:
        forms.add(s.replace("'", ""))
    return forms

def main():
    cands = set()
    for base in BASES:
        cf = case_forms(base)
        for f in list(cf):
            if " " in f:
                # separator variants for phrases
                for sep in SEPS:
                    cands.add(sep.join(f.split()))
            else:
                cands.add(f)
    # numeric affixes only for canonical (lower, joined, capitalized) single forms
    single = sorted(cands)
    aff = []
    for f in single:
        for d in DIGS:
            aff.append(f + d)
            aff.append(d + f)
    cands.update(aff)
    # cap size guard
    cands = set(c.lower().replace(" ", "") if False else c for c in cands)  # keep separators
    cands = {c for c in cands if 0 < len(c) <= 40 and all(ord(ch) < 128 for ch in c)}
    total = len(cands)
    print(f"[WLS] families={len(BASES)} bases, {total:,} unique candidates", flush=True)
    t0 = time.time()
    for i, c in enumerate(sorted(cands)):
        if check(c.encode("utf-8")):
            HITS.append(c)
            print(f"[WLS] HIT {c!r}", flush=True)
        if i and i % 2000000 == 0:
            print(f"[WLS] {i:,}/{total:,}", flush=True)
    out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "..", "image07_scan_results.txt"))
    with open(out, "a") as fh:
        for c in HITS:
            fh.write(f"HIT {c!r} md5={hashlib.md5(c.encode()).hexdigest()} fam=WLS\n")
    print(f"[WLS] COMPLETE total={total:,} elapsed={time.time()-t0:.1f}s hits={HITS}", flush=True)

if __name__ == "__main__":
    main()
