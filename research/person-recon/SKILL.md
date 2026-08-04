---
name: person-recon
description: High-fidelity reconnaissance of key individuals for sponsorship, recruiting, or business development. Focuses on identifying decision-makers, mapping their influence, and discovering reachable social/contact channels.
---

# Person Reconnaissance Workflow

This skill governs the process of identifying and locating key personas (CEOs, Founders, Country Managers, Lead Scientists) within specific organizations, especially in the Japan/APAC tech landscape.

## 1. Target Identification
- **Identify the Right Role**: Don't just look for the CEO. Look for the "Japan Country Manager", "Head of [Dept] Japan", or "Principal/Staff Scientist" (for AI/Research).
- **Cross-Reference Entities**: In joint ventures (e.g., Soneium), identify key people from both the parent companies (Sony) and the operating partners (Startale).

## 2. The Search Stack (Recursive Discovery)
Use a multi-layered approach to uncover profiles that are not directly indexed:

1. **Direct String Search**: `"Person Name" "Company Name" linkedin`
2. **Boolean Variations**: Use OR for name variations (e.g., `"Jun Watanabe" OR "渡辺 潤"`).
3. **Platform-Specific Dorks**: 
   - X (Twitter): Search for bio keywords (e.g., `site:x.com "Google DeepMind" "Tokyo" "Staff Research Scientist"`).
   - LinkedIn: Since direct browsing is often blocked by login walls, use Google search operators to find the public profile URL first.
4. **X-Search (Grok)**: Use `x_search` to find active researchers/executives who may not have updated their LinkedIn but are very active on X. This is often the highest-signal channel for AI/Web3 personas in Japan.

## 3. Contact Channel Mapping
Categorize findings by "Reachability":
- **Tier 1 (Direct)**: Public Email (rare), active X/Twitter account (high signal).
- **Tier 2 (Professional)**: LinkedIn profile ( medium signal, depends on InMail).
- **Tier 3 (Indirect)**: Company "Contact Us" forms, mutual connections.

## 4. Output Format
Deliver results in a structured table or markdown list containing:
- **Full Name** (incl. Kanji if applicable)
- **Exact Title/Role**
- **Base Location**
- **Active Social Handles** (X, LinkedIn)
- **Contact Status** (e.g., "No public email found", "Active on X")
- **Context/Notes**: Why this person is a key target (e.g., "Leads the Tokyo site").

## Pitfalls & Pro-Tips
- **The "Common Name" Trap**: "Jun Watanabe" may return a clothing brand or a K-pop star. Always anchor searches with the company name (e.g., `"Jun Watanabe" Sony`).
- **The Login Wall**: Avoid trying to "browse" LinkedIn via the browser tool as it usually hits a login wall. Use `web_search` or `x_search` to find the *link* first, then verify via search snippets.
- **Kanji Power**: Searching in Japanese (e.g., `渡辺 潤` instead of `Jun Watanabe`) often unlocks local Japanese press releases or official corporate rosters that English searches miss.
- **Sponsorship Context**: For sponsorship outreach, prioritize the "Connector" (the person who spans multiple entities) to maximize the impact of a single point of contact.
