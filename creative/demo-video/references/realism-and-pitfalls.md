# Realism checklist and rendering pitfalls

Read this when a screenshot "looks off", and before editing anything in `core/`.

## What makes a mockup read as real

Viewers pattern-match on **chrome**, not on content. Get these right and nobody questions the rest.

- **Full chrome, no shortcuts.** Every surface has a set of parts a user sees a hundred
  times a day — window controls, tabs, breadcrumbs/URL, a status bar, a panel strip.
  Missing any *one* of them is what makes something look like a mockup. See the surface's
  NOTES.md for its checklist.
- **The platform's own palette.** VS Code Dark+, the browser's `#dee1e6` chrome grey, the
  terminal's ANSI-ish greens. Do not invent a palette for the chrome; save your product
  colour for the one thing the tool contributes.
- **Real content.** Real import paths, real-sounding record names, plausible file sizes and
  timings. Placeholder text ("record one", `foo.ext`) is the fastest way to lose the room.
- **The tool narrates.** Output lines arrive one at a time with timings; a plan is stated
  before it is executed; a result is summarised at the end.
- **Counters tick** (`D.count`) and **numbers stay consistent** — if the badge says 2, the
  list must have 2 rows.
- **The world keeps living** around the demo point: other rows finish, the queue drains,
  the branch name stays the same. A world that freezes reads as a screenshot.
- **Something crosses surfaces.** A connector from a spec to a line, a drawer that explains
  a row, an info panel that flips to ✓ when the code changes. That cross-surface moment is
  usually the "wow".

## Rendering pitfalls (each of these cost a debugging round)

1. **`<pre>` + `<div>` lines double the spacing.** The newlines between `.ln` divs render as
   whitespace inside `<pre>`. Fix: `pre{white-space:normal}` and `.ln>code{white-space:pre}`.
   Already in the ide surface — keep it.
2. **Inline hints push content off-screen.** Anchor the message with
   `position:absolute; right:6px` and a left-fading background so it overlays the tail of
   long lines. Keep it ≤ 45 chars; long reasons belong in a peek/drawer/terminal.
3. **Popups must be siblings of `<code>`, not children.** Inside `<code>` with
   `white-space:pre` they inherit pre-formatting and their newlines become blank lines.
4. **Inline `<svg>` defaults to 300×150.** The connector overlay needs
   `width="1600" height="1000" viewBox="0 0 1600 1000"` or the path never appears.
5. **Scroll clamps.** `el.scrollTop = target.offsetTop - offset` silently clamps at the
   bottom; if the target is in the last screenful the offset is ignored. Give the scroller
   `padding-bottom` or move the target up.
6. **Absolutely positioned children escape their box.** Minimaps, drawers and overlays need
   `overflow:hidden` on the parent, or they leak into the panel below.
7. **An absolutely positioned panel does not scroll** unless it has `overflow:auto` — without
   it `scrollTop = 1e9` does nothing and the terminal appears stuck on its first lines.
8. **A scaled stage breaks coordinate math.** The stage is `transform: scale()`; divide every
   `getBoundingClientRect()` value by the scale before using it as an SVG coordinate
   (`D.box` does this — use it instead of raw rects).
9. **Typing under an overlay.** If a hint sits at the right of a line being typed into, show
   the hint only after the typing finishes.
10. **Fonts swap on first paint.** `record.py --settle` trims the first ~0.8 s; keep the first
    second of the story uneventful.
11. **Screenshots taken mid-animation.** Wait ≥ 10 s after triggering a stage — `snap.py`
    defaults to that. A stage that looks broken is usually a stage that was not finished.
12. **A stage that is not replayable from `reset()`.** Every `run()` must be able to start
    from the reset state; that is what makes the numbered buttons, keyboard digits and
    `snap.py` work. If a stage only looks right after the previous one, move the missing
    setup into it.
13. **Dead space.** Half-empty terminals, 4-row tables, empty drawers. Fill the surface with
    enough plausible content that the demo point is surrounded by an ordinary working day.

## Review loop

```bash
python scripts/snap.py demo.html          # PNG per stage
# look at each one, fix, re-snap
python scripts/record.py demo.html --gif --seconds 34
```

Always look at the stills before recording — a still shows layout bugs that motion hides.
