---
name: key-person-recon
description: Workflow for identifying and extracting SNS/contact accounts for key executives and founders of a target list of companies.
---

# Key Person Reconnaissance

## Trigger
Use this skill when the user asks to "pickup", "find", "list", or "search for" key persons (CEO, Founders, CTOs, etc.) and their social media/contact handles (X, LinkedIn, Facebook, Email) for a specific set of companies.

## Workflow

1. **Entity Extraction**
   - Identify the list of target companies.
   - Define the target roles (e.g., "Founder", "CEO", "Country Manager").

2. **Parallel Discovery (Delegation)**
   - Split the company list into balanced batches to avoid timeouts and rate limits.
   - Dispatch subagents to perform the following for each company:
     - Search for current leadership (Company Name + "CEO" / "Founder").
     - Cross-reference names across X, LinkedIn, and official "About" pages.
     - Verify the identity (check if the X account actually mentions the company or is verified).

3. **Data Structuring**
   - Consolidate results into a structured table.
   - **Required Columns**: Company, Score (if applicable), Name, Role, X Handle, LinkedIn URL, Facebook, Email.
   - Use placeholders (`—`) for missing data.

4. **High-Signal Synthesis**
   - Create a "Priority Contact" list based on:
     - High Score (e.g., 100).
     - High social activity/reach.
     - Strategic importance (e.g., "Attention Is All You Need" co-author).

5. **Delivery**
   - Provide a full markdown file for record-keeping.
   - Provide a concise table in the conversation/issue comment for immediate action.

## Pitfalls & Lessons

- **LinkedIn Walls**: Direct LinkedIn URL extraction often hits login walls. Present the URL but note that manual verification is recommended.
- **Corporate vs. Personal**: Distinguish clearly between a company's official X account and the CEO's personal account.
- **Name Ambiguity**: Always verify the person's current role to avoid picking up former employees or people with the same name.
- **Timeout Prevention**: For lists > 10 companies, always use `delegate_task` in small batches (approx. 5-8 companies per agent).

## Formatting Preferences
- **Tables**: Use clean markdown tables for lists.
- **Handles**: Use `@handle` format for X to make it instantly recognizable.
- **Priority**: Explicitly call out the "Top 10" or "High Priority" targets at the end.
