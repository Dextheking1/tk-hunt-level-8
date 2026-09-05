import hashlib,itertools,multiprocessing as mp,sys,time
TGT=0x0f58d719
words=[l.strip() for l in open('/home/beni/.cache/tk-scan/google-10000.txt') if l.strip().isalpha() and l.strip().isascii()][:2000]
W=[w.encode() for w in words]
SEPS=[b'',b' ']
def shard(a0):
    out=[]
    for a in range(a0[0],a0[1]):
        A=W[a]
        for b in W:
            for c in W:
                base=0
                for s in SEPS:
                    h=hashlib.md5(A+s+b+s+c if s else A+b+c).digest()
                    x=bytes(h[i]^h[i+4]^h[i+8]^h[i+12] for i in range(4))
                    if int.from_bytes(x,'little')==TGT:
                        out.append((A.decode(),s.decode() or 'EMPTY',b.decode(),c.decode()))
                        print('HIT',out[-1],flush=True)
    return (a0,out)
if __name__=='__main__':
    t=time.time()
    shards=[(i*250,(i+1)*250) for i in range(8)]
    with mp.Pool(12) as p:
        res=p.map(shard,shards)
    allhits=[h for _,hs in res for h in hs]
    open('/home/beni/.cache/tk-scan/scan2000.done','w').write(f'done elapsed={time.time()-t:.0f}s hits={allhits}\n')
    print('DONE hits=',allhits,flush=True)
