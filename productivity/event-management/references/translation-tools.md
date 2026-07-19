# Translation & Subtitle Tool Benchmarks for Events

## Requirement: Global Events with Simultaneous Interpretation
Common scenario: High-profile speaker in English $\rightarrow$ Japanese audience $\rightarrow$ Real-time screen subtitles.

### Tool Comparison Matrix

| Tool | Category | Quality | Cost/Effort | Pros/Cons |
|---|---|---|---|---|
| **Interprefy** | Professional | High (Human) | High ($\approx$¥30-50k/day) | $\checkmark$ Professional grade, low latency. $\times$ Expensive. |
| **KUDO** | Professional | High (Human) | Variable | $\checkmark$ Specialized for diplomacy/corporate. $\times$ Complex setup. |
| **VoicePing** | AI-Driven | Medium | Low-Mid (¥5-10k/day) | $\checkmark$ Fast deployment, scalable. $\times$ Lower accuracy than humans. |
| **StreamYard** | Streaming | Low-Mid | Low | $\checkmark$ Easy iPhone/Web integration. $\times$ limited native JP translation. |
| **OBS + Whisper** | Custom Dev | Medium-High | Low (Dev cost only) | $\checkmark$ Full control, no recurring fee. $\times$ High technical debt. |

### Recommended Configurations

1. **Gold Standard (Budget exists)**: 
   - Tool: **Interprefy** + 1 Certified Human Interpreter.
   - Setup: Direct audio feed $\rightarrow$ Interpreter $\rightarrow$ Overlay subtitles on main screen.

2. **Agile/Budget Standard**: 
   - Tool: **StreamYard** (for broadcast) + **VoicePing** (for subtitles).
   - Setup: iPhone Camera $\rightarrow$ StreamYard $\rightarrow$ YouTube/X.

3. **Technical/DIY Approach**:
   - Tool: **OBS** $\rightarrow$ **OpenAI Whisper API** $\rightarrow$ Custom Overlay.
   - Setup: Requires a dedicated machine for transcription/translation processing.
