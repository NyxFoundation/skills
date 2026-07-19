---
name: deep-research
description: |
  Orchestrate a deep, multi-source research investigation: decompose the question, fan out parallel
  background subagents with delegate_task(background=true), verify claims across independent sources,
  and synthesize a cited report. Load when the user asks for 深掘り調査, 徹底的に調べて, "deep research",
  a market/competitor/technology landscape, a literature survey, or any research task too big for a
  single search pass. For single-fact lookups just use web_search directly — do NOT load this.
version: 1.0.0
author: gohan (via Claude Code tuning)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, deep-research, delegation, fan-out, verification, synthesis, 調査]
---

# Deep Research Orchestration

## Pipeline

### 1. Decompose & plan (main agent, no delegation yet)
- Restate the question; list 3–6 orthogonal sub-questions (different ANGLES, not keyword variants:
  e.g. official docs / independent benchmarks / community experience / counter-evidence / recent news)
- If the request is underspecified (no timeframe, region, budget, purpose), ask ONE clarifying message first

### 2. Fan out (v0.18 background delegation)
- One subagent per sub-question via `delegate_task(background=true)` — they run in parallel and return
  as a single consolidated turn; the conversation stays unblocked
- Each subagent prompt must include: the sub-question, required output shape
  (claims + source URL + date + confidence), and the instruction to prefer primary sources
- 3–5 subagents is the sweet spot; more than 6 dilutes quality

### 3. Verify before trusting
- Any claim that is surprising, quantitative, or load-bearing needs 2+ independent sources
- Check dates — a 2024 benchmark answered as current-state is wrong in 2026
- Conflicting sources: report the conflict explicitly, don't average it away

### 4. Synthesize
- Lead with the answer/recommendation, then evidence
- Inline-cite every non-obvious claim with its URL
- End with: what remains uncertain + what would resolve it
- Long reports: put the full version in a file or Notion page, post the executive summary to Slack

## Tools of choice
- `web_search` (multiple phrasings, English AND Japanese — coverage differs)
- `web_extract` for full-page reads of the top sources
- arXiv / academic sources $\rightarrow$ use the arXiv API directly (`http://export.arxiv.org/api/query`)
- Financial Agentic Trading $\rightarrow$ see `references/agentic-trading.md`
- X/Twitter sentiment $\rightarrow$ `x_search`
- Save durable findings to Notion → skill `notion-databases`

## Anti-patterns
- Sequential searches when sub-questions are independent (use background fan-out)
- Reporting a single source as settled fact
- Quoting numbers without their measurement date
- Burying the answer under methodology narration
