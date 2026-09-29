# Giza II · The Long Count — Flood Chain look (138.000 s)

The validated sheet `station-sheets/Ere-We-Were_Giza-138-II_Station-Sheet_v1.txt` rendered in the Flood Chain
house look: no footage, the code-drawn ember ground, orange titles, rolling year + AM, QUICK FACT mid-right,
Natori/Rogue captions, CHECK line, station rail; axis card at station 5. 3 s title + 9 × 15 s = 4,140 frames.

- Voices: ElevenLabs `eleven_multilingual_v2`, Sarah (Natori) and Chris R. Glass (Rogue), one take per line,
  trimmed and levelled; measured spans in `timing.json` drive both the captions and the mix.
- `render.sh` renders the `Giza` composition muted; `mix.py` lays the voices on a 138 s house bed, ducked,
  `loudnorm I=-16` (−16.2 LUFS; −16.8 on the laptop test).
- The engine only draws the side shades when a station has footage, so the ember ground stays clean.
