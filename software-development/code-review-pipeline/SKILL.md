---
name: code-review-pipeline
description: |
  Pre-commit and post-commit code review workflows: security scanning, quality gates,
  auto-fix loops, and parallel subagent-driven code cleanup.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, security, quality, pre-commit, cleanup, refactoring, subagent]
    related_skills: [github-workflow, test-driven-development, debugging]
---

# Code Review Pipeline

This skill covers automated code review workflows: pre-commit quality gates, security scans, and parallel cleanup via subagents.

---

## Pre-Commit Review (Security + Quality Gates)

Before committing code, run this checklist:

### Security Scan
- [ ] No hardcoded secrets (API keys, tokens, passwords)
- [ ] No SQL injection vectors (parameterized queries only)
- [ ] No eval/exec on untrusted input
- [ ] No insecure deserialization
- [ ] No SSRF or open redirect vulnerabilities
- [ ] Dependencies scanned for known CVEs (`pip-audit`, `npm audit`)

### Quality Gates
- [ ] All tests pass (`pytest`, `jest`, etc.)
- [ ] Linting passes (`ruff`, `eslint`, `mypy`)
- [ ] Type coverage acceptable
- [ ] No TODO/FIXME left in committed code
- [ ] Commit message follows conventional commits format

### Auto-Fix Loop
1. Run linters and formatters.
2. If auto-fixable issues exist, apply them and re-run tests.
3. If tests fail after auto-fix, investigate manually — do not commit broken code.

---

## Parallel Subagent Cleanup

For large cleanup tasks (e.g., "simplify all error handling"), dispatch parallel subagents:

1. **Split by scope**: one agent per directory or concern.
2. **Two-stage review**:
   - Stage 1: spec compliance — did the agent follow the instructions?
   - Stage 2: code quality — is the result idiomatic, performant, readable?
3. **Merge and verify**: combine outputs, run full test suite.

### Example: Simplify Recent Changes
```
1. Identify files changed in the last commit.
2. For each file, spawn a subagent with:
   - the file content
   - the specific simplification goal (e.g., "reduce nesting", "extract helpers")
3. Collect results and present unified diff.
4. Run tests before accepting.
```

**Pitfalls**
- Subagents may produce semantically different code. Always run tests.
- Parallel agents may conflict on shared files. Scope each agent to non-overlapping files.
- Cost scales with the number of agents. Use for high-value refactors, not trivial changes.
