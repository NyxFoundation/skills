---
name: pr-drafting-workflow
description: Workflow for creating and managing public relations (PR) drafts for technical projects, incorporating Narrative Heuristic Engineering (NHE) and multi-platform synchronization (GitHub/Notion).
---

# PR Drafting Workflow

This skill governs the end-to-end process of transforming technical project states into public-facing PR drafts. It prioritizes "narrative" over "list" and ensures high-fidelity synchronization between working drafts, review platforms (GitHub), and long-term knowledge bases (Notion).

## Trigger Conditions
- User asks to "prepare PR drafts" or "fill in items for PRs".
- Task involves translating technical milestones/OSS releases into promotional content.
- Multiple projects need parallel draft generation with a consistent structure.

## Workflow Steps

### 1. Information Harvesting
- **Cross-Reference Sources**: Do not rely on a single source. Synthesize information from:
    - GitHub READMEs and technical specs.
    - Notion project databases.
    - Past press releases (to match tone/style).
    - Recent commit history or a "digest" of project progress.
- **Gap Analysis**: Identify missing items required by the PR template (e.g., specific dates, contact points, "Why now").

### 2. Narrative Construction (NHE)
- **Avoid Bullet-Point Lists**: Prefer logical, descriptive prose (Report style).
- **Exclude Rhetorical Flourish**: For technical PRs, eliminate exaggerated, emotive, or "marketing-heavy" language. Avoid "AI-isms" (e.g., overly dramatic metaphors like "hunting gaps" or "exposing to the swarm"). Do not use phrases that suggest a problem "shakes the foundations" or is a "fundamental challenge." Focus on factual correctness and precise technical definitions.
- **Accessibility (General Audience)**: Use a style that is accessible to non-specialists. When using technical terms, provide a concise explanation in parentheses immediately following the term (e.g., "NTT (Number Theoretic Transform: a mathematical transformation for fast polynomial multiplication)").
- **Link Density**: Ensure every draft includes a comprehensive "Reference Links" section with direct URLs to GitHub repositories, original papers, demo videos, and official documentation. Do not omit these.
- **Focus Areas**:
    - **The "How"**: Detail the proposed method/technical breakthrough.
    - **The "Result"**: Use concrete examples or execution results to prove value.
- **Template Adherence**: Map the narrative directly to the required items specified by the user/template.

### 3. Parallel Execution (Scaling)
- For multiple projects, use `delegate_task` to spawn subagents.
- **Context Injection**: Pass the specific project's harvested data and the global NHE guidelines to each subagent to ensure consistency.
- **Verification**: Read and review subagent outputs before delivery; manually fill gaps for missing projects.

### 4. Multi-Platform Delivery
- **GitHub (Review Loop)**:
    - Post drafts as individual comments on the tracking issue to avoid character limits and allow granular feedback.
    - Provide a summary table at the end listing all projects, external verification status, and key dates.
- **Notion (Knowledge Base)**:
    - Save drafts to the designated database (e.g., Scrapbox DB).
    - Use structured blocks (Headings, Bullet points) rather than one giant text block.
    - Apply relevant tags (e.g., `PR原稿`, `ProjectName`) for future retrieval.

## Pitfalls & Constraints
- **Character Limits**: GitHub comments have limits. Split large drafts into multiple comments.
- **External Approval**: Flag drafts that require external (third-party) approval (e.g., partner companies) and mark them clearly as "Review Required".
- **Notion Block Limits**: Notion API has a 100-block limit per page creation. Split content into chunks if necessary.

## Verification
- [ ] Does the draft avoid simple bullet lists in favor of a narrative structure?
- [ ] Are all template items filled?
- [ ] Is the draft present in both GitHub (for review) and Notion (for storage)?
- [ ] Are third-party dependencies (approvals) clearly highlighted?
