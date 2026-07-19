# NyxFoundation/skills

Agent skills authored by Nyx Foundation — a single repository that any agent environment
(Claude Code, hermes agent, per-project workspaces) references as its skill source.

Every skill is one directory containing a `SKILL.md` (YAML frontmatter: `name`, `description`,
optionally `allowed-tools`) plus any supporting files, following the
[Claude Code skills convention](https://docs.claude.com/en/docs/claude-code/skills).
Skills are grouped **by domain**, not by agent. Only skills we authored live here — skill packs
that ship with vendors or upstream tools (Cloudflare, hermes-agent, …) are installed from their
own sources, not mirrored into this repo.

## Domains

| Directory | Contents |
|---|---|
| `autonomous-ai-agents/` | Multi-agent orchestration (kanban-multi-agent) |
| `creative/` | Narrative design and visualization — narrative-heat-engineering (NHE), emotion-curve-feedback, narrative-content-writing, [visually-3d](https://github.com/NyxFoundation/visually-3d) |
| `data-science/` | Japanese-ready data visualization (jp-dataviz) |
| `devops/` | Environment and operations workflows (nixos-environment, devops-workflows, mordred-hermes-setup) |
| `formal-methods/` | Formal specification and verification ([docs2formalspec](https://github.com/NyxFoundation/docs2formalspec)) |
| `presentation/` | Slidev deck authoring (slide, arch-diagram, animated-concept-slide) |
| `productivity/` | Documents, events, Notion workflows, Slack integration |
| `research/` | Deep research, formalization research programs, academic writing, research-to-repo workflows |
| `security/` | Specification-anchored security auditing ([speca](https://github.com/NyxFoundation/speca)) |
| `software-development/` | Planning, debugging, code review, delegation, and GitHub workflows |

Some skills (`creative/visually-3d`, `formal-methods/docs2formalspec`, `security/speca`) are thin
wrappers that `git clone` a Nyx Foundation tool repo and drive its CLI — the skill documents the
clone step and the workflow.

Notable pairing: **narrative-heat-engineering** (design side) and **emotion-curve-feedback**
(diagnostic side) form one methodology for any sequential content — slide decks, articles,
landing pages, papers — write with NHE, diagnose with the emotion curves, then iterate.

## Using these skills

Clone once, then link the skills you want into your agent's skill directory:

```bash
git clone https://github.com/NyxFoundation/skills.git ~/workspace/skills

# Claude Code — per project:
mkdir -p .claude/skills
ln -s ~/workspace/skills/security/speca .claude/skills/speca
ln -s ~/workspace/skills/presentation/* .claude/skills/

# Claude Code — user-global: link into ~/.claude/skills/ instead.

# hermes agent — sync into the hermes skill directory:
rsync -a ~/workspace/skills/ ~/.hermes/skills/
```

Update flow: edit skills **in this repo** via PR; after merge, each environment runs
`git -C ~/workspace/skills pull` and repeats its link/sync step. Local skill directories are
disposable mirrors — never the editing target.

## Adding a skill

1. Create `<domain>/<skill-name>/SKILL.md` with frontmatter (`name`, `description`; keep the
   description trigger-oriented — it is what the agent uses to decide relevance).
2. Keep supporting files inside the same directory; reference them with relative paths.
3. Only original skills belong here — don't mirror vendor or upstream skill packs.
4. **No secrets** — see below.

## Public-repo policy (hard gate)

This repo is public. Never commit:

- API keys, tokens, credentials, private keys, `.env` files
- Personal information or personal-workflow skills (private repo names, personal database IDs)
- Internal-only URLs, hostnames, or identifiers

Placeholders like `ghp_xxxx…` / `you@example.com` are fine. Review every PR against this list
before merge.

## License

MIT — see [LICENSE](LICENSE).
