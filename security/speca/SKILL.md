---
name: speca
description: >
  Run a specification-anchored security audit with SPECA (NyxFoundation/speca): derive typed security
  properties from natural-language specs and audit implementations via structured proof-attempt
  reasoning. Load when the user asks for a smart-contract / protocol security audit, spec-conformance
  audit, or mentions SPECA.
allowed-tools: bash, read, write
---

# SKILL: speca (git-based tool)

## Setup

The tool is the public repo `NyxFoundation/speca` (MIT, paper: arXiv:2604.26495).

```bash
# Bootstrap with the TUI (recommended)
npx speca-cli@latest doctor    # check toolchain
npx speca-cli@latest init      # create BUG_BOUNTY_SCOPE.json + TARGET_INFO.json
npx speca-cli@latest run --target <id>

# Or run the orchestrator directly
git clone https://github.com/NyxFoundation/speca.git "${SPECA_HOME:-$HOME/workspace/speca}"
cd "${SPECA_HOME:-$HOME/workspace/speca}"
npm install -g @anthropic-ai/claude-code
uv sync && bash scripts/setup_mcp.sh
uv run python3 scripts/run_phase.py --target <id> --workers 4
```

Outputs land in `outputs/<phase>_PARTIAL_*.json`; browse with `speca-cli browse outputs/<...>.json`.
Full docs: https://speca.pages.dev/

## Sub-skills

The repo ships Claude Code skills under `.claude/skills/` (copies bundled here for reference):

- `spec-discovery/` — crawl a seed URL and collect all technical specification documents.
- `subgraph-extractor/` — extract the relevant implementation subgraph for a property under audit.

When working inside a speca clone these load automatically from the repo; the copies in this
directory are the pinned reference versions.

## Honesty rules

- Report findings with their evidence chain (spec quote → property → proof-attempt trace); never
  report a pattern-match hunch as a confirmed finding.
- Distinguish tool/extraction defects from genuine spec or implementation defects.
