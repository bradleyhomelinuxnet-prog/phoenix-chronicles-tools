import json, os, subprocess
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
def srcpath(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
want=[52,56,58,15,48,38,1,24,34,26,16,11]
for idx in want:
    k=order[idx-1]; v=M[k]; out=f"A{idx:02d}.mp4"
    if os.path.exists(out): continue
    wr(f"a{idx}.txt",v['am']); wr(f"y{idx}.txt",v['yr']); wr(f"p{idx}.txt",v['ph']); wr(f"t{idx}.txt",v['ttl'])
    vf=[]
    A="alpha='min(1\\,min((t-0.6)/1.2\\,(14.2-t)/1.2))'"
    if v['am']: vf.append(f"drawtext=fontfile={FB}:textfile=a{idx}.txt:x=70:y=66:fontsize=56:fontcolor=0xE8D7B0:shadowcolor=black@0.85:shadowx=3:shadowy=3:{A}")
    yt=134 if v['am'] else 70
    vf.append(f"drawtext=fontfile={FR}:textfile=y{idx}.txt:x=74:y={yt}:fontsize=32:fontcolor=0x9EC9F0:shadowcolor=black@0.85:shadowx=2:shadowy=2:{A}")
    vf.append(f"drawtext=fontfile={FR}:textfile=p{idx}.txt:x=74:y={yt+42}:fontsize=23:fontcolor=0xE8D7B0@0.62:shadowcolor=black@0.85:shadowx=2:shadowy=2:{A}")
    vf.append(f"drawtext=fontfile={FB}:textfile=t{idx}.txt:x=70:y=h-92:fontsize=34:fontcolor=white@0.92:shadowcolor=black@0.9:shadowx=3:shadowy=3:{A}")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',srcpath(k),'-frames:v','360','-vf',",".join(vf),
      '-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-af','lowpass=f=5200,loudnorm=I=-20:TP=-3:LRA=11,afade=t=in:st=0:d=0.5,afade=t=out:st=14.3:d=0.7,aresample=48000',
      '-c:a','aac','-b:a','160k','-t','15',out,'-y'],check=True)
    print(idx, v['yr'], v['ttl'], flush=True)
print('ATMODONE')
