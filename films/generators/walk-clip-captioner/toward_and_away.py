import json, os, subprocess, sys
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
def sp(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
def seg(idx, kind):
    """kind: 'in' = 0-5 approach, 'out' = 10-15 departure"""
    k=order[idx-1]; v=M[k]
    out=f"{'I' if kind=='in' else 'O'}{idx:02d}.mp4"
    if os.path.exists(out): return out
    ss = '0' if kind=='in' else '10'
    wr(f"my{idx}.txt", (v['am']+"   " if v['am'] else "")+v['yr'])
    wr(f"mt{idx}.txt", v['ttl'])
    A="alpha='min(1\\,min((t-0.3)/0.7\\,(4.6-t)/0.7))'"
    vf=(f"drawtext=fontfile={FB}:textfile=my{idx}.txt:x=70:y=70:fontsize=44:fontcolor=0xE8D7B0:shadowcolor=black@0.85:shadowx=3:shadowy=3:{A},"
        f"drawtext=fontfile={FR}:textfile=mt{idx}.txt:x=70:y=h-88:fontsize=28:fontcolor=white@0.88:shadowcolor=black@0.9:shadowx=2:shadowy=2:{A}")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-ss',ss,'-i',sp(k),
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000',
      '-map','0:v','-map','1:a','-frames:v','120','-vf',vf,
      '-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-c:a','aac','-b:a','128k','-t','5',out,'-y'],check=True)
    return out
if __name__=='__main__':
    idxs=[int(x) for x in sys.argv[1].split(',')]
    for i in idxs:
        seg(i,'in'); seg(i,'out')
        print(i,flush=True)
    print('SEGDONE')
