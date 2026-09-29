#!/usr/bin/env python3
"""Harmonic enrichment for the sub-only synthesized beds.
Keeps the original sub drone + ticks exactly (timing untouched), adds a harmonic
layer (3rd..12th harmonics of the drone) so the bed is audible on laptop/phone
speakers.  Usage: enrich.py in.mp4 out_bed.wav [harm_gain] [tick_gain]
"""
import sys, subprocess, numpy as np, scipy.signal as sg
from scipy.io import wavfile

src, out = sys.argv[1], sys.argv[2]
HG = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0   # harmonic layer gain (rel. to drone RMS)
TG = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0   # extra gain on the >300 Hz tick band
SR = 48000
tmp = out + '.src.wav'
subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-vn', '-ac', '2', '-ar', str(SR),
                '-c:a', 'pcm_s16le', tmp], check=True)
sr, x = wavfile.read(tmp)
x = x.astype(np.float64) / 32768.0
if x.ndim == 1:
    x = np.stack([x, x], axis=1)
m = x.mean(axis=1)
N = len(m)

def sos(kind, fc, order=4):
    return sg.butter(order, fc, btype=kind, fs=SR, output='sos')

def process(m, tt):
    # 1) drone band (sub) and tick band
    d = sg.sosfiltfilt(sos('low', 160), m)
    t = sg.sosfiltfilt(sos('high', 300), m)

    # 2) envelope-flattened drone -> Chebyshev harmonics -> re-envelope
    env = np.abs(sg.hilbert(d))
    env = sg.sosfiltfilt(sos('low', 8, 2), env)          # smooth envelope (8 Hz)
    env = np.maximum(env, 0)
    peak = env.max() + 1e-9
    u = d / (env + 0.02 * peak)                          # ~unit-amplitude carrier
    u = np.clip(u, -1.0, 1.0)
    T = {1: u}
    T[2] = 2 * u * u - 1
    for n in range(3, 13):
        T[n] = 2 * u * T[n - 1] - T[n - 2]
    # weights favour 3rd..6th (165-330 Hz for a 55 Hz drone), taper to the 12th (660 Hz)
    w = {2: 0.35, 3: 0.90, 4: 0.85, 5: 0.65, 6: 0.55, 7: 0.35, 8: 0.40, 9: 0.22, 10: 0.25, 11: 0.12, 12: 0.18}
    h = sum(w[n] * T[n] for n in w)
    h = h * env                                           # follow the drone's own fades
    h = sg.sosfiltfilt(sos('high', 140), h)               # drop DC / fundamental leakage
    h = sg.sosfiltfilt(sos('low', 1600, 2), h)            # keep it warm
    # slow breathing on the harmonic layer (0.07 Hz), never below 55 %
    h = h * (0.775 + 0.225 * np.sin(2 * np.pi * 0.07 * tt))

    # 3) gain: harmonic RMS = HG x drone RMS
    rms = lambda a: np.sqrt(np.mean(a * a) + 1e-12)
    return h, d


# chunked (memory-safe for long pieces): 90 s chunks, 3 s overlap, linear crossfade
CH, OV = 90 * SR, 3 * SR
h = np.zeros(N); d = np.zeros(N)
pos = 0
while pos < N:
    a0 = max(0, pos - OV); a1 = min(N, pos + CH + OV)
    hh, dd = process(m[a0:a1], np.arange(a0, a1) / SR)
    # write region [pos, min(N,pos+CH)) with crossfade over the leading OV samples
    w0 = pos; w1 = min(N, pos + CH)
    seg_h = hh[w0 - a0:w1 - a0]; seg_d = dd[w0 - a0:w1 - a0]
    if pos > 0:
        n = min(OV, w1 - w0)
        ramp = np.linspace(0, 1, n)
        # previous pass already filled [pos, pos+OV) with its tail; blend
        h[w0:w0 + n] = h[w0:w0 + n] * (1 - ramp) + seg_h[:n] * ramp
        d[w0:w0 + n] = d[w0:w0 + n] * (1 - ramp) + seg_d[:n] * ramp
        h[w0 + n:w1] = seg_h[n:]; d[w0 + n:w1] = seg_d[n:]
    else:
        h[w0:w1] = seg_h; d[w0:w1] = seg_d
    # pre-fill the next overlap with this chunk's tail so the blend has something
    if w1 < N:
        e1 = min(N, w1 + OV)
        h[w1:e1] = hh[w1 - a0:e1 - a0]; d[w1:e1] = dd[w1 - a0:e1 - a0]
    pos += CH
t = sg.sosfiltfilt(sos('high', 300), m)
rms = lambda a: np.sqrt(np.mean(a * a) + 1e-12)
h = h * (HG * rms(d) / rms(h))
# 4) gentle stereo: delayed copies (11 ms / 17 ms) on L/R
def delay(a, ms):
    k = int(SR * ms / 1000)
    return np.concatenate([np.zeros(k), a[:-k]])
x[:, 0] += h + (TG - 1) * t; x[:, 0] += 0.35 * delay(h, 11)
x[:, 1] += h + (TG - 1) * t; x[:, 1] += 0.35 * delay(h, 17)
del t, d, m
x *= 0.891 / (np.abs(x).max() + 1e-9)                  # -1 dBFS peak; loudnorm comes after
wavfile.write(out, SR, (x * 32767).astype(np.int16))
y = x

f, P = sg.welch(y.mean(axis=1), SR, nperseg=8192)
tot = P.sum()
band = lambda a, b: 100 * P[(f >= a) & (f < b)].sum() / tot
print(f"{src.split('/')[-1]}: centroid {(f*P).sum()/tot:.0f} Hz | <150 {band(0,150):.1f}%  150-800 {band(150,800):.1f}%  800-4k {band(800,4000):.1f}%")
