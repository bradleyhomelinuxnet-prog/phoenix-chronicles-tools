# ERE WE WERE — HANDOFF TO FABLE
**Reel IV evidence-card template · quick-fact extension · manuscript-aligned fact library**
Prepared 28 Sep 2026 · zero Higgsfield credits spent to date on this template

---

## 0. READ THIS FIRST — three corrections to likely assumptions

1. **This is not a Higgsfield preset and not an ffmpeg build.** The proof was rendered by a
   **Remotion 4.0.529** React project. The captions, counter, ribbon and previz ground are all
   code. Higgsfield only supplies footage that *later* drops in behind the text.
   No Ere We Were clips have been generated yet — the proof runs on a code-drawn background.
2. **A generator already exists. Do not rebuild it.** Edit the Remotion project and re-render.
3. **The walker films are the proven work and the house standard.** Bee's words, 28 Sep:
   *"the walker films are the best thing we've done - that works."* Ere We Were is the
   **information** register; the walker films are the **narrative** register. Do not replace
   one with the other. See §7.

## 0a. STATUS — 29 Sep, Fable's first pass. Most of §5 is done.

| # | Task | State |
|---|---|---|
| 1 | Layer 9 QUICK FACT in `StationScene.tsx` | **DONE** — live at 4.6–9.0 s, right 72 / top 392 / max 620, `text-wrap: balance` |
| 2 | `fact?: string` on the Station type; `CLOCK.fact` in `theme.ts` | **DONE** |
| 3 | 57 facts written from the anchors + manuscripts, every number checked | **DONE** — all 12–22 words |
| 4 | 45 s proof re-rendered with layer 9 | **DONE** — `outputs\Ere-We-Were_Proof-45s_v2_QuickFact.mp4`, 1350 frames |
| 5 | Full lane | not yet |
| + | Lane length generalised (`n = laneStations.length`) so a show can have any station count | **DONE** — 19 was hardcoded in four places |
| + | **New lane: FLOOD** (ember) — F01 2239 / F02 1687 / F03 1135 / F04 583 BC | **DONE** — `outputs\EreWeWere_TheFloodChain_119_v1.mp4`, 79.000 s, 2370 frames |

The engine on Bee's machine (`OMG2\remotion\src\`) has all of it. `stations.json` now holds 61 stations in 4 lanes.

**Rendering here works:** `REMOTION_BROWSER=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`.
The full Chrome refuses old-headless; the headless shell is fine. **Render stations one at a time** (`Station` composition with `--props='{"id":"E02"}'`, ~90 s each). The `Walk`/`Series` compositions hang after the first station in this sandbox — three stations stalled at 14 MB of pre-encode for six minutes. Concat the singles afterwards **with the concat filter, not the demuxer**: Remotion's parts are timebase 1/90000 and ffmpeg cards are 1/15360, and the demuxer + `-c copy` produced a file where only 407 of 2370 frames decoded. Verify with `-count_frames`.

---

## 1. WHERE EVERYTHING LIVES

| What | Path |
|---|---|
| Engine (canonical) | `CoWorkOS\WORK AREAS\Phoenix-Chronicles\ere-we-were-project\outputs\Ere-We-Were_Remotion_v1.zip` |
| Engine (unpacked, identical) | `Desktop\OMG2\remotion\` |
| The proof Bee approved | `Desktop\Ere-We-Were_Proof-45s_v1.mp4` — 1920×1080, **30 fps**, 1350 frames, 45.000 s, **no audio** |
| Style guide / anatomy | `Desktop\Rogue Proof.html` — every rule, pulled from source |
| Station data | `remotion\src\data\stations.json` — 419 KB, **57 stations in 3 lanes of 19** |
| Fill-in sheet | project `outputs\Rogue-Proof_Fill-In-Sheet_v1.txt` |
| Fonts (self-hosted) | `remotion\public\fonts\` — Cormorant Garamond 500/600/700, IBM Plex Mono 400/500/600 |
| Footage drop | `remotion\public\clips\<STATION_ID>.mp4` replaces the previz ground |
| Voice drop | `remotion\public\audio\<STATION_ID>-natori.mp3` etc. |

Key source files: `StationScene.tsx` (all 8 layers), `theme.ts` (palette + clock),
`data.ts` (types + Annus Mundi maths), `Walk.tsx`, `WalkField.tsx` (previz ground).

---

## 2. THE TEMPLATE AS BUILT — 8 layers on 1920×1080

| # | Layer | Type | Colour | Position | Timing |
|---|---|---|---|---|---|
| 1 | Eyebrow | Plex Mono 19 px, .20em; ID at 600 | ID lane colour, rest `ash` | left 72, top 54 | always |
| 2 | Counter | Cormorant 500 118 px tabular; sub Plex 20 px .18em | `bone`; sub `ash` | right 72, top 34, right-aligned | rolls prev year → this, 0–1.9 s |
| 3 | Title block | kicker italic 34 · title 700 76 px .03em · subtitle italic 30 | kicker/sub `bone2`; title lane colour | left 72, top 300, max 980 | fade + 18 px rise at 1.9 s |
| 4 | Captions | tag Plex 18 .22em · line Cormorant 44 px / 1.22 | tag speaker colour; line `bone` | centred, bottom 210, max 1320 | types on word by word |
| 5 | Check line | Plex 18 px / 1.45 | label `bone2`, text `ash` | left 72, bottom 132, max 1500 | in 9.0–9.5, out 13.8–14.5 |
| 6 | Clock bar | 4 px track, 12 px ticks | track white 8 %, fill lane 90 % | left/right 72, bottom 96 | fills across station |
| 7 | Station ribbon | Plex 12.5 px .08em, one cell per station | now lane+glow, mirror `bone2`, rest `ash2` | left/right 72, bottom 40 | always |
| 8 | Previz ground | SVG grid, red body, 46 embers | `obsidian` field | full frame under vignette | until `clips/ID.mp4` exists |

**Palette (`theme.ts`)** — obsidian `#15100c` · obsidian2 `#1c1510` · panel `#231a14` ·
line `#3b2d24` · bone `#efe4d3` · bone2 `#d8cbb8` · ash `#a1927f` · ash2 `#6f6355` ·
ember `#f2701d` · ember2 `#ffb057` · ice `#8fd0ff` · ice2 `#77a8dd` · gold `#e2c069` · red `#8d1a1a`
**Lanes** — EVIDENCE = ice · CHRONICON = ember2 · CIPHER = gold
**Speakers** — NATORI = ember2 · ROGUE = ice

**The 15-second clock (`CLOCK` in theme.ts)** — 450 frames at 30 fps:
`hook 1.9 · natori 2.4–7.8 · rogue 8.6–13.6 · speechDone 13.8 · exit 14.5 · out 15.0`

---

## 3. THE NEW LAYER — 9 · QUICK FACT

Bee's ask: *"putting up a 'quick fact' maybe 'mid right' of the flick … a quick fact that
pops up right centered justified."*

**Why mid-right works:** the title block occupies x 72–1052 / y 300–450. The counter
occupies y 34–150 on the right. The band **x 1100–1848, y 380–700 is empty in every
station.** That is the only large free area on the canvas and it is on the correct side
for right-aligned type. A mockup over a real frame (station E02) is attached as
`QuickFact_Mockup_v1.png` — it collides with nothing.

### Spec

| Property | Value |
|---|---|
| Anchor | `position:absolute; right:72; top:392; maxWidth:620; textAlign:'right'` |
| Hairline | 200 px × 1 px, right-aligned at `top:392`, lane colour at 40 % |
| Label | `QUICK FACT` — Plex Mono 600, 17 px, letterSpacing `.22em`, **lane colour**, at `top:408` |
| Fact | Cormorant Garamond 500, **34 px**, lineHeight **1.32**, `bone2`, right-aligned, from `top:446` |
| Motion | opacity 0→1 over 0.4 s **and** translateY 14→0 (ease-out quad). 14 px, not the title's 18 — it must read as subordinate. |
| In | **4.6 s** — during Natori's tail, so the eye has somewhere to go |
| Hold | through the inter-speaker silence at 7.8–8.6 s |
| Out | **8.6 → 9.0 s**, clearing the check line, which arrives at 9.0 |

### Code sketch (insert after the title block in `StationScene.tsx`)

```tsx
const factIn = interpolate(t, [4.6, 5.0, 8.6, 9.0], [0, 1, 1, 0],
  {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
const factY = interpolate(t, [4.6, 5.2], [14, 0],
  {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.quad)});
```
…then a right-aligned block using the table above, guarded by `station.fact &&`.

### Rules that keep it from ruining the frame
- **Max 22 words.** Beyond that it wraps to four lines and fights the title.
- **Never end on a one-word line.** The mockup's `on.` widow is the failure mode — balance
  the wrap or rewrite the sentence.
- **One fact per station.** It is punctuation, not a paragraph.
- **A number in every fact where one exists.** This layer is the data register.
- **If `station.fact` is empty the layer does not render.** No empty labels.

---

## 4. THE FACT LIBRARY — and the field it does *not* go in

`stations.json` already carries an **`anchor`** field, populated on all 57 stations and
**rendered nowhere**. Tempting, but wrong for this: anchors run **30–64 words (median 45)**.
That is three to five lines at 34 px.

**Add a new field `fact`, 12–22 words**, written *from* the anchor and from the two
manuscripts. Keep `anchor` as the research note behind it.

### Sources, and which is which
- **`CosmicMeasurements.docx`** — 36,777 words, 262 headings, 130 date-bearing paragraphs.
  **This is the evidence book.** Egyptology critique, the measurements, the 19/138 scripture
  work. *Primary source for facts.*
- **`PHOENIX-CODEX.docx`** — 143,632 words, 277 headings, 79 date-bearing paragraphs.
  **This is the novel** (chapters like *The Stranger in the Night*, *The Forest Hunters*).
  *Source for voice, the mirror architecture, and the Phoenix transit tables — not for
  "facts" presented as evidence.* Do not quote narrative prose as a quick fact.

### A worked example — and a caution
The Codex's own flood chain reads:
`2239 BC Great Flood · 1687 BC Ogygian · 1135 BC Phoenix Transit · 583 BC Thales`
Each gap is **552 years**, and **552 = 138 × 4**. In Annus Mundi those four are
**AM 1656 / 2208 / 2760 / 3312 = Phoenix 12 / 16 / 20 / 24** — every fourth node, exactly.
That is a first-rate quick fact.

**But** the Codex line beside 2239 BC reads *"138 × 16.22 from epoch"*, which is wrong —
AM 1656 is **138 × 12** exactly. The manuscripts contain arithmetic slips.
**Verify every number against `annusMundi()` in `data.ts` before it goes on screen.**
Conversion rule: AM 1 = 3895 BC; AD = AM − 3894.

---

## 5. WHAT TO BUILD, IN ORDER

1. **Add layer 9** to `StationScene.tsx` per §3. Render station E02 alone and compare to
   `QuickFact_Mockup_v1.png`.
2. **Add `fact` to the `Station` type** in `data.ts` and to the fill-in sheet block.
3. **Write 57 facts** — 19 EVIDENCE, 19 CHRONICON, 19 CIPHER — from the two manuscripts.
   Verify each number. Flag any that contradict the books.
4. **Re-render the 45 s proof** (E01–E03) and send it to Bee before doing the other 54.
5. **Then the full lane** — 19 × 15 s = 285 s.

### Durations Bee has standing orders on
Everything lands on **1:19–1:38 (79–98 s)** or exactly **8:31 (511 s)**, or a multiple of
138 (69 · 138 · 276 · 345 · 690 · 966). A 19-station lane at 285 s is **not** one of these —
either trim to 6 stations + cards for 1:38, or chain lanes toward 966. Verify by
**frame count, not container duration**: `frames == seconds × fps`.

---

## 6. VERIFICATION — non-negotiable

- Every station's AM ↔ calendar year through `annusMundi()`. The books slip.
- Frame counts on every render.
- The quick fact must not overlap the check line. Test at t = 8.9 and t = 9.1.
- At 30 fps, not 24. The walker films are 24; this template is 30. Do not mix in one file.

---

## 7. HOW THIS SITS BESIDE THE WALKER FILMS

The walker work is the approved standard and should not be disturbed. It lives at
`Desktop\PlanetWalker\` — 59 transcript-captioned clips, and the finished films
(`TheWholeWalk_966`, `TowardAndAway_831`, the 1:19/1:38 cuts, six 9:16 shorts).
Its own skill is saved as **`walk-clip-captioner`**.

| | Walker films | Ere We Were |
|---|---|---|
| Register | narrative — people talking | information — evidence on the record |
| Source | generated footage + its own transcribed audio | code-drawn cards, footage optional |
| Frame rate | 24 fps | 30 fps |
| Type | DejaVu, chyron-led | Cormorant + Plex, dossier-led |
| Built with | ffmpeg | Remotion |

**The obvious next move, once layer 9 is in:** Ere We Were stations make the *evidence*
inserts for a walker film — number first, then the scene. That grammar already exists and is
proven; it is `LiveOnTime_Annotated_119_v1` in `PlanetWalker\InfoAndAtmosphere\`.

---

## 8. OPEN ITEM CARRIED OVER

**The Capstone fork is still unruled.** The Extended Phoenix Timeline puts the Capstone at
2106 AD = AM 6000, which is **not** a 138 node (6000 ÷ 138 = 43.478). The spine's 44th node
is AM 6072 = 2178 AD. Two terminal structures, 72 years apart. Several finished films assert
the spine outlives AM 6000. **Do not write a quick fact that takes a side until Bee rules.**

## 9. THE TEMPLATE IS SUBJECT-AGNOSTIC — adapt it, don't fork it

Bee's note: *"and can be adapted."* The engine was built to take any subject; nothing in
`StationScene.tsx` knows it is about Göbekli Tepe. Adapt by **data and config only** — every
knob below already exists, so a new show needs no new components.

| Knob | Default | What changes |
|---|---|---|
| Speakers | NATORI ember2 2.4–7.8 · ROGUE ice 8.6–13.6 | any number, each with name tag, colour, window |
| Lanes | 3 × 19 | any count; each renders alone or chained |
| Station length | 15 s at 30 fps | the clock beats move with it |
| Under-counter line | `{PLACE}` | tokens `{PLACE} {DATE} {ID} {AM}` — Phoenix work uses `"{AM} AM · {PLACE}"` |
| Palette | house values | override per show without touching code |
| Toggles | all on | midpoint card · return-to-start · red body · LAP / mirror / camera in eyebrow |
| Outputs | proof (first 3) | full · lane · trailer · single station · title card |

**Adaptations worth building from the two manuscripts:**
- **THE MEASUREMENTS** — Cosmic Measurements' Egyptology critique. Lane colour gold.
  Facts are dimensions and tolerances; the check line carries the surveyor.
- **THE FLOOD CHAIN** — 2239 / 1687 / 1135 / 583 BC, the 552-year run at every fourth node.
  Four stations, so a short lane; pairs naturally with a walker cut.
- **THE 19 CORE CLAIMS** — `Desktop\19 CORE CLAIMS TO KNOW.txt` is already exactly 19 items,
  which is one full lane with no padding. The likeliest next build.

**Rule when adapting:** change `stations.json`, `theme.ts` colours and the `CLOCK` object.
If a change needs a new layer, it is a new layer for *every* show — add it to the template
and to `Rogue Proof.html`, never as a one-off branch.

---

*READS THE SAME RETURNING · 19138 · 83191*
