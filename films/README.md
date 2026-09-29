# Phoenix Chronicles — production paper, 28–29 September 2026

The written side of the walker films (*LIVE ON TIME · EMIT NO EVIL*), the *Ere We Were* station films, and *The Chronologist's Machine*. No video lives here — the films are on the Desktop and in the Higgsfield account; every clip named in these files is one `curl` away by the CDN pattern in `docs/PlanetWalker_NOTES_v1.txt`.

| folder | what |
|---|---|
| `docs/` | The two-day handoff and ledger (`Phoenix-Chronicles_Handoff_2026-09-29_v1.md`), the running production notes, the Ere-We-Were handoff, the Giza feature production flow, the Reel D cutting script |
| `station-sheets/` | Validated station sheets: *Giza II — The Long Count* (9 × 15 s = 138 s) and *The Machine and the Stone* (25 × 19 s + 36 s = 511 s = 8:31) |
| `skills/station-film/` | The station-film skill (v1.1.0): the format, the sheet reference, the validator, a worked example. `python3 tools/validate_sheet.py --selftest` |
| `data/` | Every spoken line in the 59-clip walker archive, timed (`AllClips_Transcripts_v2.json`), the chyrons, the 25 Cinema Studio generations of 28 Sep with ids/prompts/URLs, and the voice timing for *The Machine and the Stone* |
| `generators/` | The scripts that made the films — kept so a change is a re-run, never a rebuild by hand: the walk-clip-captioner pipeline (transcribe → speaker by pitch → captions → assemblies), the audio fixes (harmonic enrichment, house bed, voice mix), the Machine-and-Stone build, and the Remotion source for the Ere-We-Were engine with the QUICK FACT layer |

Standing arithmetic: AM 1 = 3895 BC · AD = AM − 3894 · 138 × 12 = 1,656 (the Flood) · 138 × 20 = 2,760 (the axis, 1135 BC) · 138 × 42 = 5,796 (1902) · 138 × 43 = 5,934 (2040) · 5239 + 2106 − 1 = 7,344.

The Capstone fork (AM 6000 = 2106 AD vs the spine's AM 6072 = 2178 AD) is unruled; nothing here takes a side.

*19138 · 83191 — reads the same returning.*
