# surface: webapp

A browser window over a light SaaS app — for dashboards, admin tools, review queues, workflow products, anything a non-developer would be shown.

## What to fill in

| Part | What it must say |
|---|---|
| browser tab + URL | the product's real name and a plausible path (`app.product.com/runs`) |
| side nav | 4–5 sections; the current one `on`. Real products have a boring nav |
| header | page title, the primary action button, a search box |
| `.kpis` | 4 numbers a user actually watches — always animate them with `D.count` |
| `.trows` | 10–14 rows so the table looks lived-in; real-sounding names, not "record one" |
| `.drawer` | the payload: what happened, the evidence, the fix. Fill it — an empty drawer looks fake |
| `.toast` | one confirmation, not a stream of them |

## Markup rules

- Keep the light palette. The point of this surface is that it does *not* look like an IDE;
  if the product is dark-themed, override the `:root` vars rather than reaching for the ide surface.
- Status is a `.pill` inside the row: `ok | bad | warn | run` (the `run` pill spins).
- The canvas reflows when the drawer opens (`padding-right`), so the row the drawer
  describes stays visible. Don't cover the row you are talking about.
- Rows scroll in `.trows` (`D.scrollTo('rows', 'r7', 120)`), not the page.

## Surface helpers (on top of the core D.*)

| helper | use |
|---|---|
| `D.pill(rowId, kind, label)` | row status pill |
| `D.drawer(on)` | slide the detail drawer in, reflowing the canvas |
| `D.toast(text, kind, ms)` | bottom-right toast; `ms=0` keeps it up |
| `D.cta(label, busy)` | header button label/state |
| `D.lit(rowId)` | highlight the row the story is about |
| `D.busy(on)` | progress line under the header |

## Story shape that works

idle dashboard with real numbers → the user starts the job → rows work through one by one
→ the one row that fails, with the KPI turning → the drawer opens: what happened, evidence,
fix → applied, row green, toast, numbers settle.

The viewer must believe the *queue* is real: keep the other rows moving while the failing
one is being explained. A world that freezes around the demo point reads as a mockup.
