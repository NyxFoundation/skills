---
name: corporate-financial-research
description: Workflow for extracting consolidated revenue, segment breakdowns, and technology focus areas from corporate IR materials and public data.
tags: [IR, financial-analysis, corporate-research, segment-analysis]
---

# Corporate Financial Research Workflow

This skill governs the extraction and synthesis of financial data (consolidated revenue, segment ratios) and the mapping of these business units to specific technical domains (e.g., Formal Verification, AI Safety).

## Trigger Conditions
- User asks for "連結売上" (consolidated revenue) or "セグメント構成" (segment breakdown) of specific companies.
- User wants to map corporate business units to a technical field (e.g., "Identify which parts of Toyota's business relate to Formal Verification").
- User needs a ranked list of companies by revenue within a specific industry or consortium (e.g., CSS participants).

## Execution Steps

1. **Entity Identification**: List all target companies and verify their exact corporate names (English/Japanese).
2. **Data Acquisition (Hierarchical Approach)**:
    - **Tier 1: Direct IR Access (Preferred)**: Attempt to fetch latest "決算短信" (Financial Results) or "有価証券報告書" (Annual Securities Report) via `browser_navigate` or `curl`.
    - **Tier 2: Financial Summary Sites**: Use `web_search` for trusted financial news or summary sites (e.g., Nikkei, Yahoo Finance) if direct IR sites are blocked or complex.
    - **Tier 3: Knowledge Bases (Wikipedia/Public Data)**: Use `web_extract` or `curl` on Wikipedia as a baseline. **Crucial**: Always check the date of the data (e.g., "2024年3月期") and mark it as "Estimated" or "Old" if it doesn't match the current fiscal year.
3. **Segment Breakdown Extraction**:
    - Identify the main revenue-generating segments.
    - Extract the percentage or absolute value for each segment.
    - Map these segments to the user's technical interest (e.g., "Automotive" $\rightarrow$ "ADAS/Safety Verification").
4. **Synthesis & Mapping**:
    - Rank companies by revenue.
    - Create a mapping table: `Company` $\rightarrow$ `Business Segment` $\rightarrow$ `Technical Relevance (High/Med/Low)` $\rightarrow$ `Specific Use Case`.
5. **Output Generation**:
    - Deliver a structured report (Markdown) with clear distinctions between verified data and estimations.
    - Include a "Data Freshness" column in tables.

## Pitfalls & Workarounds

- **Bot Detection/Blocking**: Many Japanese IR sites (Sony, Hitachi, etc.) block automated `curl` or `browser_navigate`.
    - *Workaround*: Fall back to financial summary articles via `web_search` or use a sequence of `browser_click` actions to simulate human navigation from the top page.
- **Complex URL Structures**: IR libraries often use session-based or dynamically generated URLs.
    - *Workaround*: Search for the specific PDF filename or use a search query like `site:company.com "決算短信" "2025"` to find direct links.
- **Stale Wikipedia Data**: Wikipedia often lags by 1-2 years for financial data.
    - *Workaround*: Treat Wikipedia as a *structural* guide (to find segment names) but verify the *numbers* via current news search.

## Verification Steps
- [ ] Does the total revenue match the sum of segments?
- [ ] Are the fiscal years (e.g., FY2025) explicitly stated for every value?
- [ ] Is the technical mapping based on public R&D statements or industry standards (e.g., ISO 26262 for automotive)?
