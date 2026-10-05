---
name: slide
description: Author and recursively refine a single Slidev slide (or a few) in THIS repo's Nyx light-theme design system — correct placement, layout, font sizes, color semantics, and one-visual-per-slide SVG discipline — then drive a render→PNG→critique→edit self-improvement loop until it reads cleanly. Use when the user wants to create, redesign, fix, or polish individual slides (not generate a whole deck from a brief — that is the presentation-pipeline skill). Distilled from the company-deck and nanto-deck branches.
---

# slide

Build or fix one slide at a time, on-brand and legible, then improve it by
looking at the rendered pixels — not just the markdown. This skill owns the
**craft of a single slide**: where things go, how big the type is, what the
colors mean, and how to iterate from a screenshot. To architect a whole deck
from a raw brief (strategy → narrative → content), use **presentation-pipeline**
instead; come here for the visual execution of each slide.

## The two reference files — read before you edit

1. **`reference/design-system.md`** — the Nyx visual language: color tokens and
   their fixed *meaning*, the typography stack, the **minimum font-size
   hierarchy** (hard floor: body ≥ 14px, labels ≥ 12px, SVG text ≥ 13px),
   the slide file skeleton, layout/placement rules, and the inline-SVG
   discipline (1 visual per slide, CSS-class styling, highlight only the core
   frame). **Open it before writing any slide markup.**
2. **`reference/recursive-refinement.md`** — the render→PNG→five-persona
   critique→surgical-edit→re-render loop, the acceptance tests, the scoring
   rubric, the export commands, and the convergence rule. **Open it before you
   start polishing.**

These are design defaults. Follow the user's current direction and accepted manual edits first;
use the repo's `CLAUDE.md` for conventions not settled by that direction.

## Technical case studies: decide before drawing

- Develop concrete case slides before forcing a deck narrative. Read the actual repository:
  implementation, specification/assertions, verification setup and result. Explain what the tool
  does, its operating principle, and one observed result using the same example.
- Choose the visual from the relationship: a circuit for hardware, a state graph for allowed and
  rejected transitions, a partition table for abstracted values, an architecture for tool roles.
  Consecutive generic flowcharts do not explain these differences.
- Give the eye one route through a dominant figure. For comparisons, align corresponding parts
  within a single comparison; avoid two unrelated figures competing for attention.
- Show a formal check's input domain, relevant timing/assumptions, expected result and actual
  discrepancy at the affected component. A tool name or a success badge alone is insufficient.
  Bound the claim to the actual check; distinguish formal results from audits and demonstrations.
- Draw circuit wires with straight segments and right-angle bends, explicit junctions and clear
  crossings. Curved return edges may suit a state graph. Use tool logos to identify actual roles.
- For an improvement, retain the baseline's orientation and highlight changed components. Put
  multiplier counts or table-word reductions beside the part that changed, with source-backed
  units. Avoid listing trivial edits when the circuit diff already conveys the improvement.
- Cut a redundant slide when the previous slide already explains its point. A short title and
  one figure can be enough; do not refill the space with process labels or restatements.
- When asked to reproduce a manual version exactly, preserve its deletions, order and formatting.
  Bring it into the build source; do not run a redesign pass or restore deleted explanations.

## The non-negotiables (full detail in `reference/design-system.md`)

- **One slide, one visual.** A title and the figure are sufficient; a one-line lead is optional;
  the rest of the message lives in a single large inline SVG. No 2×2 grids — one
  focal point, one eye-path (title → key visual → support).
- **Color is semantic and fixed.** `--accent` deep blue `#1f3a52` = verify /
  affirm / ✓; `--severe` brick `#a25434` = regression / risk / negation. Never
  swap these. Hairlines only (`--line`), never thick black borders.
- **Font sizes have a hard floor.** Display title 36px, lead 16px, kicker 12px,
  card body ≥ 14px, labels ≥ 12px, SVG text ≥ 13px. Sub-legible type is a defect
  — it must be readable by an elderly viewer in a projected room.
- **Heading structure is simple.** Use `nx-display` h1, usually a short concrete noun phrase
  (e.g. 「Leanを用いた静的解析ツール」). A message title should state an evidence-backed
  finding or implication. Omit small section kickers such as `03 ／ mulu ・13` by default.
  Aim for one line when authoring; preserve the user's layout in exact-reproduction tasks.
  Do not force italic `<em>` onto Japanese text. No `──` em-dash spam or
  declarative hype / military metaphors (青天井・希少・本丸・既成事実).
  `BIZ UDPMincho` is **wordmark-only** — never for headings, numbers, or buttons.
- **One concept = one word, deck-wide.** Don't drift terms (e.g. Trust は「信頼」で
  統一し「信用」と混ぜない). Read a strategy/type from **position + arrows + edge
  labels**, not a separate legend — minimize legends.
- **Diagram hygiene.** Arrowheads are filled triangles (`M0,0 L7,3.5 L0,7 Z`),
  not open "hand-drawn" strokes. Nodes/chips are **opaque** (translucent
  `accent-soft` lets the lines behind bleed through — use an opaque pale tint).
  No persistent pulse/blink animation — it reads as product UI, not an editorial
  deck.
- **SVG text is styled via CSS classes, not SVG attributes** (attributes collide
  with Slidev's global CSS). Decide a `viewBox`, scale only with outer
  `max-width`.
- **Logo / footer chrome.** Content slides show the Nyx logo + page number
  bottom-right (`global-bottom.vue`). Cover (title) and closing center a logo at
  the bottom and hide that corner footer (avoid a duplicate Nyx mark) — generic
  default is Nyx-only; a deck pairs its product logo with Nyx side-by-side, no
  divider (`.nx-cobrand`). Decide first/last vs. middle with `$nav` **in the
  template** (`currentPage === 1 || currentPage === $nav.total`); referencing
  `$nav` from `<script setup>` misfires on every page.
- **Japanese decks omit English `.ja` subtext.** Cut small explanatory text
  rather than shrink it.
- **No blank lines inside an HTML block** (`mdc: true` lets a blank line
  terminate the block in CommonMark).

## Workflow

1. **Read the references.** `reference/design-system.md` first, then the target
   slide file(s) and `style.css` for existing `nx-*` primitives to reuse.
2. **Author / edit** `slides/SLNN.md`. Reuse `nx-*` classes; keep per-slide CSS
   in the slide's own `<style>`. Promote anything shared to `style.css`.
3. **Render to PNG.** Build and export per-slide PNGs (commands in
   `reference/recursive-refinement.md`). Output is `dist-png/NN.png`,
   1-indexed.
4. **Look at the render with the Read tool.** Score against the acceptance tests
   and the font-size floor. Check overflow (no wrapped/clipped title), eye-flow
   (single path, single focal point), contrast, and that the visual — not a
   paragraph — carries the idea.
5. **Make surgical edits** tied to a specific pixel-level defect, then
   **re-render** as a regression guard. Repeat until it converges (every
   acceptance test passes and no edit worth ≥ 0.3 remains).

For an automated, audited version of steps 3–5 across the whole deck, the repo
ships `make refine` (externalized loop) and `make polish` (single agentic loop);
see `reference/recursive-refinement.md`. For one or two slides, run the loop
yourself in-conversation.

## Anti-patterns (these recur — do not repeat)

- A wall of text where one chart / timeline / big number would land faster.
- 2×2 grid → the eye has no starting point.
- Swapping the accent/severe color meaning, or using thick black borders.
- Sub-legible SVG or label type to fit more in.
- Set-membership (A ⊂ B) drawn as side-by-side boxes — use nested shapes.
- Editing the markdown without ever looking at the rendered PNG.
- Big-bang rewrite of a slide that already works; bundling unrelated edits.
- A title that wraps to two lines, or leans on `──` / hype words / military
  metaphors; using `BIZ UDPMincho` for a heading or number.
- Stacking flat info blocks (facts row + chips + grid) with no single focal
  point — pick a hero; a left context-card + right timeline beats a 2-up grid.
- A color legend the diagram could encode via arrows/position/edge-labels.
- An encoding (filled vs. hollow, solid vs. dashed, thick vs. thin) whose
  meaning lives only in the speaker notes — the viewer sees undifferentiated
  shapes. Put a one-line key above the figure **and** a word under each mark.
- The same closing line shape on every slide — 「〜のは、〜だからです」
  「違うのは、〜かどうかです」「ここが〜です」. Reads fine slide by slide;
  reads as generated when the deck is scrolled. **Pull every closing line into
  one column and read them together**; if the same syntax runs three slides,
  rewrite them as single 常体 statements. Mixing 敬体/常体 across the same
  role (all closing lines, all captions) is the same defect.
- A table header written as a clause (「起きたこと」「何が起きたか」) instead of
  a noun (「事例」「経過」). Exception: a header that *is* the classifying
  question (「介入したあと別の物理作用が出るか」) stays a question.
- A prior-art comparison table with no slide saying what is actually new —
  the table shows differences, not the claim. Add one slide: existing
  mechanisms on the left, what you layered on top on the right.
- A background/problem slide whose heading does not say it is the problem
  slide, or that asserts a problem with no cited real-world incident.
- Translucent nodes that let lines bleed through; open "hand-drawn" arrowheads;
  persistent pulse/blink animation.
