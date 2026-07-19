# Otter.ai Event Transcription & Translation Analysis

## Tool Overview
Otter.ai is a high-fidelity AI transcription tool. It is **NOT** a real-time translation tool, though it supports multiple languages.

## Pricing & Plans (as of July 2025)
| Plan | Price (est.) | Transcription Limit | Concurrent Meetings | Key Features |
|---|---|---|---|---|
| **Basic** | Free | 300 min/user/mo | 1 | Basic transcription |
| **Pro** | ~$10-17/user/mo | 1,200 min/user/mo | 2 | 90min max per conv, 100 vocabulary terms |
| **Business** | ~$20-30/user/mo | 6,000 min/user/mo | 3 | 4hr max per conv, 800 vocabulary terms |
| **Enterprise** | Custom | Unlimited | 3+ | SSO, SCIM, custom retention |

## Technical Nuances for Events
- **The "4-Hour Wall"**: Even Business plans limit a single conversation to 4 hours. For full-day events (e.g., 10:00-16:30), recordings must be split into multiple sessions.
- **Language Support**: Supports English, Spanish, French, German, Japanese, and Chinese.
- **The Translation Gap**: 
    - Japanese Audio $\rightarrow$ Japanese Text: $\checkmark$ (Supported)
    - Japanese Audio $\rightarrow$ English Text (Real-time): $\times$ (Not native)
    - Workflow: Otter (Transcription) $\rightarrow$ Google Translate / DeepL (Translation).
    - Expected Latency: 3-5 seconds.

## Accuracy & Domain Challenges
- **General Accuracy**: 80-90% for standard business Japanese.
- **Technical Terminology**: High failure rate for specialized AI/Tech terms without custom vocabulary.
- **Common Misrecognitions**:
    - `MCP` $\rightarrow$ "エムシーピー" or random phonetics
    - `RAG` $\rightarrow$ "ラグ" or "ラグビー"
    - `Function Calling` $\rightarrow$ Phonetic fragments
- **Mitigation**: Use the **Custom Vocabulary** feature (Business plan allows 800 terms).

## Recommended "Agentic Summit" Vocabulary
Ensure these are registered to prevent transcription drift:
- **Protocols**: MCP, Model Context Protocol, A2A, ACP
- **Tech**: RAG, Function Calling, Tool Use, Embeddings, Vector DB, Chain-of-Thought, ReAct
- **Tools**: LangChain, LlamaIndex, AutoGPT, CrewAI, Dify, n8n
- **Models**: GPT-4o, Claude, Gemini, Llama, DeepSeek
- **Orgs**: Anthropic, OpenAI, Google DeepMind, Microsoft, Cohere
