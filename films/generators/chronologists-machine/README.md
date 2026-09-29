# The Chronologist's Machine — 3:03

*Ere We Were* in the Proof-45s style: the twelve Cinema Studio event shots of 28 September 2026 in chart order,
5239 BC → 2040 AD, voiced by Natori (Sarah) and Rogue (Chris R. Glass). 3 s title + 12 × 15 s = 183 s = 3:03.

| file | what |
|---|---|
| `src/` | the Remotion engine (same as `../ere-we-were-remotion`), with a `MACHINE` lane, per-station voice timing (`voice.nIn/nOut/rIn/rOut`, measured from the takes) and side shades so the title and quick fact read on bright plates |
| `build_lane.py` | writes `src/data/stations.json` from the *Machine and the Stone* sheet (stations 1–12) with trimmed quick facts |
| `render.sh` | renders the `Machine` composition, muted |
| `mix.py` | the soundtrack: house bed (bell at every hook), each clip's own sound, the 24 voice lines, ducked, `loudnorm I=-16` |

Clips: `public/clips/M01–M12.mp4`, each 7 s shot played forward then back, stretched to 15 s.
Measured: −16.6 LUFS, −17.5 on the laptop test (high-pass 200 Hz). 5,490 frames at 30 fps.
