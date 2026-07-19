---
name: kanban-multi-agent
description: |
  Multi-agent Kanban workflows for Hermes. Covers the orchestrator playbook (decomposition, routing,
  anti-temptation rules) and the worker lifecycle (orient → work → heartbeat → block/complete),
  plus tenant isolation, workspace handling, and good handoff shapes.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, worker, routing, workflow, kanban-board]
---

# Kanban Multi-Agent Workflows

This skill covers the Hermes Kanban system for dispatching work across multiple agent profiles via a shared task board.

## Roles

| Role | Responsibility | Loads this skill when... |
|------|---------------|---------------------------|
| **Orchestrator** | Decomposes user requests, creates cards, assigns to workers, reviews results | You're the entry point routing work |
| **Worker** | Picks up assigned cards, executes tasks, reports progress, completes or blocks | You're spawned as a `kanban-worker` |

---

## Orchestrator Playbook

### Step 0: Discover Available Profiles

Before fanning out, discover what profiles actually exist on this machine:

```bash
hermes profile list
```

Unknown assignee names silently fail — the dispatcher doesn't autocorrect or fall back. A card assigned to `researcher` on a setup with only `docker-worker` sits in `ready` forever.

### When to Use the Board

1. Multiple specialists needed (research + analysis + writing)
2. Work should survive crash/restart (long-running, recurring, important)
3. Human-in-the-loop at any step
4. Multiple subtasks can run in parallel

### Anti-Temptation Rules
- **Decompose, don't execute.** The orchestrator's job is routing, not doing.
- **One concern per card.** Don't bundle unrelated tasks.
- **Define done criteria.** Every card needs a clear completion signal.

### Good Card Shape
```yaml
title: "Implement OAuth2 login"
description: |
  Add Google OAuth2 to the auth module.
  Done when: login button works, callback handler exists, tests pass.
acceptance:
  - "User can click 'Login with Google'"
  - "Callback exchanges code for token"
  - "Unit tests cover happy path and error path"
```

---

## Worker Lifecycle

The core lifecycle is auto-injected into every worker's system prompt as `KANBAN_GUIDANCE`. This skill provides deeper detail on edge cases.

### Phases
1. **Orient** — read the card, understand the task, check workspace.
2. **Work** — execute the task, use terminal/file tools as needed.
3. **Heartbeat** — report progress if the task runs long.
4. **Block** — if stuck, report blockers with specific error messages.
5. **Complete** — summarize results and hand off to downstream workers.

### Workspace Handling

| Kind | What it is | How to work |
|------|-----------|-------------|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely; GC'd on archive. |
| `dir:<path>` | Shared persistent directory | Other runs read what you write. Treat as long-lived state. |
| `worktree` | Git worktree at resolved path | Run `git worktree add` if `.git` doesn't exist, then commit here. |

### Tenant Isolation
If `$HERMES_TENANT` is set, prefix memory entries with the tenant:
- Good: `business-a: Acme is our biggest customer`
- Bad: `Acme is our biggest customer` (leaks across tenants)

### Good Handoff Shapes

**Coding task:**
```python
kanban_complete(
    summary="Implemented OAuth2 login in src/auth/oauth2.py",
    metadata={"files_changed": ["src/auth/oauth2.py", "tests/test_oauth2.py"], "tests_pass": True}
)
```

**Research task:**
```python
kanban_complete(
    summary="Found 3 viable hosting providers; comparison table in workspace/providers.md",
    metadata={"recommendation": "Render", "budget_match": True}
)
```

---

## Pitfalls

- **Silent failures**: unknown assignee names don't error — they just never get picked up.
- **Workspace leaks**: `dir:` workspaces persist across runs. Clean up temporary artifacts.
- **Git worktree orphaning**: if a worktree task crashes, the worktree may remain. Check with `git worktree list`.
- **Context budget**: workers have limited context. Don't dump entire repos into the card description.
