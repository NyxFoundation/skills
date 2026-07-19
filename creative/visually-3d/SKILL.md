---
name: visually-3d
description: >
  Turn a text description of a machine, chip, or algorithm into an inspectable 3D model plus a
  formally verified implementation, using the NyxFoundation/visually-3d CLI (driven by your local
  Claude/Codex CLI — no API keys). Load when the user wants a 3D visualization of hardware/algorithms,
  "Visioned Vibe Coding", or asks to visualize/verify/refine/invent a machine concept.
allowed-tools: bash, read, write
---

# SKILL: visually-3d (git-based tool)

## Setup

The tool is the public repo `NyxFoundation/visually-3d`. Use whichever is available:

```bash
# One-shot (recommended)
npx visually-3d --help

# Or a persistent clone
git clone https://github.com/NyxFoundation/visually-3d.git "${VISUALLY_SRC:-$HOME/workspace/visually-3d}"
cd "${VISUALLY_SRC:-$HOME/workspace/visually-3d}" && npm install && node bin/visually.js --help
```

Requires Node ≥ 18 and a local `claude` (or `codex`) CLI on PATH. No API keys, no cloud accounts.
Scenes live under `~/.visually-3d/scenes` (override with `$VISUALLY_HOME`); every run is logged under
`~/.visually-3d/runs/`.

## Core loop: visualize → verify → refine

```bash
visually visualize "<scene or name>" [--url <paper-url>] [--iters N] [--driver claude|codex]
visually verify <scene> [--backend <id>]      # z3/SMT for circuits & algorithms, sim for machines
visually refine <scene> [--rounds 3] [--visual 90]   # closed loop until visual goal met AND source verifies
```

- `visualize` fetches ground-truth evidence (reference paper + real source code) and builds/improves
  the 3D model grounded in it.
- `verify` formally verifies the gathered source with the auto-selected backend. Run `visualize` first.
- `refine` ratchets visualize → verify on the best scene until the goal is met or max rounds.

## Other verbs

```bash
visually                       # interactive TUI control panel
visually serve [--no-open]     # local web GUI
visually invent <scene> [--rounds 3] [--contradiction "…"]   # invention loop with falsifiable predictions
visually check <scene> [--png] # inspect a scene (browser or PNG contact sheet)
visually upload <scene>        # publish to the public web gallery (commit+push or fork+PR, auto-detected)
```

## Honesty rules

- `invent` records falsified predictions as honest kills — never report a falsified concept as verified.
- Only claim "verified" when the backend (SMT/sim) actually passed; otherwise report the failing metrics.
- For full documentation read `README.md` and `CLAUDE.md` in the repo clone.
