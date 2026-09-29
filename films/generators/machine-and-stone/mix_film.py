#!/usr/bin/env python3
"""Master audio for THE MACHINE AND THE STONE (511 s): bed + clip textures + 50 voices, ducked, loudnormed; mux."""
import json, subprocess, os, numpy as np, scipy.signal as sg
from scipy.io import wavfile
SR = 48000; TOTAL = 511.0; N = int(TOTAL * SR)
CS = '/home/claude/cs'
def rd(p):
    sr, x = wavfile.read(p); x = x.astype(np.float64) / 32768
    if x.ndim == 1: x = np.stack([x, x], axis=1)
    return x
def place(buf, sig, t0, gain=1.0):
    i = int(round(t0 * SR)); j = min(N, i + len(sig))
    if sig.ndim == 1: sig = np.stack([sig, sig], axis=1)
    buf[i:j] += gain * sig[:j - i]

bed = rd(f'{CS}/bed511.wav')[:N]
tex = np.zeros((N, 2)); voice = np.zeros((N, 2))
timing = json.load(open(f'{CS}/timing.json'))
lp = sg.butter(4, 5200, 'low', fs=SR, output='sos')
for n in range(1, 26):
    t0 = 36 + 19 * (n - 1)
    ap = f'{CS}/aud/S{n:02d}.wav'
    if os.path.exists(ap):                       # event clip texture: low-passed, quiet, faded in/out
        a = rd(ap)[:int(19 * SR)]
        a = sg.sosfiltfilt(lp, a, axis=0)
        rms = np.sqrt(np.mean(a ** 2)) + 1e-9
        a *= 0.03 / rms
        L = len(a); env = np.ones(L); k = int(0.8 * SR)
        env[:k] = np.linspace(0, 1, k); env[-k:] = np.linspace(1, 0, k)
        a *= env[:, None]
        place(tex, a, t0)
    for key in ('N', 'R'):
        v = rd(f'{CS}/vtrim/S{n:02d}_{key}.wav')[:, 0]
        v = sg.sosfiltfilt(sg.butter(2, 90, 'high', fs=SR, output='sos'), v)
        place(voice, v, t0 + timing[str(n)][key][0])
voice = np.tanh(voice * 1.15) / np.tanh(1.15)
# duck bed + textures under the voices
env = np.abs(voice[:, 0]); att, rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.40 * SR))
g = np.zeros(N); e = 0.0
for i in range(N):
    v = env[i]; e = v + att * (e - v) if v > e else v + rel * (e - v); g[i] = e
g = np.minimum(1.0, g / 0.08); gain = 1.0 - 0.58 * g
mix = (bed * 0.9 + tex) * gain[:, None] + voice
mix = mix / (np.abs(mix).max() + 1e-9) * 0.891
wavfile.write(f'{CS}/master_mix.wav', SR, (mix * 32767).astype(np.int16))
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', f'{CS}/master_mix.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                '-ar', str(SR), '-c:a', 'aac', '-b:a', '192k', f'{CS}/master.m4a'], check=True)
print('master.m4a written')
