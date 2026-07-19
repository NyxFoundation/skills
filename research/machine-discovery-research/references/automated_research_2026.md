# Automated Research with Lean4 Formalization (2026 Survey)

This document maps the state-of-the-art in automated mathematical research as of July 2026, emphasizing the shift from "solving problems" to "discovering theories" via formalization.

## 1. Key Systems & Paradigms

### A. Formal Proof Scaling (The "Engine")
- **DeepSeek-Prover-V2**: Massive-scale synthetic data + RL. Focuses on subgoal decomposition to tackle research-level complexity.
- **Goedel-Prover-V2**: High-efficiency (8B-32B models) using scaffolded data synthesis and self-correction.
- **Leanabell-Prover**: Explores post-training scaling and Long CoT in formal reasoning.

### B. Discovery Frameworks (The "Intuition")
- **FunSearch (DeepMind)**: LLM + Evolutionary search. Found new solutions to Cap Set and Bin Packing.
- **AlphaEvolve (Tao et al)**: Evolutionary coding agent for mathematical exploration.
- **AlphaProof**: Integration of RL + Lean for IMO-level geometry and algebra.

### C. Agentic Research (The "Scientist")
- **Danus**: Fact-Graph Memory for orchestrating multi-agent mathematical reasoning.
- **OpenProver**: Planner-Worker-Verifier architecture with whiteboard/repository.
- **MathCoPilot**: Human-AI symbiotic system for steering high-level research direction.

## 2. Critical Gaps & Opportunities
- **Unified Loop**: Lack of systems that *self-generate* a conjecture $\rightarrow$ *formalize* it in Lean $\rightarrow$ *prove* it $\rightarrow$ *derive* new conjectures.
- **Theoretical Grounding**: Most current systems are empirical (RL/SFT). Opportunity for approaches based on Type Theory, Category Theory, or Proof Theory.
- **Concept Discovery**: Transitioning from "solving known problems" to "discovering new mathematical concepts/objects" is the current frontier.

## 3. Reference Benchmarks
- **miniF2F**: Standard benchmark for Lean proving.
- **PutnamBench**: High-difficulty competition math.
- **Ramanujan Challenge**: Focus on fundamental mathematical constants.
- **Ineq-Comp**: Evaluates compositional reasoning in inequalities.
