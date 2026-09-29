#!/usr/bin/env python3
"""THE MACHINE AND THE STONE — station plates + text layers.
Reads the validated sheet, builds one 19.000 s (456-frame) station file per record with the
Ere-We-Were brand pack burned in, plus the two opening cards.  Audio is NOT here (see mix step):
each station also writes its clip-texture audio (event clips only) to aud/Sxx.wav.
"""
import re, os, subprocess, json, textwrap, sys
W, H, FPS = 1920, 1080, 24
PH = 823                      # 21:9 plate height
PY = (H - PH) // 2            # 128
DUR = 19.0; FR = 456
FONT = '/home/claude/'
SERIF = FONT + 'CormorantGaramond-500-normal.ttf'
SERIFB = FONT + 'CormorantGaramond-700-normal.ttf'
SERIFI = FONT + 'CormorantGaramond-500-italic.ttf'
MONO = FONT + 'IBMPlexMono-400-normal.ttf'
MONOB = FONT + 'IBMPlexMono-600-normal.ttf'
C = dict(obsidian='0x15100c', bone='0xefe4d3', bone2='0xd8cbb8', ash='0xa1927f', ash2='0x6f6355',
         ember='0xf2701d', ember2='0xffb057', ice='0x8fd0ff', gold='0xe2c069')
OUT = '/home/claude/cs/out'; TXT = '/home/claude/cs/txt'; AUD = '/home/claude/cs/aud'
for d in (OUT, TXT, AUD): os.makedirs(d, exist_ok=True)

# ---------------- sheet ----------------
sheet = open('/home/claude/cs/MachineAndStone_Station-Sheet_v1.txt', encoding='utf-8').read().splitlines()
stations = []; cur = None
for ln in sheet:
    m = re.match(r'^H(\d+)\s*·\s*STATION\s+(\d+)/(\d+)\s*·\s*mirror\s+(\d+)\s*·\s*(.*)$', ln.strip())
    if m:
        cur = {'n': int(m.group(2)), 'mirror': int(m.group(4)), 'rest': m.group(5).strip(), 'f': {}}
        stations.append(cur); continue
    if cur is None: continue
    f = re.match(r'^([A-Z][A-Z0-9_]{2,15})\s{2,}(.*)$', ln)
    if f: cur['f'][f.group(1)] = f.group(2).strip()
assert len(stations) == 25

def wrap(s, n): return '\n'.join(textwrap.wrap(s, n))
def tf(name, text):
    p = f'{TXT}/{name}.txt'; open(p, 'w', encoding='utf-8').write(text); return p
def dt(textfile, font, size, color, x, y, t0, t1, fade=0.5, box=False, line_spacing=8, shadow=True):
    a = (f"if(lt(t,{t0}),0,if(lt(t,{t0}+{fade}),(t-{t0})/{fade},"
         f"if(lt(t,{t1}-{fade}),1,if(lt(t,{t1}),({t1}-t)/{fade},0))))")
    s = (f"drawtext=textfile='{textfile}':fontfile='{font}':fontsize={size}:fontcolor={color}:"
         f"x={x}:y={y}:line_spacing={line_spacing}:alpha='{a}'")
    if shadow: s += ":shadowcolor=black@0.7:shadowx=0:shadowy=2"
    if box: s += ":box=1:boxcolor=black@0.45:boxborderw=14"
    return s

def station_filters(st):
    n = st['n']; f = st['f']
    machine = n <= 12; axis = n == 13
    lane = C['gold'] if axis else (C['ember2'] if machine else C['ice'])
    mv = 'AXIS' if axis else ('MOVEMENT I · THE MACHINE' if machine else 'MOVEMENT II · THE STONE')
    label = f"H{n:02d} · STATION {n} / 25 · MIRROR {st['mirror']}"
    anchor = st['rest'].upper()
    L = []
    # top bar
    L.append(dt(tf(f's{n:02d}_lab', label), MONOB, 20, C['ash'], 72, 24, 0.0, DUR, 0.4, shadow=False))
    L.append(dt(tf(f's{n:02d}_mv', mv), MONO, 17, lane, 72, 92, 0.0, DUR, 0.4, shadow=False))
    L.append(dt(tf(f's{n:02d}_anc', anchor), MONOB, 20, lane, f'w-tw-72', 24, 0.0, DUR, 0.4, shadow=False))
    L.append(dt(tf(f's{n:02d}_ttl', f['TITLE']), SERIFB, 54, C['bone'], 72, 44, 0.3, DUR, 0.6, shadow=False))
    # claim — top-left of the plate, 0.6 → 6.5
    L.append(dt(tf(f's{n:02d}_clm', wrap(f['CLAIM'], 62)), SERIFI, 34, C['bone2'], 96, PY + 34, 0.6, 6.5, 0.6, line_spacing=6))
    # fact — mid-right panel, right-aligned, 3.0 → 18.0
    fact = wrap(f['FACT'], 44)
    L.append(dt(tf(f's{n:02d}_fl', 'FACT'), MONOB, 17, lane, 'w-tw-72', 380, 3.0, 18.0, 0.5, shadow=False))
    for i, line in enumerate(fact.split('\n')):          # one drawtext per line = true right alignment
        L.append(dt(tf(f's{n:02d}_fct{i}', line), SERIF, 30, C['bone2'], 'w-tw-72', 408 + i * 42, 3.2 + i * 0.05, 18.0, 0.6))
    # check — lower-left of the plate, 6.5 → 18.4
    chk = wrap(f['CHECK'], 74)
    nlines = chk.count('\n') + 1
    cy = PY + PH - 28 - (nlines * 34) - 30
    L.append(dt(tf(f's{n:02d}_ckl', 'CHECK'), MONOB, 17, C['gold'], 96, cy - 4, 6.5, 18.4, 0.5, shadow=False))
    L.append(dt(tf(f's{n:02d}_chk', chk), SERIF, 26, C['bone'], 96, cy + 22, 6.7, 18.4, 0.6, line_spacing=6, box=True))
    return L, lane

def caption_filters(st, timing):
    """timing: dict N=(t0,t1), R=(t0,t1) — from the mix step's placement"""
    n = st['n']; f = st['f']; L = []
    for sp, key, col in (('NATORI', 'N', C['ember2']), ('ROGUE', 'R', C['ice'])):
        t0, t1 = timing[key]
        cap = wrap(f[sp], 60)
        two = '\n' in cap
        ybase = H - 128 + (18 if two else 36)
        L.append(dt(tf(f's{n:02d}_{key}lab', sp), MONOB, 17, col, '(w-tw)/2', ybase, t0 - 0.15, t1 + 0.3, 0.25, shadow=False))
        L.append(dt(tf(f's{n:02d}_{key}cap', cap), SERIF, 34, C['bone'], '(w-tw)/2', ybase + 24, t0 - 0.15, t1 + 0.3, 0.25, line_spacing=4))
    return L

def plate_chain(clip, kind):
    """returns (video filter for the plate, audio filter or None)"""
    if kind == 'event':
        v = ("[0:v]trim=end_frame=168,setpts=PTS-STARTPTS[a];[0:v]trim=end_frame=168,reverse,setpts=PTS-STARTPTS[b];"
             "[0:v]trim=end_frame=120,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0,")
        a = ("[0:a]atrim=end=7.0,asetpts=PTS-STARTPTS[x];[0:a]atrim=end=7.0,areverse,asetpts=PTS-STARTPTS[y];"
             "[0:a]atrim=end=5.0,asetpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=0:a=1")
    elif kind == 'flood':
        v = ("[0:v]trim=end_frame=144,setpts=PTS-STARTPTS[a];[0:v]trim=end_frame=144,reverse,setpts=PTS-STARTPTS[b];"
             "[0:v]trim=end_frame=144,setpts=PTS-STARTPTS[c];[0:v]trim=end_frame=24,reverse,setpts=PTS-STARTPTS[d];"
             "[a][b][c][d]concat=n=4:v=1:a=0,")
        a = ("[0:a]atrim=end=6.0,asetpts=PTS-STARTPTS[x];[0:a]atrim=end=6.0,areverse,asetpts=PTS-STARTPTS[y];"
             "[0:a]atrim=end=6.0,asetpts=PTS-STARTPTS[z];[0:a]atrim=end=1.0,areverse,asetpts=PTS-STARTPTS[w];"
             "[x][y][z][w]concat=n=4:v=0:a=1")
    else:  # giza 10 s: fwd 240 + rev 216
        v = ("[0:v]trim=end_frame=240,setpts=PTS-STARTPTS[a];[0:v]trim=end_frame=216,reverse,setpts=PTS-STARTPTS[b];"
             "[a][b]concat=n=2:v=1:a=0,crop=1280:549:0:85,")
        a = None
    v += f"scale={W}:{PH}:flags=lanczos,pad={W}:{H}:0:{PY}:color={C['obsidian']},fps={FPS},format=yuv420p"
    return v, a

CLIPS = {}
for g in json.load(open('/home/claude/cs/cinema_studio_gens.json')):
    CLIPS[g['short']] = g

def build_station(st, timing):
    n = st['n']
    short = st['f']['CLIP'].split(' ')[0]
    g = CLIPS[short]
    kind = 'flood' if short == '8786f10c' else ('event' if g['model'].endswith('3_5') else 'giza')
    src = f'/home/claude/cs/clips/{short}.mp4'
    vchain, achain = plate_chain(src, kind)
    layers, lane = station_filters(st)
    layers += caption_filters(st, timing)
    vf = vchain + ',' + ','.join(layers)
    out = f'{OUT}/S{n:02d}.mp4'
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-filter_complex', vf, '-an',
           '-frames:v', str(FR), '-r', str(FPS), '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
           '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    if achain:
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-i', src, '-filter_complex', achain,
                        '-t', str(DUR), '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', f'{AUD}/S{n:02d}.wav'], check=True)
    fr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames', '-show_entries',
                         'stream=nb_read_frames', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.strip()
    return out, fr

if __name__ == '__main__':
    timing = json.load(open('/home/claude/cs/timing.json'))   # from the mix planner
    which = [int(a) for a in sys.argv[1:]] or list(range(1, 26))
    for st in stations:
        if st['n'] in which:
            out, fr = build_station(st, timing[str(st['n'])])
            print(f'S{st["n"]:02d} {fr} frames', flush=True)
