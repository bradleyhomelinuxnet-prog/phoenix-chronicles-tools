# Phoenix Chronicles Tools

> Companion toolkit for **The Phoenix CODEX 138 Palindromic** — a predictive-chronology instrument suite built around the Archaix thesis of Jason Breshears (Phoenix 138 · Nemesis 792 · NER 600 · Metonic 19), plus a reverse-engineering study of the Ophis v9 cycle engine that inspired the grammar.

## What's in here

### Live instruments (open the `.html` files in any browser)

| File | What it is |
|---|---|
| [PSYFR1.html](PSYFR1.html) | **The Predictive Chronology Engine.** Anchor dates in, cycle-projected Z-dates out, scored against the Chronicon ledger and eclipse tables. The Oracle · The Convergence · The Wheels · The Ledger. |
| [PSYFR2.html](PSYFR2.html) | **The Field Guide.** Operator's codex for PSYFR1 — quick start, vocabulary, copy-clickable formula cookbook, worked examples, FAQ. |
| [OPHIS.html](OPHIS.html) | **Ophis v9 Field Guide.** A companion explainer for the Ophis engine that PSYFR extends — architecture, the 15 shipped operations, the 138 / 19 lattice extensions, and a live compute playground driven from this page. |

All three are **fully self-contained** — one HTML file each, no build step, no server, no bundler. Only external request is the Google Fonts stylesheet.

### Reference documents

| File | What it is |
|---|---|
| [docs/Ophis_v9_ReverseEngineering_Report.md](docs/Ophis_v9_ReverseEngineering_Report.md) | 23 KB architecture report on the Ophis v9 Electron app — packaging, MVC layout, formula engine pipeline, `.oph` file format, Excel/PDF export, astronomy stack, notable caveats. |
| [docs/Ophis_v9_DeepDive_Addendum.md](docs/Ophis_v9_DeepDive_Addendum.md) | 57 KB deep dive — end-to-end compute trace, mathematical translation of all 15 default operations, MSRF filter arrays decoded. |
| [codex/PhoenixCODEX138.txt](codex/PhoenixCODEX138.txt) | Working notes from the **Phoenix CODEX 138 Palindromic** manuscript. |
| [codex/PhoenixCODEX138_Palindromic.txt](codex/PhoenixCODEX138_Palindromic.txt) | Amazon product description for the book. |

## Live deployment

The instrument trio also lives at **[hollywood-rogue-ai-ventures.w3spaces.com](https://hollywood-rogue-ai-ventures.w3spaces.com/PSYFR1.html)**:

- [/PSYFR1.html](https://hollywood-rogue-ai-ventures.w3spaces.com/PSYFR1.html) — the engine
- [/PSYFR2.html](https://hollywood-rogue-ai-ventures.w3spaces.com/PSYFR2.html) — the guide
- [/OPHIS.html](https://hollywood-rogue-ai-ventures.w3spaces.com/OPHIS.html) — the Ophis field guide

## How to use

**Local:** double-click any `.html` file. It runs in your browser. Nothing is sent anywhere.

**Deploy your own:** the three HTML files are static and stateless. Drop them into any static-site host (GitHub Pages, Netlify, Cloudflare Pages, plain nginx). Keep them in the same directory so the relative `↗` nav links resolve.

**Extend:** paste your own Ophis-grammar formulas into PSYFR1's Custom Operation field. Legal grammar is documented in [OPHIS.html §5](OPHIS.html#grammar) and [PSYFR2.html §4](PSYFR2.html#grammar). Save your setups as `.oph` (the same JSON schema the original Ophis app uses).

## The Ophis reverse-engineering note

The documents under `docs/` are an **analytical study** of a legally obtained copy of the Ophis v9 Windows binary. They describe how the app is architected and how its formula engine evaluates — the same kind of reverse-engineering writeup that security researchers, mod communities, and interoperability projects publish routinely.

The reports quote small excerpts (function signatures, constant values, ~20-line snippets like `oph_flip`) with file:line citations, as necessary to explain what the engine does. This is analytical/critical work under fair use. **This repository does not redistribute the Ophis binary or its source code.** If you want to run Ophis itself, obtain it from its author.

If you are the Ophis author and want any specific excerpt removed, open an issue.

## Attribution

- **PSYFR engine, field guides, and Codex work** — © 2026 Bradley Rogue & Natori Saira Evren. MIT (see [LICENSE](LICENSE)).
- **Archaix thesis** (Phoenix 138 cycle · Nemesis 792 · NER 600 · Anno Mundi reckoning) — Jason Breshears, [Archaix.com](https://archaix.com). The chronology and cycle lattice are presented in this repository as *his* thesis, not as established archaeology.
- **Ophis v9** — a separate closed-source Windows app whose formula grammar inspired the PSYFR extension. The reverse-engineering study is analytical work; the app itself is not included here.
- **Fonts** — Cinzel, EB Garamond, IBM Plex Mono (Google Fonts, SIL Open Font License).

## License

MIT — see [LICENSE](LICENSE).
