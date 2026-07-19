---
name: narrative-content-writing
description: Author high-impact technical articles and reports using narrative-driven structures (NHE/Emotion Curve) to maximize engagement and professional authority.
---

# Narrative Content Writing

This skill governs the creation of technical content that avoids the \"AI-standard\" dry list format in favor of a structured narrative designed to lead a professional audience toward a specific conclusion or action.

## Core Methodology: The Narrative Hook & Emotion Curve

Technical content should not be a feature list; it should be a journey.

### 1. Structure: The NHE (Narrative-Hook-Evidence) Pattern
Avoid starting with \"In this article, we will...\". Instead, use a structured flow. **CRITICAL: Use these as a conceptual guide for the narrative flow, but NEVER include the names of these phases (e.g., \"The Valley\", \"The Pivot\") as headings or explicit labels in the final text.**
- **The Hook**: Challenge a common assumption or highlight a hidden danger. Make the reader feel the inadequacy of their current approach (e.g., \"CVE lists are not maps\").
- **The Valley (Tension)**: Present concrete, high-stakes examples of failure (Critical bugs, chain splits) to build tension and prove the problem is real.
- **The Pivot (Turn)**: Introduce the solution or the \"new lens\" (e.g., the dataset, the new method) that resolves the tension.
- **The Climax**: Demonstrate the \"superpower\" provided by the solution (e.g., Cross-client Mutation Analysis, automated formal model generation from prose).
- **Practical Application**: Provide an immediate, time-boxed action plan (e.g., \"The 30-minute plan\").
- **Trust/Transparency**: Honestly address limitations. Convert limitations into trust by showing *how* to use the tool despite them.
- **The Landing**: End with a strong, evocative call to action that leaves the reader with a new mental model.

### 2. The Emotion Curve Feedback Loop
**Bespoke Format Requirements**: For specific PR draft workflows (like NyxFoundation), follow the mandated structured header format (Summary, Date, External confirmation, etc.) but ensure the "Content" section strictly adheres to the NHE narrative flow—avoiding bullet points in favor of a cohesive story.

When reviewing drafts, diagnose the \"temperature\" of the text:
- **Cold/Dry**: Sections that feel like a manual or a list. *Fix: Inject stakes, time-boxes, or \"what happens if you don't do this\" (FOMO).*
- **Weak Landing**: A conclusion that summarizes instead of driving action. *Fix: Use a punchy, imperative final sentence.*
- **Over-Explanation**: Too much \"AI-speak\" (e.g., \"Furthermore\", \"In conclusion\"). *Fix: Use direct, punchy, a-symmetric sentence lengths.*

## Workflow & Verification

1. **Drafting**: Build the skeleton based on the NHE structure.
2. **Diagnosis**: Run an \"Emotion Curve\" check. Specifically look for \"Cold\" sections (too descriptive) or \"Weak\" landings.
3. **Iterative Polishing**: Use high-contrast phrasing (e.g., \"Not X, but Y\") to create narrative momentum.
4. **Final Polish**: Ensure the conclusion is a \"Closing the loop\" moment, not a summary.

## Pitfalls to Avoid
- **The \"Summary\" Trap**: Do not end with \"In summary, we have seen...\". End with a directive.
- **The \"Feature List\" Trap**: Do not list findings without explaining the *implication* (e.g., \"It has 2,000 rows\" $\rightarrow$ \"It is a usable map of the attack surface\").
- **The \"Balanced\" Tone**: Avoid being overly neutral. Professional authority comes from taking a definitive stance on what is critical and what is not.
