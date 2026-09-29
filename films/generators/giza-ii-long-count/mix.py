import json, subprocess, numpy as np, scipy.signal as sg
from scipy.io import wavfile
from scipy.ndimage import maximum_filter1d
SR=48000; N=int(138.0*SR)
def rd(p):
    sr,x=wavfile.read(p); x=x.astype(np.float32)/32768
    if x.ndim>1: x=x.mean(1)
    if sr!=SR: x=sg.resample_poly(x,SR,sr).astype(np.float32)
    return x
bed=rd('bed138.wav')[:N]; voice=np.zeros(N,np.float32)
tm=json.load(open('/home/claude/giza2/timing.json')); hp=sg.butter(2,90,'high',fs=SR,output='sos')
for k in range(1,10):
    t0=3+15*(k-1)
    for key,tt in (('N',tm[str(k)]['nIn']),('R',tm[str(k)]['rIn'])):
        v=sg.sosfiltfilt(hp,rd(f'/home/claude/giza2/vtrim/S{k:02d}_{key}.wav')).astype(np.float32)
        v*=0.1/(np.sqrt(np.mean(v**2))+1e-9)
        i=int(round((t0+tt)*SR)); j=min(N,i+len(v)); voice[i:j]+=v[:j-i]
voice=np.tanh(voice*1.15)/np.tanh(1.15)
env=maximum_filter1d(np.abs(voice),size=int(0.06*SR)); rel=np.exp(-1/(0.40*SR))
g=np.minimum(1.0,sg.lfilter([1-rel],[1,-rel],env)/0.08); gain=(1.0-0.58*g).astype(np.float32)
mix=bed*0.9*gain+voice; mix=np.stack([mix,mix],1); mix=mix/(np.abs(mix).max()+1e-9)*0.891
wavfile.write('mix.wav',SR,(mix*32767).astype(np.int16))
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i','mix.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar','48000','-c:a','aac','-b:a','192k','mix.m4a'],check=True)
print('ok')
