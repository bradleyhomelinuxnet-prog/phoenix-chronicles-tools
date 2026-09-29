# Station sheet — field reference

One record per station. Fields are `KEY` + two-or-more spaces + value.

| field | required | what it carries |
|---|---|---|
| `TITLE` | yes | The on-screen title. Two to four words. It is a name, not a summary. |
| `CLAIM` | yes | What the source asserts, at full strength. Do not hedge it here — the CHECK line does that job. |
| `FACT` | yes | Something independently checkable, with figures. A distance, a date, a count, a measurement. If you cannot verify it, it belongs in CLAIM. |
| *voice lines* | 2+ | Spoken dialogue, labelled by speaker. Label names are free; the validator reads them from the sheet. |
| `CHECK` | yes | Where the source and the record diverge. Must name something falsifiable: a competing date, a measured figure, a named authority. |
| `CLIP` | yes | The asset binding, or an explicit note that no footage exists yet. An empty value fails. |

## Header line

    H<nn> · STATION <i>/<N> · mirror <N+1-i> · <anchor> · <subject>

`mirror` is optional. When present it is checked.

## Shape line

    Shape: <t> s title + <N> × <M> s = <F> frames at <R> fps

Checked two ways: `t + N×M` against the declared total, and `total × fps`
against the frame count.

## Readability

Every line is measured against the time it is on screen at ~17 characters per
second. `FACT` and `CHECK` are persistent, so they get the whole station; the
voice lines are captions timed to speech, so they share it.

At 15 s per station with two voices that is roughly **255 characters** for
`FACT` or `CHECK` and **127** for each voice line. Over budget is a warning,
not an error — but a caption nobody can finish reading is not on screen in any
useful sense.

## Closing register

End the sheet with the divergences collected, and the arithmetic restated:

    WHERE THE TALK AND THE RECORD DIFFER
    • <one line per divergence>
    • Arithmetic checked: <the sums, written out>

This is not decoration. It is the reason a viewer can trust the rest.
