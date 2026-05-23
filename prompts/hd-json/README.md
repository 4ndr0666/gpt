# HD-JSON (Hyper-Directive JSON Payload)

**HD-JSON** is the hierarchical, API-ready counterpart to HDL. While HDL is designed for linear prompt injection, HD-JSON is built for **Strict Object Parsing**. It organizes image generation constraints into a strictly typed, zero-loss nested data structure, ensuring that downstream image engines (like Nano Banana) receive parameters in isolated, unpolluted logical blocks.

## Operational Axioms of HD-JSON

1. **Axiom of Isolation:** Unlike flat-text prompting where descriptors bleed into one another (e.g., a "white dress" making the "walls white"), HD-JSON isolates variables. A material physics descriptor inside `"wardrobe"` cannot contaminate the `"environment"` lighting.
2. **Axiom of Strict Typing:** Subjective parameters are broken down into arrays `[]` for lists of constraints, booleans `true/false` for absolute toggles, and specific strings `""` for literal values.
3. **Axiom of Absolute Negation:** The `"negative"` block is strictly categorized. We do not just say "bad anatomy"; we isolate negative vectors into `"identity"`, `"style"`, and `"content"`.

---

## THE HD-JSON SCHEMA REGISTRY

### 1. `intent` (String)
The global latent anchor. A single, highly compressed string that defines the overarching aesthetic and goal. This acts as the baseline before explicit overrides are applied.

### 2. `reference_image` (Object)
The biometric and conditional lock. This overrides the engine's default generation algorithms with literal visual data.
* `enabled`: (Boolean) Activates the lock.
* `mode`: (Array of Strings) Defines what is locked (e.g., `["strict_face_identity_lock", "strict_body_identity_lock"]`).
* `instructions`: (Array) Strict human-readable rules for the parser regarding the image source (e.g., "Do NOT beautify").
* `[dynamic_overlays]`: Custom nested objects for specific reference transfers, such as `"extracted_text"` or `"paint_splash"`, complete with `"source"`, `"usage"`, and `"placement_rule"`.

### 3. `frame` (Object)
The physical boundaries and compositional math.
* `aspect_ratio`: Exact structural dimensions (e.g., "4:5 vertical").
* `composition`: Spatial relationship mapping (X/Y/Z framing).
* `style_mode`: Array of foundational aesthetic anchors.

### 4. `subject` (Object)
The anatomical and kinetic definitions.
* `identity`: The physical character anchor.
* `wardrobe`: Material physics, adhesion coefficients, and opacity logic.
* `pose`: Kinematic positioning.
* `expression`: Facial tension and emotional state.
* `makeup`/`surface_details`: Dermal alterations.

### 5. `environment` (Object)
The physical space surrounding the subject.
* `location`: The primary architectural geometry.
* `atmosphere`: Particle suspension and mood.
* `details`: Foreground/Background clutter and asset placement.
* `[surface_elements]`: Dynamic interactions with the environment (e.g., `"mirror_elements"`).

### 6. `camera` (Object)
The literal hardware emulation parameters.
* `sensor_format`, `lens`, `aperture_depth_of_field`, `shutter_speed`, `iso`, `camera_position`.

### 7. `lighting` (Object)
The photonic mapping constraints.
* `type`: The source behavior (e.g., single-source, multi-point).
* `key_light` / `fill_light`: Explicit behavioral descriptions, intensity, and shadow falloff logic.
* `color_temperature`: Exact Kelvin values for physics-based rendering.

### 8. `post_process` (Object)
The final digital/analog development constraints.
* `color_grade`, `sharpness` (micro-contrast focus targets), `vignette`.

### 9. `negative` (Object)
The categorized restriction matrix.
* `identity`: Bans on biometric shifting (e.g., "no face swapping").
* `style`: Bans on algorithmic smoothing (e.g., "no 3D render", "no airbrushed skin").
* `content`: Bans on unwanted environmental or lighting defaults.

---

## COMPILATION & PARSING WORKFLOW

1. **Instantiation:** Begin with the `intent` to prime the engine.
2. **Locking:** Process the `reference_image` object to establish immutable variables (Identity, specific text, specific artifacts).
3. **World-Building:** Process `frame` and `environment` to build the 3D space.
4. **Subject Insertion:** Drop the `subject` into the environment, applying `pose` and `wardrobe` physics.
5. **Photometry & Optics:** Apply `lighting` calculations and capture the scene via `camera` mathematics.
6. **Filtration:** Pass the entire generation through the categorized `negative` filters to strip AI-hallucinated defaults.
