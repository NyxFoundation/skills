# Storyboarding a demo

Read this before writing any HTML. The story is the deliverable; the chrome is packaging.

## Write the beats first — 5–6 sentences, one per beat

Every demo that worked had the same skeleton, whatever the surface:

1. **idle** — the world as it is, believable and quiet
2. **trigger** — the user runs the tool (typed command, button, save)
3. **first easy win** — something correct and small lands. Establishes competence
4. **widen** — a second surface opens (pane, drawer, panel) that the tool reasons with
5. **the real problem** — the finding nobody would have caught alone. This is the demo
6. **resolution** — the fix applied and *verified*, then a summary the viewer can screenshot

Ask the user only if the tool's core "aha" is unclear; otherwise propose the beats and go.
Beat 5 is what people remember — if you cannot name it in one sentence, the demo has no point yet.

## One "wow" per demo

Pick a single moment that only this tool could produce: a cross-pane connector, an
auto-applied fix that re-verifies, a counterexample nobody expected. Everything else
should be quiet and correct. Two wows read as an ad; none reads as a screen recording.

## Timing that feels right (30–40 s total)

| beat | seconds | what happens |
|---|---|---|
| idle | 0–1 | the world, a blinking caret |
| trigger | 1–5 | command typed at ~38 cps, or a button that goes busy; 4–5 output lines 300–500 ms apart |
| first win | 5–9 | the first reveal cascades 600 ms apart, a counter ticks |
| widen | 9–12 | the second surface slides in (700 ms), showing "waiting…" |
| the problem | 12–16 | reveal → explanation → connector, 350 ms apart |
| the fix | 18–26 | 2 s hold on the explanation, typed fix at ~60 cps, 1.4 s re-check, ✓ |
| wrap | 26–30 | summary view: counts settled, the fixed item struck through |

Rules that come out of that table:

- **Hold 2 s on anything the viewer must read.** Text that appears and moves is text nobody read.
- **Never stack two reveals within 300 ms.** The eye can only follow one change at a time.
- **Animate every number** (`D.count`) — an instantly-correct total looks like a static mockup.
- **Show elapsed time** (`(1.8s)`, `0.9s` per step). Work that takes no time reads as fake.
- **Nothing important in the first 0.8 s** — that is trimmed as the font-swap settle window.

## Length and format

- README GIF: 20–25 s, and make beat 5 land before 15 s — most viewers leave before the loop.
- Conference/landing-page MP4: 30–40 s is the ceiling. Longer needs narration, which is a different asset.
- Recording at 1600×1000 and letting the page scale is the default; `--width 1920 --height 1200` for 1080p-ish.

## Language

Product chrome and tool output in **English** even for Japanese audiences — that is what
their real editor/terminal/app shows. Keep Japanese for captions (`D.caption`) or slide
copy around the video if the user wants it.

## Honesty

This is a storyboard of a tool that may not exist yet, so the *claims* must be ones the
tool will actually be able to make: real file paths, plausible timings, findings a
practitioner would nod at. Do not invent benchmark numbers the user has not given you —
ask, or use obviously round placeholder values and tell them which numbers to replace.
