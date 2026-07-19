---
name: event-management
description: Comprehensive workflow for planning, coordinating, and executing high-stakes professional events (summits, conferences) using Notion as the central command center.
---

# Event Management Workflow

This skill governs the professional orchestration of events, emphasizing structured data over loose notes and proactive risk management.

## Core Principles
- **Data-Driven Coordination**: Every speaker, sponsor, and task must live in a database, not a page.
- **Phase-Based Intensity**: Event planning moves through phases (e.g., Phase 1: Discovery, Phase 2: High-Density Reporting, Phase 3: Execution).
- **Reporting as a Product**: Regular, templated reports to sponsors and speakers are as important as the event itself.

## Workflow Steps

### 1. Infrastructure Setup (The Command Center)
- Ensure the following databases exist and are interlinked:
    - **Sponsor DB**: Tracks tiers, pricing, and payment status.
    - **Speaker DB**: Tracks confirmation status, session topics, and orgs.
    - **ToDo DB**: Must include `Status`, `Category`, `Priority (P0-P3)`, and `Report Target`.
    - **Meeting Memo DB**: Categorized logs of all syncs.
    - **Participant DB**: Tracks registrations, ticket types, industry/role attributes, and check-in status.
    - **Budget/Finance DB**: Tracks actual spend vs. forecast, payment dates, and vendor info.
    - **Risk Management DB**: Severity × Probability matrix for tracking and mitigation.
    - **Marketing/Promotion DB**: Tracks channel performance and rollout schedule.
    - **Staff/Shift DB**: Role assignments and hour-by-hour event timelines.
- Create a **Operational Manual (運用手順書)** page containing:
    - Reporting cadence (frequency per phase).
    - Communication templates (Sponsor/Speaker/Internal).
    - Escalation matrix (who to call for what crisis).
    - Technical requirements and tool research (e.g., translation tools, streaming setup).

### 2. Task Decomposition & Prioritization
- When auditing a project, look for \"Invisible P0s\":
    - Contract signatures & payment confirmation.
    - Ticket page launch & promo start date.
    - Final venue equipment check (WiFi, Power, AV).
    - Final timeline/agenda lock.
    - **Real-time translation/subtitle tools for global audiences.** (See `references/otter-analysis.md` for Otter.ai benchmarks).
- Batch tasks into Categories (Logistics, Sponsors, Content, Marketing, Staff, Budget).

### 3. The Reporting Loop
- **Trigger**: Moving a task to \"Done\" in the ToDo DB.
- **Action**: Select the corresponding template from the Operational Manual $\rightarrow$ Populate with specific updates $\rightarrow$ Send via Slack/Email.
- **Verification**: Log the report in the Meeting Memo or a dedicated Report DB.

## Pitfalls & Lessons
- **The \"Flat List\" Trap**: Avoid simple checklists for complex events. If a task has a \"Report Target\" or a \"Due Date\", it belongs in a DB.
- **Reporting Silence**: In high-stakes events, no news is bad news. Establish a cadence (e.g., Mon/Thu) even if there are no major updates.
- **Sponsor Friction**: Ensure \"Logo/PR Asset Collection\" is a P1 task early on to avoid last-minute scramble.
- **The \"Flat List\" Trap**: Avoid simple checklists for complex events. If a task has a \"Report Target\" or a \"Due Date\", it belongs in a DB.
- **Reporting Silence**: In high-stakes events, no news is bad news. Establish a cadence (e.g., Mon/Thu) even if there are no major updates.
- **Sponsor Friction**: Ensure \"Logo/PR Asset Collection\" is a P1 task early on to avoid last-minute scramble.
- **Sponsor Sourcing**: Don't rely on internal lists alone. Actively scrape/analyze sponsors of recent adjacent high-profile events (e.g., WebX, IVS, TOKEN2049) to identify warm leads. This involves:
    - Navigating sponsor pages via browser.
    - Cross-referencing existing DBs to identify missing entities.
    - Categorizing by tier (Title/Gold/Silver) and industry (AI, Web3, Finance) to ensure a balanced target list.
    - Batch-inserting into Notion while maintaining deduplication.
- **Participant Attribute Gap**: Raw CSV imports from platforms (Luma, etc.) usually lack detailed attributes (industry, role, attendee type). Always implement a manual curation step after import to ensure reporting accuracy.

## Support Files
- `templates/reporting-templates.md`: Standardized snippets for different stakeholders.
- `references/risk-matrix.md`: Common event risks (speaker dropouts, venue failure) and mitigation strategies.
- `references/translation-tools.md`: Benchmarks for real-time translation/subtitle tools for events.
- `references/participant-management.md`: CSV import flow and attribute curation guidelines.
