---
name: station-film
metadata:
  version: 1.1.0
description: >
  Build a short documentary film as a fixed-length "station sheet" — N stations of
  equal duration, each with a claim, a checkable fact, two narrator lines, and a
  CHECK line naming where the source and the mainstream record disagree. Use when
  someone wants to make an explainer, chronology, timeline, or documentary short
  from contested or fringe source material and wants it to hold up: dating claims,
  historical revision, health or finance claims, true crime, anything where the
  source asserts more than the record supports. Also use to review, validate or
  fix an existing station sheet. Produces a text sheet that is checked before a
  single frame renders.
---

# Station film

A format for covering contested material honestly, and a contract that fails
loudly when it does not hold.

The film is **N stations of equal length**, each a fixed number of seconds, plus
a title card. Every station makes one claim, grounds it in one checkable fact,
speaks it in two voices, and then — this is the part that matters — **says on
screen where the source and the record disagree.**

You write the sheet. You validate the sheet. Only then does anything render.

## Why the CHECK line exists

Most treatments of fringe material pick a side. Credulous ones repeat the claim;
debunking ones never let the claim breathe. Both are boring, and both leave the
viewer unable to check anything.

A station sheet does neither. It states the claim at full strength, then prints
the divergence:

    CLAIM   Fold the 7,344 years in half and the centre lands on Megiddo
    CHECK   The arithmetic holds (no year zero) · the Battle of Megiddo is
            usually dated 1457 or 1479 BC, not 1567.

The claim survives. So does the viewer's ability to judge it. A sheet whose
stations assert but never check is a different kind of film, and
`validate_sheet.py` refuses to pass it.

**Every CHECK line must name something falsifiable** — a competing date, a
measured figure, a discipline's consensus, a named scholar. "Some dispute this"
is not a CHECK line.

## The contract

The first lines of the sheet declare its shape:

    <TITLE> · <total> s · station sheet v<n>
    Shape: <t> s title + <N> × <M> s = <F> frames at <R> fps

That is an arithmetic claim, and it is checked. `t + N×M` must equal the stated
total, and `total × fps` must equal the frame count. Renders are slow and
expensive; a duration that does not add up should cost you a text file, not an
overnight encode.

Landing the total on a number that means something to the work is optional but
encouraged — it gives the edit somewhere to absorb slack.

## The station record

```
H01 · STATION 1/9 · mirror 9 · <era or anchor> · <location or subject>
TITLE   <on-screen title, 2–4 words>
CLAIM   <what the source asserts, stated at full strength>
FACT    <something independently checkable, with figures>
<VOICE-A>  <spoken line>
<VOICE-B>  <spoken line>
CHECK   <where the source and the record differ — falsifiable, named>
CLIP    <asset id, or a note that none exists yet>
```

Speaker labels are read from the sheet, so name your voices whatever the project
needs. The validator warns if a station has fewer than two.

Two voices are the format's engine: one carries the claim, the other carries the
consequence or the doubt. One voice flattens into narration.

## Captions are not optional

**Every fact appears on screen as text. Every spoken word is captioned.**

Not a style preference — the format does not work without it:

- Most social video autoplays **muted**. A claim only spoken is a claim most
  viewers never receive.
- Speech is mis-heard, and proper nouns worst of all. A viewer who mishears a
  date cannot look it up.
- A `CHECK` line that is only narrated cannot be checked. The whole point of
  this format is that a viewer can weigh the claim against the record, and
  weighing needs reading.

The layers are different and must not compete:

| layer | what it is | how long it has |
|---|---|---|
| `FACT`, `CHECK` | persistent on-screen text — plate, lower-third, panel | the whole station |
| voice lines | captions timed to speech | their share of the station |

`validate_sheet.py` measures each line against the time it is on screen at
~17 characters per second, and warns when a line cannot be read in that window.
`--rate=` changes the assumption; a lower number is a stricter, slower reader.

Measured on a real 9-station sheet, every individual line fits and **all four
together exceed the budget in every station** — which is precisely why `FACT`
and `CHECK` must dwell rather than flash, and why the voice captions cannot
carry the numbers on their own.

**Caption from a transcript, never from the script.** Generated dialogue drifts
from its prompt, and timings estimated from the script sit visibly wrong against
the mouths. Transcribe the rendered audio and time the captions to that.

## The mirror (optional)

If the sheet uses `mirror k`, station *i* must carry mirror *N+1−i*, and the
middle station is the axis. This makes the *span* the structure — the first and
last stations answer each other, and the centre is a real midpoint you can
verify by arithmetic. The validator enforces the indices, because an off-by-one
here is invisible by eye and destroys the claim.

Skip it if the material has no natural symmetry. Do not fake one.

## Workflow

1. **Gather the source.** A talk, a book chapter, a paper. Note every numeric
   claim — those become FACT and CHECK lines.
2. **Write the sheet** as plain text. Prose costs nothing to change; frames do.
3. **Check every number yourself.** The footer of the sheet should restate the
   arithmetic so a reader can follow it: `5239 + 2106 − 1 = 7,344 (no year zero)`.
   If you cannot verify it, it does not go in FACT — it goes in CLAIM.
4. **Validate:** `python3 tools/validate_sheet.py <sheet>.txt`. Fix what it says.
5. **Collect the divergences** into a closing register, so the film's honesty is
   auditable in one place.
6. **Only now** bind clips, record voices, and render.

## What is not in this skill

The look — fonts, palette, plate layout, lower-thirds, the grade — is a **brand
pack**, not part of the format. A station sheet renders in any house style. Keep
them separate; that is what lets the same format serve a different production.

`examples/giza-ii-station-sheet.txt` is a complete, validated sheet from a real
film: 9 stations, 138.000 s, palindromic span. Read it before writing your first.
