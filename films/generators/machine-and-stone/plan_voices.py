#!/usr/bin/env python3
"""Trim, fit and level the 50 lines; write timing.json (station-local seconds) and vtrim/*.wav"""
import re, json, subprocess, numpy as np, os
from scipy.io import wavfile
SR = 48000
VD = '/home/claude/cs/voices'; VT = '/home/claude/cs/vtrim'; os.makedirs(VT, exist_ok=True)
N_IN, N_MAX = 2.6, 6.0          # Natori window
R_MIN_IN, R_END = 9.2, 18.2     # Rogue may start at 9.2 or 0.45 s after Natori; must end by 18.2
def run(a): subprocess.run(a, check=True)
def load(name, max_len):
    src = f'{VD}/{name}.mp3'; tmp = f'{VT}/{name}.wav'
    run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR),
         '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,'
                'areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse',
         '-c:a', 'pcm_s16le', tmp])
    sr, x = wavfile.read(tmp); x = x.astype(np.float64) / 32768
    dur = len(x) / SR
    if dur > max_len:
        tempo = min(1.12, dur / max_len)
        run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', tmp, '-af', f'atempo={tempo:.4f}', '-c:a', 'pcm_s16le', tmp + '.t.wav'])
        sr, x = wavfile.read(tmp + '.t.wav'); x = x.astype(np.float64) / 32768
        os.replace(tmp + '.t.wav', tmp)
    voiced = x[np.abs(x) > 0.02]
    rms = np.sqrt(np.mean(voiced ** 2)) if len(voiced) else 1.0
    x = np.clip(x * (0.1 / (rms + 1e-9)), -0.98, 0.98)
    wavfile.write(tmp, SR, (x * 32767).astype(np.int16))
    return len(x) / SR
timing = {}
for n in range(1, 26):
    nd = load(f'S{n:02d}_N', N_MAX)
    n0, n1 = N_IN, N_IN + nd
    r0 = max(R_MIN_IN, n1 + 0.45)
    rd = load(f'S{n:02d}_R', max(2.5, R_END - r0))
    r1 = r0 + rd
    timing[str(n)] = {'N': [round(n0, 2), round(n1, 2)], 'R': [round(r0, 2), round(r1, 2)]}
    flag = ' <-- late' if r1 > 18.3 else ''
    print(f'S{n:02d}  N {n0:5.2f}-{n1:5.2f}  R {r0:5.2f}-{r1:5.2f}{flag}')
json.dump(timing, open('/home/claude/cs/timing.json', 'w'), indent=1)
