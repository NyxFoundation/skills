# Knowledge Bank: Trading Algorithm & DeFi Verification

## Core Research Leads (2018-2026)

### ZK-Based Private Trading
- **ChainBot (arXiv:2109.11270)**: Fundamental approach to hiding the "secret sauce" of an algorithmic trading bot using ZK proofs while proving execution integrity. Reference for "secret-sauce" concealment.
- **NECTAR (arXiv:1803.04860)**: Early work on non-interactive smart contract protocols for privacy and verification using zk-SNARKs.

### Formal Verification Tools & Approaches
- **KindHML (arXiv:2604.14038)**: Use of Hennessy-Milner logic and Kind 2 model checker to verify *temporal properties* across multiple transactions (e.g., liquidity attacks, front-running).
- **VeriSol (Microsoft)**: High-automation verifier using Boogie/Z3 for Solidity semantic conformance against state machine models.
- **Dafny Case Study (arXiv:2510.24798)**: Compositional bottom-up verification of a token sale launchpad (asset conversion, refund mechanics). Proves safety properties like "refunds $\le$ original deposit".
- **FSPVM-E (arXiv:1805.00808)**: Coq-based symbolic process virtual machine for ERC20 and Solidity, using execution-verification isomorphism.

### Honeypot & Scam Detection
- **HoneyBadger (arXiv:1902.06976)**: Symbolic execution + heuristics to detect honeypots. 87% accuracy.
- **SCSGuard (arXiv:2105.10426)**: GRU-based deep learning on N-gram bytecode patterns for fast scam detection (Ponzi/Honeypot/Phishing).

## Identified Research Gaps
- **Integrity $\neq$ Safety**: Most ZK-trading work focuses on *integrity* (the bot did what it said it would do) rather than *safety* (the bot won't lose funds to a honeypot).
- **Vault Invariants**: Lack of systemic formal verification for vault-based trading (solvency, redemption guarantees).
- **Honeypot Formalization**: Detection is solved via ML/Symbolic execution, but *formal proof* that an algorithm is immune to honeypots is missing.
