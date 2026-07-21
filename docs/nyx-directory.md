# Nyx Directory — shared IDs for skills

Canonical list of the Notion databases and Slack channels that Nyx skills reference **by ID**.
Skills point here instead of hard-coding IDs, so an ID change is a one-line edit in one place.

**No credentials live here.** API keys and tokens are configured per environment at setup time,
never committed to this repo:

- Notion API key → read from `~/.config/notion/api_key` (or the `notion` MCP server)
- Slack / other gateways → hermes gateway config (`~/.hermes/config.yaml`, secrets in `~/.hermes/.env`)

## Notion databases

| Name | Database ID |
|------|-------------|
| Business Card DB | `382d05af-0d5a-8031-957a-e0901f9634cc` |
| Scrapbox DB | `253d05af-0d5a-80f2-8bab-e846887dc258` |
| Log DB | `298d05af-0d5a-8052-946c-f9e443b4c970` |
| 採用面談 | `302d05af-0d5a-80ef-907a-e1ae99b73a05` |
| SPECA ROI simulation | `a9f387da-609a-4ccf-aa90-7ff6c8505604` |
| White-hat Hacking Reward Distribution | `2d3d05af-0d5a-802e-a6c5-c11919e3f5b4` |

## Slack channels

Public/shared channels only — DMs and per-topic thread groups are intentionally excluded.

| Name | Channel ID |
|------|-----------|
| ai | `C098U5EV6BV` |
| pj-biz-eris | `C0AP05HB38F` |
| pj-rd-speca | `C0AP96Y8DD1` |
| pj-rd-privacy | `C0APK6NRDCL` |
| pj-rd-pqc | `C0AQAD433QQ` |
| meishi-kokan | `C0BB1NDF4NS` |

## Members (Notion / Slack user IDs)

_Not yet tracked in a central file. Fill in as needed:_

| Name | Notion user ID | Slack user ID |
|------|----------------|---------------|
| _(add members here)_ | | |

---

_Maintained in [NyxFoundation/skills](https://github.com/NyxFoundation/skills). Update via `sync.sh`._
