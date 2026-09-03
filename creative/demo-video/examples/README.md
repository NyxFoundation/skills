# Examples

Finished demos, kept as reference material — open one next to the surface's `NOTES.md`
when you want to see how far the chrome should be filled in.

| file | surface | story |
|---|---|---|
| `ide-solidity-check-envelope.html` | ide | A Solidity hook checked against a Lean spec: redundant checks struck through, a missing-check gap revealed with a counterexample and a cross-pane connector, the fix typed in and re-verified |

These are **built** artifacts (engine + chrome + story inlined), not templates.

Read them for the *content* standard — how densely the chrome is filled, how real the code
and the findings are, how the beats land — not for the API: the Solidity one predates the
shared engine and carries its own hand-written runtime and `s1…s5` stage classes. Start new
demos from `scripts/new_demo.py`, and copy content out of an example rather than copying the
file, unless the new story is nearly the same story.

## Adding an example

Drop the finished HTML here with a `<surface>-<slug>.html` name, add a row above, and say in
one line what the story is. If it is a demo of a real Nyx tool, record the MP4/GIF elsewhere
(this repo stays text) and link it from the tool's own README.
