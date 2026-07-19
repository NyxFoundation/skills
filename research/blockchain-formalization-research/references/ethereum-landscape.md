# Ethereum Formalization Landscape (2026)

This reference maps the state of Ethereum's formalization across its stack, used as a baseline for gap analysis and identifying targets for Lean4 unified formalization.

## Execution Layer (EVM)
- **KEVM (K Framework)**: Most comprehensive operational semantics. Covers opcodes, gas, and state transitions. $\rightarrow$ [GitHub: runtimeverification/evm-semantics]
- **eth-isabelle (Isabelle/HOL)**: Early Lem-based approach. $\rightarrow$ [GitHub: pirapira/eth-isabelle] (Archived)
- **zkEVM-verifier (Lean4)**: Prototype covering arithmetic opcodes. $\rightarrow$ [GitHub: GideonDevRel/zkevm-verifier-prototype]
- **EELS (Python)**: Official executable spec. Not formally verified but is the semantic ground truth. $\rightarrow$ [GitHub: ethereum/execution-specs]

## Consensus Layer (PoS)
- **Ethereum PoS (Rocq/Dafny)**: Formal verification of PoS core. $\rightarrow$ [Refer to formal-eth list]
- **CBC Casper (Isabelle/HOL)**: Correct-by-construction Casper. $\rightarrow$ [GitHub: ethereum/cbc-casper] (Archived)
- **Consensus Specs (Python)**: Ground truth for PoS semantics. $\rightarrow$ [GitHub: ethereum/consensus-specs]

## Networking Layer (P2P)
- **Current State**: $\mathbf{VOID}$. No significant formalizations of devp2p, libp2p, or RLPx found.
- **Gap**: High priority for a "Complete Formalization" project.

## Cryptography
- **Lean4 Progress**: FRI and some ZK-related primitives are being formalized (via formal-eth).
- **Other**: KZG (Isabelle/HOL) and various commitment schemes.

## Summary Matrix

| Layer | status | Tool | Ground Truth |
|---|---|---|---|
| P2P | $\times$ | None | devp2p/libp2p code |
| Consensus | $\text{partially}$ | Rocq/Dafny | consensus-specs (Py) |
| Execution | $\checkmark$ | K / Lean4 | execution-specs (Py) |
| Crypto | $\text{partially}$ | Lean4/Isabelle | EIPs / Academic papers |
