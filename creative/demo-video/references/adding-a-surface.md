# Adding a surface

A **surface** is the chrome a demo is staged in — an editor, a shell, a browser app, a
phone, a chat client, a CAD viewer. The engine (`core/`) never changes; a surface is four
files plus notes:

```
surfaces/<name>/
  surface.css      chrome + palette. May override :root vars and .stage's grid
  surface.html     the stage's inner markup (no <html>/<body>; it is injected into .stage)
  surface.js       optional helpers, added to D inside an IIFE
  storyboard.js    a runnable 5–6 beat starter story for this surface
  NOTES.md         first non-heading line = the one-line pitch shown by --list
```

Then it just works: `python scripts/new_demo.py -s <name> -o demo.html`.

## Rules

- **Own the chrome, borrow the engine.** Never redefine `D` helpers that already exist;
  add surface-specific ones (`D.pill`, `D.step`, `D.renumber`). Keep names short and verbal.
- **`#stMsg` and `#term`** are the two ids the core touches by convention: `D.msg()` writes
  to `#stMsg`, `D.tline/prompt` append to `#term`. Include them if the surface has anywhere
  sensible to put them; omit them and those helpers simply no-op.
- **`.stage` is 1600×1000, always.** Set its `display`/`grid-template-rows` in your
  surface.css. Do not change the stage size — every script, the connector overlay and the
  16:10 aspect assume it.
- **Class conventions the engine relies on:** `.lit` = "this element is being called out",
  `.busy` on `.stage` = work in progress, `.caret` = blinking cursor. Style them; do not rename them.
- **Two states minimum for anything animated** — a resting state and a lit state with a
  `transition`, so a stage can be replayed.
- **The starter storyboard must run end-to-end unedited** and look plausible in a
  screenshot. It is the thing an author reads to learn the surface.

## Checklist before committing a surface

```bash
python scripts/new_demo.py -s <name> -o /tmp/x.html --force
python scripts/snap.py /tmp/x.html --outdir /tmp/snaps      # look at EVERY stage
```

- [ ] every stage renders with no JS errors (snap.py prints them)
- [ ] stage N looks right when jumped to directly (replayable from `reset()`)
- [ ] no dead space: the surface looks like a working day, not a demo fixture
- [ ] chrome checklist for this platform is complete (window controls, nav, status)
- [ ] NOTES.md: what to fill in, markup rules, helper table, story shape
- [ ] add a row to the surfaces table in SKILL.md

## Surfaces worth adding next

mobile app (phone frame), chat/messaging client, notebook (Jupyter), CI pipeline view,
map/geo tool, 3D viewer, design canvas, spreadsheet, wearable/embedded display.
Each is an afternoon of CSS and buys a whole category of demos.
