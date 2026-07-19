# AI-Native Mathematics & Machine Discovery Landscape

This reference maps the key players, papers, and conceptual shifts in AI-driven mathematical discovery.

## 1. The "Compression" Paradigm
- **Core Theory**: Mathematics is viewed as the search for optimal compression (macros) of primitive symbols.
- **Key Work**: *Compression is all you need: Modeling Mathematics* (Aksenov et al., 2026).
- **Insight**: Human mathematics (HM) is a small, highly-compressed subset of formal mathematics (FM). AI-native math can explore the vast "uncompressed" space to find new, efficient macros.

## 2. Major Systems & Breakthroughs
| System | Focus | Key Discovery/Achievement | Reference |
|---|---|---|---|
| **AlphaTensor** | Matrix Mult. | Faster algorithms via RL | Nature (2022) |
| **AlphaGeometry** | Geometry | IMO-level problem solving | Nature (2024) |
| **AlphaProof** | Formal Proofs | Silver-medal IMO standard in Lean 4 | Nature (2024/25) |
| **FunSearch** | Open Problems | New solutions to cap set problem | Nature (2023) |
| **DeepSeek-Prover** | Scalability | Large-scale synthetic data for Lean 4 | arXiv (2024) |

## 3. AI-Discovered Concepts
- **Natural Slope**: Found by DeepMind in knot theory. An example of AI identifying a geometric/algebraic relation that was previously unknown to humans.
- **Combinatorial Invariance**: AI-guided discovery of new formulas for Kazhdan-Lusztig polynomials in representation theory.

## 4. Toolchain for Machine Math
- **Formalization**: Lean 4 $\rightarrow$ `mathlib` (The "Gold Standard" for verification).
- **Autoformalization**: The process of translating Natural Language $\rightarrow$ Formal Specification.
- **Synthetic Data**: Creating millions of "correct-by-construction" proofs to train LLMs.

## 5. Open Questions for Research
- Can AI create a definition that is *impossible* to express naturally in English but allows for a massive leap in proof efficiency?
- Does the "compression" efficiency of a definition correlate with its "mathematical beauty" or utility?
- How can we "back-translate" AI-native definitions into human-understandable concepts?
