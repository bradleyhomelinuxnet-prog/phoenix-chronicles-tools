import json, os, subprocess
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
M=json.load(open('/home/claude/tx/meta.json')); order=json.load(open('/home/claude/full/order.json'))
def sp(k):
    for b in ('/home/claude/src','/mnt/user-data/uploads/PlanetWalker'):
        p=os.path.join(b,k)
        if os.path.exists(p): return p
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
S=[(1,"YEAR ONE.\nAGAIN.","Genesis calls it the beginning.\nIt isn’t. It’s a reboot.","V1_YearOneAgain"),
   (11,"NO BODY.\nNO INSCRIPTION.","9,068 inches a side.\nLevel within two centimetres.\nOnly numbers.","V2_OnlyNumbers"),
   (19,"EVERY CYCLE\nSOMEONE DIGS OUT","and calls it history.","V3_DigsOut"),
   (27,"HALFWAY\nTO WHAT?","1135 BC. Atlantis goes under,\nthe Bronze Age ends.\n“Look back.”","V4_HalfwayToWhat"),
   (52,"26° 31′","three hundred forty-five feet\nthrough solid rock.","V5_SolidRock"),
   (59,"THE PYRAMID READS\nITS OWN NUMBER","Year 6,000. The count closes.\nThen what? Year one. Again.","V6_ReadsItsOwnNumber")]
for n,(idx,big,sub,name) in enumerate(S,1):
    k=order[idx-1]; v=M[k]
    wr(f"b{n}.txt",big); wr(f"s{n}.txt",sub); wr(f"h{n}.txt",(v['am']+"  ·  " if v['am'] else "")+v['yr'])
    fc=("[0:v]split=2[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.18[b];"
        "[fg]scale=1080:-2[f];[b][f]overlay=(W-w)/2:(H-h)/2[c];"
        f"[c]drawtext=fontfile={FR}:textfile=h{n}.txt:x=(w-text_w)/2:y=150:fontsize=32:fontcolor=0xE8D7B0@0.8:shadowcolor=black@0.85:shadowx=2:shadowy=2,"
        f"drawtext=fontfile={FB}:textfile=b{n}.txt:x=(w-text_w)/2:y=1300:fontsize=68:line_spacing=12:fontcolor=0xE8D7B0:shadowcolor=black@0.9:shadowx=3:shadowy=3:enable=between(t\\,0.5\\,14.6),"
        f"drawtext=fontfile={FR}:textfile=s{n}.txt:x=(w-text_w)/2:y=1500:fontsize=40:line_spacing=12:fontcolor=white:shadowcolor=black@0.9:shadowx=3:shadowy=3:enable=between(t\\,1.8\\,14.6)[v]")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-i',sp(k),'-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000',
      '-filter_complex',fc,'-map','[v]','-map','0:a','-frames:v','360',
      '-c:v','libx264','-crf','21','-preset','veryfast','-pix_fmt','yuv420p','-r','24',
      '-af','loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=0.3,afade=t=out:st=14.6:d=0.4,aresample=48000',
      '-c:a','aac','-b:a','160k','-t','15',f"{name}_9x16.mp4",'-y'],check=True)
    print(name,flush=True)
print('VDONE')
