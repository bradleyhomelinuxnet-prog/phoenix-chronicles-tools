import json, os, subprocess, sys
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
REAL={1,3,6,7,8,10,11,14,17,18,20,23,24,28,32,36,38,43,44,47,48}
AXIS=27
IDXS=[i for i in range(1,51) if i!=AXIS]          # 49 clips
def sp(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
def chy(idx, retro):
    v=M[order[idx-1]]
    wr(f"by{idx}.txt",(v['am']+"   " if v['am'] else "")+v['yr']); wr(f"bt{idx}.txt",v['ttl'])
    col = '0x9EC9F0' if retro else '0xE8D7B0'      # retrograde years run blue
    A="alpha='min(1\\,min((t-0.3)/0.7\\,(4.6-t)/0.7))'"
    return (f"drawtext=fontfile={FB}:textfile=by{idx}.txt:x=70:y=70:fontsize=44:fontcolor={col}:shadowcolor=black@0.85:shadowx=3:shadowy=3:{A},"
            f"drawtext=fontfile={FR}:textfile=bt{idx}.txt:x=70:y=h-88:fontsize=28:fontcolor=white@0.88:shadowcolor=black@0.9:shadowx=2:shadowy=2:{A}")
def run(args): subprocess.run(args,check=True)
def approach(idx):
    out=f"BI{idx:02d}.mp4"
    if os.path.exists(out): return
    run(['ffmpeg','-nostdin','-loglevel','error','-ss','0','-i',sp(order[idx-1]),
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v','-map','1:a',
      '-frames:v','120','-vf',chy(idx,False),'-c:v','libx264','-crf','19','-preset','veryfast',
      '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','128k','-t','5',out,'-y'])
def depart(idx):
    out=f"BO{idx:02d}.mp4"
    if os.path.exists(out): return
    if idx in REAL:
        run(['ffmpeg','-nostdin','-loglevel','error','-ss','10','-i',sp(order[idx-1]),
          '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v','-map','1:a',
          '-frames:v','120','-vf',chy(idx,False),'-c:v','libx264','-crf','19','-preset','veryfast',
          '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','128k','-t','5',out,'-y'])
    else:
        run(['ffmpeg','-nostdin','-loglevel','error','-ss','0','-t','5','-i',sp(order[idx-1]),
          '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000',
          '-filter_complex',f"[0:v]reverse,{chy(idx,True)}[v]",'-map','[v]','-map','1:a',
          '-frames:v','120','-c:v','libx264','-crf','19','-preset','veryfast',
          '-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','128k','-t','5',out,'-y'])
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for i in IDXS[a:b]:
        approach(i); depart(i); print(i, 'real' if i in REAL else 'RETRO', flush=True)
    print('CHUNKDONE')
