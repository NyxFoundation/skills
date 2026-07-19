---
name: notion-workflow-optimization
description: High-fidelity Notion page authoring and management for project proposals and structured task deliverables.
---

# Notion Workflow Optimization

This skill governs the process of transforming raw research and proposals into structured, actionable Notion pages. It focuses on high-signal formatting and the mitigation of common API pitfalls.

## Trigger Conditions
- User asks to "create a proposal," "save to page," or "document a plan" in Notion.
- Task requires structured deliverables (tables, to-do lists, headings) rather than simple text updates.

## Core Workflow
1. **Context Retrieval**: Read the target page/database first to understand existing structure and properties.
2. **Proposal Synthesis**: Draft the content in a structured format (Heading 2 $\rightarrow$ Heading 3 $\rightarrow$ Bullet/Paragraph $\rightarrow$ To-Do).
3. **Atomic Block Writing**: Use `blocks/children` append/patch operations to build the page.
4. **Verification**: Verify the block count or content via API to ensure the write was successful.

## Implementation Patterns

### High-Signal Formatting
- **Heading 2**: Main proposal title (e.g., `📋 提案：[Topic]`).
- **Heading 3**: Sub-sections (e.g., `評価基準`, `推奨構成`).
- **Rich Text Formatting**: Use bold for key terms and colors (e.g., red for warnings/critical gaps) to improve legibility.
- **Actionable Ends**: Every proposal must end with a `to_do` block section labeled "次のアクション" to ensure the proposal leads to execution.

### Handling API Pitfalls
- **Archive Errors**: If a `400 validation_error` occurs stating a block is archived, first call `PATCH /v1/pages/{id}` with `{"archived": false}` before attempting to edit children.
- **Rich Text Schema**: Always wrap text in the `rich_text` array: `{"type": "text", "text": {"content": "..."}}`. Simple strings will cause `validation_error`.

## Pitfalls & Lessons
- **Content Truncation**: Large blocks may be truncated in logs. Always verify critical content through a follow-up read if unsure.
- **Siloed Updates**: When updating multiple pages, verify the status of each independently (as seen in the ZKTokyo session) to avoid missing failures in a batch.

## Deliverable Quality Standard
A successful Notion proposal must include:
1. **Executive Summary/Premise**: Clear goals and constraints.
2. **Detailed Analysis/Comparison**: Trade-offs between options (e.g., Tool A vs Tool B).
3. **Concrete Recommendation**: A specific, reasoned choice.
4. **Implementation Map**: Layouts, schedules, or specific configurations.
5. **Next Steps**: Clear, checkable tasks.
