# NyxFoundation/skills

Agent skills authored by Nyx Foundation — a single repository that any agent environment
(Claude Code, hermes agent, per-project workspaces) references as its skill source.

Every skill is one directory containing a `SKILL.md` (YAML frontmatter: `name`, `description`,
optionally `allowed-tools`) plus any supporting files, following the
[Claude Code skills convention](https://docs.claude.com/en/docs/claude-code/skills).
Skills are grouped **by domain**, not by agent. Only original skills we authored live here —
skill packs that ship with vendors or upstream tools (Cloudflare, hermes-agent, …) and rehashes
of standard agent capabilities (Claude Code's built-in dataviz / deep-research / code-review,
generic debugging or GitHub workflow guides) are installed from their own sources or simply not
duplicated, never mirrored into this repo.

## Domains

| Directory | Contents |
|---|---|
| `autonomous-ai-agents/` | Multi-agent orchestration (kanban-multi-agent) |
| `creative/` | Narrative design and visualization — narrative-heat-engineering (NHE), emotion-curve-feedback, narrative-content-writing, [visually-3d](https://github.com/NyxFoundation/visually-3d) |
| `devops/` | Environment and operations workflows (nixos-environment, devops-workflows, mordred-hermes-setup) |
| `formal-methods/` | Formal specification and verification ([docs2formalspec](https://github.com/NyxFoundation/docs2formalspec)) |
| `presentation/` | Slidev deck authoring (slide, arch-diagram, animated-concept-slide) |
| `productivity/` | Event management, Notion workflow optimization, Slack integration |
| `research/` | Formalization research programs, research-to-repo workflow, LaTeX editing craft |
| `security/` | Specification-anchored security auditing ([speca](https://github.com/NyxFoundation/speca)) |
| `software-development/` | Nyx-specific dev workflows — PR drafting, asset hosting, interests-issue authoring, procedural 3D visualization |

Some skills (`creative/visually-3d`, `formal-methods/docs2formalspec`, `security/speca`) are thin
wrappers that `git clone` a Nyx Foundation tool repo and drive its CLI — the skill documents the
clone step and the workflow.

Notable pairing: **narrative-heat-engineering** (design side) and **emotion-curve-feedback**
(diagnostic side) form one methodology for any sequential content — slide decks, articles,
landing pages, papers — write with NHE, diagnose with the emotion curves, then iterate.

## Using these skills

Clone once, then run `integrate.sh` to symlink every skill here into your agent's skill
directory. Symlinks keep this repo authoritative — `git pull` updates every linked agent at once.

```bash
git clone https://github.com/NyxFoundation/skills.git ~/workspace/skills
cd ~/workspace/skills

./integrate.sh                 # link all skills into Claude Code AND hermes agent
./integrate.sh --claude        # Claude Code only  (~/.claude/skills)
./integrate.sh --hermes        # hermes agent only (~/.hermes/skills)
./integrate.sh --list          # list linkable skills
./integrate.sh --status        # show what is currently linked from this repo
./integrate.sh nyx-interests narrative-heat-engineering   # only specific skills
./integrate.sh --remove        # unlink this repo's skills again
```

Once linked, drive a skill by name from the agent — e.g. tell Claude
「rewrite with narrative-heat-engineering(NHE) skill」 or 「add an issue for Nyx interests」.
`--copy` makes standalone copies instead of symlinks; `--force` overwrites an existing real
directory; targets can be pointed elsewhere with `CLAUDE_SKILLS_DIR=` / `HERMES_SKILLS_DIR=`.

<img width="2525" height="941" alt="image" src="https://github.com/user-attachments/assets/fd5c198b-bd51-459b-b3fd-f3ac66077954" />

<img width="2553" height="824" alt="image" src="https://github.com/user-attachments/assets/634a0ec1-f3e7-4fb1-bbf9-9e435e23250d" />

Update flow: edit skills **in this repo** via PR; after merge, each environment runs
`git -C ~/workspace/skills pull` — symlinks pick up the change with no re-link needed. Local
skill directories are disposable mirrors — never the editing target.

## Self-improvement flow

Because the skills are **symlinked** into each agent, editing a skill from inside Claude Code or
hermes edits this repo's working tree directly — there is no separate copy to reconcile. To publish
an improvement, run `sync.sh` from the repo root:

```bash
./sync.sh                  # commit all changes (auto message) + push
./sync.sh "why it changed" # commit with your own message + push
./sync.sh --pull           # pull others' updates into repo + every linked agent
./sync.sh --status         # what changed since last push
```

`sync.sh` refuses to commit anything matching a credential pattern (tokens, keys, `-----BEGIN
PRIVATE KEY-----`) so secrets never reach this public repo. **Agents: after improving a skill,
run `./sync.sh` to publish it** — the improvement then reaches every other environment on its next
`./sync.sh --pull`.

## Adding a skill

1. Create `<domain>/<skill-name>/SKILL.md` with frontmatter (`name`, `description`; keep the
   description trigger-oriented — it is what the agent uses to decide relevance).
2. Keep supporting files inside the same directory; reference them with relative paths.
3. Only original skills belong here — don't mirror vendor or upstream skill packs.
4. **No secrets** — see below.

## Public-repo policy (hard gate)

This repo is public. Never commit:

- API keys, tokens, credentials, private keys, `.env` files
- Personal information (individuals' emails, private Notion/Slack **user** IDs, DM/thread IDs)

**Allowed:** non-credential resource identifiers that skills need to address shared workspace
objects — Notion **database** IDs and Slack **channel** IDs — are kept in
[`docs/nyx-directory.md`](docs/nyx-directory.md) and referenced by skills instead of being
hard-coded in each one. These IDs are not secrets (they cannot be used without a separately
configured API key/token), so they may live here. Credentials are always configured per
environment at setup, never committed.

Placeholders like `ghp_xxxx…` / `you@example.com` are fine. Review every PR against this list
before merge.

## License

MIT — see [LICENSE](LICENSE).
