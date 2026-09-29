#!/usr/bin/env python3
"""House bed synth (audible voicing): 55 Hz drone with harmonics 2..12, slow breathing,
struck 528 Hz bell at hooks, soft 990 Hz tick at ticks, low thud at exits.
Usage: housebed.py out.wav DURATION [--hooks 1.9,16.9] [--ticks 8.6] [--thuds 14.5] [--base 55]
"""
import sys, argparse, numpy as np
from scipy.io import wavfile

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('dur', type=float)
ap.add_argument('--hooks', default=''); ap.add_argument('--ticks', default=''); ap.add_argument('--thuds', default='')
ap.add_argument('--base', type=float, default=55.0)
ap.add_argument('--fadein', type=float, default=0.5); ap.add_argument('--fadeout', type=float, default=1.2)
a = ap.parse_args()
SR = 48000
N = int(round(a.dur * SR))
t = np.arange(N) / SR
lst = lambda s: [float(v) for v in s.split(',') if v.strip()]

# --- drone: two slightly detuned voices, harmonics weighted for small speakers
w = {1: 1.0, 2: 0.45, 3: 0.90, 4: 0.85, 5: 0.65, 6: 0.55, 7: 0.35, 8: 0.40, 9: 0.22, 10: 0.25, 11: 0.12, 12: 0.18}
def voice(f0, phase):
    s = np.zeros(N)
    for n, g in w.items():
        s += g * np.sin(2 * np.pi * f0 * n * t + phase * n)
    return s
drone = voice(a.base, 0.0) + 0.7 * voice(a.base * 2 ** (4 / 1200), 1.3)   # +4 cents beating
drone *= 0.775 + 0.225 * np.sin(2 * np.pi * 0.07 * t + 0.4)                 # breathing
drone /= np.abs(drone).max()

# --- events
def place(sig_fn, when, gain):
    out = np.zeros(N)
    for w0 in when:
        i = int(w0 * SR)
        if i >= N: continue
        seg = sig_fn(t[: N - i])
        out[i:i + len(seg)] += gain * seg
    return out

def bell(tt):
    parts = [(1.0, 1.0, 2.4), (2.0, 0.55, 1.6), (2.71, 0.40, 1.1), (3.0, 0.28, 0.9), (4.2, 0.18, 0.6)]
    s = np.zeros_like(tt)
    for r, g, tau in parts:
        s += g * np.sin(2 * np.pi * 528 * r * tt) * np.exp(-tt / tau)
    s *= np.minimum(1, tt / 0.006)                       # 6 ms strike
    return s / np.abs(s).max()

def tick(tt):
    s = np.sin(2 * np.pi * 990 * tt) * np.exp(-tt / 0.07) + 0.4 * np.sin(2 * np.pi * 1320 * tt) * np.exp(-tt / 0.04)
    return s / np.abs(s).max()

def thud(tt):
    s = np.sin(2 * np.pi * 110 * tt) * np.exp(-tt / 0.35) + 0.5 * np.sin(2 * np.pi * 165 * tt) * np.exp(-tt / 0.25)
    s *= np.minimum(1, tt / 0.01)
    return s / np.abs(s).max()

mix = 0.55 * drone + place(bell, lst(a.hooks), 0.9) + place(tick, lst(a.ticks), 0.5) + place(thud, lst(a.thuds), 0.7)

# --- fades
fi = int(a.fadein * SR); fo = int(a.fadeout * SR)
env = np.ones(N)
env[:fi] = np.linspace(0, 1, fi)
env[N - fo:] = np.linspace(1, 0, fo)
mix *= env

# --- gentle stereo width: delayed copies
def delay(x, ms):
    k = int(SR * ms / 1000); return np.concatenate([np.zeros(k), x[:-k]])
L = mix + 0.25 * delay(mix, 9)
R = mix + 0.25 * delay(mix, 14)
y = np.stack([L, R], axis=1)
y = y / (np.abs(y).max() + 1e-9) * 0.891
wavfile.write(a.out, SR, (y * 32767).astype(np.int16))
print(f"wrote {a.out} {a.dur}s hooks={a.hooks} ticks={a.ticks} thuds={a.thuds}")
