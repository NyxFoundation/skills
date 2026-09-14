---
name: youtube-technical-viz
description: Workflow for creating high-fidelity technical architecture and flow diagrams for YouTube content, focusing on accessibility, clarity, and "island-style" compositions.
---

# YouTube Technical Visualization

This skill governs the creation of technical diagrams (architecture, data flow, security models) specifically designed for video content where viewers must be able to follow complex paths quickly.

## Core Principles
- **Island-Style Composition (AWS Metaphor)**: Group related components into "islands" (large dashed boundary boxes). Nest smaller islands within larger ones (e.g., Secure Element inside a Hardware Device) to represent trust boundaries and physical/logical containment.
- **Scenario-Based Color Coding**: Do not use one color for all arrows. Assign distinct colors to specific scenarios (e.g., Key Generation = Red, Signing = Blue) so multiple flows can coexist on one diagram without confusion.
- **Numbered Sequential Flow**: Every flow must be traceable via numbers (① $\rightarrow$ ② $\rightarrow$ ③). Place numbers in small circles centered on the arrows.
- **High Contrast / Dark Mode**: Prefer dark backgrounds (`#0d1117`) with high-contrast accents (neon-like colors for flows) to ensure legibility on YouTube's compressed video format.

## Implementation Workflow
1. **Define the Islands**: Identify the top-level actors (dApp, User Device, Server, Blockchain).
2. **Define the Nesting**: Identify sub-components (e.g., within "Device" $\rightarrow$ "Firmware" and "Secure Element").
3. **Map the Scenarios**: List the distinct flows to be visualized (e.g., "Seed Recovery", "Transaction Signing").
4. **Assign Colors**: Map each scenario to a unique, high-contrast color.
5. **Plot and Number**: Draw the arrows, ensuring the sequence is logical and the numbers are clearly visible.
6. **Add Contextual Metadata**: Include a legend for colors and "Vuln-Boxes" (summary of common vulnerabilities for that specific architecture) to add immediate value.

## Pitfalls & Best Practices
- **Avoid "Spaghetti" Lines**: Use `connectionstyle="arc3,rad=..."` to create slightly curved lines that avoid overlapping components.
- **Key Markers**: Explicitly mark where private keys are stored or derived using a distinct visual cue (e.g., a red dashed box labeled "KEY").
- **Legibility**: Use large font sizes for headers and a clean, sans-serif font (e.g., IPAGothic).
- **Avoid Overcrowding**: If a diagram becomes too complex, split it into "Architecture View" and "Detailed Scenario View" rather than squeezing everything into one.

## Tooling (Matplotlib)
- Use `FancyBboxPatch` for islands and components.
- Use `annotate` with `arrowprops` for sequential flows.
- Use `Circle` for step numbering.
