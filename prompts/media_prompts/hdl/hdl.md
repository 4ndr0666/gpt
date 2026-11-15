# HDL and HDL-JSON Unified Specification

**Revision 1.0.0 · Unified edition · 4ndr0666’s Hyper-Directive Language**

HDL and HDL-JSON describe the same image-generation intent. HDL is the compact, human-authored notation. HDL-JSON is the typed interchange form, also called HD-JSON in the original notes. A single normalized intent feeds either a prompt-only workflow or a backend adapter. Neither notation is itself a vendor API, a renderer, or proof that the output satisfies the brief.

The unified version number starts a new specification series. It does not renumber or replace the original HDL v8.0 source document. This revision incorporates both source documents and leaves them unchanged.

## 1. Design principles

1. **Compress repeated intent, not evidence.** Describe shared properties once. Use local overrides for the differences between views. Do not invent a number to make a brief look more precise.
2. **Specify the visible consequence.** “A hard flash leaves a short, crisp shadow behind the subject” works across more backends than an unexplained shader coefficient. Keep a physical parameter when it is measured, intentional, or supported by the target. Name its visible aim when useful.
3. **Keep evidence scoped.** A photo can anchor the appearance of a garment from one angle without establishing its construction from another. A previous render can identify drift without becoming independent evidence of the reference subject’s proportions.
4. **Distinguish intent from enforcement.** Types, references, precedence, and supported output dimensions can be checked by software. Visual likeness, silhouette, text legibility, and material appearance are judged on the image. Nested scopes reduce authoring ambiguity, but do not guarantee that a generative backend will keep attributes isolated.
5. **Use explicit coordinates when geometry needs them.** View names and visual descriptions are sufficient for ordinary image briefs. Do not require a synthetic 3D reconstruction for cropped or uncalibrated references.

## 2. One model, two serializations

| Canonical HDL block | HDL-JSON key | Role |
|---|---|---|
| `!INIT_META:` | top-level `version` and `intent` | Document version and global brief |
| `!INIT_REFERENCES:` | `references` | Ordered asset bindings, roles, and coverage |
| `!INIT_CONSTRAINTS:` | `constraints` | Scoped preserved properties and local exceptions |
| `!EXEC_FRAME:` | `frame` | Overall framing and ordered panel plan |
| `!EXEC_SUBJECT:` | `subject` | Appearance, wardrobe, pose, and reference-based correction |
| `!EXEC_ENVIRONMENT:` | `environment` | Backdrop, atmosphere, and placements |
| `!EXEC_CAMERA:` | `camera` | Optics, viewpoint, focus, and exposure intent |
| `!EXEC_LIGHTING:` | `lighting` | Light sources and visible behavior |
| `!FINALIZE_POST_PROCESS:` | `post_process` | Grade, grain, sharpness, and stitching |
| `!FINALIZE_OUTPUT:` | `output` | Deliverable dimensions, color space, format, and seed request |
| `!FINALIZE_NEGATIVE:` | `negative` | Scoped avoidance cues |
| `!FINALIZE_REVIEW:` | `review` | Observable acceptance criteria |
| `!FINALIZE_EXTENSIONS:` | `extensions` | Namespaced optional data outside the portable core |

The prefixes group responsibilities. They do not run a generation in stages. HDL-JSON object member order is immaterial. Arrays retain author order. In particular, the panel array sets display order and the first reference listed in an anchor list is primary.

### 2.1 HDL syntax

Canonical HDL is UTF-8 text. A block header starts at column one. Its fields are indented by two spaces. Blank lines and full-line `//` comments are allowed between headers and fields, including before the first header. There are no inline comments. LF and CRLF are accepted. Leading UTF-8 BOM is not part of the syntax.

~~~text
header      = one exact block name from the mapping table
field       = two spaces, "- ", field-name, ": ", JSON-value
field-name  = [A-Z][A-Z0-9_]*
~~~

A JSON value can span lines while an array or object remains open. Its continuation lines must be indented at least four spaces. JSON lexical and escaping rules still apply. Strings containing line breaks use escaped newlines. Fields are unique within a block, and each block can appear at most once. Duplicate object keys are rejected at every depth in either format. Unknown block or field names are errors in the portable core. Empty sections follow the same type rules as their HDL-JSON counterparts.

Map direct field names to lowercase. Do not recase nested JSON keys, text literals, filenames, or asset identifiers. For an array-valued section use the sole field `ITEMS`. These sections are `REFERENCES`, `CONSTRAINTS`, and `REVIEW`. For object-valued sections map the fields directly, except `EXTENSIONS`, which uses the sole field `DATA` to preserve namespace keys. Flatten the two fields in `META` to the top level. Canonical emitters use the table’s block order. Input order of blocks and fields does not change meaning.

### 2.2 HDL-JSON syntax and equivalence

The root is a JSON object. Do not include comments, trailing commas, bare tokens, or numeric strings where numbers are expected. Booleans are `true` or `false`, not quoted strings. The portable core has no nullable fields. Omit optional fields when unknown or unspecified. Extension values may be any valid JSON value. Numerically equivalent JSON numbers compare by value, not by spelling. A reader that cannot represent a value without loss must diagnose it instead of rounding silently.

HDL → model → HDL-JSON and HDL-JSON → model → HDL MUST preserve all core and extension data, including array order and exact decoded strings. Comments, indentation, property order, and equivalent escape spellings are not part of semantic round-tripping. Validate the model before emission. Unsupported versions are errors in strict mode, not requests to guess a compatible schema.

## 3. Portable field registry

Below, `!` after a field name means required. All other fields are optional. Every object is closed unless explicitly defined as an open map. Unlisted fields are errors. A string must contain at least one non-whitespace character. `id` is an ASCII identifier matching `[a-z][a-z0-9_-]*`. `text[]` means an array of strings. No list has an implied order of priority except where specified.

| Object | Fields and types |
|---|---|
| Document | `version!: "1.0.0"`, `intent!: text`, `references: Reference[]`, `constraints: Constraint[]`, `frame: Frame`, `subject: Subject`, `environment: Environment`, `camera: Camera`, `lighting: Lighting`, `post_process: Post`, `output: Output`, `negative: Negative`, `review: Review[]`, `extensions: open map` |
| Reference | `id!: id`, `asset!: text`, `role!: "source" or "diagnostic"`, `coverage!: text[]`. Coverage must contain at least one entry. |
| Constraint | `id!: id`, `mode!: "preserve" or "exception"`, `target!: path`, `rule!: text`, `anchors: id[]`, `panel: id`, `supersedes: id` |
| Frame | `aspect_ratio: ratio`, `shot: text`, `framing: text`, `composition: text`, `style_mode: text[]`, `panels: Panel[]` |
| Panel | `id!: id`, `view!: text`, `subject_azimuth_deg: number in [0,360)`, `pose: text`, `expression: text`, `framing: text`, `camera_position: Position` |
| Subject | `identity: text`, `appearance: text`, `pose: text`, `expression: text`, `surface_details: text[]`, `wardrobe: Wardrobe`, `proportion_correction: Correction` |
| Wardrobe | `description!: text`, `material: text`, `visible_effects: text[]` |
| Correction | `anchors!: id[]`, `observed_drift!: text`, `target!: text`, `preserve!: path[]`, `cross_view_rule: text`. Anchors and preserve lists must be nonempty. |
| Environment | `location: text`, `atmosphere: text`, `details: text[]`, `surface_elements: SurfaceElement[]` |
| SurfaceElement | `id!: id`, `placement!: text`, `literal_text: text`, `appearance: text`, `source: id` |
| Camera | `sensor_format: text`, `lens: text`, `focal_length_mm: positive number`, `f_number: positive number`, `shutter_seconds: positive number`, `iso: positive integer`, `position: Position`, `focus_target: text`, `focus_effect: text` |
| Position | `space!: "world", "subject", or "camera"`, `xyz_m!: exactly three finite numbers` |
| Lighting | `type: text`, `sources: Light[]`, `shadow_effect: text` |
| Light | `id!: id`, `role!: "key", "fill", "rim", "background", or "practical"`, `cct_k: positive number`, `position: Position`, `visible_effect: text` |
| Post | `color_grade: text`, `sharpness: text`, `grain: text`, `vignette: text`, `composite_stitch: text` |
| Output | `width_px: positive integer`, `height_px: positive integer`, `format: "png", "jpeg", or "webp"`, `color_space: text`, `seed: integer in [0, 4294967295]`, `required: output-key[]` |
| Negative | `identity: text[]`, `style: text[]`, `content: text[]`, `composition: text[]` |
| Review | `id!: id`, `target!: path`, `criterion!: text`, `required!: boolean`, `panel: id` |

- **Ratio** is `W:H` with positive base-10 integers and no spaces or leading zeros. Compare ratios by integer cross-multiplication, not string equality. When specified, width and height must appear together. If both dimensions and a ratio are specified, they must agree exactly.
- **Path** is a dot-separated sequence of exact core object field names, starting at a render section. It can name a whole object, an array as a unit, or a declared field within an object. It cannot traverse array positions or extensions. Valid roots are `frame`, `subject`, `environment`, `camera`, `lighting`, `post_process`, and `output`. Paths can name declared fields not populated elsewhere, so a reference alone can provide a visual baseline. Panel selection is a separate field. For panel-specific review, `frame.framing` names the effective framing for that panel.
- **ID scope.** IDs must be unique within each of the reference, panel, constraint, surface-element, light-source, and review arrays. An anchor or surface `source` must resolve to a reference. A `panel` must resolve to a panel. An asset handle is a host binding, not an instruction to fetch a URL or open a path.
- **Output enforcement.** `required` may name only present members of `width_px`, `height_px`, `format`, `color_space`, and `seed`. If it names one dimension, it must name both. `seed` is a requested backend value, not a promise of repeatability. An upscaled image can satisfy delivered pixel dimensions if the workflow permits that path, but it must be reported as upscaled rather than native resolution.
- **Extensions.** Top-level namespace keys use reverse-domain-style ASCII names such as `example.hdl`. Each name must have at least two dot-separated labels, each beginning with a lowercase letter and containing only lowercase letters, digits, and hyphens. Preserve values on conversion. Ignore them for core rendering unless a registered handler accepts them. Unrecognized extensions cannot override core invariants.
- **Omission.** Do not synthesize camera settings, lighting ratios, reference coverage, or measurements. An absent panel list means a single composition with no named panel ID. An explicit panel list must contain at least one panel.

### 3.1 Geometry and panel inheritance

Use meters. A world frame has origin at the nominal subject ground point, `+X` to the right of the nominal front camera, `+Y` up, and `+Z` toward that camera. A subject frame uses the same axes at the neutral front pose and rotates with the subject. A camera frame originates at the camera center with `+X` image-right, `+Y` image-up, and `+Z` backward along the optical axis. A camera’s own position cannot be expressed in its camera frame. Do not infer camera orientation from position alone.

`subject_azimuth_deg` describes an upright subject turn with a fixed camera. `0` faces the camera, `45` turns the front toward image-right, `90` is profile facing image-right, and `180` faces away. It is a requested orientation, not reconstructed skeletal data. If the text view and numeric azimuth clearly disagree, the adapter should report the conflict for review rather than select an angle silently.

Panels inherit subject pose and expression, frame framing, and camera position. Their corresponding explicit fields override the inherited value unless a preservation constraint prevents it. Treat named views as views of one subject, unless the intent explicitly says otherwise. Do not make projected silhouettes mirror-identical when the optics, angle, or stance explain a difference.

## 4. Resolution and precedence

1. **Validate the document.** Check grammar, field types, IDs, paths, ratio, and cross-field rules. Structural errors prevent compilation. Asset handles can remain unresolved when translating between serializations. A render plan must resolve the handles it uses.
2. **Resolve references by purpose.** A `source` can anchor only what its coverage supports. A `diagnostic` can illustrate an earlier error, but MUST NOT appear in an `anchors` list or as a surface element’s `source`. For overlapping source coverage, consult anchor IDs in order. If evidence conflicts at comparable angles or scale, report the ambiguity instead of averaging, inventing precision, or picking a diagnostic image as the baseline. Coverage and conflict in visual evidence are semantic review tasks, not consequences of type checking.
3. **Apply defaults and panel overrides.** Global `intent` supplies context; it does not trump explicit fields. Panel overrides apply only to their panel.
4. **Apply preservation constraints.** A `preserve` rule with no `panel` applies to the whole image and all panels. A panel-scoped rule applies only there. Its anchor list is optional. An omitted list preserves the available input or base spec described in `rule`. An explicit list must be nonempty. A local exception must name an existing panel and a `supersedes` ID pointing to a global `preserve` rule with the exact same `target`. It may change only that inherited rule in that panel. Exceptions cannot carry `anchors` or target another exception. Preserve rules cannot carry `supersedes`.
5. **Do not guess when rules collide.** For overlap detection, two targets overlap when identical or when one is a dot-component ancestor of the other in the same effective panel or global scope. Overlapping rules remain in force if compatible. An exception replaces only the named rule and never cancels another overlapping rule. Reject two exceptions for the same panel and superseded rule. If applicable explicit instructions contradict, stop resolution and identify the conflicting fields or rule IDs. Do not treat object order or a negative cue as authority to override them. Determining whether two prose instructions conflict may require human review.
6. **Apply corrections narrowly.** Correction `target` describes the revised appearance, `observed_drift` describes what not to repeat, and `preserve` lists the neighboring properties that must not change. The correction is confined to the proportion change stated in `target` and cannot override preservation rules. If preserving and correcting the same feature, phrase preservation against the original evidence, not against the rejected render. Missing evidence is not permission to infer absolute size, weight, body-fat percentage, or unshown geometry. Report approximated views when needed.
7. **Bind backend capabilities.** Native control, emulation, and prompt guidance are distinct. An adapter must distinguish them before rendering. No directive overrides the host’s capabilities or constraints.

### 4.1 Prompt-only and adapter workflows

**Prompt-only.** Lead with `intent`, asset roles, and preservation constraints. Describe the shared scene, then ordered panel differences, then camera, lighting, material effects, and narrowly scoped negatives. Include the correction as a positive target plus the specific previous drift. Keep review criteria separate unless phrased as visible instructions. A model receiving raw HDL can interpret it as prompt text, but only a conforming parser can claim HDL validation.

**Adapter.** Report a path or rule ID, a status, and a short explanation for each explicitly requested render setting. Use `native` when a backend accepts the setting as a control, `prompt_only` when it is conveyed as text, `post_process` when a declared downstream operation will apply it, and `unsupported` when there is no implementation. Do not silently substitute a native setting. If an `output.required` property cannot be delivered through a supported native control or declared post-process, stop before dispatch. Prompt-only delivery does not satisfy that requirement. `review.required` is different. It specifies an output check, not a native backend feature.

Typical examples are native pixel dimensions on some backends, prompt-only flash appearance on others, and a post-process resize when declared. A deterministic serialization or seed does not make an image generator deterministic. No valid HDL or HDL-JSON document guarantees successful rendering or visual fidelity.

### 4.2 Diagnostics and acceptance

A diagnostic contains a stable code, severity, location, and readable message. For HDL, include line and column when known. For model errors, include the field path or rule ID. Suggested codes are `E_SYNTAX`, `E_DUPLICATE`, `E_VERSION`, `E_TYPE`, `E_UNKNOWN_FIELD`, `E_UNBOUND_REFERENCE`, `E_SCOPE`, `E_CONFLICT`, and `E_REQUIRED_UNSUPPORTED`. Warn with `W_PROMPT_ONLY`, `W_REFERENCE_GAP`, or `W_EXTENSION_IGNORED` where applicable.

Report each output review item as `pass`, `fail`, or `not_assessed`, with an evidence note. A required item must pass before anyone labels the output accepted. A correctly parsed document or successful render is not visual acceptance. For a multi-panel image, verify view order, head-to-toe framing, comparable scale, reference fidelity, and lack of changes outside scope. Where comparison is meaningful, match source and output angle and normalize scale before comparing apparent proportions. Never compare a cropped oblique source to a frontal render as if image-plane widths were physical measurements.

## 5. Paired example — correcting a triptych without redesigning the subject

The asset names below are illustrative host handles. Replace them with actual bindings when rendering. The prior render identifies drift. It does not supply measurements. Front and three-quarter photos anchor the angles they show. The rear view is an approximation where not directly supported.

### 5.1 HDL

~~~hdl
// Shared room and wardrobe. Correct silhouette drift only.
!INIT_META:
  - VERSION: "1.0.0"
  - INTENT: "Photorealistic full-body turnaround of one adult subject in a blue halter outfit in the reference studio."
!INIT_REFERENCES:
  - ITEMS: [
      {"id":"front","asset":"front-photo","role":"source","coverage":["front silhouette","face and haircut","outfit color","room layout"]},
      {"id":"angle","asset":"angle-photo","role":"source","coverage":["three-quarter silhouette","visible garment cut"]},
      {"id":"prior","asset":"prior-render","role":"diagnostic","coverage":["prior silhouette drift"]}
    ]
!INIT_CONSTRAINTS:
  - ITEMS: [
      {"id":"room","mode":"preserve","target":"environment.location","anchors":["front"],"rule":"Keep the visible shelf and neon layout fixed across views."}
    ]
!EXEC_FRAME:
  - ASPECT_RATIO: "16:9"
  - SHOT: "full body"
  - FRAMING: "Show crown to toes at comparable scale, with headroom and visible floor."
  - PANELS: [
      {"id":"front","view":"front","subject_azimuth_deg":0},
      {"id":"angle","view":"front three-quarter toward image-right","subject_azimuth_deg":45},
      {"id":"rear","view":"rear","subject_azimuth_deg":180}
    ]
!EXEC_SUBJECT:
  - APPEARANCE: "Keep the visible face, haircut, and natural skin texture reference-consistent."
  - POSE: "Neutral upright stance."
  - WARDROBE: {"description":"Blue halter outfit with the reference cut and coverage.","visible_effects":["Subtle highlights follow the folds."]}
  - PROPORTION_CORRECTION: {
      "anchors":["front","angle"],
      "observed_drift":"The prior render widened the pelvis and hips relative to the shoulders.",
      "target":"Match the visible shoulder-to-hip relationship and waist-to-hip contour at comparable angles. Do not widen the silhouette or slim it beyond the evidence.",
      "preserve":["subject.appearance","subject.wardrobe","subject.pose","frame.framing"],
      "cross_view_rule":"Use one reference-consistent build. Let apparent width change with the turn. Treat unsupported rear details as approximate."
    }
!EXEC_ENVIRONMENT:
  - LOCATION: "Reference room with white shelving and purple neon."
!EXEC_CAMERA:
  - FOCUS_EFFECT: "A fixed chest-level view with clear garment edges and natural perspective."
!EXEC_LIGHTING:
  - SOURCES: [
      {"id":"flash","role":"key","cct_k":5500,"visible_effect":"Hard on-axis flash with bright highlights and a crisp shadow behind the subject."},
      {"id":"ambient","role":"fill","cct_k":3200,"visible_effect":"Faint warm spill in the background recesses."}
    ]
!FINALIZE_NEGATIVE:
  - STYLE: ["skin smoothing","automatic symmetry correction"]
  - COMPOSITION: ["cropped feet","inconsistent figure scale"]
!FINALIZE_REVIEW:
  - ITEMS: [
      {"id":"silhouette","target":"subject.proportion_correction","criterion":"At matched angles and scale, the front and three-quarter silhouettes no longer show excess lateral width against the source photos.","required":true},
      {"id":"framing","target":"frame.framing","criterion":"All three views retain comparable figure scale and show the entire body.","required":true}
    ]
~~~

### 5.2 HDL-JSON

~~~json
{
  "version": "1.0.0",
  "intent": "Photorealistic full-body turnaround of one adult subject in a blue halter outfit in the reference studio.",
  "references": [
    {"id": "front", "asset": "front-photo", "role": "source", "coverage": ["front silhouette", "face and haircut", "outfit color", "room layout"]},
    {"id": "angle", "asset": "angle-photo", "role": "source", "coverage": ["three-quarter silhouette", "visible garment cut"]},
    {"id": "prior", "asset": "prior-render", "role": "diagnostic", "coverage": ["prior silhouette drift"]}
  ],
  "constraints": [
    {"id": "room", "mode": "preserve", "target": "environment.location", "anchors": ["front"], "rule": "Keep the visible shelf and neon layout fixed across views."}
  ],
  "frame": {
    "aspect_ratio": "16:9",
    "shot": "full body",
    "framing": "Show crown to toes at comparable scale, with headroom and visible floor.",
    "panels": [
      {"id": "front", "view": "front", "subject_azimuth_deg": 0},
      {"id": "angle", "view": "front three-quarter toward image-right", "subject_azimuth_deg": 45},
      {"id": "rear", "view": "rear", "subject_azimuth_deg": 180}
    ]
  },
  "subject": {
    "appearance": "Keep the visible face, haircut, and natural skin texture reference-consistent.",
    "pose": "Neutral upright stance.",
    "wardrobe": {
      "description": "Blue halter outfit with the reference cut and coverage.",
      "visible_effects": ["Subtle highlights follow the folds."]
    },
    "proportion_correction": {
      "anchors": ["front", "angle"],
      "observed_drift": "The prior render widened the pelvis and hips relative to the shoulders.",
      "target": "Match the visible shoulder-to-hip relationship and waist-to-hip contour at comparable angles. Do not widen the silhouette or slim it beyond the evidence.",
      "preserve": ["subject.appearance", "subject.wardrobe", "subject.pose", "frame.framing"],
      "cross_view_rule": "Use one reference-consistent build. Let apparent width change with the turn. Treat unsupported rear details as approximate."
    }
  },
  "environment": {"location": "Reference room with white shelving and purple neon."},
  "camera": {"focus_effect": "A fixed chest-level view with clear garment edges and natural perspective."},
  "lighting": {
    "sources": [
      {"id": "flash", "role": "key", "cct_k": 5500, "visible_effect": "Hard on-axis flash with bright highlights and a crisp shadow behind the subject."},
      {"id": "ambient", "role": "fill", "cct_k": 3200, "visible_effect": "Faint warm spill in the background recesses."}
    ]
  },
  "negative": {
    "style": ["skin smoothing", "automatic symmetry correction"],
    "composition": ["cropped feet", "inconsistent figure scale"]
  },
  "review": [
    {"id": "silhouette", "target": "subject.proportion_correction", "criterion": "At matched angles and scale, the front and three-quarter silhouettes no longer show excess lateral width against the source photos.", "required": true},
    {"id": "framing", "target": "frame.framing", "criterion": "All three views retain comparable figure scale and show the entire body.", "required": true}
  ]
}
~~~

## 6. Migration from the original notes

Legacy HDL remains readable as prompt text. It is not canonical HDL 1.0.0. A migration tool can recognize known names, but should emit a report of normalizations and unresolved fields. It must not guess when two aliases assign conflicting values. The previous triptych prompt using `!INIT_` and `!EXEC_` JSON keys is likewise legacy input, not valid HDL-JSON 1.0.0.

| Legacy construct | Unified representation |
|---|---|
| `!INIT_MEM_LOCK_PROTOCOL`, `!INIT_MEM_LOCK`, `MASTER_IDENTITY`, `SOURCE_ANCHOR`, `reference_image` | Bound `references` plus scoped `constraints` and `subject.identity`. Move the actual intent of a lock into a rule, not a fabricated backend flag. |
| `!INIT_ENVIRONMENTAL_PHYSICS`, `!ENV_ATMOSPHERICS`, `!ENV_CHRONOS` | `environment`. Move source-specific light properties into `lighting`. |
| `!ENV_PHOTOMETRY`, `!EXEC_PHOTONIC_DISTRIBUTION`, `!EXEC_PHOTOMETRY` | Split mixed blocks among `lighting`, `camera` and `frame`. Use per-source CCT instead of one conflicting global number. |
| `!LENS_PHYSICS`, `!LENS_SENSOR_MAP`, `!EXEC_OPTICAL_ENGINE_PARAMS` | `camera`, `frame.aspect_ratio` and `post_process.grain` as applicable. Lens model names belong to `camera.lens`, not shutter speed. |
| `!BIO_DERMAL_MAP`, `!EXEC_BIO_RENDER_PIPELINE` | `subject.appearance` and `subject.surface_details`. |
| `!BIO_ANATOMY_LOCK`, `!EXEC_ANATOMICAL_CALIBRATION` | `constraints` for preservation and `subject.proportion_correction` for observed drift. |
| `!EXEC_MATERIAL_DYNAMICS`, `!EXEC_MATERIAL_PHYSICS` | `subject.wardrobe` and `visible_effects` within it. Keep unsupported shader or vendor fields in a named extension, with no implied core behavior. |
| `!EXEC_KINETIC_MATRIX`, `!EXEC_COMPOSITION_MATRIX` | Ordered `frame.panels`, shared `subject.pose`, and explicit local view settings. Convert numbered labels to stable IDs. |
| `TEXT_RECON_ENGINE`, `dynamic_overlays` | `environment.surface_elements` for supported scene surfaces. Store other overlay data in an extension. Preserve literal text exactly. |
| `!INIT_GEOMETRIC_SEED` | `output.seed` only if it denotes a real integer seed request. Leave it unset otherwise. |
| `!FINALIZE_STRATEGY`, `!FINALIZE_OUTPUT`, `GLOBAL_NEGATIVE_BIAS`, `!INIT_VALIDATION` | Separate `post_process`, `output`, `negative`, and `review`. Review criteria are observable checks, not automated filtering passes by default. |

Migration examples: use `85` for a supplied `85mm` focal length under `focal_length_mm`, `2.8` for a supplied `f/2.8` under `f_number`, and a native boolean only for a field that actually has boolean semantics. Translate `8K_UHD` to `7680` × `4320` only when it explicitly means 8K UHD pixel dimensions. Do not convert shorthand for visual fidelity into a resolution promise.

## 7. Conformance and evaluation

Claim conformance by component. A **reader** enforces syntax and the portable registry. A **serializer** preserves the normalized model in both directions. A **planner** additionally resolves asset bindings, scope and adapter capability. A **reviewer** evaluates the resulting image against the declared criteria. These claims are independent.

Minimum conformance cases for implementations:

| Test | Expected result |
|---|---|
| Decode both examples in §5 | Identical typed model with the same panel and anchor order |
| Re-emit in either notation and reparse | Same model; HDL comments and whitespace need not survive |
| Duplicate `intent` or duplicate a nested key | Reject before normalization |
| Change `required` from `true` to `"TRUE"` on a review item | Reject type mismatch |
| Duplicate a panel ID or reference an unknown panel | Reject |
| Insert `prior` in the correction’s `anchors` | Reject diagnostic-as-authority |
| Request `16:9` and deliver `1536` × `1024` as matching native dimensions | Reject the inconsistent request if those are the requested dimensions, or mark delivered dimensions as failing the stated ratio if found after rendering |
| Add a local exception for a different target than its superseded rule | Reject |
| Add two exceptions for the same panel and superseded rule | Reject |
| Include an unknown core key | Reject; allow unknown namespaced extension data and preserve it |
| Bind a required `seed` or pixel size to a prompt-only backend | Reject unless a supported path satisfies the actual required property |
| Parse valid HDL-JSON but crop the feet in the image | Parsing passes; the required framing review fails |

For prompt effectiveness testing, run a baseline and a revision with the same inputs, backend, and settings. Use several samples per condition and match seeds where the backend supports it. Compare like angles at matched scale. Score reduction of the targeted drift separately from unintended changes to unchanged properties. Record failures and unsupported settings, not just successful examples.

## Source basis

Adapted from 4ndr0666’s `hdl.md` (including the v8.0 literal-consequence rule) and `hd-json.md` (the original hierarchical registry). The unified version, grammar, field definitions, precedence rules, and conformance profile are the revision introduced here.
