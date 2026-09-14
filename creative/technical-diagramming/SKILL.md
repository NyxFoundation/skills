---
name: technical-diagramming
description: Guidelines for creating high-fidelity technical architecture and flow diagrams using Matplotlib for the user.
---

# Technical Diagramming for Gohan

Guidelines for producing "AWS-style" architecture diagrams that balance structural boundaries with sequential process flows.

## Design Principles

### 1. The "Island" Architecture (AWS-Style)
Instead of flat flowcharts, use nested boundaries ("Islands") to represent trust boundaries or physical/logical containers.
- **Outer Islands**: Major actors (e.g., "Host PC", "Hardware Device", "Blockchain").
- **Nested Islands**: Internal layers (e.g., "Firmware" inside "Hardware Device", "Secure Element" inside "Firmware").
- **Components**: Functional blocks (boxes) inside islands. Use a "KEY" marker (red dashed border) to highlight where private keys are stored or derived.

### 2. Scenario-Based Sequential Flows
Avoid generic arrows. Use scenario-specific coloring and explicit labeling.
- **Label Format**: `StepNumber: Action` (e.g., `1: TX Request`, `2: Sign TX`).
- **Traceability**: Each color group (Scenario) should be numbered sequentially (1, 2, 3...) starting from the trigger.
- **Visuals**:
  - Use `FancyBboxPatch` for islands and components.
  - Use `annotate` with `connectionstyle="arc3,rad=..."` to avoid overlapping labels.
  - Labels should have a semi-transparent background (`bbox`) to remain legible over arrows.

## Recommended Color Palette (Dark Mode)
- **Background**: `#0d1117`
- **Islands**: `#161b22` (face), `#30363d` (edge)
- **Components**: `#1c2333` (face), `#484f58` (edge)
- **Scenarios**:
  - Key Generation/Recovery: `#f85149` (Red)
  - Signing/Transaction: `#58a6ff` (Blue)
  - Query/Display: `#d29922` (Yellow)
  - Update/Recovery: `#3fb950` (Green)
  - Verification/Third-party: `#bc8cff` (Purple)

## Technical Implementation (Matplotlib)
- **Fonts**: Always ensure CJK fonts are loaded for Japanese text (e.g., `IPAGothic` or `Noto Sans CJK JP`).
- **Backend**: Use `matplotlib.use("Agg")` for headless environments.
- **Legend**: Include a scenario legend and a "Common Vulnerabilities" box per diagram to link architecture to security failures.
