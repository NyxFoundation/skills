# Consensus Formalization Landscape: DAG-based and Decoupled BFT

## Overview
Mapping of formal verification efforts for modern high-performance consensus protocols, specifically focusing on DAG-based and Decoupled Consensus architectures.

## Key Protocol Families & Formalization Status (as of 2026)

### 1. Decoupled Consensus (Narwhal/Tusk, Bullshark, Mysticeti)
- **Architecture**: Separation of reliable transaction dissemination (mempool) from transaction ordering.
- **Current Status**: 
    - **Narwhal/Tusk**: Primarily hand-proven. No comprehensive machine-checked formalization.
    - **Bullshark**: Partial verification of safety using TLA+ (Bertrand et al., 2024). Full verification in theorem provers (Lean/Coq/Agda) is a significant gap.
    - **Mysticeti**: Hand-proven safety and liveness. Highly critical target for formalization due to its use in Sui.
- **Research Gap**: The transition from TLA+ model checking to dependent type proofs (Lean) for these specific protocols is an open research opportunity.

### 2. Classic BFT (HotStuff, Tendermint)
- **HotStuff/LibraBFT**: Formally verified in Agda (Carr et al., 2022) for safety in a single epoch.
- **Tendermint**: Verified using Ivy (Praveen et al., 2024) and TLA+ for safety.
- **Comparison**: Classic BFTs are more "mature" in terms of formalization than DAG-based counterparts.

### 3. Other DAG-BFT / Specialized
- **Algorand**: Verified in Coq (Alturki et al., 2019) for non-asynchronous safety.
- **General DAG-BFT with Dynamic Stake**: Verified in ACL2 (Coglio & McCarthy, 2025) for non-forking.

## Tooling Mapping for Consensus
- **Model Checkers (TLA+, Ivy, ByMC)**: Fast for safety, but limited by state space or specific inductive invariants. Used for "industrial-strength" quick checks.
- **Theorem Provers (Lean, Coq, Agda, Isabelle)**: High effort, but provides absolute mathematical certainty for arbitrary network sizes and complex liveness properties.
- **LLM-Augmented Verification (IsabeLLM)**: Emerging trend (2026) using LLMs to guide theorem prover proofs (e.g., Bitcoin PoW in Isabelle).

## Verification Targets for New Research
- **Liveness Proofs**: Most formalizations stop at Safety. Proving "something eventually happens" (Liveness) is a higher-value target.
- **Optimal Latency**: Proving that a protocol achieves the theoretical lower bound (e.g., 3 rounds in Mysticeti) formally.
- **Dynamic Stake/Membership**: Proving correctness when the validator set changes frequently (Dynamic Stake).
