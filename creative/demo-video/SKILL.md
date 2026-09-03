---
name: demo-video
description: Build a realistic, animated "this is what it will look like" product demo as a single self-contained HTML storyboard, then record it deterministically to MP4/GIF with Playwright + ffmpeg. The chrome comes from a swappable surface pack — IDE/editor, terminal/CLI, browser SaaS app, and more added over time — so it fits any product, not just developer tools. Use whenever the user asks for a demo video, product teaser, 動作イメージ, イメージ映像, デモ動画, a GIF for a README or landing page, a mockup of something "in action", or a storyboard of a flow — especially before the thing actually exists. Also use it to make a rough HTML mockup look real, to re-record an existing demo at a different size, or to add a new surface pack.
---

# Demo video

Fake the product, not the platform. The output is one HTML file that looks like the real
thing, plays a scripted 30–40 s story on load, and records to MP4/GIF with one command.
Because every frame is deterministic, re-recording after a change costs nothing — which is
why HTML beats screen-recording at the storyboard stage, and why the asset can later be
swapped for a real recording without changing the story.

## Workflow

1. **Write the story first, in 5–6 beats** — one sentence each: *idle → trigger → first
   easy win → widen (a second pane/drawer/panel) → the real problem, revealed → the fix,
   applied and verified*. Read `references/storyboarding.md`. Ask the user only if the
   product's core "aha" is unclear; otherwise propose the beats and go.
2. **Pick the surface** the story is staged in (`python scripts/new_demo.py --list`):

   | surface | for |
   |---|---|
   | `ide` | editor extensions, LSPs, linters, analyzers, provers — value shows up next to code |
   | `terminal` | CLIs, build/test tools, coding agents, pipelines — value arrives as streaming output |
   | `webapp` | dashboards, admin tools, review queues — a product a non-developer is shown |

   None of them fit? Add one: `references/adding-a-surface.md` (four files, an afternoon).
3. **Assemble**: `python scripts/new_demo.py -s ide -o speca-demo.html -t "SPECA"`.
   The output is self-contained (engine + chrome + a runnable starter story inlined).
   Assemble once, then edit that file — re-running the assembler overwrites it.
4. **Fill the chrome and the content** per the surface's `NOTES.md` — real names, real
   paths, real idioms, 3–4 findings not ten, enough surrounding content that the demo
   point sits inside an ordinary working day.
5. **Script the beats in `D.define([...], reset)`** at the bottom of the file. Each stage
   must be re-runnable from `reset()` — that is what makes the numbered buttons, the
   keyboard digits and `snap.py` work.
6. **Check with stills before recording**: `python scripts/snap.py demo.html`, then look at
   every `snaps/stage-N.png` against `references/realism-and-pitfalls.md`. Fix, re-snap.
   A still shows layout bugs that motion hides.
7. **Record**: `python scripts/record.py demo.html --gif --seconds 34` → `demo.mp4` (+ `.gif`).
   `--seconds` must cover the whole story plus ~2 s. Hand the user the HTML, the MP4 and the
   record command together so they can re-render after an edit.

Scripts need Playwright and ffmpeg: `uv run --with playwright python scripts/snap.py …`
works without installing anything globally, and the scripts fall back to a system Chromium
when Playwright's own download is missing (NixOS) — override with `DEMO_CHROMIUM=/path/to/chromium`.

## Engine helpers (`D.*`, same on every surface)

| helper | use |
|---|---|
| `D.define(stages, reset)` / `D.go(n)` / `D.replay()` | the storyboard runner |
| `D.type(t, text, cps)` | typed text with human jitter (38 cps command, 60 cps code) |
| `D.sleep(ms)` | holds — 2 s on anything the viewer must read |
| `D.tline(html)` / `D.prompt()` / `D.endPrompt()` | terminal output with a blinking caret |
| `D.lit(t, on)` / `D.cls(t, name, on)` | reveal a called-out element / toggle any class |
| `D.count(t, to, fmt)` | ticking number — never reveal a total instantly |
| `D.scrollTo(box, target, offset)` | scroll a pane to a line/row |
| `D.link(a, b, opts)` / `D.unlink()` | dashed connector between two elements |
| `D.msg(s)` / `D.busy(on)` / `D.caption(s)` | status text / progress state / narration caption |
| `D.text` `D.html` `D.q` `D.qa` `D.box` | DOM shorthands (`D.box` = rect in stage coordinates) |

Targets take a bare id (`'W1'`), a selector (`'.ln.err'`) or an Element.
Keyboard: digits jump to a stage, `r` replays. `?rec=1` hides the authoring controls and is
what the scripts use.

## Style rules that matter

- **One "wow" per demo** (the cross-surface moment: connector, drawer, auto-applied fix that
  re-verifies). Everything else quiet and correct.
- Product chrome and tool output in **English** even for Japanese audiences — that is what
  their real editor/terminal/app shows. Japanese goes in captions or the slide around the video.
- Short inline messages (≤ 45 chars); long explanations in a peek, drawer or terminal box.
- Hold 2 s on anything to be read; never stack reveals < 300 ms apart; animate every number.
- Don't invent a palette or a font for the chrome — the surface packs' platform tokens are
  the point. Spend your product colour on the one thing the tool contributes.
- Don't invent benchmark numbers the user hasn't given you; use obviously round placeholders
  and tell them which to replace.

## Files

- `scripts/new_demo.py` — assemble a demo from core + a surface pack (`--list`, `--force`)
- `scripts/snap.py` — per-stage PNGs for review · `scripts/record.py` — HTML → MP4 (+GIF)
- `core/` — `engine.css`, `engine.js`, `shell.html`: the stage, the runner, the helpers.
  Surface-agnostic; edit only when a helper is missing for *every* surface
- `surfaces/<name>/` — `surface.css` / `surface.html` / `surface.js` / `storyboard.js` / `NOTES.md`
- `examples/` — finished demos worth copying from (see `examples/README.md`)
- `references/storyboarding.md` — beats, timing table, holds, length, honesty
- `references/realism-and-pitfalls.md` — what makes it read as real, and every rendering bug
  already hit once (read when a screenshot looks wrong)
- `references/adding-a-surface.md` — how to add a new surface pack, with a review checklist
