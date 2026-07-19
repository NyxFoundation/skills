# Financial Agentic Trading Knowledge Bank

## Core Paradigms
- **RL-based**: Focuses on optimizing reward functions. High performance but prone to regime shift failures. (e.g., FinRL, Meta-RL-Crypto).
- **LLM-based**: Focuses on reasoning, information synthesis, and planning. Better at handling unstructured data (news, filings) but prone to "stochastic" execution instability.
- **Hybrid (LLM + RL)**: Uses LLMs as high-level feature extractors or risk critics, and RL for low-level execution/optimization (e.g., FinRL-DeepSeek).

## Key Evaluation Challenges
- **Data Leakage**: LLMs often have training data that overlaps with backtest periods. Masking identifiers (KTD-Fin) is required.
- **Intelligence-to-Profit Conversion**: The "cost of intelligence" (inference time/token cost) must be offset by incremental profit (TradeLens).
- **Execution Gap**: There is a significant difference between "signal generation" and "order-level execution" (slippage, latency, order book dynamics).

## Advanced Architectures
- **Hierarchical Multi-Agent**: Manager $\rightarrow$ Analyst structures for specialized information processing (FinCon).
- **Reflective/Memory-Aware**: Using self-critique and layered memory to adapt strategies over time without full retraining (TradingGPT, CryptoTrade).
- **Verification Layers**: Using TEEs or ZK-proofs to ensure the agent actually executed the decision it reasoned about (VET).

## Asset-Specific Nuances (Crypto)
- **On-chain vs Off-chain**: High value in fusing on-chain transparency with off-chain social sentiment.
- **Volatility**: Requires higher risk-sensitivity and faster regime-detection than traditional equities.
