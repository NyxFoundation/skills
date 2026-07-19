---
name: development-planning
description: |
  Software development planning and methodology: throwaway spikes, implementation planning,
  subagent-driven execution, and test-driven development (RED-GREEN-REFACTOR).
  Load when structuring HOW to build something (spike vs TDD vs delegation). To just write a
  plan document without executing, see skill plan.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, spike, prototyping, subagent, tdd, implementation, workflow, methodology]
    related_skills: [github-workflow, debugging, code-review-pipeline]
---

# Development Planning

This skill covers the planning and methodology layer of software development: validating ideas before building, writing actionable plans, executing via subagents, and enforcing TDD discipline.

---

## Spike — Throwaway Experiments

Before committing to a full build, run a quick throwaway experiment to validate feasibility.

### When to Spike
- Uncertain technical approach ("Can library X do Y?")
- Unfamiliar API or protocol
- Performance concern ("Will this be fast enough?")
- Integration risk ("Do these two services talk to each other?")

### Rules
1. **Timebox**: 30-60 minutes max. Set a timer.
2. **Disposable**: the spike code is throwaway. Do not commit it to main.
3. **One variable**: test exactly one hypothesis per spike.
4. **Document findings**: write a short summary of what worked, what didn't, and the recommended path forward.
5. **Kill or promote**: after the spike, either abandon the idea or write a real implementation plan.

### Pitfalls
- Scope creep: "While I'm here, let me also try Z..." — no. One hypothesis.
- Over-polishing: making the spike code production-ready defeats the purpose.
- Skipping the summary: without documented findings, the spike was wasted.

---

## Writing Implementation Plans

Transform a spec or requirements into an actionable markdown plan saved to `.hermes/plans/`.

### Plan Structure
```markdown
# Plan: <Feature Name>

## Goal
One sentence describing the desired outcome.

## Tasks
- [ ] Task 1 — bite-sized, exact file paths
- [ ] Task 2 — includes complete code examples
- [ ] Task 3 — verification steps

## Files
| File | Action |
|------|--------|
| `src/auth.py` | Add OAuth handler |
| `tests/test_auth.py` | Add unit tests |

## Verification
- [ ] All tests pass
- [ ] Linting passes
- [ ] Manual smoke test
```

### Rules
- Each task should be completable in ≤30 minutes.
- Include exact file paths and function signatures.
- Provide complete code examples, not stubs.
- Mark the plan as **no-execution** — the agent implements it in follow-up turns.

---

## Subagent-Driven Development

Execute implementation plans by dispatching independent subagents per task.

### Workflow
1. **Split the plan** into non-overlapping tasks.
2. **Dispatch** one `delegate_task` per task with a fresh context.
3. **Two-stage review**:
   - Stage 1: spec compliance — did the subagent follow the instructions?
   - Stage 2: code quality — is the result idiomatic and performant?
4. **Merge** results and run full test suite.

### When to Use Subagents
- Multiple independent tasks can run in parallel.
- The task is large enough that a single agent would lose context.
- Quality assurance requires a second set of eyes.

### Pitfalls
- Overhead: each subagent consumes tokens and time. Not worth it for trivial tasks.
- Context isolation: subagents don't share memory. Pass all needed state explicitly.
- Merge conflicts: scope tasks to non-overlapping files when possible.

---

## Test-Driven Development (TDD)

Enforce RED-GREEN-REFACTOR: write a failing test first, make it pass, then clean up.

### The Cycle
1. **RED**: write a test for the new behavior. Run it. It should fail.
2. **GREEN**: write the minimum code to make the test pass. No elegance yet.
3. **REFACTOR**: clean up the code while keeping all tests green.

### Rules
- No production code without a failing test first.
- Tests should be fast (<1s total).
- One logical assertion per test.
- Use descriptive test names that explain the behavior.

### When NOT to Use TDD
- Spikes and throwaway experiments (no tests needed).
- Purely mechanical refactors (existing tests cover it).
- UI-heavy features where behavior is visual and hard to assert programmatically.

### Example
```python
# RED
import pytest
from mymodule import add

def test_add_returns_sum():
    assert add(2, 3) == 5  # fails because add() doesn't exist yet

# GREEN
def add(a, b):
    return a + b  # minimum code

# REFACTOR
# (nothing to refactor here, but in real code you'd extract helpers, rename variables, etc.)
```
