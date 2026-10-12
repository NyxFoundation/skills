# surface: world

A 2D network map of a simulated world — agents on the left, the thing they all have to go through in the middle, contracts holding state on the right. For simulations, multi-agent systems, protocol/network demos, anything where the story is *traffic between nodes* rather than a screen someone is looking at.

## What to fill in

| Part | What it must say |
|---|---|
| top bar | what is being simulated, the run's identity (regime/seed/epoch), and a clock that ticks |
| left column (`.node.agent`) | the actors, with a real address and the one thing each is trying to do |
| `.chain` | whatever every actor must pass through — a chain, a broker, a scheduler. The mempool rows are where ordering becomes visible |
| right column (`.node.venue`) | the state holders, each with **one** number that the story will move |
| `.tape` (`#term`) | the log the system actually writes. Real event names, real timestamps, 25–30 lines by the end |
| `.board` | the scoreboard — the reason any of this mattered |

There is no "before" state worth showing on an empty map: bring nodes up with `D.up()` in the first beat so the viewer watches the world assemble.

## Markup rules

- Nodes are absolutely positioned inside `.map` (1600×620). Left column `left:36px`, right column `left:1328px`, rows every 76px from `top:24px`. Keep to that grid or the wires bend oddly.
- Node roles are classes: `.agent` (round dot), `.venue` (square dot), `.unk` (amber, an actor deployed it), `.evil` (rose, the adversary). The colour *is* the taxonomy — do not add a fourth hue for decoration.
- Both SVG layers must carry `width="1600" height="1000" viewBox="0 0 1600 1000"`; an inline `<svg>` without them silently renders 300×150.
- One number per node (`.st b`). A node with three numbers is a dashboard, and the eye stops following the motion.

## Surface helpers (on top of the core D.*)

| helper | use |
|---|---|
| `D.up(id, on)` | bring a node online (opacity + lift) |
| `D.wire(a, b, {from,to,midX,cls})` | draw a persistent wire; `cls` `'hot'` or `'evil'` |
| `D.hot(a, b, cls)` | restyle a wire that already exists |
| `D.tx(a, b, {midX,ms,colour,r})` | send a dot along that path; **await it** to sequence on arrival |
| `D.stat(id, value, mood)` | a node's number; mood `''｜moved｜gain｜loss` |
| `D.tag(id, kind, label)` | the corner badge: `ok｜warn｜bad` |
| `D.block(n)` | advance the clock and pulse the indicator |
| `D.mem(id, {what,who,fee,state,evil})` | a row in the block; `state` `'mined'｜'rev'` |
| `D.memClear()` · `D.feed(html)` | clear the block list · the line under it |
| `D.score(id, value, mood)` · `D.note(on)` | scoreboard row · the closing explanation |
| `D.rank()` | re-sort the scoreboard by value and renumber it |
| `D.newGen()` | **call first in `reset()`** — stops in-flight dots from a previous run |

## Story shape that works

world assembles → the actors join → one actor acts and a number on the far side moves →
several actors want the same thing and the ordering decides it → an actor introduces
something the system did not deploy → the adversary uses it → the scorer says what it was worth.

Two things carry it. **Await the dot**: state must change when the transaction *lands*, not
when it is sent — that one detail is what makes the map read as a simulation instead of an
animation. And **keep the world moving around the demo point**: the clock never stops, the
other nodes keep their numbers, nothing freezes while the interesting thing is explained.
