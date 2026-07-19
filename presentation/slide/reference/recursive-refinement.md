# Recursive self-improvement — render → critique → edit → re-render

A slide is judged by the pixels it renders, not the markdown it's written in. So
the only honest way to improve one is to **export it to an image, look at the
image, and edit toward a defect you can see** — then re-render to confirm you did
not regress. This is the visually-3d self-improvement methodology applied to
slides. Two acceptance harnesses ship in the repo (`make refine`, `make polish`);
for one or two slides, run the loop yourself in-conversation.

## The loop (run this per slide, or per small batch)

1. **Render** the current deck to per-slide PNGs (commands below).
2. **Open every PNG with the Read tool** — score what the audience actually sees.
3. **Critique before editing** (Self-Refine, Madaan 2023): write down the
   specific defects and which slide ids they sit on.
4. **Apply 3–6 surgical `Edit`s** to `slides/SL*.md`, each tied to one named
   pixel-level defect. Prefer `Edit` over `Write`; never big-bang rewrite a slide
   that already works; never bundle unrelated changes.
5. **Re-render** as a regression guard. If the deck no longer exports, restore
   the last good version.
6. **Repeat** until convergence: every acceptance test passes and no remaining
   edit is worth ≥ 0.3 on the rubric. Carry unfinished items forward as explicit
   notes for the next pass (Reflexion, Shinn 2023).

Adopt only edits that *measurably* lift the weakest viewpoint (Gödel-machine
principle). Do not satisfy a rule's letter while betraying an acceptance test
(Goodhart caution).

## Three acceptance tests (every pass applies all three)

1. **Skim test** — flipping the renders alone (no speaker), the hook, the spine
   of the argument, and the close all land. Action titles carry the message; no
   slide is a wall of text.
2. **Want test** — every slide raises what the viewer wants through **evidence,
   not assertion**: a track record, a number, an apt comparison. A bare claim
   ("great value", "you'll be ahead") fails.
3. **Delivery test** — a senior leader could present it tomorrow: specific,
   credible, visually clean, on-brand.

## The five-persona panel — the deck's score is the *minimum*

Score the slide as each persona in turn; do not let any rubber-stamp. The score
is the **weakest** persona's — so it never converges until every viewpoint is
satisfied (multi-persona review resists premature convergence).

| key | Persona | Wants | Scores low when… |
|---|---|---|---|
| `donor` | 寄付検討者 | legitimacy, what the gift becomes, felt impact | vague use of funds / abstract results |
| `sponsor` | 懐疑的な企業スポンサー判断者 | concrete return, ROI, hard evidence, **apt comparison** | mismatched comparison / claim with thin proof |
| `researcher` | 同分野の研究者 | a real research agenda, substance, no hype | buzzwords / hollow technical claims |
| `layperson` | 非ドメインの一般聴衆 | follow it with zero prior knowledge | undefined jargon/acronyms / assumed background |
| `design_critic` | デザイン批評家 | intuitiveness, eye-flow, type large & high-contrast enough for an elderly viewer, visual hierarchy, minimal text | too much text / sub-legible type / a paragraph where a figure belongs / no single focal point |

Adapt the persona set to the deck's real audience — but keep `design_critic` and
`layperson`, the two that catch legibility and jargon defects regardless of
topic.

## The nine diagnostic lenses (use to *find* defects)

Clarity · Desire & Expectation Lift · Story · Emotional Impact · Credibility ·
Differentiation · Culture · Visual Readability · Executive Pitch Quality.

Two rules every persona enforces:
- **Show, don't tell.** An idea a chart / timeline / icon / single big number
  could carry faster must not stay a paragraph.
- **Comparisons must be apt.** Both sides on the same axis, A vs its real
  alternative B.
- **Legible & eye-flow.** Every element readable by an elderly viewer; one focal
  point; the layout guides the eye title → key visual → support. Competing focal
  points are a defect.

## Hard editing rules

- **Score the render, edit the markdown.** Tie every edit to a pixel-level defect
  a persona named.
- **Never invent facts.** Pull numbers from `inputs/`, `outputs/`, `public/`.
- **Match the deck's `output_language`** (Japanese decks omit `.ja` subtext).
- **Title overflow is non-negotiable** — a wrapped or clipped title is an instant
  defect.
- **Density budget:** title ≤ 24 全角 / 36 半角; 3–5 points × ≤ 80 chars.
- **Respect the font-size floor** (see `design-system.md` §3).

## Convergence

Stop when *every* persona scores ≥ 4.5 **and** no persona can name a concrete
edit worth ≥ 0.3. Also stop if the weakest score plateaus (no improvement across
a pass) — a plateau means the remaining gaps need a different approach, not
another identical pass.

## PNG export commands

Standard (Slidev's bundled chromium):

```bash
bun run build
bunx slidev export slides.md --format png --output dist-png --per-slide
# single slide: add --range 3   (or a list: --range 3,4)
```

Decks with live `<Scene3D>` 3D never reach network-idle (the WebGL loop runs
forever) and the default export hangs — screenshot after a fixed wait instead:

```bash
bunx slidev export slides.md --format png --output dist-png \
  --per-slide --wait-until none --wait 5000
```

`slidev export` needs `playwright-chromium`, deliberately NOT a `package.json`
dependency (its Chromium download breaks the Cloudflare build). Install on demand
without saving it:

```bash
npm install --no-save playwright-chromium
```

On NixOS the bundled chromium fails (missing libglib); pass a system browser:

```bash
CHROMIUM=$(nix-shell -p chromium --run "command -v chromium")
nix-shell -p chromium --run \
  "bunx slidev export slides.md --format png --output dist-png \
     --executable-path $CHROMIUM --per-slide"
```

If chromium cannot run at all, fall back to a headless Firefox screenshot of the
running dev/preview server (`firefox --headless --window-size=1920,1080
--screenshot=out.png "http://localhost:PORT/N?print"`), taking the largest of a
few attempts since first-paint timing varies.

Output lands at `dist-png/NN.png` (slide 1-indexed); open each with the Read
tool. `dist-png/` is git-ignored.

## The bundled harnesses (whole-deck automation)

The repo's `Makefile` ships two loops for batch refinement of an existing deck
(`slides.md` + `slides/` present):

- **`make refine [REFINE_ITERS=N]`** — externalized loop (`scripts/refine.sh`):
  each iteration renders per-slide PNGs, invokes Claude once to score the panel
  and apply surgical edits, then re-renders as a regression guard. Every
  iteration's prompt, PNGs, JSONL trace, and a deck snapshot are kept under
  `.refine/<timestamp>/` (git-ignored) for audit; it restores the last good deck
  if a pass breaks the build. Driven by `prompts/11_Visual_Self_Improvement.md`.
- **`make polish`** — a single agentic Claude call that loops internally
  (`prompts/10_Recursive_Self_Improvement.md`).

Use these for an established deck; use the in-conversation loop above for one or
two slides.
