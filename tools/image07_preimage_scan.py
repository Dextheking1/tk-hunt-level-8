#!/usr/bin/env python3
# Preregistered 2026-09-05 image07 passphrase preimage scan (H mapping validated in-repo).
# H(p) = LE32-fold of MD5 quarters; target seed 0x0f58d719.
# Family arg: F36 -> a-z0-9 lengths 1..6 ; F62 -> a-zA-Z0-9 lengths 1..5
import hashlib, itertools, sys, time, os, multiprocessing as mp

T0 = bytes([0x19, 0xd7, 0x58, 0x0f])  # little-endian target 0x0f58d719
Q = None

def check(p: bytes) -> bool:
    h = hashlib.md5(p).digest()
    if (h[0] ^ h[4] ^ h[8] ^ h[12]) != T0[0]: return False
    if (h[1] ^ h[5] ^ h[9] ^ h[13]) != T0[1]: return False
    if (h[2] ^ h[6] ^ h[10] ^ h[14]) != T0[2]: return False
    return (h[3] ^ h[7] ^ h[11] ^ h[15]) == T0[3]

def scan(args):
    chars, L = args
    n = len(chars) ** L
    cnt = 0
    for tup in itertools.product(chars, repeat=L):
        p = bytes(tup)
        if check(p):
            Q.put(('H', p))
        cnt += 1
        if cnt % 10000000 == 0:
            Q.put(('p', L, cnt))
    Q.put(('p', L, n))
    return L

def main():
    fam = sys.argv[1]
    here = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.normpath(os.path.join(here, '..', 'image07_scan_results.txt'))
    if fam == 'F36':
        lengths = [1, 2, 3, 4, 5, 6]
        chars = b'abcdefghijklmnopqrstuvwxyz0123456789'
    else:
        lengths = [1, 2, 3, 4, 5]
        chars = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    total = sum(len(chars) ** L for L in lengths)
    global Q
    ctx = mp.get_context('fork')
    Q = ctx.Queue()
    procs = 2
    with ctx.Pool(processes=procs) as pool:
        res = pool.imap_unordered(scan, [(chars, L) for L in lengths])
        finished = 0
        counts = {}
        hits = []
        last = time.time()
        it = iter(res)
        try:
            while finished < len(lengths):
                # nonblocking drain of Q
                while not Q.empty():
                    try:
                        msg = Q.get_nowait()
                    except Exception:
                        break
                    if msg[0] == 'H':
                        hits.append(msg[1])
                    elif msg[0] == 'p':
                        counts[msg[1]] = msg[2]
                try:
                    nxt = next(it)
                    finished += 1
                    counts[nxt] = len(chars) ** nxt
                except StopIteration:
                    pass
                now = time.time()
                if now - last > 20:
                    last = now
                    s = sum(counts.values())
                    print(f"[{fam}] per-length counts {dict(sorted(counts.items()))} total {s:,}/{total:,} "
                          f"({100.0 * s / max(1, total):.1f}%) finished={finished}/{len(lengths)} hits={len(hits)}",
                          flush=True)
                time.sleep(0.5)
        except KeyboardInterrupt:
            print('interrupted', flush=True)
        # drain
        while not Q.empty():
            try:
                msg = Q.get_nowait()
            except Exception:
                break
            if msg[0] == 'H':
                hits.append(msg[1])
        with open(outpath, 'a') as f:
            for h in hits:
                f.write(f'HIT {repr(h)} md5={hashlib.md5(h).hexdigest()} fam={fam}\n')
        print(f"[{fam}] COMPLETE total={total:,} hits={[x for x in hits]}", flush=True)

if __name__ == '__main__':
    main()
