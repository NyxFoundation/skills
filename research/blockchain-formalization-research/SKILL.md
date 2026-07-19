---
name: blockchain-formalization-research
description: >
  Specialized workflow for researching and mapping the formal verification landscape of blockchain protocols.
  Focuses on identifying formal specifications, proof assistants used (Lean, Coq, Isabelle, K),
  and gap analysis across the networking, consensus, and execution layers.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [blockchain, formal-verification, lean4, evm, consensus, p2p, gap-analysis]
---

# Blockchain Formalization Research

Guidelines for investigating the state of formal verification for blockchain protocols, with a focus on mapping existing work to identify gaps for new formalization efforts.

## When to Use

Load this skill when the user asks to survey the formalization status of a blockchain (e.g., Ethereum), identify "complete" formalizations, search for specific EIP formalizations, or perform a gap analysis across the protocol stack.

## Research Workflow

1. **Multi-Layer Mapping**: Decompose the blockchain into distinct layers to ensure comprehensive coverage:
    - **Networking/P2P**: Discovery, handshakes, gossip, libp2p/devp2p.
    - **Consensus**: Block production, finality, validator sets, slashing. Consider structural patterns like Decoupled Consensus (mempool vs ordering) and DAG-based BFT.
    - **Execution/VM**: Opcode semantics, state transitions, gas accounting, ABI (e.g., EVM, WASM).
    - **Cryptography**: Commitment schemes, signature verification, zero-knowledge proofs (e.g., KZG, BLS, FRI).
    - **Application/Contract**: Specific DeFi protocols or system contracts (e.g., Uniswap, Deposit contracts). Focus on *economic safety* (e.g., solvency, solvency-preservation, redistribution logic) and *adversarial robustness* (e.g., honeypot detection, front-running resistance).

2. **Source Identification**:
    - **GitHub Search**: Target keywords combining protocol names with proof assistants (`"ethereum" "isabelle"`, `"evm" "lean4"`, `"casper" "coq"`).
    - **Academic Repositories**: Search arXiv and conference proceedings (e.g., CSF, POPL, PLDI).
    - **Foundation Repositories**: Check official "specs" repositories (e.g., `ethereum/consensus-specs`, `ethereum/execution-specs`) to see if they serve as the ground truth for formalizations.
    - **Awesome Lists**: Search for "Awesome [Protocol] Formal Verification" lists to find curated community mappings.

3. **Evaluation Criteria**:
    - **Verification Depth**: Is it a "specification" (Python/TLA+), a "verified implementation" (Coq/Lean), or "symbolic execution" (K Framework/Manticore)?
    - **Completeness**: Does it cover the entire spec or just a subset (e.g., only 7 arithmetic opcodes)?
    - **Current Status**: Is the project active, WIP, or archived? (Crucial for deciding whether to build upon it or start fresh).

- **Gap Analysis Synthesis**:
    - Construct a matrix mapping Layer $\to$ Formalization Status $\to$ Tool used.
    - Identify "blind spots" (e.g., P2P layers are almost always omitted in blockchain formalizations).
    - For Application/Trading layers, distinguish between *Execution Integrity* (ZK-proofs) and *Economic Safety* (Formal Verification). See `references/trading-verification.md`.

## Pitfalls

- **Confusing "Specs" with "Formalizations"**: Execution specs (like EELS in Python) are *executable* but not *formally verified*. Distinguish between a reference implementation and a mathematical proof.
- **Tool Fragmentation**: Verification work is often split across K, Coq, Isabelle, and Lean. A "complete" formalization usually requires synthesizing results from multiple tools.
- **Version Drift**: Blockchain protocols evolve rapidly (Hardforks). Ensure the formalization targets the current version (e.g., PoS vs PoW) and not an obsolete one.

## Verification Steps

- Verify that all identified projects are linked to a public repository or paper.
- Cross-reference "completed" claims in Awesome lists with actual commit history and proof files.
