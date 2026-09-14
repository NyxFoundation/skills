---
name: youtube-technical-narrative
category: creative
description: Designing high-impact technical educational content for YouTube using Narrative Heat Engineering (NHE) and data-driven storytelling.
---

# Technical Content Design for YouTube (NHE)

Guidelines for designing high-impact technical educational content (specifically for YouTube) using the Narrative Heat Engineering (NHE) framework.

## Trigger Conditions
- When asked to plan a YouTube video, technical presentation, or educational series.
- When transforming a dataset or technical audit into a public-facing narrative.

## Core Principles
1. **Central Proposition (NHE Step 3)**: Every video must have one single, provocative, and counter-intuitive central proposition. Avoid "Overview of X"; prefer "X is actually Y".
2. **S-Curve Heat Management**: Structure the narrative to oscillate between high-tension (problem/crisis/counter-intuition) and low-tension (explanation/resolution/safe harbor).
3. **Visual-First Evidence**: Technical claims must be backed by visual artifacts (diagrams, commit diffs, logs) rather than just text descriptions.
4. **Audience-Centric Framing**: Translate technical vulnerabilities into "User-Facing Risks" (e.g., instead of "buffer overflow", use "how an attacker can steal your seed").

## Workflow
1. **Proposition Discovery**: Analyze data to find the "surprising truth" (e.g., "Hardware wallets are hacked via UI deception, not seed theft").
2. **Structure Mapping**:
    - **Hook**: Immediate tension. Challenge a common belief.
    - **The Gap**: Show the distance between "what users think" and "what the data shows".
    - **Mechanism Deep Dive**: Step-by-step visual explanation of the "How".
    - **Resolution/Action**: Concrete steps the user can take to be safer.
3. **Asset Generation**:
    - Create high-contrast, dark-mode compatible diagrams (prefer `#0d1117` backgrounds for YouTube/Dev audiences).
    - Use color-coding for trust boundaries (e.g., Red for keys, Green for signing, Blue for network).
    - **Architecture Flows**: Map the "Key Location" $\rightarrow$ "Processing Path" $\rightarrow$ "Vulnerability Point" to make abstract bugs tangible.
4. **Title & Meta Engineering**:
    - Use "Number-based" hooks (e.g., "16,854 entries reveal...").
    - Avoid clickbait; use "Intellectual Curiosity" hooks.

## Pitfalls
- **Too much breadth**: Trying to cover 10 different bugs. Pick 3-5 representative "clusters" of bugs.
- **Text-heavy slides**: If a diagram has more than 3 sentences of text, it's a document, not a video asset.
- **Over-explaining the obvious**: Assume the audience knows basic terms, but explain the *nuanced* failure mode.

## Verification
- Does the title promise a specific discovery?
- Does the "Central Proposition" invert a common misconception?
- Are the visuals capable of explaining the mechanism without the narrator speaking?
