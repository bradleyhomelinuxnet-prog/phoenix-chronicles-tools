# Changelog

## 1.1.0

- **Captions are required, and measured.** Every fact appears on screen as text;
  every spoken word is captioned. `validate_sheet.py` now warns when a line
  cannot be read in the time it is shown, at ~17 characters per second, with
  `--rate=` to change the assumption.
- `FACT` and `CHECK` are budgeted against the whole station (persistent text);
  voice lines against their share of it (captions timed to speech).

## 1.0.0

First release.

- The station-sheet format: fixed-length stations, two voices, and a required
  CHECK line naming where the source and the record diverge.
- `tools/validate_sheet.py` — arithmetic, station count, required fields, mirror
  indices. Exit 0 / 1, `--json` for pipelines.
- `--selftest` proves the checker catches its eight failure classes on the
  machine it is installed on.
- `examples/giza-ii-station-sheet.txt` — a complete sheet from a finished film.
