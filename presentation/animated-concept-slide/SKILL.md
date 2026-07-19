---
name: animated-concept-slide
description: Build a Slidev lecture slide whose body is a single conceptual SVG diagram that morphs through 4-6 phases on a continuous auto-loop. Use for ANY topic where one architecture / one protocol / one workflow / one system evolves through distinct states — attack timelines, protocol walkthroughs (TLS handshake, ZK proof verify, bridge message flow), state-machine lifecycles, before-after refactors, config-change demonstrations, layered-architecture explainers, deployment pipelines, request lifecycles, consensus rounds, anything that goes A → B → C → D within the same set of actors. Trigger this skill whenever the user asks for any of: "アニメで見せる", "morphing diagram", "動く図", "再現", "可視化", "concept diagram", "drill-down", "深掘り", "ascon-proposal みたいに", "もっと手触り感", "1 枚で流れを見せる", "図がそのまま動く感じ" — or when an existing static slide (comparison table, bullet list, side-by-side panels) should be converted into a single morphing diagram. The pattern is topic-agnostic; the SVG actors, color states, and phase captions change per slide but the machinery is identical.
---

# Animated concept-diagram slide

A reusable Slidev pattern: one Vue component renders one SVG that auto-morphs through 4-6 phases on a continuous loop. The story is told by the diagram changing in place, not by switching slides, stepping panels, or scrolling bullets.

This pattern works for any topic with a sequence of states inside a stable architecture. The actors and colors change per topic; the machinery does not.

**Read [CLAUDE.md §15](../../../CLAUDE.md)** in this repo for the project-specific scaffold (exact viewBox, fonts, palette, file paths, verification commands). The reference implementation is `components/KelpAttackDemo.vue` paired with `slides/SL08b.md` — read both before starting any new instance because they encode alignment, color, and timing decisions that took several iterations to find.

## When this pattern wins

Use when the slide needs to convey **a sequence of state changes inside a stable set of actors**. The actors stay put; their states change. The viewer's eye anchors on each actor and watches it transform.

Concrete topic types it's been used (or could be used) for:

- **Protocol walkthrough** — TLS handshake (client/server/cert authority round-trips), ZK proof verification (prover/verifier challenge rounds), cross-chain bridge message flow (source → relayer → destination), consensus rounds (proposer → voters → finality).
- **System architecture explainer** — request flowing through CDN → load balancer → app server → cache → DB, each layer lighting up as the request hits it.
- **Attack / failure timeline** — KelpDAO × LayerZero exploit (multi-DVN multisig collapses to 1, RPCs get DDoS'd, false attestation), Bybit/Safe wallet attack (UI vs calldata divergence over phases).
- **Before-after / evolution** — config change (3 DVNs → 1 DVN), migration (monolith → microservices), refactor sequence (extract module → introduce interface → swap impl).
- **State machine / lifecycle** — transaction lifecycle (pending → mempool → block → confirmed → finalized), deployment pipeline (build → test → stage → canary → prod), order lifecycle.
- **Concept progression** — sumcheck protocol rounds (polynomial degrees collapse), MPC computation (parties exchange shares), zkVM execution trace (CPU cycle → instruction → memory effect).

Use a different pattern when:
- The story is a static comparison (X vs Y) → horizontal 3-card layout (see `inputs/rules.md` §3)
- The diagram is a single still figure → Mermaid or static SVG asset under `public/images/`
- The narrative actually needs separate slides (different topics, not states of one topic) → split into multiple SL pages

## Anatomy (two files)

```
slides/SL<NN>.md              # ~30 lines — title + <YourDemo /> + sources footer + speaker notes
components/<YourDemo>.vue     # ~500 lines — phase machinery + SVG + scoped CSS
```

The slide markdown carries no body content beyond the title and component mount — verbose lecture context lives only in speaker notes. The component carries all visual logic.

Naming convention: `<Topic>Demo.vue` and `SL<NN>b.md` for drill-downs that follow an overview slide. The "b" suffix marks "drill-down companion to NN". The component class prefix should be short and unique (`kf-` for kelp flow, `bd-` for bybit demo, `th-` for TLS handshake) so scoped styles don't collide.

## Phase machinery (Vue 3 composition)

A `phase` ref auto-advances via `setTimeout` with per-phase durations (config-change moments want longer hold than DDoS-burst moments). Visual state is derived via `computed()` from `phase.value`; CSS transitions on `fill`/`stroke`/`opacity`/`transform` do the actual morphing.

```ts
const totalPhases = 6
const phaseDurations = [3500, 4500, 3500, 4500, 5000, 4500]  // ms per phase

// Sync init from URL — required for screenshots and lecturer deep-links
function getInitialPhase() {
  if (typeof window === 'undefined') return { phase: 0, play: true }
  const p = new URLSearchParams(window.location.search)
  const raw = p.get('phase') ?? p.get('stage')
  if (raw == null) return { phase: 0, play: true }
  const s = parseInt(raw, 10)
  return (!Number.isNaN(s) && s >= 0 && s < totalPhases)
    ? { phase: s, play: false }   // pinned phase → no auto-advance
    : { phase: 0, play: true }
}
const initial = getInitialPhase()
const phase = ref(initial.phase)
const isPlaying = ref(initial.play)
```

The `?phase=N` URL hook is non-negotiable. Without it Firefox CLI screenshots (which fire at page-load before any animation runs) can only capture phase 0, and the lecturer cannot deep-link to a phase in their notes. Initialize `phase` *synchronously* from URL (not inside `onMounted`) — otherwise the first render uses phase=0 and Vue's keyed transitions catch mid-flight, leaving the wrong value on screen at screenshot time.

Pick `totalPhases` based on the story's natural beats (typically 4-6). Pick `phaseDurations` per beat — pivotal moments (a config flips, a node fails) want ~4500ms; transient bursts (DDoS impact) want ~3500ms; the climax / drain / final state wants ~5000ms.

## One SVG, single coordinate system

Everything visual lives in **one** `<svg viewBox="0 0 1200 ~430">`. Don't overlay HTML divs on an SVG wire layer:

- Single coordinate system means a node at `x=600` aligns with a wire ending at `x=600` with no layer-positioning math
- CSS transitions on SVG attributes compose cleanly with Vue `<transition>` for enter/leave
- Traveling particles are just `<circle>` with CSS `@keyframes` animating `transform: translateX(Npx)` along a wire

viewBox 1200 wide gives 1 SVG unit ≈ 1 px on screen (slide canvas is 1280 wide). Use that as your mental scale when picking font sizes.

## State morphs, not state switches

The core visual idiom is *state classes that morph an existing element*, not branches that swap markup:

```vue
<g class="td-actor"
   :class="{ 'is-active': stage === i,
             'is-done':   stage >  i,
             'is-failed': failed && i === failPoint }">
  <rect class="td-actor-bg"/>
  <!-- icon + label -->
</g>
```

```css
.td-actor-bg { fill: white; stroke: #94a3b8; transition: fill .5s, stroke .5s; }
.td-actor.is-active .td-actor-bg { stroke: #dc2626; fill: #fef2f2;
                                   filter: drop-shadow(0 0 6px rgba(220,38,38,.5)); }
.td-actor.is-done   .td-actor-bg { stroke: #10b981; fill: #f0fdf4; }
.td-actor.is-failed .td-actor-bg { fill: #1f2937; stroke: #dc2626; }
```

The element never unmounts. Its colors and accents shift. The viewer's eye stays anchored on the same actor while the actor's *state* tells the story. This is what makes the animation feel cinematic instead of slideshow-y.

Reserve `v-if` for elements that genuinely don't exist yet — the "drain" callout that appears only on the last phase, the "consensus reached" badge that appears only after enough votes, the new component that gets introduced mid-evolution. Everything that persists across phases should be a state class.

## Actors as iconic shapes

Each node gets an SVG-drawn iconic representation of its role, above (or beside) its text label, both centered in the node rect. Drawn as inline `<path>`/`<circle>`/`<rect>` — no external icon library. The icon establishes the actor's *role* so the label can be short.

| Actor type | Icon idea |
|---|---|
| Human user / client | stick figure (circle head + trapezoid body) |
| HTTP request / message | envelope (`<rect>` + flap line) |
| Verifier / signer / authority | shield (pentagon + check mark) |
| Datastore / vault / contract holding value | vault (square + center circle + cross) |
| Server / node / RPC | stacked rectangles with LEDs |
| Gear / processor / executor | gear or hexagon |
| Block / step / state | rounded rect with state label |
| Cache / queue | stacked tubes or layered rects |
| Network / cloud / external | cloud silhouette or dashed boundary |

For sub-actors stacked inside a cluster (e.g. multiple signers, multiple shards), icon-left + text-right works better than icon-above due to height constraints. Make sure the icon-text pair is visually centered on the box center (not just left-aligned with padding).

## Grouping for boundaries (chain bands or equivalent)

When the diagram crosses a system boundary (chain A ↔ chain B, trust zone ↔ untrusted, client ↔ server, on-chain ↔ off-chain, before ↔ after), wrap each side's actors in a dashed `<rect>` with a small label. The boundary becomes visual, not textual.

```svg
<rect x="50" y="30" width="395" height="125" rx="8"
      fill="rgba(99,102,241,0.05)" stroke="#94a3b8"
      stroke-width="1.5" stroke-dasharray="6 4"/>
<text x="65" y="50" font-size="14" font-weight="700" fill="#4f46e5"
      letter-spacing="0.12em">CLIENT SIDE</text>
```

Use tinted backgrounds (~5% opacity) for each side. An off-boundary entity (a relay, an off-chain verifier, a CDN, a queue) sits *outside* any band — its between-bands position tells the viewer it belongs to neither.

## How phase progression is communicated (no bottom phase bar)

**Do not add a bottom phase bar with caption + dots + ⏸▶⟲ buttons.** It looks like a useful affordance but it pulls the viewer's eye away from the diagram and reintroduces panel-thinking through the UI. The figure itself should communicate phase progression.

Use these three channels instead:

1. **A `code` / `formula` / `config` strip above the SVG** — one short line per phase, swapped via `<transition name="...-fade" mode="out-in">`. Carries the technical content (assignment, predicate, config setting) — viewer can ignore it and still follow the diagram.

   Caption examples across topic types:
   - protocol: `① ClientHello` / `② ServerHello + cert` / `③ key exchange` / `④ finished`
   - attack: `setConfig(requiredDVNCount: 1)  // 1-of-1 — 1 票で release`
   - proof: `π ← Prove{ ∃W : exploit(W, C) = drain }`
   - architecture: `idle` / `request lands at LB` / `cache hit` / `DB query` / `response`

2. **Color-state changes on the actors themselves** — healthy → compromised → failed, idle → active → done. The viewer's eye anchors on each actor and watches it change. This is the primary signal.

3. **`v-if` for transient climax elements** — drain box at phase 5, accepted ✓ badge after verify, "HALTED" banner when paused. Out of view until the moment they matter.

Never put a "STEP 3/5" header, breadcrumb, or progress indicator inside the diagram — that's panel-thinking, which this pattern explicitly avoids.

`?phase=N` URL pinning (for screenshots and lecturer deep-links) still works without any UI — it's read in the sync init function.

## Speaker notes carry the lecture

The slide body is a silent diagram. The verbal lecture lives in the speaker notes, structured as:

```markdown
<!--
Speaker Notes:
【概要】<topic in 1-2 sentences>
【前提】<assumptions, hypothetical scenarios, key constraints>
【図の読み方】<which actor is what, how to follow the flow>
【各 phase の物語】
  phase 0 — ...
  phase 1 — ...
  ...
【講義での強調点】<the actual lesson — why this matters>
-->
```

The notes can be verbose because they double as the handout / printed reference. The diagram itself stays terse — title (1 line) + minimal labels + state colors + phase caption.

## Iteration loop (this is where the design earns its quality)

A first-cut animated slide will look wrong in 3-5 specific ways regardless of topic. Plan for 5-7 iterations with the user. The typical feedback arc (this has been observed empirically — future iterations will hit the same things):

| Iteration N feedback | Forces this fix |
|---|---|
| "step-by-step panels are confusing" / "ステップごとの図だとわかりづらい" | concept-diagram over pipeline, single morphing SVG |
| "actors should look like actors, not just text" / "アクターっぽくしたい" | SVG-drawn icons instead of text-only boxes |
| "position is off" / "位置がずれてる" | icon-above-text centered, not icon-left-text-right drift |
| "bottom is overflowing" / "下にはみ出てる" | shorter viewBox, tighter line heights |
| "title is verbose" / "タイトルくどい" | single-line title; verbose context → speaker notes |
| "arrows too short / spacing tight" / "もっと矢印伸ばして" | 55px+ gaps, centered diagram |
| "small text won't be readable" / "文字小さい" | ≥14px floor, remove sub-labels and detail lines |

Each iteration cycle:

1. **Edit** the Vue component (state, layout, fonts, icons)
2. **Build**: `bun run build` (~7s)
3. **Ensure SPA server** is running on port 4002 (`python3 /tmp/spa_server.py`)
4. **Screenshot each phase** with parallel attempts to dodge blank-page race:
   ```bash
   for p in 0 1 2 3 4 5; do
     for a in 1 2 3 4; do
       firefox --headless --window-size=1920,1080 \
         --screenshot=/tmp/_p${p}_a${a}.png \
         "http://localhost:4002/${SLIDE_N}?print&phase=${p}" 2>/dev/null &
     done
     wait
     # take the largest file (smallest = blank from race)
   done
   ```
5. **Read each PNG** with the Read tool and look critically
6. **Take the user's feedback verbatim** — don't "improve" beyond what they said

By the time you land, the slide should contain only: title (1 line) + code/formula strip (1 line, phase-driven) + SVG (icons + names + state-driven colors + transient v-if climax) + sources footer. **No bottom phase bar / no panel UI.** Nothing else.

## Adapting to a new topic

Starting from the reference implementation (`components/KelpAttackDemo.vue`), the swap-out checklist:

1. **Rename component + CSS prefix** — `<Topic>Demo.vue` + new prefix like `th-` / `tx-` / `dp-`
2. **Define actors** — what shapes does this topic have? (client/server, prover/verifier, services in a layered architecture, signers in a multisig, RPC nodes, etc.)
3. **Pick icons** — match each actor to an iconic shape from the table above (or design new ones)
4. **Define states** — what colors mean what? (healthy/active/failed/pending/done — pick a 3-5 state palette and stick with it)
5. **Write phase definitions** — code/formula strip (short caption per phase) + computed states derived from `phase.value`
6. **Position actors** — bridge highway (horizontal flow) is one layout; protocol round-trip (zig-zag between two columns) is another; layered architecture (vertical stack) is another. Pick what matches the topic.
7. **Add grouping bands** if the topic has boundaries (chains, trust zones, sides of a protocol)
8. **Wire the optional bits** — particles flowing along wires (for messages/requests), drain/result callout at the end (for the climax)
9. **Write speaker notes** carrying the lecture
10. **Iterate** — screenshots per phase, take user feedback verbatim, adjust

The machinery (phase ref, URL init, sync init, CSS transitions, screenshot loop) stays identical across topics. The actors / colors / layout / captions change.

## What this skill is *not*

- Not a generic Slidev component generator — it specifically produces the "story unfolds inside one architecture" pattern
- Not for 3D scenes — the `ascon-proposal` branch uses Three.js for live 3D, which is a different pattern; if the user explicitly wants 3D, point them there
- Not for static reference diagrams (Mermaid wins) or comparison slides (horizontal cards win)

## Reference

`components/KelpAttackDemo.vue` + `slides/SL08b.md` in this repo is the canonical full instance. Read both before starting a new one. [CLAUDE.md §15](../../../CLAUDE.md) lists every concrete knob (exact font sizes, color palette, file paths, gap distances, viewBox dimensions, screenshot commands) — use it as the project's authoritative style guide for this pattern.
