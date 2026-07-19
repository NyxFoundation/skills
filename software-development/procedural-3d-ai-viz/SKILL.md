---
name: procedural-3d-ai-viz
description: Workflow for building platforms that convert unstructured blueprints/URLs into interactive 3D visualizations using a JSON Scene Descriptor intermediate format.
---

# Procedural 3D Scene Visualization with AI

This skill describes the workflow for building a platform that converts unstructured text/URLs (blueprints) into interactive 3D visualizations using a "JSON Scene Descriptor" intermediate format.

## Core Concept
Instead of asking an LLM to generate complex 3D files (GLTF/OBJ) which are prone to syntax errors, the AI generates a standardized JSON schema describing primitives (shapes), their spatial coordinates, metadata, and logical connections. The frontend then renders these procedurally using Three.js.

## Implementation Workflow

### 1. Schema Design (`shared/schema.json`)
Define a strict schema that includes:
- **Parts**: `id`, `name`, `shape` (box, cylinder, sphere), `position` [x, y, z], `size` [w, h, d], `color`, `material`, `role`, `description`.
- **Connections**: A mapping of IDs (e.g., `part_a` -> `[part_b, part_c]`).

### 2. AI Analyst Pipeline (`apps/server/analyst.py`)
- **Prompt Engineering**: Use a "PhD Mechanical Engineer" persona.
- **Spatial Heuristics**: Provide the AI with rules for plausible placement (e.g., "sensors should be on the periphery", "mounting plates should be at z=0").
- **Format Enforcement**: Mandate the output as a JSON object matching the schema.

### 3. Procedural Rendering (`apps/web/src/components/Viewer.tsx`)
- Use `@react-three/fiber` and `@react-three/drei`.
- Map the `shape` field from JSON to Three.js geometries (`<boxGeometry />`, `<cylinderGeometry />`).
- Implement a selection state to highlight parts and their associated metadata.

### 4. Connectivity Visualization (`apps/web/src/components/Connections.tsx`)
- Iterate through the `connections` array.
- Draw lines/cylinders between the center points of connected parts.
- Implement visual feedback (glowing lines) when a connected node is selected.

## Pitfalls & Solutions
- **Random Clusters**: AI often places objects randomly. **Solution**: Define a "Chassis" or "Base" object in the prompt to anchor coordinates.
- **Symmetry/Alignment**: Primitives can overlap. **Solution**: Use a multi-step prompt (identify parts $\to$ define spatial layout $\to$ refine connections).
- **CORS Issues**: Frontend and Backend on different ports. **Solution**: Use `fastapi.middleware.cors` with `allow_origins=["*"]` (or specific domain) during development.
