---
name: coding-agent-delegation
description: |
  Delegate coding tasks to autonomous CLI agents — Claude Code, Codex CLI, and OpenCode.
  Covers installation, authentication, prompt engineering, review workflows, and common pitfalls
  for each tool. Pick the right agent for the job based on cost, PTY support, and model family.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, delegation, claude, codex, opencode, cli-agent, autonomous-coding]
    related_skills: [github-workflow, development-planning]
---

# Coding Agent Delegation

This skill covers how to delegate coding work to autonomous CLI agents that run locally and perform multi-step operations (refactoring, feature implementation, PR review) without requiring an API key for every call.

## Agent Comparison

| Agent | Model | PTY Support | Auth | Cost | Best For |
|-------|-------|-------------|------|------|----------|
| **Claude Code** | Claude 4.6 Opus | Full PTY (interactive TUI) | Anthropic API key or Claude Pro | API metered; Pro subscription if available | Deep reasoning, long-context refactors, interactive debugging sessions |
| **Codex CLI** | GPT-5.4 / o4-mini | No PTY (JSON stream) | OpenAI API key | API metered | Fast iterations, OpenAI model family, REST fallback |
| **OpenCode** | OpenRouter or local | No PTY (stateful sessions) | OpenRouter key or local endpoint | OpenRouter credit | Multi-model routing, local/self-hosted models, cost optimization |

Rule of thumb:
- **Claude Code** when the task is complex, the codebase is large, or you need interactive debugging.
- **Codex** when you want OpenAI models, faster setup, or REST API fallback.
- **OpenCode** when you need to switch models mid-session, run local models, or minimize API spend.

---

## Claude Code

### Installation
```bash
# npm (recommended)
npm install -g @anthropics/claude-code
# Or standalone binary from Anthropic releases
```

### Authentication
- Set `ANTHROPIC_API_KEY` in environment, or
- Log in with Claude Pro subscription (browser auth) via `claude login`

### Key Usage Patterns
```bash
# Start in a repo
claude

# One-shot command (non-interactive)
claude -p "explain the auth flow in src/"

# Review a PR
claude -p "review the changes in this PR"

# Refactor across files
claude -p "refactor all error handling to use a central logger"
```

### Prompt Engineering Tips
- Use `-p` for non-interactive mode; omit it for PTY TUI.
- Claude Code reads `.claude-code/` context files automatically.
- For long tasks, break into directory-scoped prompts rather than one giant prompt.
- Use `/cost` to check spend before large refactors.

### Pitfalls
- **Cost accumulation**: Claude Code makes many API calls. Set spending alerts.
- **Git state**: Claude Code auto-commits by default. Review `.claude-code/settings.json` if you want manual commits.
- **Large repos**: It auto-indexes the repo. Very large repos may hit context limits.

---

## Codex CLI

### Installation
```bash
# npm
npm install -g @openai/codex
```

### Authentication
- `OPENAI_API_KEY` environment variable (required)
- Optional: `OPENAI_ORG_ID` for organization billing

### Key Usage Patterns
```bash
# Start interactive session
codex

# One-shot command
codex -p "add error handling to upload.js"

# Review PR
codex -p "review PR #42"

# Specify model
codex --model o4-mini -p "quick fix"
```

### Prompt Engineering Tips
- Codex outputs a JSON event stream. Parse it for automation.
- The `-p` flag is the primary non-interactive interface.
- Use `--model` to switch between GPT-5.4 (deep) and o4-mini (fast/cheap).

### Pitfalls
- **No PTY**: Cannot run interactive commands inside the agent. Use Claude Code for that.
- **Rate limits**: OpenAI rate limits apply per-organization.
- **Tool limits**: Fewer built-in tools than Claude Code (no file search, no bash execution).

---

## OpenCode

### Installation
```bash
# npm
npm install -g @opencode/cli
```

### Authentication
- `OPENROUTER_API_KEY` for cloud models, or
- Local endpoint URL for self-hosted models (e.g., llama.cpp, vLLM)

### Key Usage Patterns
```bash
# Start with default model
opencode

# Switch model mid-session
opencode --model anthropic/claude-sonnet-4

# Run with local endpoint
opencode --endpoint http://localhost:8000/v1

# Review PR
opencode -p "review PR for security issues"
```

### Prompt Engineering Tips
- OpenCode supports multi-model routing: start cheap (local), escalate to cloud if stuck.
- Use `--context-files` to preload relevant files into the prompt.
- State is persisted across runs in `~/.opencode/sessions/`.

### Pitfalls
- **Model switching latency**: Each `--model` change may require a new connection warmup.
- **Local endpoint health**: If the local server crashes, OpenCode falls back to cloud (cost surprise).
- **OpenRouter credit**: Set a low credit limit to avoid accidental spend during model exploration.

---

## General Agent Workflow

1. **Verify installation**: `which claude || which codex || which opencode`
2. **Verify auth**: run a harmless read command first
3. **Scope the task**: one directory or one concern at a time
4. **Review before commit**: agents may produce functional but ugly code
5. **Track cost**: all three support cost queries; use them

## When NOT to Use an Agent
- One-line fixes — just edit the file directly
- Tasks requiring human judgment (design reviews, UX decisions)
- Sensitive operations (deleting production data, rotating secrets)
- When the codebase is not in git (agents assume git for rollback)
