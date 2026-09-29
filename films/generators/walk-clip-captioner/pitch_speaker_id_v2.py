import json, subprocess, numpy as np, os
d=json.load(open('transcripts.json'))
try: old=json.load(open('pitch.json'))
except: old={}
def src(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def f0(path,s,e):
    dur=max(0.25,e-s)
    raw=subprocess.run(['ffmpeg','-nostdin','-v','error','-ss',str(s),'-t',str(dur),'-i',path,'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout
    x=np.frombuffer(raw,dtype=np.float32)
    if x.size<2000: return None
    sr=16000;W=1024;hop=256;out=[]
    for i in range(0,len(x)-W,hop):
        w=x[i:i+W]
        if np.sqrt((w**2).mean())<0.01: continue
        w=w-w.mean(); ac=np.correlate(w,w,'full')[W-1:]
        if ac[0]<=0: continue
        ac/=ac[0]; lo,hi=int(sr/300),int(sr/70); seg=ac[lo:hi]
        if seg.size==0: continue
        p=np.argmax(seg)+lo
        if ac[p]<0.3: continue
        out.append(sr/p)
    return float(np.median(out)) if len(out)>=3 else None
res={}
for k,segs in d.items():
    if k in old and len(old[k])==len(segs): res[k]=old[k]; continue
    p=src(k)
    res[k]=[{**s,'f0':f0(p,s['s'],s['e'])} for s in segs]
json.dump(res,open('pitch.json','w'),indent=0)
v=[s['f0'] for a in res.values() for s in a if s['f0']]
print('clips',len(res),'segments',sum(len(a) for a in res.values()),'voiced',len(v))
print('quartiles',[round(np.percentile(v,q)) for q in (10,25,50,75,90)])
lo=sum(1 for x in v if x<135); print('below135',lo,'above',len(v)-lo)
