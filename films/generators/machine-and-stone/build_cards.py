#!/usr/bin/env python3
"""Title card (17 s) and contract card (19 s) for THE MACHINE AND THE STONE."""
import subprocess, os
W, H, FPS = 1920, 1080, 24
FONT = '/home/claude/'
SERIF = FONT + 'CormorantGaramond-500-normal.ttf'; SERIFB = FONT + 'CormorantGaramond-700-normal.ttf'
SERIFI = FONT + 'CormorantGaramond-500-italic.ttf'; MONO = FONT + 'IBMPlexMono-400-normal.ttf'; MONOB = FONT + 'IBMPlexMono-600-normal.ttf'
C = dict(bone='0xefe4d3', bone2='0xd8cbb8', ash='0xa1927f', ember2='0xffb057', ice='0x8fd0ff', gold='0xe2c069')
TXT = '/home/claude/cs/txt'; OUT = '/home/claude/cs/out'; BG = '/home/claude/flood/bg.png'
def tf(name, text):
    p = f'{TXT}/{name}.txt'; open(p, 'w', encoding='utf-8').write(text); return p
def dt(textfile, font, size, color, x, y, t0, t1, fade=0.8, ls=10):
    a = (f"if(lt(t,{t0}),0,if(lt(t,{t0}+{fade}),(t-{t0})/{fade},if(lt(t,{t1}-{fade}),1,if(lt(t,{t1}),({t1}-t)/{fade},0))))")
    return (f"drawtext=textfile='{textfile}':fontfile='{font}':fontsize={size}:fontcolor={color}:x={x}:y={y}:"
            f"line_spacing={ls}:alpha='{a}'")
def card(name, dur, layers):
    vf = ','.join(layers) + f",fade=t=in:st=0:d=0.6,fade=t=out:st={dur-0.7}:d=0.7,format=yuv420p"
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-loop', '1', '-framerate', str(FPS), '-i', BG,
                    '-vf', vf, '-frames:v', str(int(dur * FPS)), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'medium',
                    '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', f'{OUT}/{name}.mp4'], check=True)
    fr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
                         'stream=nb_read_frames', '-of', 'csv=p=0', f'{OUT}/{name}.mp4'], capture_output=True, text=True).stdout.strip()
    print(name, fr, 'frames')

# ---- title, 17 s
T = 17.0
card('T', T, [
    dt(tf('t_a', 'ERE WE WERE'), MONOB, 22, C['ember2'], '(w-tw)/2', 300, 0.8, T - 0.6),
    dt(tf('t_b', 'THE MACHINE AND THE STONE'), SERIFB, 104, C['bone'], '(w-tw)/2', 350, 1.4, T - 0.6),
    dt(tf('t_c', 'twenty-five stations · 8:31'), SERIFI, 40, C['bone2'], '(w-tw)/2', 500, 2.6, T - 0.6),
    dt(tf('t_d', 'Everything on screen was rendered in Cinema Studio on the night of 28 September 2026.\n'
                 'Twelve fires. One axis. Twelve chambers. Nothing was generated for this film.'),
       SERIF, 30, C['ash'], '(w-tw)/2', 640, 4.6, T - 0.6, ls=12),
    dt(tf('t_e', 'NATORI · Sarah      ROGUE · Chris R. Glass'), MONO, 17, C['ash'], '(w-tw)/2', 780, 6.4, T - 0.6),
    dt(tf('t_f', '19138 · 83191 — reads the same returning'), MONO, 18, C['gold'], '(w-tw)/2', 960, 8.0, T - 0.6),
])
# ---- contract, 19 s
K = 19.0
card('K', K, [
    dt(tf('k_a', 'THE CONTRACT'), MONOB, 22, C['gold'], '(w-tw)/2', 150, 0.6, K - 0.6),
    dt(tf('k_b', 'Every station makes one claim, grounds it in one checkable fact,\n'
                 'speaks it in two voices, and prints where the source and the record disagree.'),
       SERIF, 40, C['bone'], '(w-tw)/2', 215, 1.2, K - 0.6, ls=14),
    dt(tf('k_c', 'MOVEMENT I · THE MACHINE'), MONOB, 19, C['ember2'], '(w-tw)/2', 420, 3.4, K - 0.6),
    dt(tf('k_d', 'twelve fires, 5239 BC to 2046 AD, in the order the chart keeps them'), SERIFI, 32, C['bone2'], '(w-tw)/2', 452, 3.6, K - 0.6),
    dt(tf('k_e', 'STATION 13 · THE AXIS'), MONOB, 19, C['gold'], '(w-tw)/2', 540, 5.0, K - 0.6),
    dt(tf('k_f', 'the shaft to the star: twelve fires behind it, twelve chambers ahead'), SERIFI, 32, C['bone2'], '(w-tw)/2', 572, 5.2, K - 0.6),
    dt(tf('k_g', 'MOVEMENT II · THE STONE'), MONOB, 19, C['ice'], '(w-tw)/2', 660, 6.6, K - 0.6),
    dt(tf('k_h', 'twelve chambers, out of the pyramid to the desert'), SERIFI, 32, C['bone2'], '(w-tw)/2', 692, 6.8, K - 0.6),
    dt(tf('k_i', 'Station k mirrors station 26 − k. Each clip plays forward, then backward. The last line returns the first.'),
       SERIF, 28, C['ash'], '(w-tw)/2', 820, 8.6, K - 0.6),
    dt(tf('k_j', '36 s cards + 25 × 19 s = 511.000 s = 12,264 frames at 24 fps · sheet validated before render'),
       MONO, 16, C['ash2' if 'ash2' in C else 'ash'], '(w-tw)/2', 960, 10.0, K - 0.6),
])
