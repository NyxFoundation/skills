---
name: machine-discovery-research
description: >
  Specialized workflow for investigating "AI-native mathematics" and machine-discovered 
  mathematical concepts. Focuses on the intersection of LLMs, formal verification (Lean), 
  and information-theoretic views of mathematics (compression).
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ai-native-math, machine-discovered, lean, formal-verification, compression, deepmind]
---

# Machine Discovery Research

This skill provides a structured approach to researching mathematical discoveries made by AI and the emergent field of "AI-native mathematics"—mathematics designed for AI's internal representation and verification rather than human intuition.

## When to Use

Load this skill when the user asks about:
- AI-discovered mathematical conjectures, definitions, or theorems.
- The relationship between LLMs and formal proof assistants (Lean, Isabelle, Coq).
- Theories on "compression" as the fundamental driver of mathematical definition (e.g., Aksenov et al. 2026).
- State-of-the-art systems like AlphaProof, AlphaGeometry, FunSearch, and DeepSeek-Prover.
- **Automated Research Systems**: Designing closed-loop systems that integrate theory generation, formalization, and verification.

## Key Concepts & Frameworks

### 1. AI-Native Mathematics
The shift from "AI for Human Math" (translating human theorems to formal code) to "AI for AI Math" (AI creating definitions that are optimal for AI's internal compression and verification).

### 2. Compression as Definition
The theory that a "good" mathematical definition is essentially a macro that compresses a repetitive or complex set of primitive operations. AI-native math seeks definitions that maximize this compression efficiency for the model's architecture.

### 3. The Formal Loop
The cycle of: `AI Hypothesis` $\rightarrow$ `Formalization (Lean)` $\rightarrow$ `Verification (Compiler)` $\rightarrow$ `Self-Improvement/Reinforcement`.

## Research Workflow

1. **Landscape Mapping**: 
   - Search for specific AI-discovered constants or concepts (e.g., "natural slope" in knot theory).
   - Track the transition from "discovery by pattern recognition" $\rightarrow$ "discovery by formal search".
2. **Technical Analysis**:
   - Analyze the "compression ratio" or dependency depth of machine-generated proofs vs. human proofs.
   - Compare synthetic data generation methods (e.g., DeepSeek-Prover's large-scale synthetic data).
3. **Verification Audit**:
   - Identify the formal system used (Lean 4 is current SOTA).
   - Check for the existence of the result in `mathlib` or other formal libraries.

## Pitfalls & Lessons

- **Human Interpretation Bias**: AI may discover a relationship that is mathematically true but lacks a "natural" name in human language. Avoid forcing a human-centric interpretation unless explicitly requested.
- **Formalization Gap**: A result "found" by an LLM is only a conjecture until it is formally verified in a system like Lean. Distinguish clearly between "LLM discovery" and "Formally Verified Discovery".
- **Rate Limits on Research**: When performing deep dives into arXiv or DeepMind blogs, combine `web_search` with `browser_navigate` to bypass API rate limits and get full page content.

## Reference Materials
- See `references/ai_math_landscape.md` for a curated map of key papers and systems.
