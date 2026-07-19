---
name: cross-domain-formalization-research
description: >
  Specialized workflow for investigating the formalization of non-mathematical domains 
  (Economics, Quantum Information, Chemical Physics, etc.) using interactive theorem provers like Lean 4.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [formalization, lean4, interdisciplinary, economics, quantum-info, physics, academic-research]
---

# Cross-Domain Formalization Research

Guidelines for mapping the "formalization frontier" in fields where interactive theorem proving (ITP) is emerging but not yet standard.

## When to Use
Load this skill when the user wants to:
- Survey existing formalizations of theories in non-pure-math domains (e.g., "Is game theory formalized in Lean?").
- Identify "white spaces" or unformalized areas in a specific scientific or social field.
- Analyze the impact of formalization on a domain (e.g., discovery of proof gaps in original papers).
- Coordinate the definition of a domain-specific library (consensus on definitions).

## Workflow

1. **Breadth Discovery (arXiv/Google Scholar)**:
   - Use a combination of `Lean` + `formalization` + `[Domain Keyword]`.
   - Search for specific library names (e.g., `EconCSLib`, `Lean-Quantum`) once a lead is found.
   - Use `browser_navigate` and `browser_console` (DOM extraction) to paginate through arXiv results quickly.

2. **Deep Dive & Gap Analysis**:
   - Extract abstracts to identify *what* exactly was formalized (axioms, core theorems, or specific applications).
   - Look for mentions of "discovered gaps in published proofs" or "non-obvious constraints"—these are high-value signals for the utility of formalization.
   - Identify the "Foundational Axioms" used from `mathlib` to understand the technical dependencies.

3. **Network Mapping**:
   - Identify key researchers and labs leading the effort (e.g., the role of authority figures like Cirac in Quantum Info).
   - Check for open-source footprints (GitHub repositories) to see the actual implementation of definitions.

4. **Synthesis & Reporting**:
   - Categorize findings by domain (Economics $\to$ Game Theory $\to$ Mechanism Design).
   - Highlight the "Formalization State" (e.g., "Exploratory", "Library-scale", "Verified-Application").

## Pitfalls & Lessons

- **The "OR" Search Trap**: Broad boolean queries (e.g., `Lean AND (Physics OR Chemistry)`) in arXiv can return too many irrelevant results. Prefer narrow, specific queries first, then expand.
- **Definition Drift**: In emerging domains, different groups may formalize the same concept differently. Always check if the formalization aims for a "standard library" (like `mathlib`) or a specific application.
- **The "Sorry" Gap**: A paper claiming formalization may still contain `sorry` (unproven goals). Always check if the "core constructions" are `sorry`-free.
- **AI-Formalization Noise**: With the rise of LLM-assisted formalization (e.g., `MathCoPilot`), distinguish between "AI-generated" and "Human-verified" formalizations.

## Reference Architecture for Reports
When synthesizing, structure the report as:
- **Domain Mapping**: What has been done?
- **Technical Approach**: Which ITP? Which libraries?
- **Academic Value**: Did it find bugs? Did it prove new results?
- **Strategic Gaps**: What is still missing? (The "White Space").
