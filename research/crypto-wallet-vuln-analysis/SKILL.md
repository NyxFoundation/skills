---
name: crypto-wallet-vuln-analysis
description: Workflows for analyzing cryptocurrency wallet vulnerabilities using structured datasets, focusing on the disconnect between displayed data and signed data.
---

# Crypto Wallet Vulnerability Analysis

This skill governs the analysis of wallet vulnerabilities, specifically identifying where the "trust boundary" is breached and how vulnerabilities manifest in the transaction signing flow.

## Core Analysis Framework

When analyzing wallet vulnerabilities (especially using the `wallet-vuln-dataset`), focus on the **signing pipeline**:
`dApp/RPC` $\rightarrow$ `TX Construction` $\rightarrow$ `Encoding` $\rightarrow$ `UI/UX Display` $\rightarrow$ `User Confirmation` $\rightarrow$ `Signing`.

### Key Vulnerability Classes
1. **Signed-Differs-From-Shown (Display Gap)**:
   - The most critical class for Hardware Wallets.
   - **Mechanism**: The bytes sent to the secure element for signing are different from the bytes parsed and displayed to the user.
   - **Root Causes**: Small screens leading to omission of data, parser bugs in firmware, or malicious RPCs providing malformed data that is ignored by the UI but accepted by the signer.
2. **Signature Verification Gap**:
   - Flaws in the verification logic within the wallet firmware or library.
3. **Encoding Canonicalization**:
   - Accepting non-canonical encodings (e.g., U256 padding) that can lead to malleability or unexpected execution.

## Analysis Workflow

1. **Path Mapping**: Identify the attack path. 
   - **Hostile RPC/Network**: Data is corrupted at the source.
   - **Malformed Input**: dApp sends logically incorrect data.
   - **Pairing/Deeplink**: Data enters via side-channels.
2. **Mechanism Identification**: Determine if the bug is in the *display* (UI), the *parser* (firmware/lib), or the *verifier* (crypto logic).
3. **Cross-Wallet Comparison**: 
   - Compare HW wallets (display-constrained) vs. Software wallets (lib-constrained).
   - Note that HW wallets often have the highest count of "Display Gap" bugs due to their physical constraints.

## Pitfalls & Lessons
- **The "Seed Security" Fallacy**: Do not assume a wallet is safe just because the seed is in a Secure Element (SE). Most vulnerabilities occur in the *data* the seed is asked to sign, not the seed itself.
- **SPOF Analysis (ERC-4337)**: When analyzing Account Abstraction, distinguish between the **EntryPoint** (singleton protocol infrastructure, trusted root) and **Paymasters/Bundlers** (third-party service providers).

## Verification
- Verify results by correlating `attack_path` with `mechanism` and `root_cause` in the dataset.
- Use `Counter` and cross-tabulation scripts to identify patterns across wallet categories.
