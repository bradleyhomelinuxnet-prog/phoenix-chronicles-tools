import json, os, subprocess
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
def sp(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
IDX=[1,9,10,11,13,15,26,32,50,51,52,53,55,56,58,59]
for pos,idx in enumerate(IDX,1):
    k=order[idx-1]; v=M[k]; out=f"S{pos:02d}.mp4"
    if os.path.exists(out): continue
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-ss','10','-i',sp(k),'-frames:v','1',f"p{pos:02d}.png",'-y'],check=True)
    wr(f"y{pos}.txt",v['yr']); wr(f"t{pos}.txt",v['ttl']); wr(f"c{pos}.txt",f"{pos} OF 16  ·  OFF THE GRID")
    vf=("zoompan=z='min(zoom+0.0012,1.10)':d=48:s=1920x1080:fps=24,"
      f"drawtext=fontfile={FB}:textfile=y{pos}.txt:x=70:y=70:fontsize=54:fontcolor=0xE8D7B0:shadowcolor=black@0.85:shadowx=3:shadowy=3,"
      f"drawtext=fontfile={FR}:textfile=c{pos}.txt:x=w-tw-70:y=82:fontsize=24:fontcolor=0x9EC9F0@0.8:shadowcolor=black@0.85:shadowx=2:shadowy=2,"
      f"drawtext=fontfile={FB}:textfile=t{pos}.txt:x=70:y=h-92:fontsize=34:fontcolor=white@0.94:shadowcolor=black@0.9:shadowx=3:shadowy=3,"
      "fade=t=in:st=0:d=0.10,fade=t=out:st=1.88:d=0.12")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-loop','1','-i',f"p{pos:02d}.png",
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v','-map','1:a',
      '-frames:v','48','-vf',vf,'-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-c:a','aac','-b:a','128k','-shortest',out,'-y'],check=True)
print('STILLSDONE')
