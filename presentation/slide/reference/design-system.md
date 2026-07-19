# Nyx slide design system

The visual language for slides in this repo, distilled from `CLAUDE.md`,
`style.css`, and the company-deck / nanto-deck slides. Matches the Nyx HP
(`tokens.css`). When this and `CLAUDE.md` disagree, `CLAUDE.md` wins.

## 1. Color tokens — values fixed, meanings fixed

| Token | Value | Role |
|---|---|---|
| `--bg` | `#faf9f5` | warm off-white canvas |
| `--bg-2` | `#f3f1ea` | card / inset surface; ground for highlight frames |
| `--bg-sunken` | `#eeeae0` | deepest tier |
| `--ink` | `#18181a` | near-black (warm) — main title / body |
| `--ink-dim` | `#55524c` | body secondary |
| `--ink-faint` | `#9a958c` | caption / strike-through |
| `--accent` | `#1f3a52` | deep ink-blue — **verify / proof / affirm / ✓** |
| `--severe` | `#a25434` | muted brick — **regression / risk / negation** |
| `--line` | `rgba(24,24,26,.10)` | hairline (thick black borders are banned) |
| `--line-strong` | `rgba(24,24,26,.22)` | kicker top rule, table header rule |
| `--accent-soft` | `rgba(31,58,82,.08)` | accent fill behind a highlighted frame |

**The color semantics are fixed and never swapped:** accent blue = Verifiable /
positive, severe brick = Regression / negative. Across consecutive slides the
colors carry a narrative ("regression 赤茶 → progress 青"). Use only ONE
highlighted (accent-framed) element per visual; everything else is a `--line`
1px lightweight frame.

## 2. Typography stack

| Font | Role |
|---|---|
| `Cormorant Garamond` (italic) | decorative `<em>`, math glyphs (π, ∀) |
| `Shippori Mincho` | Japanese body & title ground (`--font-jp-serif`) |
| `JetBrains Mono` | kicker, axis labels, code-ish (`VERIFY( π )`, `01 ／ 問題`) |
| `Inter` | `--font-sans` default UI/body |
| `BIZ UDPMincho` | wordmark (`Nyx Foundation`, `AI` symbol); set with `!important` to beat the global sans |

H1 (`nx-display`) is Cormorant + Shippori, weight 300, with the core phrase in
`<em>` → italic + accent blue. `<em>` is a *semantic* "this is the core of the
sentence" tag, not generic bold emphasis.

## 3. Font-size hierarchy — HARD FLOOR, enforce in SVG too

| Role | Size | Use |
|---|---|---|
| `nx-display` | **36px** | slide main title (h1) |
| Hero declaration | 46–56px | center-thesis slide statement |
| `nx-lead` | **16px** | lead body |
| subtitle / `.ja` | **15px** | sub-explanation under h1 |
| `nx-kicker` | **12px** | section kicker |
| card body | **≥ 14px** | dom-body / proj-body etc. |
| label / caption | **≥ 12–13px** | mono tags, file labels |
| SVG body text | **≥ 13–16px** | chart axes, legends |
| SVG headline | 22–44px | emphasis words inside a chart |

**Forbidden:** body < 12px, label < 11px — unreadable when projected. SVG text
must hit this floor too, applied **via `class`**, never raw `font-size`
attributes. The rule the design critic enforces: every element large and
high-contrast enough for an elderly viewer in the back row.

## 4. Heading + layout skeleton (every slide)

```
[nx-kicker]   mono UPPER, 0.18em tracking, top hairline rule.  e.g.  01 ／ 問題
[nx-display]  Cormorant + Shippori h1, ~36px, core phrase in italic <em>
(optional) verse-line-lead   2px left rule + bg-2, ONE line of lead
MAIN VISUAL  one large inline SVG — let the figure carry the message
```

Kicker form is `数字 ／ 日本語` (`01 — The Problem` is wrong). Lead `<b>` keys a
vocabulary term, closed in ink black (not accent). One visual per slide; body is
the verse line at most — cut the rest.

### Slide file structure (`slides/SLNN.md`)

```html
---
layout: default
---
<div class="sec">
  <div class="sec-head">
    <span class="nx-kicker">02 ／ 私たちの答え</span>
    <h1 class="nx-display">誰が言うかより、<em>何が確かめられたか</em>。</h1>
  </div>
  <div class="verse-line-lead">...one line...</div>
  <div class="vt-wrap">
    <svg viewBox="0 0 1000 320" class="vt-chart" xmlns="http://www.w3.org/2000/svg">
      ...inline SVG, text styled by class...
    </svg>
  </div>
</div>
<style>
.sec { padding: 0.9rem 2.6rem 0.5rem; }
/* per-slide scoped CSS; shared primitives belong in style.css as .nx-* */
</style>
```

- Canvas is **980×551 (16:9)** by default in this repo; scale SVG with outer
  `max-width`, not by re-laying-out internals.
- `.sec` padding ≈ `0.9rem 2.6rem` (HP `.sec` baseline).
- Each slide's `<style>` is scope-independent. Shared `.nx-*` primitives live in
  `style.css` (`nx-kicker`, `nx-display`, `nx-lead`, `nx-eyebrow`, grid bg…) —
  reuse them; do not redefine.

## 5. Placement & layout principles

- **One axis, one eye-path.** Linear top→bottom or left→right. Title → key
  visual → support. Multiple focal points / a 2×2 grid = defect (the eye has no
  start).
- **Comparisons** go as 3–4 side-by-side cards on the *same axis* (A vs its real
  alternative B), never mismatched.
- **Set membership (A ⊂ B)** is drawn as **nested shapes**, never parallel
  boxes (parallel boxes duplicate and confuse).
- **Never write the same element in two places.**
- Images: `max-h-[300–460px]` to stay inside the 1280×720 safe area when a deck
  uses the wider canvas.
- Whitespace is generous; one highlighted frame draws the eye, rest are
  hairlines.

## 6. Inline-SVG discipline (the main visual)

1. **Inline SVG.** Style font / size / color through **CSS classes**, not SVG
   attributes — attributes collide with Slidev's global CSS.
2. Decide a `viewBox`; scale only via outer `max-width`.
3. Minimal shapes: circles, rects, line segments; `stroke-linecap="round"`.
4. **Highlight only the core frame** — `bg-2` fill + accent 2px border says "look
   here"; everything else is a `--line` 1px lightweight frame.
5. Math glyphs (π, ∀, ＋, ✓) are oversized stand-ins for key ideas; `+` in a
   circle reads as an operator.
6. Machine/verification feel = mono + bracket notation (`VERIFY( π )`,
   `01 ／ 問題`).

## 7. Text rules

- No English `.ja` subtext on Japanese decks.
- Cut small explanatory text — unreadable text is worthless.
- Strike-through = mono + `ink-faint` for the "vocabulary of negation"
  (past / deprecated).
- Lead `<b>` keys a term (ink black), it is not accent emphasis.

## 8. Slide-type → visual pattern

| Type | Pattern |
|---|---|
| Hero / central thesis | left-aligned declaration + grid bg (`.nx-grid-bg`) + status pulse |
| Problem / threat | large SVG chart, severe brick for the regression direction, big italic numbers |
| Thesis / answer | 3-stage flow (STAGE 01/02/03), center 02 in an accent frame |
| Enumeration (domains / ways-in) | card grid: bg-2, line frame, mono tag + JP heading |
| Single proper noun (house / org) | photo + large italic Cormorant heading + mono position label |

## 9. Ops commands

```bash
bun run dev      # dev server http://localhost:3030
bun run build    # static build → dist/
```

PNG export and the refinement loop: see `recursive-refinement.md`.

## 10. Gotchas (cost real time before)

- `mdc: true`: **a blank line inside an HTML block terminates the block** in
  CommonMark. Keep HTML blocks blank-line-free.
- SVG text via attributes silently loses to global CSS — always use `class`.
- `Nyx Foundation` wordmark needs `--font-wordmark` (`BIZ UDPMincho`) with
  `!important` or the global sans overrides it.
- The old brand "ZK Tokyo" / "zktokyo" must be fully removed — grep for zero
  residue.
- Do not escape `$` (currency): write `$292M`, not `\$292M`.
