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

The repo's `CLAUDE.md` is the authoritative source these distill; if it and a
reference disagree, `CLAUDE.md` wins.

## The non-negotiables (full detail in `reference/design-system.md`)

- **One slide, one visual.** Body text is a kicker + a one-line lead at most;
  the rest of the message lives in a single large inline SVG. No 2×2 grids — one
  focal point, one eye-path (title → key visual → support).
- **Color is semantic and fixed.** `--accent` deep blue `#1f3a52` = verify /
  affirm / ✓; `--severe` brick `#a25434` = regression / risk / negation. Never
  swap these. Hairlines only (`--line`), never thick black borders.
- **Font sizes have a hard floor.** Display title 36px, lead 16px, kicker 12px,
  card body ≥ 14px, labels ≥ 12px, SVG text ≥ 13px. Sub-legible type is a defect
  — it must be readable by an elderly viewer in a projected room.
- **Heading structure is fixed.** `nx-kicker` (`01 ／ 日本語`, mono uppercase) →
  `nx-display` h1 with the *core* phrase wrapped in `<em>` (italic Cormorant,
  accent blue). `<em>` marks the sentence's core, not mere emphasis. The h1 must
  fit **one line** — shorten rather than wrap. No `──` em-dash spam; avoid
  declarative hype / military metaphors in titles and kickers (青天井・希少・本丸・
  既成事実). Kickers are plain section words (背景／現状／課題／答え, コンペ／カンファレンス).
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
- Translucent nodes that let lines bleed through; open "hand-drawn" arrowheads;
  persistent pulse/blink animation.
