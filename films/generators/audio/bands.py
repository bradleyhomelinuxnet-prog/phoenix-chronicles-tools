import sys, numpy as np, subprocess, scipy.signal as sg
from scipy.io import wavfile
def load(p):
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',p,'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','/home/claude/audiofix/_a.wav'],check=True)
    sr,x=wavfile.read('/home/claude/audiofix/_a.wav'); return sr, x.astype(np.float64)/32768
for p in sys.argv[1:]:
    sr,x=load(p)
    f,P=sg.welch(x,sr,nperseg=8192)
    def band(a,b): 
        m=(f>=a)&(f<b); return P[m].sum()
    tot=P.sum()
    cen=(f*P).sum()/tot
    print(f"{p.split('/')[-1]:45s} centroid {cen:6.0f} Hz | <150:{100*band(0,150)/tot:5.1f}%  150-800:{100*band(150,800)/tot:5.1f}%  800-4k:{100*band(800,4000)/tot:5.1f}%  >4k:{100*band(4000,24000)/tot:5.1f}%  peak {20*np.log10(np.abs(x).max()+1e-9):5.1f} dBFS")
