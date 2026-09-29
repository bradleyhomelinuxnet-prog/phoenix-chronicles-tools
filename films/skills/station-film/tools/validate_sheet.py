#!/usr/bin/env python3
"""
Validate a station sheet before anything is rendered.

A station sheet is a contract: a fixed frame count, a fixed number of stations,
and a required set of fields on each one. Rendering is expensive and slow, so
every error this can catch on a text file is an error that does not cost a
render. It reads one sheet and exits non-zero if the sheet does not hold.

    python3 validate_sheet.py path/to/sheet.txt
    python3 validate_sheet.py path/to/sheet.txt --json
    python3 validate_sheet.py --selftest      # prove the tool works here

WHAT IT ENFORCES, AND WHY EACH ONE

  Arithmetic     The header declares `3 s title + N x M s = F frames at R fps`.
                 If those do not agree the film cannot land on its stated
                 duration, and you find out after the render instead of before.

  Station count  The header says N. The body must contain N stations, numbered
                 1..N with no gaps. A dropped station is silent otherwise.

  Required fields  Every station carries TITLE, CLAIM, FACT, two speaker lines,
                 CHECK and CLIP. A station missing one still renders; it just
                 renders wrong, or renders a claim with nothing behind it.

  CHECK          The load-bearing one. CHECK is where the source and the record
                 disagree, written on screen. A sheet whose stations assert but
                 never check is a different kind of film, and this refuses to
                 call it this format. Empty CHECK lines fail.

  Mirror index   If the sheet uses mirrors, station i must carry mirror N+1-i.
                 The palindrome is a structural claim; an off-by-one breaks it
                 and is invisible by eye.

  Readable       Every fact has to be READ, not just heard. Most social video
                 autoplays muted, speech is mis-heard, and a CHECK line nobody
                 can read is a CHECK line that does no work. So each line is
                 measured against the time it is on screen at a standard
                 subtitle reading rate (~17 characters per second).

                 The budgets differ because the layers differ. FACT and CHECK
                 are persistent on-screen text and get the whole station. The
                 voice lines are captions timed to speech, so they share the
                 station between them. Measured on a real 9-station sheet every
                 line fits, while all four together do not -- which is exactly
                 why they cannot all be competing captions.

The speaker names, the field order and the station count are all read FROM the
sheet. Nothing here is specific to one production.
"""

import json
import re
import sys
from pathlib import Path

REQUIRED = ['TITLE', 'CLAIM', 'FACT', 'CHECK', 'CLIP']

# Characters per second a viewer can comfortably read. 17 is the common
# broadcast subtitle rate for adults; --rate overrides it.
READING_RATE = 17
STATION_RE = re.compile(
    r'^H(?P<h>\d+)\s*[·|]\s*STATION\s+(?P<n>\d+)\s*/\s*(?P<of>\d+)'
    r'(?:\s*[·|]\s*mirror\s+(?P<mirror>\d+))?'
    r'(?:\s*[·|]\s*(?P<rest>.*))?$'
)
# "3 s title + 9 x 15 s = 4,140 frames at 30 fps" — separators and the
# multiplication sign vary by keyboard, so accept the usual ones.
SHAPE_RE = re.compile(
    r'(?P<title>[\d.]+)\s*s\s+title\s*\+\s*(?P<n>\d+)\s*[x×]\s*(?P<each>[\d.]+)\s*s'
    r'\s*=\s*(?P<frames>[\d,]+)\s*frames\s+at\s+(?P<fps>[\d.]+)\s*fps',
    re.I,
)
TOTAL_RE = re.compile(r'(?P<total>[\d.]+)\s*s\s*[·|]\s*station sheet', re.I)


def parse(text):
    lines = text.splitlines()
    sheet = {'shape': None, 'declared_total': None, 'stations': [], 'speakers': set()}

    for ln in lines:
        if sheet['shape'] is None:
            m = SHAPE_RE.search(ln)
            if m:
                sheet['shape'] = {
                    'title_s': float(m.group('title')),
                    'n': int(m.group('n')),
                    'each_s': float(m.group('each')),
                    'frames': int(m.group('frames').replace(',', '')),
                    'fps': float(m.group('fps')),
                }
        if sheet['declared_total'] is None:
            m = TOTAL_RE.search(ln)
            if m:
                sheet['declared_total'] = float(m.group('total'))

    current = None
    for ln in lines:
        m = STATION_RE.match(ln.strip())
        if m:
            current = {
                'n': int(m.group('n')),
                'of': int(m.group('of')),
                'mirror': int(m.group('mirror')) if m.group('mirror') else None,
                'header': ln.strip(),
                'fields': {},
            }
            sheet['stations'].append(current)
            continue
        if current is None:
            continue
        f = re.match(r'^([A-Z][A-Z0-9_]{2,15})\s{2,}(.*)$', ln)
        if f:
            key, val = f.group(1), f.group(2).strip()
            current['fields'][key] = val
            if key not in REQUIRED:
                sheet['speakers'].add(key)
    return sheet


def check(sheet, rate=READING_RATE):
    errs, warns = [], []
    shape = sheet['shape']

    if not shape:
        errs.append('no shape line found — expected "<t> s title + <N> x <M> s = <F> frames at <R> fps"')
    else:
        n, each, title_s = shape['n'], shape['each_s'], shape['title_s']
        computed = title_s + n * each
        if sheet['declared_total'] is not None and abs(computed - sheet['declared_total']) > 1e-6:
            errs.append(
                f"duration does not add up: {title_s:g} + {n}x{each:g} = {computed:g}s, "
                f"but the sheet is titled {sheet['declared_total']:g}s"
            )
        expected_frames = round(computed * shape['fps'])
        if expected_frames != shape['frames']:
            errs.append(
                f"frame count does not match: {computed:g}s x {shape['fps']:g}fps = "
                f"{expected_frames} frames, sheet says {shape['frames']}"
            )
        if len(sheet['stations']) != n:
            errs.append(f"header declares {n} stations, body contains {len(sheet['stations'])}")

    seen = set()
    for st in sheet['stations']:
        tag = f"station {st['n']}"
        if st['n'] in seen:
            errs.append(f'{tag}: duplicated')
        seen.add(st['n'])

        for key in REQUIRED:
            if key not in st['fields']:
                errs.append(f'{tag}: missing {key}')
            elif not st['fields'][key]:
                errs.append(f'{tag}: {key} is empty')

        spoken = [k for k in st['fields'] if k not in REQUIRED]
        if len(spoken) < 2:
            warns.append(f'{tag}: {len(spoken)} speaker line(s); this format expects two voices')

        # Readability. On-screen text that cannot be read in the time it is
        # shown is not on screen in any useful sense.
        if shape:
            each = shape['each_s']
            spoken_n = max(len(spoken), 1)
            for key in ('FACT', 'CHECK'):
                val = st['fields'].get(key, '')
                budget = int(rate * each)
                if len(val) > budget:
                    warns.append(
                        f'{tag}: {key} is {len(val)} chars, over the {budget} readable '
                        f'in {each:g}s at {rate}/sec — shorten it or it cannot be read'
                    )
            voice_budget = int(rate * each / spoken_n)
            for key in spoken:
                val = st['fields'][key]
                if len(val) > voice_budget:
                    warns.append(
                        f'{tag}: {key} is {len(val)} chars, over the {voice_budget} one of '
                        f'{spoken_n} voices can caption in {each:g}s'
                    )

        if st['mirror'] is not None and shape:
            want = shape['n'] + 1 - st['n']
            if st['mirror'] != want:
                errs.append(f"{tag}: mirror is {st['mirror']}, should be {want}")

    if shape:
        missing = sorted(set(range(1, shape['n'] + 1)) - seen)
        if missing:
            errs.append(f"stations absent from the body: {missing}")

    return errs, warns


MINIMAL = """DEMO \u00b7 33.0 s \u00b7 station sheet v1
Shape: 3 s title + 2 \u00d7 15 s = 990 frames at 30 fps

==============================================================================
H01 \u00b7 STATION 1/2 \u00b7 mirror 2 \u00b7 anchor \u00b7 subject
TITLE   FIRST
CLAIM   the source says a thing
FACT    a checkable figure, 12 units
VOICEA  a spoken line
VOICEB  another spoken line
CHECK   the record says 14 units, not 12
CLIP    asset-1
==============================================================================
H02 \u00b7 STATION 2/2 \u00b7 mirror 1 \u00b7 anchor \u00b7 subject
TITLE   SECOND
CLAIM   the source says another thing
FACT    a second checkable figure
VOICEA  a spoken line
VOICEB  another spoken line
CHECK   named authority dates it otherwise
CLIP    asset-2
==============================================================================
"""


def selftest():
    """
    Prove this tool catches what it claims to, on THIS machine, with no files.

    A validator nobody has seen fail is indistinguishable from one that always
    passes. This builds a known-good sheet, breaks it four ways, and asserts the
    right complaint comes back each time. Run it after install, before trusting
    any result.
    """
    cases = [
        ('a good sheet passes', MINIMAL, None),
        ('a missing CHECK is caught',
         MINIMAL.replace('CHECK   the record says 14 units, not 12\n', ''),
         'missing CHECK'),
        ('an empty CHECK is caught',
         MINIMAL.replace('CHECK   the record says 14 units, not 12', 'CHECK   '),
         'CHECK is empty'),
        ('durations that do not add up are caught',
         MINIMAL.replace('2 \u00d7 15 s', '2 \u00d7 16 s'),
         'does not add up'),
        ('a wrong frame count is caught',
         MINIMAL.replace('= 990 frames', '= 991 frames'),
         'frame count does not match'),
        ('a bad mirror index is caught',
         MINIMAL.replace('STATION 1/2 \u00b7 mirror 2', 'STATION 1/2 \u00b7 mirror 1'),
         'mirror is 1, should be 2'),
        ('a dropped station is caught',
         MINIMAL.split('H02')[0],
         'body contains 1'),
    ]

    failures = 0
    for name, text, want in cases:
        errs, warns = check(parse(text))
        if want is None:
            ok = not errs
            detail = '; '.join(errs) if errs else 'clean'
        else:
            ok = any(want in e for e in errs)
            detail = '; '.join(errs) or 'no error raised'
        print(f"  {'ok  ' if ok else 'FAIL'}  {name}" + ('' if ok else f'  -> {detail}'))
        failures += 0 if ok else 1

    # the warning path, checked separately so a silent regression shows
    _, warns = check(parse(MINIMAL.replace('VOICEB  another spoken line\n', '', 1)))
    ok = any('speaker line' in w for w in warns)
    print(f"  {'ok  ' if ok else 'FAIL'}  a single-voice station warns")
    failures += 0 if ok else 1

    print()
    if failures:
        print(f'{failures} self-test(s) FAILED — do not trust this install')
        return 1
    print('self-test passed — the validator catches what it claims to')
    return 0


def main():
    if '--selftest' in sys.argv:
        print('station-film validator self-test')
        return selftest()

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    as_json = '--json' in sys.argv
    rate = READING_RATE
    for a in sys.argv[1:]:
        if a.startswith('--rate='):
            rate = float(a.split('=', 1)[1])
    if not args:
        print(__doc__.strip().splitlines()[0])
        print('usage: validate_sheet.py <sheet.txt> [--json] [--rate=17] | --selftest')
        return 2

    path = Path(args[0])
    sheet = parse(path.read_text(encoding='utf-8'))
    errs, warns = check(sheet, rate)

    if as_json:
        print(json.dumps({
            'sheet': str(path), 'shape': sheet['shape'],
            'stations': len(sheet['stations']),
            'speakers': sorted(sheet['speakers']),
            'errors': errs, 'warnings': warns,
        }, indent=2))
        return 1 if errs else 0

    s = sheet['shape']
    print(f'sheet   {path.name}')
    if s:
        print(f"shape   {s['title_s']:g}s title + {s['n']} x {s['each_s']:g}s "
              f"= {s['frames']} frames at {s['fps']:g}fps")
    print(f"voices  {', '.join(sorted(sheet['speakers'])) or '(none found)'}")
    print(f"read    {len(sheet['stations'])} stations")
    for w in warns:
        print(f'  warn  {w}')
    for e in errs:
        print(f'  FAIL  {e}')
    print('\nsheet holds' if not errs else f'\n{len(errs)} problem(s) — fix before rendering')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
