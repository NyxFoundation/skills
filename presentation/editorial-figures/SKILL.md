---
name: editorial-figures
description: Produce polished, editorial-quality figures as image files (PNG, optionally SVG) with Python and matplotlib, sharing one cohesive paper-and-ink look and clean Japanese (Noto CJK JP) typography. Covers seven reusable archetypes — divergence / scissors charts, radial convergence (hub-and-spoke) diagrams, stat-card evidence dashboards, concept / flow diagrams (inputs to engine to outputs), calendar timelines, donut-plus-bar composites, and venue / zoning layouts. Use this skill whenever the user wants figures, diagrams, charts, or 図 / グラフ / ダイアグラム for a proposal, pitch deck, report, 企画書, or slide; wants a SET of visuals that look consistent; needs Japanese text rendered cleanly in matplotlib (avoiding tofu boxes); or asks for downloadable image figures rather than an inline sketch. Prefer it over ad-hoc matplotlib whenever visual polish, a shared palette, or Japanese typography matter. Also use it to extend or restyle figures already produced this way.
compatibility: Requires Python with matplotlib and numpy; uharfbuzz + fonttools and system Noto CJK fonts for Japanese. On this NixOS workstation everything is available via `uv run` (see nixos-environment skill).
metadata:
  type: reference
  domain: presentation
---

# Editorial figures

Generate proposal- and deck-grade static figures with a deliberate editorial
look: a warm paper background, near-black ink, restrained accents, serif
headlines over sans labels, and crisp Japanese type. The goal is a *set* of
figures that look like they came from the same studio, not a pile of default
matplotlib charts. Output is image files the user downloads or drops into a doc
(Notion, slides, PDF) — not inline sketches.

## Setup — do this first

1. **Copy the style module into the working directory** so `import style` works:
   ```bash
   cp <this-skill-dir>/assets/style.py ./style.py
   ```
   (`<this-skill-dir>` is wherever this skill is linked, e.g.
   `~/.claude/skills/editorial-figures` or the repo path
   `.../presentation/editorial-figures`.) On first import, `style.py`
   auto-builds the Japanese font faces it needs into a cache dir outside the
   repo (`~/.cache/editorial-figures/fonts`, or `$EDITORIAL_FIGURES_FONTDIR`).
   The first import warms all 8 weights in ~2-3 min; later imports are instant.
2. **Run Python with the dependencies via `uv`** (NixOS has no pip/brew/apt — see
   the `nixos-environment` skill). The verified invocation is:
   ```bash
   uv run --with matplotlib --with numpy --with uharfbuzz --with fonttools python your_figures.py
   ```
3. **If Japanese renders as □ (tofu)** or you want to pre-warm / diagnose fonts:
   ```bash
   uv run --with matplotlib --with numpy --with uharfbuzz --with fonttools \
       python <this-skill-dir>/scripts/setup_fonts.py
   ```
   It prints the system Noto CJK files it found (via `fc-list`, nix-store aware)
   and verifies each cached face loads in matplotlib.

**How the font layer works (so you can trust or debug it):** the system Noto CJK
fonts on NixOS are variable-font `.ttc` collections that matplotlib/FreeType
cannot load directly. `style.py` therefore uses HarfBuzz (uharfbuzz) to subset
each weight to a Japanese glyph set and instance the `wght` axis (fast, ~0.6s
each), then fontTools converts the variable CFF2 to a static CFF that FreeType
can load, caching the result. If uharfbuzz is missing it falls back to the slow
fontTools instancer; if no Noto CJK is found it falls back to any Japanese
family matplotlib can locate.

## The design system (`assets/style.py`)

`import style as S` gives you the palette, fonts, and drawing helpers. Build
every figure through these so the set stays consistent.

**Palette (semantic, not decorative):**

| Token | Role |
| --- | --- |
| `PAPER` / `CARD` | warm background / brighter panels |
| `INK` / `SOFT` / `MUTED` / `FAINT` | text from primary to faint |
| `HAIR` | hairline borders |
| `SLATE` (+`_L`,`_BG`) | cool, calm, neutral default; "down"/"cheap" |
| `RUST` (+`_L`) | warm; reserved for *rising risk* or sparing emphasis |
| `GOLD` `TEAL` `PLUM` `OLIVE` | extra category hues |
| `CAT` | a cohesive 8-colour categorical sequence |

Keep colour scarce: paper + ink carry most figures; `SLATE` is the workhorse;
`RUST` earns its place only when something is rising, alarming, or the one thing
to look at. Avoid rainbow palettes.

**Type:** Noto Sans CJK JP weights via `S.F["reg"|"med"|"bold"|"black"|"light"]`
and Noto Serif CJK JP via `S.F["smed"|"sbold"|"ssemi"]`. **Serif for headlines,
sans for labels and body.** `S.title_block(fig, head, sub)` sets this up.

**Helpers:** `S.new(w,h)` (paper fig+ax, axis off), `S.t(...)` (text),
`S.rrect(...)` (rounded rect / card), `S.arrow(...)`, `S.chip(...)` (pill tag),
`S.title_block(...)`, `S.save(fig, name)` (dpi 200, tight bbox, to the outputs
dir), `S.lighten(hex, amt)` (tint toward white).

## Workflow — every time

1. **Open `references/recipes.md`** and read the recipe(s) for the archetype(s)
   you need. Each is a parameterised function you adapt by editing its data
   lists/dicts.
2. Copy `style.py` into the working directory (above).
3. Write each figure as its own small function; keep the *data* in lists/dicts
   at the top so it is easy to edit. One figure = one function.
4. `S.save(fig, "figN_name.png")` — saves to the current working directory (or
   `$EDITORIAL_FIGURES_OUTDIR`). It returns the path.
5. **Open every PNG with the `Read` tool and fix it.** Most defects are
   invisible until rendered: tofu glyphs, text hidden behind a filled shape
   (z-order), overlapping lines, lopsided padding. Re-render until clean. This
   step is not optional — it is where the quality comes from.
6. Report the finished PNG paths to the user. Then offer obvious follow-ups: an
   English version, a 16:9 crop for slides, or a uniform export size for Notion.

The single most common bug: **a filled `Circle`/`Wedge` hides the text on top of
it.** Give such labels `zorder=5` or `6`. (See the convergence recipe.)

## Choosing an archetype

| The user wants to show… | Archetype | Recipe |
| --- | --- | --- |
| One thing falling while another rises; a gap opening | Divergence | recipes §1 |
| Several domains converging into one idea | Radial convergence | recipes §2 |
| A wall of headline numbers / evidence | Stat-card dashboard | recipes §3 |
| Inputs feeding a process that yields outputs | Concept flow | recipes §4 |
| An event placed inside a date window | Calendar timeline | recipes §5 |
| A composition plus ranked channels/sources | Donut + bars | recipes §6 |
| Rooms / zones of a venue or space | Zoning / floor plan | recipes §7 |

If the request fits none cleanly, compose from the helpers using the nearest
recipe as scaffolding, keeping the same sizes, palette, and `title_block`.

## Conventions (what makes it look intentional)

- **Headlines state the takeaway, not the topic** — "生成は安く、検証は高くなる",
  not "コスト比較".
- **Annotate at the source:** label curves at their ends, wedges via a legend
  list beside the donut — avoid detached legends that force eye travel.
- **No overlaps:** anchor stacked text with `va="top"` and explicit y steps;
  budget a hero number's height as `points/72` data units before placing the
  line beneath it.
- **Symmetric padding:** equal inner margins; for a zoning container, the right
  zones must inset from the border by the same amount as the left.
- **Data honesty:** before drawing dates, prices, rankings, or anything
  "current", confirm it with `WebSearch` first — Japanese public holidays,
  equinox-based dates, FX rates, and leadership all drift. Label ranges as
  ranges, cite a source on every stat card, and note when wedges use midpoints.
- **Consistency across a set:** reuse `style.py`, the same figure widths, and
  one `title_block` style for all figures in a deliverable.

## Files

- `assets/style.py` — palette, fonts (self-building JP cache), drawing helpers. Copy to cwd.
- `references/recipes.md` — the seven archetype recipes + the full conventions list. Read before building.
- `scripts/setup_fonts.py` — optional font cache warm-up / troubleshooting.
