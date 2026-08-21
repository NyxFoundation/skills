---
name: native-pptx-deck
description: |
  Build a presentation deck as a native .pptx with python-pptx — real text runs, shapes and charts the
  recipient can edit, not screenshots wrapped in a file — then harden it through a render → look → fix
  loop plus recursive external review until it survives being opened in PowerPoint and Google Slides,
  and ship it to Drive with rclone. Covers the design-system layer (tokens, type scale, 12-column grid),
  the OOXML workarounds python-pptx has no API for (letter-spacing, fill alpha, curve smoothing, theme
  shadows, group transforms), the text-metrics problem and how to survive it, the Google Slides importer
  traps that make a file refuse to open, Assertion–Evidence headline rules that stop copy reading as
  try-hard, and the Japanese-typography trap where an italic Latin serif fake-slants CJK. Trigger on:
  「スライドを作って」「pptx で作って」「PowerPoint の資料」「デッキを組んで」「python-pptx で」
  「スライドの構成を考えて」, or any request to produce an editable slide deck rather than a rendered image.
---

# Native .pptx decks

Build the deck as **real PowerPoint objects** — text runs, shapes, charts — not a .pptx with a
screenshot on each slide.

This is harder than an HTML deck and **the failures are quiet**. python-pptx raises no error for text
overflowing its shape, for a font that does not exist on the machine, or for a property assignment
that does nothing at all. Almost every rule below was learned by shipping a file that looked fine
locally and then broke somewhere else.

| # | Artifact | Format | Role |
|---|---|---|---|
| 1 | The deck | `.pptx` | What the recipient opens, projects, and edits |
| 2 | Render | `.pdf` + per-slide `.png` | What **you** look at every round, and what you ship alongside for anyone without the fonts |
| 3 | Build scripts | `.py` in the repo | Design layer + content layer. The reproducible source |

Row 3 is the point. A deck built by hand in PowerPoint cannot be regenerated next month with new
numbers. One built from a script can.

---

## When not to use this

| Situation | Use instead |
|---|---|
| The deck already exists in Slidev / HTML and you only need a file to project | Export PNG → `assets/png_to_pptx.py` |
| The design leans on webfonts you cannot install on the presenting machine | HTML deck |
| The visual is an SVG illustration and you cannot convert it | HTML deck, or SVG → EMF (see `references/portability.md`) |
| One-off, thrown away after the meeting | Whatever is fastest |
| It is a proposal / WBS / estimate for a client | `pmbok-proposal-wbs` |

Native pays off when the recipient must **edit** it, when it must survive **Google Slides import**,
or when the same deck ships **every month** with new numbers.

---

## Read these before writing slide code

| File | Read it when |
|---|---|
| `references/design-system.md` | Setting up tokens, type scale, and the grid |
| `references/ooxml-workarounds.md` | python-pptx has no API for what you need, or a property silently did nothing |
| `references/layout-and-text.md` | Anything overflows, collides, or sits in the wrong place |
| `references/layout-patterns.md` | **Choosing a layout — read before laying out a single slide.** Design principles with sources, the baseline-row grid, density budgets, and 11 page layouts keyed to slide purpose |
| `references/slide-type-catalogue.md` | **Choosing what to draw inside the layout.** 69 collected diagram/slide types with sources (Duarte, Roam, Zelazny, SmartArt, consulting decks), folded into a 12-item working list |
| `references/slide-copy-rules.md` | Writing headlines and body copy — **read before writing a single headline** |
| `references/portability.md` | The file will not open, or renders differently somewhere |
| `references/review-loop.md` | Driving the render → look → fix cycle and the external review |

---

## Order of work

**Do not skip step 1.** Restructuring 12 slides of absolute coordinates is expensive; restructuring a
table in a chat message is free.

### 1. Settle the audience and the venue, in writing

Get these two before anything else. Getting them wrong wastes every round that follows.

```
聞き手:     誰が見るのか。何を知りたくて来ているのか
場の性格:   月次共有 / 勉強会 / ピッチ / 審査。「雑に話す場」なのか作り込む場なのか
尺:         スライドで何分話し、質疑に何分残すのか
その後:     懇親があるのか。何をして帰ってほしいのか
```

If the venue has a written description (an event page, an invite), **read it**. A deck built with a
heat-engineering narrative was rejected with 「構成がいまみたけど変すぎる」 because the event page said
「スライドや完成された発表ではなく、雑に話す場」. Four rounds of review had already passed by then.

### 2. Agree the slide list as a table

```
| # | 枚 | 聞き手に何が分かってほしいか | 載せる事実 | 型 |
```

**Name the layout type for every slide** from `references/layout-patterns.md`.
A slide with no chosen type becomes "headline + rows of text" by default, which is how a deck
ends up as a document. If three slides in a row are type J (table), that is a valley — split them
or convert some to another type.

Naming the layout (A–K, §4) only decides the **page**. For any slide whose evidence is a figure,
also name the **diagram** — take it from `references/slide-type-catalogue.md` §7 (the 12-item
working list). Write both in the plan, e.g. `C + 構成図`. A slide with a layout but no named
diagram type reliably degenerates into a bulleted list on the right-hand side.

The catalogue's §0 gives the order to pick in: what question does this slide answer (Roam) →
if it is numbers, which comparison (Zelazny) → if not, which relation (Duarte) → which page
layout. **If step 1 has two answers, the slide has two messages — split it before drawing.**

Get a nod on this before writing code. Also decide now which slides are **fixed chassis** and which
are **monthly cartridge** if the deck recurs.

### 2.5 The decision sheet — fill this in before writing any code

Rounds are spent on **decisions**, not on execution. Measured across one deck: ten review rounds,
and every one of them turned on a choice that could have been made up front — what the headline
asserts, what the figure's vocabulary is, where the visual weight sits. Once those were settled the
code converged in one or two rounds.

So write these six lines per slide, in the plan, before opening an editor.

```
1. 誰に      この分野の何を知らない人か
2. 見出し    実現する世界を平叙文で（現状の否定にしない。§1.1）
             連作なら文型を固定（§1.2）
3. 証拠      写真 / スクショ / 図 / 数字 のどれか 1 つ
4. 図なら    問い(Roam) → 数字なら比較(Zelazny)／関係(Duarte) → 版面(A〜K)
             ノードの語彙・アイコン・箱の形（§4.5）
5. 強調      色を点ける 1 箇所だけ。赤茶＝未着手 / 青＝検証が効いている
6. 開く語    残す固有名詞はどれか。残り全部を日常語に開く
```

Two checks on the sheet itself, before you build:

- **ブロックは 3 つまでか**（§2.6）。4 つ以上ある枚は、その時点で「ダサい」と言われる
- **見出しで言ったことが、図の中にも現れるか。** 「証明で担保される」と締めるのに図に青い
  要素が 1 つも無ければ、図は現状しか語っていない

Auditing a deck you already built by *labelling* each slide with a type is not an audit — you will
pass yourself every time. **Re-derive from step 1 with the existing slide out of view**, then
compare. That is the only way the catalogue tells you anything you did not already believe.

### 3. Build

```
scripts/build_pptx/<project>.py   # design layer: tokens, grid, primitives, every OOXML hack
scripts/build-<deck>.py           # content layer: one function per slide
out/<deck>.pptx
```

Keep the layers apart. The design layer is reusable across months and decks; the content layer is
throwaway. **Every OOXML hack belongs in the design layer** so slide code stays readable.

Use PEP 723 inline metadata so no environment setup is needed (works on NixOS without pip):

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0"]
# ///
```

```bash
uv run scripts/build-<deck>.py out/<deck>.pptx
```

### 4. Render and actually look at it — every round

```bash
bash assets/render.sh out/deck.pptx /tmp/render
uv run assets/measure.py out/deck.pptx      # 密度を数える
```

`measure.py` prints characters, paragraphs and picture count per slide against the density budget
in `references/layout-patterns.md`. Slides with **zero pictures and 250+ characters, several in a
row**, are where the deck goes flat.

Read `contact.png` **first** — overflow, collision and empty-bottom are easier to spot at thumbnail
size. Then open individual slides and read the copy.

Expect 3–5 rounds of layout fixes. Overflow is normal, not a sign you did something wrong:
see `references/layout-and-text.md` for why (there are no text metrics).

### 5. Pre-review gate — run this before you pay for a review round

```bash
uv run assets/selfcheck.py out/deck.pptx
```

A reviewer's first two rounds are mostly findings a script can make. Measured on one deck: of the
19 findings across rounds 1 and 2, **14 (74%) were mechanically detectable** — duplicate kickers,
an agenda that does not cover its sections, a headline that describes an activity instead of making
a claim, counts that do not add up across slides, numbers with no label, a name listed once and
never mentioned again.

**Do not send a deck to the reviewer until this exits 0.** Each round costs 5–15 minutes and a
reviewer that spends its budget on mechanical findings never reaches the judgment calls.

The gate deliberately splits its output:

| Output | Meaning |
|---|---|
| **検出** (exit 1) | Mechanically certain. Fix before reviewing |
| **参考** (does not block) | Needs a human look. Japanese semantic mapping cannot be decided by a script |

What it cannot see: whether the deck matches the venue's stated purpose, whether a slide carries two
messages, whether a fact's weight lands with this audience. Those are what the reviewer is for.

### 6. External review

`references/review-loop.md`. Budget 4–7 rounds — **2–3 if the gate ran first**. Use an agent that
did not author the deck.

**If the deck has diagrams, run a second, separate loop with a viewer persona on the PNGs alone**
(`review-loop.md` §「視聴者役」). A text reviewer reads a diagram charitably and never reports a
misread icon; a viewer told to write *what they literally see* reports them on the first pass.
Three rounds converges.

### 7. Preflight

```bash
uv run assets/preflight.py out/deck.pptx
```

Catches the conditions that make a file refuse to open elsewhere. **Mandatory if it will touch
Google Slides.** One finding is enough to stop shipping.

### 8. Ship

```bash
rclone copy out/ gdrive: --drive-root-folder-id <FOLDER_ID> --stats-one-line
rclone check out/ gdrive: --drive-root-folder-id <FOLDER_ID>
```

**`rclone check` must pass before you say you uploaded it.** Use `--stats-one-line`, never
`--progress` from a script — it emits hundreds of lines of carriage-returned noise.

Three rules that each cost a round when broken:

1. **Never ship on a gate NG.** Run `selfcheck.py` *before* `rclone copy`, not after. Shipping
   first and fixing second means the recipient sees the broken version.
2. **Re-render every companion artifact.** If `out/` also holds a PDF or PNGs, regenerate them in
   the same command as the upload. A stale PDF sat two hours next to a current `.pptx` and the
   recipient — who opened the PDF, because Drive previews PDFs instantly and `.pptx` slowly —
   reported "nothing changed."
3. **Replacing a file in place keeps the URL but not the preview.** Drive serves the thumbnail it
   generated at first upload. The file is correct and the page still looks old. Prove it with
   `md5sum` on a fresh download, and offer a **version-stamped copy** (`deck-v0821-1126.pptx`) so
   the recipient has something unambiguous to open.

Tell the recipient, unprompted:

- the font names they need (without them it silently substitutes and the type hierarchy collapses)
- that the PDF is a LibreOffice approximation and **the real PowerPoint is authoritative**
- which slides are most likely to overflow, so they know where to look

---

## Hard rules

- **Never ship without looking at a render.** Not a claim about the code — the actual pixels.
- **Never claim a property worked because the assignment did not raise.** `ser.smooth = True` does
  nothing. `shadow.inherit = False` does not remove the theme shadow. Check the XML.
- **Never trust the local render as final.** LibreOffice approximates PowerPoint. Word wrapping in
  particular differs, and wrapping is exactly what overflow depends on.
- **Never size a text box by eye.** Estimate the line count with a safety factor.
- **Never italicise CJK with a Latin serif.** It fake-slants. This alone can make a deck read as
  try-hard.
- **Never write a headline that ends in 「〜の話。」「〜こと。」.** Assertion–Evidence: one claim,
  as a full sentence.
- **Never put a fact on a slide you cannot source.** `[要確認]` does not ship silently — say it.
- **Never lay out a slide without naming its type first.** Untyped slides default to text rows.
- **Never read a slide's own sentences aloud.** Redundancy principle — reading and listening
  compete. What is on the slide is evidence; what you say is the argument.
- **Never open a review round on a deck that fails `selfcheck.py`.** You are paying a reviewer to
  find what a regex already found.

---

## Reusable assets

| File | What it does |
|---|---|
| `assets/nyx_design.py` | Reference design layer — tokens, 12-column grid, primitives, every OOXML workaround. Copy and re-token it |
| `assets/render.sh` | .pptx → PDF → per-slide PNG → contact sheet |
| `assets/selfcheck.py` | **Pre-review gate.** Catches ~3/4 of what a reviewer's first two rounds would say |
| `assets/measure.py` | Per-slide density audit against the budget in `references/layout-patterns.md` |
| `assets/preflight.py` | Portability checks: transforms, degenerate extents, float coords, child order, fonts |
| `assets/png_to_pptx.py` | Wrap rendered PNGs into a .pptx — the non-native escape hatch, with speaker notes |

---

## Monthly decks

If it recurs, split it explicitly:

| Part | What it is | Every month |
|---|---|---|
| **Chassis** | Cover, who-we-are, what-we-do, closing | Date only |
| **Cartridge** | This month's content slides | Rewritten |
| **Half-fixed** | Counts, the one concrete example | Numbers swapped |

Write down which is which, in the repo, next to the build script.

Two rules that make a recurring deck worth recurring:

1. **Put the month-over-month delta on a slide.** A recurring deck that cannot be compared across
   issues has no reason to be recurring. From issue 2 onward, show 先月 +5 → 今月 +9.
2. **Do not re-read the fixed slides in full every month.** Issue 1 spends 60 seconds on the framing;
   issue 2 onward spends 15 and moves on. The novelty for a repeat attendee lives in the delta, not
   in the chassis.

Automate the input gathering. A script that pulls the month's raw material into one briefing file
(`fetch-month.py` style — issues, notes, counts, a keyword-based first-pass classification that a
human then corrects) is worth more than any slide template.
