---
name: github-workflow
description: |
  Complete GitHub developer workflow — authentication, repository management, pull requests, code review,
  issue triage, and codebase metrics. Covers both `gh` CLI and `git` + `curl` fallback paths.
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, git, workflow, pull-requests, code-review, issues, repositories, authentication, ci-cd]
    related_skills: [coding-agent-delegation, development-planning, debugging]
---

# GitHub Workflow

This skill covers the entire GitHub developer lifecycle: authenticate → manage repos → create PRs → review code → triage issues → inspect codebase health. It supports both the `gh` CLI (richer) and `git` + `curl` fallback (portable).

## THIS MACHINE: two GitHub accounts via MCP (READ FIRST)

Two GitHub MCP servers are configured with different tokens:
- `github-sannai` — sannai's personal repositories (personal PAT)
- `github-nyx` — NyxFoundation org (org PAT); namespace `NyxFoundation/repo-name`

For ANY write operation (push, create repo, PR, issue edit) where the user did not specify the
account: ask 「sannai（個人）と nyx（NyxFoundation）どちらで作業しますか？」 and WAIT — never assume.
Prefer the matching MCP server's tools over `gh`/`curl` so the right token is used automatically.

## Quick Detection

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → use `gh` for everything
2. If `gh` is installed but not authenticated → use "gh auth" method
3. If `gh` is not installed → use "git-only" method (no sudo needed)

---

## Authentication

### Method 1: Git-Only (HTTPS Token or SSH)

**HTTPS with Personal Access Token (most portable)**

1. Create token at https://github.com/settings/tokens
   - Scopes: `repo`, `workflow`, `read:org`
2. Configure git:
   ```bash
   git config --global credential.helper store
   git ls-remote https://github.com/<user>/<repo>.git
   # Enter username + token as password
   ```
3. Set identity:
   ```bash
   git config --global user.name "Name"
   git config --global user.email "email@example.com"
   ```

**SSH Key Authentication**

```bash
# Generate key
ssh-keygen -t ed25519 -C "email@example.com" -f ~/.ssh/id_ed25519 -N ""
# Add public key to https://github.com/settings/keys
ssh -T git@github.com
# Rewrite HTTPS to SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### Method 2: gh CLI Authentication

```bash
# Interactive (desktop)
gh auth login

# Token-based (headless)
echo "<TOKEN>" | gh auth login --with-token
gh auth setup-git
gh auth status
```

### API Token for curl Fallback

```bash
export GITHUB_TOKEN="<token>"
# Or extract from git credentials:
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
```

**Troubleshooting**

| Problem | Solution |
|---------|----------|
| `git push` asks for password | Use PAT as password; GitHub disabled password auth |
| `remote: Permission denied` | Token lacks `repo` scope — regenerate |
| `Authentication failed` | `git credential reject` then re-authenticate |
| SSH port 22 blocked | Add `Port 443` and `Hostname ssh.github.com` to `~/.ssh/config` |
| Multiple GitHub accounts | Use SSH host aliases or per-repo credential URLs |

---

## Repository Management

### Clone / Create / Fork

```bash
# gh CLI
gh repo clone owner/repo
cd repo
gh repo fork --clone
gh repo create my-project --public --clone

# Git-only
git clone https://github.com/owner/repo.git
cd repo
# Fork via GitHub web UI or API:
curl -s -H "Authorization: token $GITHUB_TOKEN"   -X POST https://api.github.com/repos/owner/repo/forks
```

### Remote Management

```bash
# Add upstream remote
gh repo set-default owner/repo
git remote add upstream https://github.com/upstream/repo.git

# View remotes
git remote -v
gh repo view --web
```

### Releases and Secrets

```bash
# Create release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes"

# List secrets
gh secret list
gh secret set MY_SECRET --body "value"
```

---

## Pull Request Workflow

### Create a PR

```bash
# Step 1: branch
git checkout -b feature/my-change

# Step 2: commit (conventional commits recommended)
git commit -m "feat(auth): add OAuth2 login"

# Step 3: push
git push -u origin feature/my-change

# Step 4: open PR
gh pr create --title "Add OAuth2 login" --body "Closes #123"
# Or with template
cat <<'EOF' | gh pr create --title "Add OAuth2 login" --body-file -
## Summary
Add OAuth2 login flow.

## Changes
- Added `auth/oauth2.ts`
- Updated `middleware.ts`

## Testing
- [ ] Unit tests
- [ ] Integration tests
EOF
```

### Review and Merge

```bash
# List PRs
gh pr list
gh pr list --state merged --limit 20

# View a PR
gh pr view 42 --web
gh pr diff 42

# Check CI status
gh run list --branch feature/my-change
gh run view --web

# Merge
gh pr merge 42 --squash --delete-branch
gh pr merge 42 --merge --delete-branch
```

### CI Troubleshooting

```bash
# Re-run failed checks
gh run rerun <run-id>

# View logs
gh run view <run-id> --log

# Download artifacts
gh run download <run-id>
```

---

## Code Review

### Review a PR via gh CLI

```bash
# View diff
gh pr diff 42

# Checkout PR locally
gh pr checkout 42

# Add review comment
gh pr review 42 --comment -b "Consider adding error handling here"

# Approve
gh pr review 42 --approve -b "LGTM!"

# Request changes
gh pr review 42 --request-changes -b "Please add tests for the edge cases"
```

### Review via REST API (fallback)

```bash
# Post review comment on a specific line
curl -s -H "Authorization: token $GITHUB_TOKEN"   -X POST https://api.github.com/repos/owner/repo/pulls/42/reviews   -d '{"body":"Consider null-checking","event":"COMMENT"}'

# Submit review
curl -s -H "Authorization: token $GITHUB_TOKEN"   -X POST https://api.github.com/repos/owner/repo/pulls/42/reviews/REVIEW_ID/events   -d '{"event":"APPROVE"}'
```

### Review Checklist

Before approving any PR, verify:
- [ ] Security: no hardcoded secrets, no SQL injection vectors, no unsafe eval
- [ ] Tests: new code has tests; existing tests still pass
- [ ] Documentation: README, API docs, or inline comments updated
- [ ] Backward compatibility: breaking changes are documented
- [ ] Scope creep: PR only does what the title says

---

## Issues Management

### Create and Triage

```bash
# Create issue
gh issue create --title "Bug: login fails on Safari" --body "Steps to reproduce..."

# Create issue from file (for long/structured descriptions)
gh issue create --title "Research Idea: X" --body-file a_detailed_description.txt

**Pro Tip: Mass Issue Updates**
When updating multiple existing issues with structured content:
1. Write the updated content to local temporary files (e.g., `/tmp/issueN.txt`).
2. Use `gh api -X PATCH repos/owner/repo/issues/N -f body="$(cat /tmp/issueN.txt)"` for precision and to avoid shell escaping issues with long multi-line strings.
3. Avoid using heredocs directly inside complex shell commands; prioritize file-based inputs.

# List issues
gh issue list --state open --label bug
gh issue list --assignee @me

# View issue
gh issue view 123 --web

# Close issue
gh issue close 123 --comment "Fixed in #456"
```

### Labels and Assignment

```bash
# Add labels
gh issue edit 123 --add-label "bug,critical"
gh issue edit 123 --remove-label "needs-triage"

# Assign
gh issue edit 123 --add-assignee "@me"
gh issue edit 123 --add-assignee "teammate"
```

### Templates

Use issue templates stored in `.github/ISSUE_TEMPLATE/`:
- `bug_report.md` — steps to reproduce, expected vs actual behavior
- `feature_request.md` — problem, proposed solution, alternatives

**Pro Tip: External Issue Control**
To restrict issue creation to organization members while allowing public comments:
1. Use a GitHub Action that triggers on `issues: [opened]`.
2. Check the author's permission level via `repos.getCollaboratorPermissionLevel`.
3. Automatically close issues from users with `read` or `none` permissions, posting a polite redirection comment.


---

## Codebase Inspection

### Lines of Code and Language Breakdown

```bash
pip install pygount 2>/dev/null || pip install --break-system-packages pygount

cd /path/to/repo
pygount --format=summary   --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info"   .
```

### Project-Type Exclusions

```bash
# Python
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JS/TS
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

### Quick Stats

```bash
# File count by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20

# Total files excluding common skip dirs
find . -type f   ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/venv/*"   | wc -l
```

---

## Support Files

This skill includes helper references under:
- `references/ci-troubleshooting.md` — common CI failure patterns
- `references/conventional-commits.md` — commit message conventions
- `references/github-api-cheatsheet.md` — curl snippets for common operations
- `templates/pr-body-bugfix.md` — PR template for bug fixes
- `templates/pr-body-feature.md` — PR template for features
- `templates/bug-report.md` — issue template for bug reports
- `templates/feature-request.md` — issue template for feature requests
- `scripts/gh-env.sh` — quick auth detection helper
