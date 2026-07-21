#!/usr/bin/env bash
# integrate.sh — link NyxFoundation/skills into your agent(s).
# -----------------------------------------------------------------------------
# This repo is the single source of truth for Nyx-authored agent skills.
# Run this script to symlink every skill here into your agent's skill directory,
# so Claude Code and/or hermes agent can use them (e.g. "NHEスキルつかって"
# → narrative-heat-engineering).
#
# Symlinks keep the repo authoritative: `git pull` in this repo updates every
# linked agent instantly. Use --copy for standalone copies instead.
#
#   ./integrate.sh                 link all skills into Claude Code AND hermes
#   ./integrate.sh --claude        link into Claude Code only (~/.claude/skills)
#   ./integrate.sh --hermes        link into hermes only     (~/.hermes/skills)
#   ./integrate.sh --list          list linkable skills in this repo
#   ./integrate.sh --status        show what is currently linked from this repo
#   ./integrate.sh --copy          copy instead of symlink
#   ./integrate.sh --force         overwrite existing real directories
#   ./integrate.sh --remove        unlink this repo's skills from the target(s)
#   ./integrate.sh <name> ...      operate on specific skill names only
#
# Targets can be overridden: CLAUDE_SKILLS_DIR=... HERMES_SKILLS_DIR=...
# -----------------------------------------------------------------------------
set -euo pipefail

# repo root = directory of this script (resolve symlinks)
SELF="$0"; while [ -L "$SELF" ]; do SELF="$(readlink "$SELF")"; done
REPO="$(cd "$(dirname "$SELF")" && pwd)"

CLAUDE_SKILLS="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
HERMES_SKILLS="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills}"

MODE=symlink   # symlink | copy
FORCE=0
declare -a TARGETS=()   # filled from flags; default = both
declare -a ONLY=()      # specific skill names

c_b=$'\033[1m'; c_d=$'\033[2m'; c_g=$'\033[32m'; c_y=$'\033[33m'; c_r=$'\033[31m'; c_x=$'\033[0m'
ok()   { printf '%s✓%s %s\n' "$c_g" "$c_x" "$*"; }
warn() { printf '%s⚠%s  %s\n' "$c_y" "$c_x" "$*" >&2; }
die()  { printf '%s✗%s %s\n' "$c_r" "$c_x" "$*" >&2; exit 1; }

frontmatter_name() {
  awk 'NR==1&&$0=="---"{fm=1;next} fm&&$0=="---"{exit}
       fm&&/^name:[ \t]*/{sub(/^name:[ \t]*/,"");gsub(/^["'\'']|["'\'']$/,"");print;exit}' "$1"
}

# Emit "name<TAB>dir" for every TOP-LEVEL skill (a SKILL.md whose ancestors,
# up to the repo root, contain no other SKILL.md — so sub-skills are excluded).
list_skills() {
  find "$REPO" -name SKILL.md -not -path '*/.git/*' | sort | while read -r f; do
    local d parent top; d="$(dirname "$f")"; top=1
    parent="$(dirname "$d")"
    while [ "$parent" != "$REPO" ] && [ "$parent" != "/" ]; do
      [ -f "$parent/SKILL.md" ] && { top=0; break; }
      parent="$(dirname "$parent")"
    done
    [ "$top" = 1 ] || continue
    local n; n="$(frontmatter_name "$f")"; [ -n "$n" ] || n="$(basename "$d")"
    printf '%s\t%s\n' "$n" "$d"
  done
}

wanted() {   # 0 if this skill name should be processed
  [ ${#ONLY[@]} -eq 0 ] && return 0
  local x; for x in "${ONLY[@]}"; do [ "$x" = "$1" ] && return 0; done; return 1
}

link_into() {   # <target-dir> <label>
  local base="$1" label="$2" n src tgt
  mkdir -p "$base"
  while IFS=$'\t' read -r n src; do
    wanted "$n" || continue
    tgt="$base/$n"
    if [ -L "$tgt" ]; then rm -f "$tgt"
    elif [ -e "$tgt" ]; then
      if [ "$FORCE" = 1 ]; then rm -rf "$tgt"
      else warn "[$label] $n: 実体ディレクトリが既存。スキップ（上書きは --force）"; continue; fi
    fi
    if [ "$MODE" = copy ]; then cp -r "$src" "$tgt"; ok "[$label] $n ${c_d}(copy)${c_x}"
    else ln -s "$src" "$tgt"; ok "[$label] $n ${c_d}→ ${src#$REPO/}${c_x}"; fi
  done < <(list_skills)
}

unlink_from() {   # <target-dir> <label>
  local base="$1" label="$2" n src tgt
  while IFS=$'\t' read -r n src; do
    wanted "$n" || continue
    tgt="$base/$n"
    if [ -L "$tgt" ]; then rm -f "$tgt"; ok "[$label] unlink $n"; fi
  done < <(list_skills)
}

status_for() {   # <target-dir> <label>
  local base="$1" label="$2" n src tgt any=0
  printf '%s%s%s %s(%s)%s\n' "$c_b" "$label" "$c_x" "$c_d" "$base" "$c_x"
  while IFS=$'\t' read -r n src; do
    tgt="$base/$n"
    if [ -L "$tgt" ] && [ "$(cd "$(dirname "$tgt")" && readlink "$tgt")" = "$src" ]; then
      any=1; printf '  %s%-32s%s %slinked%s\n' "$c_b" "$n" "$c_x" "$c_g" "$c_x"
    elif [ -e "$tgt" ]; then printf '  %s%-32s%s %s(別の実体が存在)%s\n' "$c_b" "$n" "$c_x" "$c_y" "$c_x"
    fi
  done < <(list_skills)
  [ "$any" = 1 ] || printf '  %s（このリポからのリンクなし）%s\n' "$c_d" "$c_x"
}

# ---- args ----
action=link
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)   sed -n '2,29p' "$SELF"; exit 0;;
    --claude)    TARGETS+=(claude);;
    --hermes)    TARGETS+=(hermes);;
    --list)      action=list;;
    --status)    action=status;;
    --remove)    action=remove;;
    --copy)      MODE=copy;;
    --force)     FORCE=1;;
    -*)          die "不明なオプション: $1";;
    *)           ONLY+=("$1");;
  esac
  shift
done
[ ${#TARGETS[@]} -gt 0 ] || TARGETS=(claude hermes)

case "$action" in
  list)
    printf '%sLinkable skills%s %s(%s)%s\n' "$c_b" "$c_x" "$c_d" "$REPO" "$c_x"
    while IFS=$'\t' read -r n src; do printf '  %s%-34s%s %s%s%s\n' "$c_b" "$n" "$c_x" "$c_d" "${src#$REPO/}" "$c_x"; done < <(list_skills)
    ;;
  status)
    for t in "${TARGETS[@]}"; do
      [ "$t" = claude ] && status_for "$CLAUDE_SKILLS" "Claude Code"
      [ "$t" = hermes ] && status_for "$HERMES_SKILLS" "hermes agent"
    done;;
  remove)
    for t in "${TARGETS[@]}"; do
      [ "$t" = claude ] && unlink_from "$CLAUDE_SKILLS" "Claude Code"
      [ "$t" = hermes ] && unlink_from "$HERMES_SKILLS" "hermes agent"
    done;;
  link)
    for t in "${TARGETS[@]}"; do
      [ "$t" = claude ] && link_into "$CLAUDE_SKILLS" "Claude Code"
      [ "$t" = hermes ] && link_into "$HERMES_SKILLS" "hermes agent"
    done
    echo
    printf '%s※ Claude Code は反映に新規セッションが必要な場合あり。確認: ./integrate.sh --status%s\n' "$c_d" "$c_x"
    ;;
esac
