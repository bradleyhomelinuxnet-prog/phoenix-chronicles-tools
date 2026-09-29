import json, subprocess, glob, numpy as np, scipy.signal as sg
from scipy.io import wavfile
from scipy.ndimage import maximum_filter1d
SR=48000; TOTAL=183.0; N=int(TOTAL*SR)
def rd(p):
    sr,x=wavfile.read(p); x=x.astype(np.float32)/32768
    if x.ndim==1: x=np.stack([x,x],1)
    if sr!=SR: x=sg.resample_poly(x,SR,sr,axis=0).astype(np.float32)
    return x
def place(buf,sig,t0,g=1.0):
    i=int(round(t0*SR)); j=min(N,i+len(sig)); buf[i:j]+=g*sig[:j-i]
bed=rd('bed183.wav')[:N]
tex=np.zeros((N,2),np.float32); voice=np.zeros((N,2),np.float32)
st=json.load(open('/home/claude/rem-machine/src/data/stations.json'))['lanes'][0]['stations']
U='/mnt/user-data/uploads/Desktop/Chronotecture-Charts_Update_v1/'
lp=sg.butter(4,5200,'low',fs=SR,output='sos'); hp=sg.butter(2,90,'high',fs=SR,output='sos')
for i,s in enumerate(st):
    t0=3+15*i
    src=glob.glob(U+f"hf_*_{s['clip']}*.mp4")[0]
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i',src,'-vn','-ac','2','-ar',str(SR),'tmp.wav'],check=True)
    a=rd('tmp.wav'); a=sg.sosfiltfilt(lp,a,axis=0).astype(np.float32)
    a=a*(0.035/(np.sqrt(np.mean(a**2))+1e-9))
    L=len(a); k=int(0.8*SR); env=np.ones(L,np.float32); env[:k]=np.linspace(0,1,k); env[-k:]=np.linspace(1,0,k)
    a*=env[:,None]
    place(tex,a,t0+0.2); place(tex,a,t0+0.2+L/SR-0.8)      # the clip's own sound, twice, as it plays there and back
    n=int(s['id'][1:])
    for key,tt in (('N',s['voice']['nIn']),('R',s['voice']['rIn'])):
        v=rd(f'/home/claude/cs/vtrim/S{n:02d}_{key}.wav')[:,0]
        v=sg.sosfiltfilt(hp,v).astype(np.float32)
        place(voice,np.stack([v,v],1),t0+tt)
voice=np.tanh(voice*1.15)/np.tanh(1.15)
env=maximum_filter1d(np.abs(voice[:,0]),size=int(0.06*SR))
rel=np.exp(-1/(0.40*SR)); g=sg.lfilter([1-rel],[1,-rel],env).astype(np.float32)
g=np.minimum(1.0,g/0.08); gain=(1.0-0.58*g).astype(np.float32)
mix=(bed*0.9+tex)*gain[:,None]+voice
mix=mix/(np.abs(mix).max()+1e-9)*0.891
wavfile.write('mix.wav',SR,(mix*32767).astype(np.int16))
subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-i','mix.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-ar',str(SR),'-c:a','aac','-b:a','192k','mix.m4a'],check=True)
print('mix.m4a ok')
