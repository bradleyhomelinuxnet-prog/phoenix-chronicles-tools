import subprocess, os
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
A='0xE8D7B0'; B='0x9EC9F0'
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
def card(out,dur,lines):
    vf=[]
    for i,(txt,y,size,col,font) in enumerate(lines):
        wr(f"k_{out}_{i}.txt",txt)
        vf.append(f"drawtext=fontfile={font}:textfile=k_{out}_{i}.txt:x=(w-text_w)/2:y={y}:fontsize={size}:fontcolor={col}:alpha='min(1\\,min((t-0.35)/0.75\\,({dur-0.35}-t)/0.75))'")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-f','lavfi','-i',f'color=c=black:s=1920x1080:r=24:d={dur}',
      '-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=48000','-map','0:v','-map','1:a','-frames:v',str(int(dur*24)),
      '-vf',",".join(vf),'-c:v','libx264','-crf','20','-preset','veryfast','-pix_fmt','yuv420p','-r','24','-c:a','aac','-b:a','160k','-shortest',f"{out}.mp4",'-y'],check=True)
def flick(out, slots, secs, bells):
    wr(f"l_{out}.txt","\n".join(f"file '{s}'" for s in slots)+"\n")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-f','concat','-safe','0','-i',f"l_{out}.txt",'-c','copy',f"b_{out}.mp4",'-y'],check=True)
    ins=['-i',f"b_{out}.mp4"]; fc=["[0:a]volume=1[m]"]; mixes=["[m]"]
    for n,t in enumerate(bells,1):
        ins+=['-i','/home/claude/reeld/b2/bell.wav']
        fc.append(f"[{n}:a]adelay={int(t*1000)}|{int(t*1000)},volume=0.75[b{n}]"); mixes.append(f"[b{n}]")
    fc.append("".join(mixes)+f"amix=inputs={len(bells)+1}:normalize=0,alimiter=limit=0.95,atrim=0:{secs},asetpts=N/SR/TB[a]")
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error']+ins+['-filter_complex',";".join(fc),
      '-map','0:v','-map','[a]','-t',str(secs),'-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',f"{out}.mp4",'-y'],check=True)
    nf=subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=nb_frames','-of','csv=p=0',f"{out}.mp4"],capture_output=True,text=True).stdout.strip()
    print(out, nf, 'expect', secs*24, 'OK' if nf.startswith(str(secs*24)) else 'MISMATCH', flush=True)
F=lambda n: f"F{n:02d}.mp4"
# ---- 8:31 palindrome on the Phoenix nodes, axis = THE AXIS -------------------
out16=[5,6,7,8,12,14,16,17,18,19,20,21,22,23,24,25]
card('PX_T',8,[("LIVE ON TIME · EMIT NO EVIL",370,25,A+"@0.6",FR),("SIXTEEN OUT, SIXTEEN BACK",440,62,A,FB),
  ("the axis of the palindrome is the axis of the chronology",535,25,A+"@0.5",FR),("AM 2760  ·  1135 BC  ·  138 × 20",600,28,B+"@0.85",FR)])
card('PX_E',8,[("it returns to the first fire",460,34,A+"@0.85",FR),("8:31",530,64,B,FB)])
flick('LiveOnTime_SixteenOutSixteenBack_831_v1',
  ['PX_T.mp4']+[F(n) for n in out16]+[F(27)]+[F(n) for n in reversed(out16)]+['PX_E.mp4'], 511, [0.2, 503.0])
# ---- themed cuts -------------------------------------------------------------
def themed(out, title, sub, idxs, secs):
    cd=8 if secs==98 else 4
    lines=[("LIVE ON TIME · EMIT NO EVIL",400,25,A+"@0.6",FR)] if cd==8 else []
    lines+=[(title,470 if cd==8 else 480,66,A,FB),(sub,575 if cd==8 else 580,25,A+"@0.5",FR)]
    card(f"C_{out}",cd,lines)
    flick(out, [f"C_{out}.mp4"]+[F(n) for n in idxs], secs, [0.2])
themed('LiveOnTime_TheFloods_138_v1','THE FLOODS','the water remembers what the calendar forgot',[3,5,9,18,19,22],98)
themed('LiveOnTime_TheDarkSuns_138_v1','THE DARK SUNS','six times the light went wrong',[17,21,31,34,37,40],98)
themed('LiveOnTime_TheClockBuilders_119_v1','THE CLOCK BUILDERS','who cut the stone and why they counted',[2,7,8,10,16],79)
themed('LiveOnTime_DragonsTheyWrote_119_v1','DRAGONS, THEY WROTE','what people put in the record when the sky moved',[30,39,41,42,45],79)
