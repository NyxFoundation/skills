# Privacy Pool Anonymity Analysis Reference

## Key Metrics for Quantitative Evaluation
- **Anonymity Set Size**: The number of users/transactions in a pool that are indistinguishable.
- **Effective Anonymity Set**: The set size after removing users identified via heuristics (clustering, timing).
- **Linkability Rate**: Percentage of deposits that can be correctly matched to withdrawals.

## Common De-anonymization Heuristics
- **FIFO (First-In First-Out)**: Assuming the earliest deposit is the most likely candidate for a subsequent withdrawal.
- **Round-trip Analysis**: Matching deposits and withdrawals of the same amount within a specific time window (especially for CEX $\leftrightarrow$ Mixer flows).
- **Transaction Graph Clustering**: Grouping addresses based on interaction history or shared funding sources.
- **Timing/Age Analysis**: Using the distribution of "decoy" ages or transaction timestamps to identify real inputs.

## Reference Papers & Findings
- **Tornado Cash (2025)**: FIFO matching and cross-chain analysis linked >$2.3B in withdrawals (Cristodaro et al.).
- **Monero (2017)**: Age distribution analysis achieved 80% accuracy in identifying real inputs (Möser et al.).
- **Zcash (2018)**: Usage pattern heuristics significantly reduced the effective anonymity set (Kappos et al.).
