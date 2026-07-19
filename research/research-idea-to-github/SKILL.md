---
name: research-idea-to-github
description: >
  Workflow for transforming raw research ideas or a list of topics into structured, 
  well-researched GitHub Issues for a public-facing research repository.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, github, issue-template, academic-synthesis, defi]
---

# Research Idea to GitHub Issue Workflow

This skill governs the process of taking a high-level research interest (e.g., "DeFi Operation Standardization") and expanding it into a professional, research-backed GitHub Issue intended for an audience of researchers, students, and engineers.

## When to Use
Use this skill when the user wants to "organize a topic and add it as an issue" in a research repository (like `NyxFoundation/interests`).

## Workflow

1. **Deconstruction**: Break down the raw idea into key components:
   - Core Objective (What is being solved?)
   - Importance (Why now? What is the pain point?)
   - Expected Contribution (What does success look like?)

2. **Academic Contextualization (The "Research" Phase)**:
   - Perform multi-angle searches (arXiv, Google Scholar, specialized blogs) for "Prior Art".
   - Identify specific papers or frameworks that provide the foundation.
   - **Requirement**: For each cited work, extract: `Link` + `Brief Summary` + `Connection to the current idea` (Why is this relevant?).

3. **Internal Synergy Mapping**:
   - Search the organization's existing repositories/docs for related work.
   - Identify existing tools, datasets, or frameworks that can be leveraged.
   - Explicitly map how the new idea benefits from or extends current internal projects.

4. **Drafting the Issue**:
   Use a structured template (as defined by the repo's `ISSUE_TEMPLATE.md`). Core sections:
   - **Overview**: Elevator pitch.
   - **Why (Importance)**: Detailed problem statement.
   - **What (Contribution)**: Specific goals/outputs.
   - **Prior Art**: The researched links and their relevance.
   - **Internal Synergy**: Connections to organization work.
   - **Target Audience**: Who should care/contribute.

5. **Verification & Delivery**:
   - Review for "AI-isms" and excessive verbosity.
   - Ensure no private/internal links (e.g., Notion) are included in public issues.
   - Use `gh issue create` to push the final draft.

## Pitfalls & Preferences

- **Public vs. Private**: Always verify if the issue is going to a public repo. **NEVER include internal documentation links (e.g., Notion, private wikis) in public GitHub issues.**
- **Nyx Foundation Specifics**:
    - All links to Nyx projects MUST be public GitHub links or links to `nyx.foundation`.
    - The designated contact for all discussions is `contact@nyx.foundation`.
- **Evidence over Claims**: Do not just say "there are papers on this." List the actual papers, their arXiv IDs, and why they matter.
- **Narrative Flow**: Avoid simple bullet points for the "Why" and "What" sections. Use a logical narrative that explains the progression from problem to solution.
- **Connection Mapping**: The value is in the *connection* between the prior art and the new idea. Don't just list papers; explain the "bridge."

## Templates
- See `templates/research-issue-draft.md` for the preferred structure.
