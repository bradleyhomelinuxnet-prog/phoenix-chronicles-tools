import json, os, subprocess, textwrap, re
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
P=json.load(open('/home/claude/tx/pitch.json')); M=json.load(open('/home/claude/tx/meta.json'))
def src(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def yr_key(v):
    m=re.match(r'(\d+) (BC|AD)', v['yr'])
    if not m: return 9999
    n=int(m.group(1)); return -n if m.group(2)=='BC' else n
order=sorted(M, key=lambda k:(yr_key(M[k]), k))
json.dump(order, open('order.json','w'))
def wr(p,s): open(p,'w').write(s)
for i,k in enumerate(order,1):
    n=f"{i:02d}"; v=M[k]; out=f"F{n}.mp4"
    if os.path.exists(out): continue
    wr(f"a{n}.txt",v['am']); wr(f"y{n}.txt",v['yr']); wr(f"p{n}.txt",v['ph']); wr(f"t{n}.txt",v['ttl'])
    vf=[]
    if v['am']: vf.append(f"drawtext=fontfile={FB}:textfile=a{n}.txt:x=70:y=66:fontsize=56:fontcolor=0xE8D7B0:shadowcolor=black@0.85:shadowx=2:shadowy=2")
    yt = 134 if v['am'] else 70
    vf.append(f"drawtext=fontfile={FR}:textfile=y{n}.txt:x=74:y={yt}:fontsize=32:fontcolor=0x9EC9F0:shadowcolor=black@0.85:shadowx=2:shadowy=2")
    vf.append(f"drawtext=fontfile={FR}:textfile=p{n}.txt:x=74:y={yt+42}:fontsize=23:fontcolor=0xE8D7B0@0.62:shadowcolor=black@0.85:shadowx=2:shadowy=2")
    vf.append(f"drawtext=fontfile={FB}:textfile=t{n}.txt:x=70:y=h-96:fontsize=32:fontcolor=white@0.92:shadowcolor=black@0.85:shadowx=2:shadowy=2")
    for j,s in enumerate(P[k]):
        t=s['t'].strip()
        if not t: continue
        st=max(0.0,s['s']-0.15); en=min(14.95,s['e']+0.30)
        if en-st<0.35: continue
        who='NATORI' if (s['f0'] or 160)>=135 else 'ROGUE'
        col='0xF0C89E@0.85' if who=='NATORI' else '0x9EC9F0@0.85'
        L=textwrap.wrap(t,46)[:2] or [t]
        wr(f"d{n}_{j}.txt","\n".join(L)); wr(f"s{n}_{j}.txt",who)
        yb=178 if len(L)>1 else 150
        vf.append(f"drawtext=fontfile={FR}:textfile=s{n}_{j}.txt:x=(w-text_w)/2:y=h-{yb+42}:fontsize=23:fontcolor={col}:shadowcolor=black@0.85:shadowx=2:shadowy=2:enable=between(t\\,{st:.2f}\\,{en:.2f})")
        vf.append(f"drawtext=fontfile={FB}:textfile=d{n}_{j}.txt:x=(w-text_w)/2:y=h-{yb}:fontsize=38:line_spacing=10:fontcolor=white:box=1:boxcolor=black@0.45:boxborderw=15:shadowcolor=black@0.85:shadowx=2:shadowy=2:enable=between(t\\,{st:.2f}\\,{en:.2f})")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',src(k),'-frames:v','360','-vf',",".join(vf),
      '-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-af','loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.3,afade=t=out:st=14.6:d=0.4,aresample=48000',
      '-c:a','aac','-b:a','160k','-t','15',out,'-y'],check=True)
    print(n,v['yr'],v['ttl'][:28],flush=True)
print('DONE')
