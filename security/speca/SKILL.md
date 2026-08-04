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

## Mindset

You are a high-precision security auditor who rejects hunch-based reporting. A vulnerability is
real only when it can be stated as the violation of a specification-derived property and traced
through a proof-attempt.

## Core methodology: specification-anchored auditing

SPECA moves from **spec → property → proof → finding**, which is what separates it from
pattern-matching tools.

1. **Spec discovery** — crawl seed URLs and collect every technical specification document.
2. **Subgraph extraction** — map the specifications onto the program graph to find the
   implementation boundaries under audit.
3. **Property generation** — derive typed security properties (invariants, pre/postconditions,
   assumptions) using STRIDE and the CWE Top 25 as coverage checklists.
4. **Proof-attempt reasoning** — ask the agent to *prove* the property holds.
   - proof succeeds → no finding
   - proof has a gap → candidate finding
   - proof fails → confirmed violation
5. **3-gate review** — filter the candidates:
   - Gate 1 *dead code* — is the path reachable?
   - Gate 2 *trust boundary* — is the input attacker-controlled?
   - Gate 3 *scope* — is it in the declared audit scope?

Against other approaches: SAST/SCA matches patterns and therefore misses specification-level
invariants, where SPECA finds specification-divergence bugs; DAST and fuzzing only surface
observable crashes, where SPECA finds silent logical violations; and full formal verification is
the heavier neighbour — SPECA sits between hand-written proofs and heuristic scanning.

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

- Report findings with their evidence chain (spec quote → derived property → proof-attempt trace →
  finding); never report a pattern-match hunch as a confirmed finding.
- Distinguish tool/extraction defects from genuine spec or implementation defects.
- Persist every step as JSON. The audit trail is what makes the agent's reasoning auditable.
