#!/usr/bin/env python3
"""Lay Natori/Rogue lines onto a station film over its bed, duck the bed under speech,
loudnorm, remux (video copied).  Usage:
  voicemix.py video.mp4 bed.wav out.mp4 START:ID [START:ID ...]
CLOCK per station: natoriIn 2.4, rogueIn 8.6 (or after Natori), speech must end by 14.4.
"""
import sys, subprocess, numpy as np, scipy.signal as sg
from scipy.io import wavfile

video, bedp, out = sys.argv[1], sys.argv[2], sys.argv[3]
stations = [(float(a.split(':')[0]), a.split(':')[1]) for a in sys.argv[4:]]
SR = 48000
VD = '/home/claude/voices'

def run(a): subprocess.run(a, check=True)

def load_voice(name, max_len):
    """trim silence, fit into max_len seconds (atempo <= 1.12), return float mono @48k"""
    src = f'{VD}/{name}.mp3'; tmp = f'{VD}/_{name}.wav'
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
    # equalise the two voices: every line to the same RMS (-20 dBFS over its voiced samples)
    voiced = x[np.abs(x) > 0.02]
    rms = np.sqrt(np.mean(voiced ** 2)) if len(voiced) else 1.0
    x = x * (0.1 / (rms + 1e-9))
    x = np.clip(x, -0.98, 0.98)
    return x

# bed
sr, bed = wavfile.read(bedp); bed = bed.astype(np.float64) / 32768
if bed.ndim == 1: bed = np.stack([bed, bed], axis=1)
N = len(bed)
voice = np.zeros(N)
log = []
for start, sid in stations:
    n = load_voice(f'{sid}_N', 5.9)
    n_in = start + 2.4
    n_end = n_in + len(n) / SR
    r_in = max(start + 8.6, n_end + 0.35)
    r = load_voice(f'{sid}_R', max(3.0, (start + 14.4) - r_in))
    r_end = r_in + len(r) / SR
    for sig, t0 in ((n, n_in), (r, r_in)):
        i = int(round(t0 * SR)); j = min(N, i + len(sig))
        voice[i:j] += sig[:j - i]
    log.append(f'{sid}: N {n_in:5.2f}-{n_end:5.2f} ({len(n)/SR:.2f}s)  R {r_in:5.2f}-{r_end:5.2f} ({len(r)/SR:.2f}s)')

# voice polish: gentle high-pass, soft limiter
voice = sg.sosfiltfilt(sg.butter(2, 90, 'high', fs=SR, output='sos'), voice)
voice = np.tanh(voice * 1.15) / np.tanh(1.15)
# duck: envelope of voice -> bed gain 1.0 -> 0.42 (-7.5 dB), 60 ms attack / 400 ms release
env = np.abs(voice)
att, rel = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.40 * SR))
g = np.zeros(N); e = 0.0
for i in range(N):                       # slow in numpy but N <= 80 s * 48k = 3.8M -> fine
    v = env[i]
    e = v + att * (e - v) if v > e else v + rel * (e - v)
    g[i] = e
g = np.minimum(1.0, g / 0.08)             # full duck once the voice is above ~-22 dBFS
gain = 1.0 - 0.58 * g
mix = bed * gain[:, None] + 1.0 * np.stack([voice, voice], axis=1)
mix = mix / (np.abs(mix).max() + 1e-9) * 0.891
wavfile.write(out + '.mix.wav', SR, (mix * 32767).astype(np.int16))
run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', out + '.mix.wav', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
     '-ar', str(SR), '-c:a', 'aac', '-b:a', '192k', out + '.m4a'])
run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', video, '-i', out + '.m4a', '-map', '0:v:0', '-map', '1:a:0',
     '-c:v', 'copy', '-c:a', 'copy', '-shortest', '-movflags', '+faststart', out])
print('\n'.join(log))
