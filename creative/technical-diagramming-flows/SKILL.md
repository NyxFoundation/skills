---
name: technical-diagramming-flows
description: Workflow for creating high-fidelity technical architecture and data-flow diagrams for educational content (e.g., YouTube).
---

# Technical Diagramming Flows

This skill governs the creation of architecture and process diagrams where the goal is to explain complex technical systems to a human audience.

## Core Principles

### 1. Architecture vs. Flow
- **Architecture** shows the "where" (boundaries, components, key locations).
- **Flow** shows the "how" (the sequence of actions over time).
- For educational content, combining both is essential. Do not just draw boxes; show the movement of data.

### 2. The "Island" (Boundary) Pattern
When representing systems with different trust levels or physical locations:
- Use **Islands (Boundary Boxes)** to group components.
- Nested Islands: Use nested boxes to show hierarchy (e.g., Device $\rightarrow$ Firmware $\rightarrow$ Secure Element).
- Simplified Islands: If the internal components are too cluttered, use the island as a simple boundary and move the internal logic into the flow arrows.

### 3. The "Node + Action" Pattern (v4)
For maximum legibility and "AWS-style" cleanliness:
- **Nodes**: Use compact "Icon + Label" nodes instead of large boxes.
- **Edges (Flows)**: All logic resides in the arrows.
- **Edge Labeling**: Always use `[Step Number]: [Action Name]` (e.g., `1: Request Signature` $\rightarrow$ `2: Verify PIN`).
- **Color Coding**: Use distinct colors for different scenarios (e.g., Red for KeyGen, Blue for Signing, Green for Updates) to allow multiple flows to coexist on one map.

## Execution Workflow

1. **Define Actors**: Identify all entities (dApp, Host PC, Secure Element, Blockchain).
2. **Map Scenarios**: Define the 2-3 primary paths (e.g., "The happy path for signing", "The recovery path").
3. **Layout Nodes**: Position actors logically (usually Left $\rightarrow$ Right or Top $\rightarrow$ Bottom).
4. **Draw Flows**:
   - Use `annotate` with `connectionstyle="arc3,rad=..."` to avoid overlapping lines.
   - Place labels in a background-filled box to ensure readability against the background.
5. **Add Context**:
   - **Key Markers**: Explicitly mark where private keys reside (e.g., a "K" badge).
   - **Vuln Boxes**: Attach a "Top Vulnerabilities" box to the relevant actor to link the architecture to the security risks.

## Pitfalls & Corrections
- **Avoid Over-Boxing**: Too many nested boxes (Venn-diagram style) can become visually noisy. Prefer the "Compact Node" approach if the logic is complex.
- **Legibility**: Ensure font sizes are consistent and contrast is high (Dark mode backgrounds with bright, distinct scenario colors).
- **Redundancy**: If a function can be expressed by the arrow action, do not create a separate box for that function inside the node.
