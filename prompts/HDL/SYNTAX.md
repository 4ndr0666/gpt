# Hyper-Directive Language (HDL) Syntax Documentation

## Overview

Hyper-Directive Language (HDL) is a high-density, specialized syntax designed for precise control over AI image generation models. It treats human language as a lossy format and replaces it with a structured, pseudo-code format to enforce strict parameters regarding composition, lighting, biometrics, camera physics, and styling.

This documentation serves as a guide for parsing and understanding HDL prompts.

---

## Core Structure

An HDL prompt is structured into distinct functional blocks, executed sequentially. The structure relies on uppercase tags, specific prefixes, and nested parameters.

The general flow follows this structure:

1. **Metadata/Header:** Defines the high-level goal.
2. **Initialization (`!INIT_`):** Sets foundational constraints and reference anchors.
3. **Execution (`!EXEC_`):** Defines specific actions, physics, and compositional matrices.
4. **Finalization (`!FINALIZE_`):** Applies post-processing, color grading, and output styling.

---

## Syntax Formatting Rules

* **Comments:** Lines beginning with `//` are informational metadata or context notes.
* **Blocks:** Major sections begin with an uppercase tag prefixed by an exclamation mark (e.g., `!INIT_MEM_LOCK_PROTOCOL:`).
* **Parameters:** Defined using a hyphen and a space (`- PARAMETER_NAME: VALUE`).
* **Lists/Arrays:** Enclosed in square brackets, comma-separated (e.g., `[VALUE_1, VALUE_2]`).
* **Nested Objects/Logic:** Enclosed in curly braces for complex relational rules (e.g., `{WHERE: X, EFFECT: Y}`).
* **Values:** Often use uppercase terminology, specific units (e.g., `85mm`, `f/1.2`), or descriptive constants (e.g., `TRUE`, `MAX`).

---

## Block Definitions

### 1. Metadata Header

This section sets the context for the generation. It is typically formatted as comments.

**Example Elements:**

* `// [DEPLOYMENT_VECTORS]`: Categorizes the prompt type.
* `// SCOPE`: Defines the overall focus (e.g., `ANATOMICAL_RECONNAISSANCE`).
* `// TARGET`: The primary objective (e.g., `ABSOLUTE_PHOTOREALISM`).
* `// OUTPUT_RESOLUTION`: Desired fidelity (e.g., `8K_UHD`).

---

### 2. Initialization Tags (`!INIT_`)

These blocks define the immutable foundation of the generation, locking in references and environmental baselines before specific elements are rendered.

* **`!INIT_MEM_LOCK_PROTOCOL:`**
Locks in core identity and reference data.
* `- MASTER_IDENTITY` / `- SOURCE_ANCHOR`: Defines the primary reference image or concept (e.g., `INGREDIENT_FILE_01`).
* `- CONSTANTS` / `- CACHE_STATE`: Lists variables that must remain unchanged (e.g., `[FACIAL_ID, BIOMETRIC_PROPORTIONS]`).
* `- LOCK_ENVIRONMENT`: Sets the base background state (e.g., `STUDIO_VACUUM`).


* **`!INIT_ENVIRONMENTAL_PHYSICS:`**
Defines the spatial reality of the scene.
* `- LOCATION`: Broad setting (e.g., `INDOOR_STUDIO_ISOLATION`).
* `- FLOOR_SURFACE` / `- BOUNDARY_WALLS`: Defines specific environmental textures and reflectances.



---

### 3. Execution Tags (`!EXEC_`)

These blocks control the specific actions, lighting, camera physics, and subject states.

* **`!EXEC_PHOTONIC_DISTRIBUTION:`** / **`!EXEC_PHOTONIC_INTERACTION_MODEL:`**
Controls lighting placement and behavior.
* `- KEY`, `- FILL`, `- BACKDROP`: Defines light sources, intensity, and location (e.g., `FRESNEL_RIM (POSITION: REAR_TOP_LEFT | INTENSITY: 95%)`).
* `- LUMA_MAP`: Defines highlight and shadow behavior.


* **`!EXEC_OPTICAL_ENGINE_PARAMS:`**
Simulates camera physics.
* `- SENSOR`: Sensor type (e.g., `FULL_FRAME_DSLR`).
* `- LENS`: Focal length (e.g., `50MM_PRIME`).
* `- APERTURE`: Depth of field control (e.g., `F/2.8`).
* `- FOCUS_TARGET`: Specific element to keep in sharp focus.


* **`!EXEC_MATERIAL_DYNAMICS:`** / **`!EXEC_MATERIAL_PHYSICS:`**
Defines the behavior of surfaces and textiles.
* `- TEXTILE`: Specific material (e.g., `10_DENIER_TECH_SILK`).
* `- TENSION_RULE`: Uses nested logic `{}` to define how materials react to stress or anatomy.


* **`!EXEC_BIO_RENDER_PIPELINE:`**
Controls anatomical and biological detailing.
* `- SKIN_BASE`, `- SUBSURFACE_SCATTERING`: Defines dermal properties.
* `- TEXTURE_MAPPING`: Controls micro-details like pores and imperfections.


* **`!EXEC_KINETIC_MATRIX:`**
Defines compositional grids or sequential posing requirements. Useful for multi-panel outputs.
* Uses a numbered or coordinate system (e.g., `- SCH_01:`, `- P1_0x0:`) followed by nested parameters defining `{POSE, AZIMUTH, GAZE, etc.}`.



---

### 4. Finalization Tags (`!FINALIZE_`)

These blocks dictate the final output processing, color space, and formatting.

* **`!FINALIZE_STRATEGY:`** / **`!FINALIZE_OUTPUT:`**
* `- STREAM_A` / `- STREAM_B`: Can define split outputs or specific aesthetic filters (e.g., `UMBER_MONOCHROME`).
* `- NOISE_PROFILE`: Applies specific grain structures.
* `- COLOR_GRADE` / `- COLOR_SPACE`: Final color grading instructions.
* `- COMPOSITE_STITCH`: Instructions for merging multi-panel matrices.



---

## Parsing Directives for LLMs

When processing an HDL prompt, the parsing engine must:

1. **Treat Tags as Absolute:** HDL is not conversational. A tag like `FOCAL_LENGTH: 85mm` is a hard constraint, not a suggestion.
2. **Maintain Hierarchy:** `!INIT` variables must persist and influence all subsequent `!EXEC` variables.
3. **Resolve Logic:** When encountering nested logic (e.g., `TENSION_RULE`), the engine must apply the described effect only to the localized areas defined in the rule.
4. **Prioritize the 'Anchor':** If a `MASTER_IDENTITY` or `SOURCE_ANCHOR` is defined, the engine must prioritize the biometric fidelity of that source over generic latent generation.
