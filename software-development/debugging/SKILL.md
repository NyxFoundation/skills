---
name: debugging
description: |
  Systematic debugging across Python, Node.js, and general software.
  Covers the 4-phase root-cause methodology, Python pdb + debugpy remote (DAP),
  Node.js --inspect via Chrome DevTools Protocol, and Hermes TUI slash-command debugging.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, python, nodejs, pdb, debugpy, dap, cdp, root-cause, troubleshooting, tui]
    related_skills: [test-driven-development, github-workflow]
---

# Debugging

This skill covers debugging techniques across runtimes (Python, Node.js) and the systematic methodology for finding root causes before fixing.

---

## Systematic Debugging — 4-Phase Root Cause

Before touching any code, follow this sequence:

1. **Understand the bug**: reproduce it reliably, write down the exact symptom vs expected behavior.
2. **Form a hypothesis**: what could cause this? List at least 3 possibilities ranked by likelihood.
3. **Design an experiment**: the cheapest way to falsify one hypothesis. This could be a log line, a temporary patch, or a test case.
4. **Verify the fix**: after the change, run the reproduction case. Also run the full test suite to catch regressions.

### Key Principles
- **Don't fix what you don't understand.** A fix that works by accident is a future bug.
- **Bisect ruthlessly.** Use `git bisect` if the bug appeared recently.
- **Add telemetry before fixing.** If you can't reproduce locally, add logging and redeploy.
- **Write a regression test.** Every bug fix should come with a test that fails before the fix and passes after.

---

## Python Debugging — pdb + debugpy

### pdb (built-in, always available)

```python
import pdb; pdb.set_trace()  # drop into REPL at this line
```

**Commands inside pdb**
- `n` — next line
- `s` — step into function
- `c` — continue
- `p <expr>` — print expression
- `l` — list source
- `q` — quit

### debugpy (remote DAP debugger)

Use when you need to debug a running process (e.g., a server, a background job) from VS Code or another DAP client.

**Setup**
```bash
pip install debugpy
```

**Launch**
```python
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()  # blocks until VS Code attaches
```

**Attach from VS Code**
```json
{
  "type": "python",
  "request": "attach",
  "connect": { "host": "localhost", "port": 5678 }
}
```

**Pitfalls**
- `debugpy` does not work with `pdb` active in the same process.
- Set `DEBUGPY_LOG_DIR` for verbose logging when attach fails.
- In containers, expose the debug port and use `host.docker.internal`.

---

## Node.js Debugging — --inspect + Chrome DevTools Protocol

**Start Node with inspector**
```bash
node --inspect-brk=0.0.0.0:9229 script.js
```

**Connect with Chrome**
1. Open `chrome://inspect`
2. Click "Open dedicated DevTools for Node"
3. The debugger pauses on the first line; click resume to run

**CLI-only debugging via CDP**
```bash
# Install ndb or chrome-launcher for headless inspection
npx ndb script.js
```

**Pitfalls**
- `--inspect-brk` pauses immediately; use `--inspect` to run until a `debugger;` statement.
- In Docker, bind to `0.0.0.0`, not `127.0.0.1`.
- Source maps: if using TypeScript, ensure `sourceMap: true` in `tsconfig.json`.

---

## Debugging Hermes TUI Slash Commands

When a Hermes TUI slash command (e.g., `/plan`, `/debug`) fails:

1. Check the **gateway log** — errors often originate there before reaching the agent.
2. Inspect the **Python handler** — slash commands route through `agent/slash_commands.py`.
3. Check the **Ink UI layer** — TUI rendering issues may be TypeScript/Node errors.
4. Use `NODE_ENV=development` when running the gateway locally for verbose React/Ink output.
5. If the command hangs, check if a subprocess (e.g., `claude-code`) is waiting for PTY input.

### Common Failures
- "Command not found" — the slash command handler isn't registered in `slash_commands.py`.
- "Timeout" — a subprocess blocked the event loop. Use `timeout=` in `terminal()` calls.
- "Malformed JSON" — the gateway serialized an invalid payload. Check the handler's return type.
