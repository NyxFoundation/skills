---
name: academic-conference-recon
description: Systematic reconnaissance of academic conferences and workshops to inform guest lecture proposals, research alignment, and submission strategies.
---

# Academic Conference Reconnaissance

This skill provides a workflow for analyzing the history, structure, and trends of academic conferences (and their associated workshops) to ensure that proposed talks or submissions are timely, distinct from previous years, and aligned with the community's interests.

## Trigger Conditions
- User is asked to propose a talk/lecture for a conference or workshop.
- User needs to understand the "vibe," target audience, or recurring themes of a specific academic event.
- User needs to identify potential gaps in a conference program where their specific research would be a strong fit.

## Workflow

### 1. Broad Program Discovery
- Navigate to the official conference website for the current and previous 3-5 years.
- Extract the high-level structure:
    - Keynote speakers and their topics.
    - Session categories (Tracks/Workshops).
    - The balance between academic research and industrial application.
    - Hybrid/On-site/Online modality trends.

### 2. Targeted Workshop Analysis
If the target is a specific workshop (e.g., FWS, BWS):
- **Chronology**: Identify when the workshop was established.
- **Content Evolution**: Track how topics have shifted. (e.g., from tool-centric to application-centric).
- **Guest Lecture Patterns**:
    - Who were the invited speakers?
    - What was the "angle" of their talks? (e.g., "Intro to Tool X" vs. "Applying X to Real-world Problem Y").
    - Duration and format (e.g., 50-minute talk + Q&A, combined with tutorials/hands-on).

### 3. Ecosystem Mapping
- **Institutional Presence**: Identify recurring universities, research labs (e.g., NICT, JST), and corporate partners (e.g., NTT, Hitachi, Toyota).
- **Keyword Extraction**: List the dominant technical terms appearing in the last 2-3 years to use in the proposal's abstract for better alignment.

### 4. Gap Analysis & Positioning
- Compare the user's proposed topic against the extracted history.
- **Avoid Redundancy**: If "Intro to Lean 4" was done last year, pivot to "Lean 4 in Production for Project X."
- **Identify Synergy**: Find connections between the user's work and other workshops (e.g., Blockchain $\leftrightarrow$ Formal Verification).

## Pitfalls & Tips
- **Dynamic Content**: Program pages are often just lists of titles. Always attempt to extract "Abstracts" or "Overviews" to understand the *depth* of the content.
- **Hidden Gems**: Look for "BoF" (Birds of a Feather) or "Lightning Talk" sessions to find emerging interests that aren't yet in the main keynote.
- **Naming Conventions**: Be aware of acronyms (e.g., CSS in Computer Science vs. CSS in Web Dev) and use site-specific searches (`site:domain.org`) to filter noise.

## Verification
- [ ] Does the proposal abstract avoid repeating a topic covered in the last 2 years?
- [ ] Are the keywords used in the abstract consistent with the conference's recent trends?
- [ ] Is the suggested format (Talk vs. Tutorial vs. Panel) consistent with the workshop's typical structure?
