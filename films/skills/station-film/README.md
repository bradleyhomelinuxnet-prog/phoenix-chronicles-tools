# station-film

A format for making short documentary films about contested material — and a
checker that refuses to let a broken one reach a render.

**Zero dependencies.** One Python file, standard library only. No install, no
package manager, no API key, nothing to subscribe to.

## What it is

Your film is **N stations of equal length** plus a title card. Each station makes
one claim, grounds it in one checkable fact, speaks it in two voices, and prints
**where the source and the mainstream record disagree**.

That last line is the point:

```
CLAIM   Fold the 7,344 years in half and the centre lands on Megiddo
CHECK   The arithmetic holds (no year zero) · the Battle of Megiddo is
        usually dated 1457 or 1479 BC, not 1567.
```

The claim survives at full strength. So does the viewer's ability to judge it.

## Why a checker

Renders are slow and expensive. A sheet that does not add up should cost you a
text file, not an overnight encode. `validate_sheet.py` enforces:

- the declared duration and frame count actually agree
- every station is present and numbered
- every station carries TITLE, CLAIM, FACT, two voices, CHECK and CLIP
- **CHECK is never missing and never empty** — a sheet that asserts without
  checking is refused
- mirror indices are consistent, if the sheet uses them

## Install

Drop the folder so `SKILL.md` sits directly inside it:

```
~/.claude/skills/station-film/SKILL.md
```

On Windows that is `C:\Users\<you>\.claude\skills\station-film\SKILL.md`.

Extracting the zip usually leaves you one level too deep
(`station-film/station-film/SKILL.md`) — check that before anything else.

## Verify the install

```
python3 tools/validate_sheet.py --selftest
```

This builds a known-good sheet, breaks it eight ways, and asserts the right
complaint comes back each time. It touches no files and needs no network. A
validator nobody has watched fail is indistinguishable from one that always
passes, so run this before trusting a result.

Then check it against the worked example:

```
python3 tools/validate_sheet.py examples/giza-ii-station-sheet.txt
```

Expect `sheet holds`.

## Use

1. Write a station sheet as plain text — see `reference/SHEET-FORMAT.md`.
2. `python3 tools/validate_sheet.py your-sheet.txt`
3. Fix what it says.
4. Only then bind clips, record voices, and render.

`--json` gives machine-readable output for a build pipeline. Exit code is 0 when
the sheet holds, 1 when it does not, so it drops straight into CI or a Makefile.

## What is deliberately not here

The **look** — fonts, palette, plates, lower-thirds, the grade. That is a brand
pack, and keeping it separate is what lets this format serve a production that
looks nothing like the example.

`examples/giza-ii-station-sheet.txt` is a complete, validated sheet from a
finished film: 9 stations, 138.000 s, palindromic span. Read it before writing
your first.
