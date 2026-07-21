#!/usr/bin/env bash
# sync.sh — publish/refresh self-improvements to the skills repo.
# -----------------------------------------------------------------------------
# Skills are SYMLINKED into each agent (see integrate.sh), so when Claude,
# hermes or Codex edits a skill file it edits THIS repo's working tree directly.
# This helper turns that edit into a commit + push (or pulls others' updates), so
# self-improvement flows back to NyxFoundation/skills without manual git steps.
#
#   ./sync.sh                    commit ALL changes (auto message) and push
#   ./sync.sh "message"          commit with your message and push
#   ./sync.sh --pull             git pull --rebase (refresh repo + every linked agent)
#   ./sync.sh --status           show what changed since last push
#   ./sync.sh --no-push "msg"     commit only, don't push
#
# Agents: after improving any skill, run `./sync.sh` from the repo root to
# publish. Prefer editing skills in the repo (or via the symlink) — never the
# disposable per-agent mirror as a separate copy.
# -----------------------------------------------------------------------------
set -euo pipefail

SELF="$0"; while [ -L "$SELF" ]; do SELF="$(readlink "$SELF")"; done
REPO="$(cd "$(dirname "$SELF")" && pwd)"
cd "$REPO"

c_g=$'\033[32m'; c_y=$'\033[33m'; c_r=$'\033[31m'; c_x=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_g" "$c_x" "$*"; }
warn() { printf '%s⚠%s  %s\n' "$c_y" "$c_x" "$*" >&2; }
die()  { printf '%s✗%s %s\n' "$c_r" "$c_x" "$*" >&2; exit 1; }

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "not a git repo: $REPO"

PUSH=1; MSG=""
case "${1:-}" in
  --status) git status -s; exit 0;;
  --pull)   git pull --rebase && ok "pulled — repo と全リンク先エージェントが最新化"; exit 0;;
  --no-push) PUSH=0; MSG="${2:-}";;
  -h|--help) sed -n '2,20p' "$SELF"; exit 0;;
  *) MSG="${1:-}";;
esac

# Secret gate: never let credentials reach this public repo.
staged_scan() {
  git diff --cached -U0 | grep -E '^\+' \
    | grep -EI 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]+|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|secret_[A-Za-z0-9]{20,}' \
    | grep -viE 'xxxx|example|placeholder|ghp_x|your[_-]?token' || true
}

git add -A
if git diff --cached --quiet; then warn "変更なし。何もしません。"; exit 0; fi

hit="$(staged_scan)"
[ -z "$hit" ] || { printf '%s\n' "$hit" | sed 's/^/  /'; die "秘密情報らしき文字列を検出。コミット中止（public repo）。誤検知なら手動で対処。"; }

if [ -z "$MSG" ]; then
  changed=$(git diff --cached --name-only | awk -F/ '/SKILL.md$/{print $(NF-1)}' | sort -u | paste -sd, -)
  [ -n "$changed" ] || changed=$(git diff --cached --name-only | head -3 | paste -sd, -)
  MSG="skill update: ${changed:-changes} ($(date +%Y-%m-%d))"
fi

git commit -q -m "$MSG"
ok "committed: $MSG"
if [ "$PUSH" = 1 ]; then
  git push -q origin HEAD && ok "pushed → $(git remote get-url origin)"
else
  warn "--no-push 指定。push は手動で: git push"
fi
