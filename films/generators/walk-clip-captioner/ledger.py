import json, os, subprocess, re
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
def srcpath(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
nodes=[]
for i,k in enumerate(order,1):
    v=M[k]
    m=re.search(r'138 × (\d+)', v['ph'])
    if v['am'] and m: nodes.append((i,k,v,int(m.group(1))))
nodes.sort(key=lambda x:x[3])
print('phoenix nodes',len(nodes),'first',nodes[0][3],'last',nodes[-1][3])
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
for pos,(idx,k,v,mult) in enumerate(nodes,1):
    out=f"L{pos:02d}.mp4"
    if os.path.exists(out): continue
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-ss','11','-i',srcpath(k),'-frames:v','1',f"s{pos:02d}.png",'-y'],check=True)
    wr(f"la{pos:02d}.txt",v['am']); wr(f"ly{pos:02d}.txt",v['yr'])
    wr(f"lm{pos:02d}.txt",f"138 × {mult}"); wr(f"lt{pos:02d}.txt",v['ttl'])
    wr(f"lc{pos:02d}.txt",f"FIRE {pos} OF 43")
    vf=("zoompan=z='min(zoom+0.0012,1.10)':d=48:s=1920x1080:fps=24,"
        f"drawtext=fontfile={FB}:textfile=la{pos:02d}.txt:x=70:y=70:fontsize=58:fontcolor=0xE8D7B0:shadowcolor=black@0.85:shadowx=3:shadowy=3,"
        f"drawtext=fontfile={FR}:textfile=ly{pos:02d}.txt:x=74:y=140:fontsize=34:fontcolor=0x9EC9F0:shadowcolor=black@0.85:shadowx=2:shadowy=2,"
        f"drawtext=fontfile={FB}:textfile=lm{pos:02d}.txt:x=w-tw-70:y=76:fontsize=44:fontcolor=0x9EC9F0@0.92:shadowcolor=black@0.85:shadowx=3:shadowy=3,"
        f"drawtext=fontfile={FR}:textfile=lc{pos:02d}.txt:x=w-tw-74:y=134:fontsize=22:fontcolor=0xE8D7B0@0.55:shadowcolor=black@0.85:shadowx=2:shadowy=2,"
        f"drawtext=fontfile={FB}:textfile=lt{pos:02d}.txt:x=70:y=h-92:fontsize=34:fontcolor=white@0.94:shadowcolor=black@0.9:shadowx=3:shadowy=3,"
        "fade=t=in:st=0:d=0.10,fade=t=out:st=1.88:d=0.12")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-loop','1','-i',f"s{pos:02d}.png",
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v','-map','1:a',
      '-frames:v','48','-vf',vf,'-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-c:a','aac','-b:a','128k','-shortest',out,'-y'],check=True)
    if pos%10==0: print('made',pos,flush=True)
print('LEDGERDONE')
