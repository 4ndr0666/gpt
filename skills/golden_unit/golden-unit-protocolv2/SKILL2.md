---
name: golden-unit-protocol
description: A strict, medium-agnostic regression-prevention and architectural-integrity protocol for revising an existing artifact (code, prose, math, schemas, systems orchestration, or contracts). Invoke this skill ONLY when the user explicitly references "the Golden-Unit Protocol," asks for a "golden-unit pass," or explicitly asks for unit-by-unit hash/digest-verified revision with regression and architectural-soundness guarantees. Do NOT use this for ordinary edit requests unless the user has invoked the protocol by name or asked for this specific level of rigor.
allowed-tools: vm_shell
---

# The Golden-Unit Protocol v3 (Elite Tier)

*A medium-agnostic, zero-drift regression-prevention and architectural-integrity protocol for LLM-driven revisions across code, prose, mathematics, data schemas, systems orchestration, and legal contracts.*

---

## 0. Purpose & Core Guarantees

The Golden-Unit Protocol eliminates two primary structural failure modes in AI-driven artifact revision:

1. **Silent Regression**: Silently dropping a previously working capability, edge-case handler, or contract guarantee during refactoring.
2. **Architectural Drift**: Defaulting to fragile, host-mutating, chimeric, or over-defensive patterns that are statistically common in training data rather than architecturally sound.

The protocol separates verification into explicit, verifiable gates:

```
[ Baseline Artifact ] ──► [ Atomization & Baseline Manifest ]
                                    │
                                    ▼
[ Candidate Artifact ] ──► [ Dual-Gate Verification Pipeline ]
                                ├── Gate 1: Regression Check (Hash + Semantic Digest)
                                └── Gate 2: Architectural Soundness Firewall (§4 Directives)
                                    │
                                    ▼
                          [ Emission & Narration Contract ]
```

---

## 1. Phase 1: Atomization — Domain-Specific Boundary Resolution

Before modifying any line or clause, decompose the canonical artifact into **named units**: the smallest domain-native elements with independent identity.

### Domain Unit Mapping Table

| Domain | Natural Unit | Stable Naming Convention |
|---|---|---|
| **Code** (Python, JS, C++, Go, Rust, etc.) | Function, method, class, exported constant, config block | `[Module.]Class.method` or `[Module.]function_name` |
| **Prose / Documentation** | Claim, requirement, section, distinct assertion | `Section_X.Claim_Y` or `Req_Z` |
| **Mathematics** | Lemma, theorem, equation, derivation step | `Theorem_A`, `Lemma_B.Step_C` |
| **Data / Schema** | Key, record, field, table definition | `Table.field_name` or `Schema.key` |
| **Systems Orchestration** | Process boundary, resource allocation, lifecycle stage | `Service.Lifecycle_Stage` (e.g., `Docker.acquire`) |
| **Legal / Contractual Text** | Clause, defined term, numbered provision | `Clause_X.Y` or `Term_Z` |

### Boundary Resolution Rules

1. **Name-Based Identity**: A unit's identity is strictly its **stable name**, never its character position or line index. Naming survives reordering and refactoring.
2. **Nested Scope Qualification**: Methods inside classes must be qualified as `ClassName.method_name` to prevent namespace collisions.
3. **Atomic Fallback**: If an artifact lacks natural sub-units, the entire artifact is treated as a single unit. Do not manufacture artificial boundaries that conflict with domain idioms.

---

## 2. Phase 2: Manifest Generation — Quad-Attribute Tuple

Every unit in the baseline and candidate manifests is recorded as a JSON object with four mandatory fields:

```json
{
  "unit": "<stable_qualified_name>",
  "hash": "<sha256_of_literal_unit_content>",
  "digest": "<one_sentence_behavioral_guarantee_and_contract>",
  "class": "<orchestrator | volatile-logic | n/a>"
}
```

### Field Definitions & Semantics

- **`unit`**: Unique, qualified stable identifier.
- **`hash`**: Exact SHA-256 hash of the literal unit content (stripping non-semantic whitespace where appropriate). Detects structural changes instantly.
- **`digest`**: A single, rigorous sentence capturing what the unit does, asserts, handles, or guarantees. A hash mismatch detects *change*; the digest evaluates *safety*.
- **`class`**: Operational classification for system units:
  - `orchestrator`: Durable control flow, lifecycle management, state transitions, or dispatch.
  - `volatile-logic`: High-complexity, dependency-heavy, untrusted, or execution-heavy logic (e.g., subprocesses, parsing, network I/O, compilation).
  - `n/a`: Non-executing units (prose, math derivations, data schemas). Units with `class: "n/a"` skip Gate 2 (§4) entirely.

---

## 3. Phase 3: Gate 1 — Three-Way Regression Verification

For every unit in `Baseline ∪ Candidate`:

```
                       ┌─────────────────────────┐
                       │   Unit Hash Check       │
                       └────────────┬────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │ Hash Matches           │ Hash Differs           │ Missing from Candidate
           ▼                        ▼                        ▼
     [ UNCHANGED ]            [ CHANGED ]               [ MISSING ]
   Pass & Skip Narration    Compare Semantic Digests    AUTOMATIC HARD FAIL
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                 Superset / Equiv          Drops Guarantee
                       [ PASS ]              [ REGRESSION HARD FAIL ]
```

- **MISSING**: Present in baseline, absent in candidate → **Automatic Hard Fail**. No assumptions of "unused code" or "implicit redundancy."
- **UNCHANGED**: Hashes match identically → **Pass**. Omit from conversational narration to eliminate signal noise.
- **CHANGED**: Hashes differ → **Mandatory Digest Comparison**:
  - **Superset / Equivalent**: The candidate digest preserves all baseline behavioral guarantees, edge-case handlers, and output constraints, while potentially adding capabilities → **Pass**.
  - **Dropped Guarantee**: Candidate drops any capability, exception handler, bounds check, or edge-case guarantee → **Hard Fail Regression**, regardless of code brevity, elegance, or execution speed.

---

## 4. Phase 4: Gate 2 — Architectural Soundness Firewall (§4 Directives)

This gate runs on every unit classified as `orchestrator` or `volatile-logic` that is either newly written or marked `CHANGED` in Gate 1. Both Gate 1 and Gate 2 must pass independently.

### Directives Checklist (Any Single Violation = Hard Fail)

- **4.1 Isolation over Host Mutation**:
  - Volatile logic (untrusted execution, file processing, subprocesses) must execute within isolated, disposable sandboxes or strictly scoped temporary paths.
  - Orchestrators must never mutate global host state directly. They inject inputs, trigger bounded execution, and collect explicit outputs.
- **4.2 Hard Timeouts on External Executions**:
  - Every external call, HTTP request, subprocess invocation, or system interaction must have an explicit, system-enforced timeout. Infinite waits are hard fail defects.
- **4.3 Base + Patch Lineage**:
  - Iterative operations must apply diffs/patches against a pristine baseline. Never copy-and-accumulate directories or state, which causes unbounded state bloat and breaks deterministic rollbacks.
- **4.4 Ruthless Resource Reclamation**:
  - Every allocated resource (file handles, network sockets, sub-processes, temp directories) must be bound to an unconditional cleanup path (`finally` / POSIX `trap`) that fires on success, exception, or cancellation.
  - Concurrency failure: If a worker fails, all sibling tasks/futures must be explicitly cancelled immediately.
  - Cleanup routines must tolerate idempotency ("resource already released") without surfacing errors.
- **4.5 Paradigm Purity (No Chimeras)**:
  - Commit fully to one execution model (e.g., pure async, pure sync, declarative pipeline).
  - Never blend conflicting paradigms (e.g., blocking I/O inside async event loops, direct DOM mutation inside React hooks).
- **4.6 EAFP Execution over Defensive LBYL**:
  - Attempt operations directly and handle specific exceptions at the failure site (Easier to Ask for Forgiveness than Permission).
  - Avoid redundant, brittle pre-flight checks (Look Before You Leap) that duplicate OS or runtime kernel validation.
- **4.7 Monolith Decoupling (No Tacking-On)**:
  - When integrating clean code into a large legacy file, preserve the clean unit's minimal architecture rather than wrapping it in boilerplate.
  - If a unit exceeds its single responsibility, split it into composable sub-units connected by clean interfaces.

---

## 5. Phase 5: Trigger Scope & Incremental Delta Protocol

1. **Unit-Scoped Re-verification**: Modifying a unit triggers re-hashing, digest re-evaluation, and Gate 2 checks on **that specific unit only**.
2. **Untouched Units**: Untouched units are asserted `UNCHANGED` by omission. Do not re-evaluate the global manifest unless executing a full audit.

---

## 6. Phase 6: Emission & Narration Contracts

Three decoupled artifacts must be generated:

### 6a. The Verification Artifact
The complete JSON manifest (`unit`, `hash`, `digest`, `class`) for every unit evaluated during the session.

### 6b. The Emission Artifact
The complete, literal revised artifact.
- **STRICT DIRECTIVE**: Zero placeholders, zero `// rest unchanged`, zero `...`.
- Delivered as a complete file or document.

### 6c. The Narration
Conversational narration presented to the user **MUST contain ONLY the CHANGED or FAILED units**, formatted with:
- Unit Name & Verdict (`CHANGED` / `FAILED`)
- Baseline Digest vs. Candidate Digest
- Specific Gate 2 Directive status (if applicable)
- **STRICT NOISE REDUCTION**: Never re-display `UNCHANGED` units in chat.

---

## 7. Behavioral Overrides & Guardrails

1. **Zero-Sycophancy Correction Path**: State failure mechanisms and resolutions directly. Eliminate performative apologies or self-criticism.
2. **Anti-Hallucination Anchor**: Canonical source data and explicit constraints are fixed. Never extrapolate or invent unstated user requirements.
3. **Mandatory Architectural Challenge**: If a user prompt requests a violation of Gate 2 (e.g., "run un-sandboxed mutation without a timeout"), explicitly challenge the request, cite the specific failure directive, and provide a compliant alternative.

---

## 8. Fail-Safe Halt Conditions

Stop execution and request user clarification when:
- Canonical baseline content is ambiguous, truncated, or contradictory.
- A Gate 1 digest comparison cannot be conclusively evaluated as a superset.
- A unit's classification (`orchestrator` vs `volatile-logic` vs `n/a`) is ambiguous.
- A requested change forces the dropping of a baseline guarantee without a compliant alternative.

---

## 9. Verification Automation Harness

For code files (Python, JS/TS), leverage the automated AST parser script `golden_unit_hash.py`:

```bash
python3 /working_dir/c_3e045397dd366d77/skills/golden-unit-protocol/scripts/golden_unit_hash.py \
  --baseline baseline_file.py \
  --candidate candidate_file.py
```

For non-code or manual unit verification, supply manual JSON definitions:

```bash
python3 /working_dir/c_3e045397dd366d77/skills/golden-unit-protocol/scripts/golden_unit_hash.py \
  --manual-units baseline_units.json \
  --manual-units-candidate candidate_units.json
```

*Note*: The automated script handles unit extraction and literal hash checks. Semantic digest evaluation (Gate 1) and architectural soundness checks (Gate 2) are performed directly by the agent model on all `CHANGED` units.
