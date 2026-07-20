---
name: nixos-environment
description: |
  Survival guide for this NixOS workstation: no pip/brew/apt, Python only via uv run, nix store paths,
  CJK font locations, systemd user services, and the Hermes gateway layout. Load when a command is
  "not found", an install step suggests pip/brew/apt, Python imports fail, fonts break, or you need to
  run/inspect services or system packages on this machine.
version: 1.0.0
author: gohan (via Claude Code tuning)
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [nixos, environment, uv, nix, systemd, fonts, troubleshooting]
---

# NixOS Workstation Environment

This machine is NixOS: the filesystem is immutable outside your home dir, and FHS paths
(`/usr/bin`, `/usr/share`, `/lib`) mostly don't exist. GPU: NVIDIA RTX 5090.

## Package management — what to do INSTEAD

| If docs say… | Do this here |
|---|---|
| `pip install X` | `uv run --with X python3 …` (ephemeral, no global installs) |
| `brew install X` / `apt install X` | `nix-shell -p X --run '…'` for one-offs; permanent installs need `/etc/nixos` + `sudo nixos-rebuild switch` (ask the user) |
| `npm install -g X` | `npx -y X` (ephemeral) |
| binary download (dynamic-linked) | often FAILS on NixOS (missing FHS loader) — prefer nix-shell or a static binary |

## Python

- ALWAYS `uv run`, never bare `python3`/`pip`:
  `uv run --with matplotlib,numpy,pandas python3 -c "…"`
- `ModuleNotFoundError` → add the package to `--with` and retry
- Charts with Japanese text: matplotlib FT2Font cannot load the system Noto CJK Variable Font
  by fname — set `font.family` to a name list (`Noto Sans CJK JP`, …) after a font-cache refresh;
  see `creative/emotion-curve-feedback/references/matplotlib-cjk-fonts.md` for the full fix

## Useful paths

- Fonts: `/run/current-system/sw/share/fonts/opentype/noto-cjk/` (Noto Sans CJK JP installed);
  list with `fc-list :lang=ja`
- System binaries: `/run/current-system/sw/bin/`
- Nix store (immutable): `/nix/store/…` — never edit; rebuilds swap symlinks

## Services (systemd user units)

- Hermes gateway: `systemctl --user status hermes-gateway` (defined via home-manager in
  `/etc/nixos/home-hermes.nix`, pinned to a nix store path — updates need a rebuild, see below)
- Logs: `journalctl --user -u hermes-gateway -n 100`

## Hermes self-knowledge

- Config/state: `~/.hermes/` (config.yaml, skills/, memories/, workspace/)
- Secrets live in `~/.hermes/.env` (referenced from config via `${VAR}` / `key_env`) — never
  write plaintext tokens into config.yaml
- Upgrading hermes: `cd ~/hermes-agent && git fetch --tags && git merge --ff-only <tag> &&
  nix build .#messaging`, then swap the `hermesPkg` pin in `/etc/nixos/home-hermes.nix` and
  `sudo nixos-rebuild switch` (needs the user)
