---
name: golden-unit-protocol
description: >
  A strict, medium-agnostic regression-prevention and architectural-integrity
  protocol for revising any artifact — code (Python, JS/TS, Go, Rust, Java,
  C, C++, C#, Kotlin, Swift, PHP, Scala, Dart, Ruby, Lua, Elixir, Haskell,
  Bash, PowerShell, SQL, TOML, YAML, JSON), prose, mathematics, data schemas,
  systems orchestration, or legal contracts. Invoke ONLY when the user
  explicitly references "the Golden-Unit Protocol," asks for a
  "golden-unit pass," or asks for unit-by-unit hash/digest-verified revision
  with regression and architectural-soundness guarantees. Do NOT use for
  ordinary edit requests ("fix this bug," "clean up this doc") unless the user
  has invoked the protocol by name — it is intentionally heavyweight.
allowed-tools: vm_shell
version: "4.0.0"
script: scripts/golden_unit_hash.py
---

# The Golden-Unit Protocol v4

*A medium-agnostic, zero-drift regression-prevention and architectural-integrity
protocol for LLM-driven revisions across code, prose, mathematics, data schemas,
systems orchestration, and legal contracts.*

---

## 0. Purpose & Core Guarantees

The Golden-Unit Protocol eliminates two structural failure modes in AI-driven
artifact revision:

1. **Silent Regression** — silently dropping a previously working capability,
   edge-case handler, or contract guarantee during refactoring.
2. **Architectural Drift** — defaulting to fragile, host-mutating, chimeric, or
   over-defensive patterns that are statistically common in training data rather
   than architecturally sound.

The protocol separates verification into four explicit, independently-verifiable
phases:

```
[ Baseline Artifact ] ──► [ §1 Atomization & Baseline Manifest ]
                                          │
                                          ▼
[ Candidate Artifact ] ──► [ Dual-Gate Verification Pipeline ]
                               ├── Gate 1: Regression Check (Hash + Semantic Digest)
                               └── Gate 2: Architectural Soundness Firewall
                                          │
                                          ▼
                             [ §6 Emission & Narration Contract ]
```

Both gates are independent. A candidate can be a strict behavioral superset of
the baseline (Gate 1 passes) and still be architecturally unsound (Gate 2 fails).
Both must pass before any revision is emitted.

---

## 1. Atomization — Define the Unit Before Touching Anything

Before modifying any line or clause, decompose the canonical artifact into
**named units**: the smallest domain-native elements with independent identity.

### Domain Unit Mapping Table

| Domain | Natural Unit | Stable Naming Convention |
|---|---|---|
| **Code** (any language) | Function, method, class, exported constant, config block | `[Module.]Class.method` or `[Module.]function_name` |
| **Prose / Documentation** | Claim, requirement, section, distinct assertion | `Section_X.Claim_Y` or `Req_Z` |
| **Mathematics** | Lemma, theorem, equation, derivation step | `Theorem_A`, `Lemma_B.Step_C` |
| **Data / Schema** | Key, record, field, table definition | `Table.field_name` or `Schema.key` |
| **Systems Orchestration** | Process boundary, resource allocation, lifecycle stage | `Service.Lifecycle_Stage` (e.g., `Docker.acquire`) |
| **Legal / Contractual Text** | Clause, defined term, numbered provision | `Clause_X.Y` or `Term_Z` |

### Boundary Resolution Rules

1. **Name-Based Identity**: A unit's identity is strictly its **stable name**,
   never its character position or line index. `lines 501–1000` is not a unit —
   it is explicitly prohibited as a boundary.
2. **Nested Scope Qualification**: Methods inside classes must be qualified as
   `ClassName.method_name` to prevent namespace collisions.
3. **Atomic Fallback**: If an artifact has no natural sub-units, the entire
   artifact is one unit. Do not manufacture boundaries that conflict with domain
   idioms.

---

## 2. The Manifest — Quad-Attribute Tuple

Every unit in the baseline and candidate manifests is a JSON object with four
mandatory fields:

```json
{
  "unit":   "<stable_qualified_name>",
  "hash":   "<sha256_of_literal_unit_content>",
  "digest": "<one sentence: what this unit does, asserts, handles, or guarantees>",
  "class":  "<orchestrator | volatile-logic | n/a>"
}
```

**Field semantics:**

- **`unit`** — unique qualified stable identifier per §1 naming conventions.
- **`hash`** — SHA-256 of the literal unit content. Detects structural change
  instantly. Hash equality does not imply behavioral equivalence — that requires
  the §3 digest comparison.
- **`digest`** — one rigorous sentence capturing the behavioral guarantee or
  contract. A hash mismatch detects *change*; the digest evaluates *safety*.
- **`class`** — answers one question: is this unit the durable **orchestrator**
  (control flow, lifecycle, dispatch) or **volatile logic** (subprocess,
  parsing, network I/O, compilation, untrusted execution)?
  - `orchestrator`: persists across the system's lifetime.
  - `volatile-logic`: should be disposable and sandboxed.
  - `n/a`: non-executing — prose, math derivations, pure data schemas. Skips
    Gate 2 (§4) entirely.

---

## 3. Gate 1 — Regression Verification

For every unit in `Baseline ∪ Candidate`:

```
                    ┌─────────────────────────┐
                    │     Unit Hash Check     │
                    └────────────┬────────────┘
                                 │
          ┌──────────────────────┼────────────────────────┐
          │ Hash matches         │ Hash differs           │ Absent from candidate
          ▼                      ▼                        ▼
    [ UNCHANGED ]          [ CHANGED ]               [ MISSING ]
  Pass. Skip narration.  Compare digests.         AUTOMATIC HARD FAIL
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
          Superset / Equiv        Drops Guarantee
               [ PASS ]         [ REGRESSION HARD FAIL ]
```

**MISSING** — automatic hard fail, no exceptions, no assumptions of "probably
unused."

**UNCHANGED** — pass. Do not re-display in narration. Silence on an UNCHANGED
unit is the correct narration for it.

**CHANGED** — mandatory digest comparison. Does the candidate digest preserve
all baseline behavioral guarantees, edge-case handlers, and output constraints?
- Superset or equivalent → **pass**.
- Drops any guarantee, error-handling path, or bounds check → **regression hard
  fail**, regardless of whether the candidate is cleaner, faster, or shorter.

This step requires reading and judgment. It cannot be merged into the hash check.

---

## 4. Gate 2 — Architectural Soundness Firewall

Runs on every unit classified `orchestrator` or `volatile-logic` that is either
newly written or carries a `CHANGED` verdict from Gate 1.

**Any single violation across 4.1–4.7 is a hard fail. Gate 2 runs independently
of Gate 1 — a Gate 1 pass does not satisfy or reduce Gate 2 requirements.**

**4.1 — Isolation over host mutation.**
Does volatile logic run inside a disposable sandbox (container, chroot, strictly-
scoped temp tree), or does it mutate the host environment directly?

**4.2 — Hard timeouts on every external execution.**
Does every subprocess, container run, HTTP request, or external call have an
explicit, system-enforced timeout?

**4.3 — Base + patch lineage.**
When tracking iterative state, does the unit apply diffs to a pristine base —
or copy entire directories per iteration?

**4.4 — Ruthless resource reclamation.**
Is every allocated resource bound to an unconditional cleanup path (`finally` /
POSIX trap) that fires on success, exception, and cancellation? Does a single
worker failure cancel all sibling futures? Do cleanups tolerate "already
released" idempotently?

**4.5 — No architectural chimeras.**
Does this unit commit to one execution paradigm (purely async, purely sync,
strictly declarative) without blending incompatible models?

**4.6 — EAFP over defensive LBYL.**
Does this unit attempt operations directly and catch specific exceptions at the
failure site — rather than running pre-flight checks that duplicate kernel error
reporting?

**4.7 — No tacking-on to a rotting monolith.**
If integrating a clean piece into a larger failing file, does the result
preserve the clean piece's simplicity — or bury it in scaffolding to fit the
monolith's shape?

---

## 5. Trigger Scope — Unit-Scoped, Not File-Scoped

Any time a named unit is touched, re-hash, re-digest, and — if its class
warrants it — re-run Gate 2 on **that unit only**. Untouched units are asserted
UNCHANGED by omission. Never re-derive the whole manifest unless performing a
full audit.

---

## 6. Emission & Narration — Three Decoupled Contracts

**6a. The Verification Artifact** — the full JSON manifest (`unit`, `hash`,
`digest`, `class`) for every unit evaluated during the session. Always complete.

**6b. The Emission Artifact** — the full literal revised artifact with zero
placeholders, no "rest unchanged," no "for brevity" truncations.

**6c. The Narration** — only CHANGED units and Gate 2 failures, with baseline
digest vs. candidate digest and the specific directive(s) at issue. UNCHANGED
units are never re-shown in narration.

> *Completeness of the artifact (6b) is mandatory.*
> *Completeness of the transcript (6c) is a different, weaker requirement.*

---

## 7. Behavioral Overrides

1. **No apologies, no sycophancy.** State the mechanism of failure and the fix
   directly.
2. **No hallucinated intent.** Canonical source and explicit instructions are
   fixed. Do not extrapolate beyond what is strictly necessary.
3. **No placeholders, ever** — a restatement of §6b as behavioral discipline.
4. **Challenge architecturally unsound requests.** If a request would force a
   §4 violation, name the specific directive, explain the failure mode, and
   provide the compliant alternative.

---

## 8. Halt Conditions

Stop and ask rather than guess when:

- A unit's canonical content is missing, ambiguous, or contradicted by context.
- A §3 digest comparison is genuinely unclear.
- A §4 architectural classification is ambiguous.
- An instruction requires dropping a baseline guarantee with no compliant
  alternative available.

---

## 9. Worked Example

**Baseline unit** (Python, `fetch_user`):

```python
def fetch_user(user_id):
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    return resp.json()
```

```json
{
  "unit":   "fetch_user",
  "hash":   "a1b2c3...",
  "digest": "Fetches a user by id over HTTP and returns parsed JSON; no timeout, no error handling on non-200 or network failure.",
  "class":  "volatile-logic"
}
```

**Candidate unit** (after revision):

```python
def fetch_user(user_id, timeout=5):
    try:
        resp = requests.get(
            f"https://api.example.com/users/{user_id}", timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise UserFetchError(f"could not fetch user {user_id}") from e
```

```json
{
  "unit":   "fetch_user",
  "hash":   "d4e5f6...",
  "digest": "Fetches a user by id over HTTP with a bounded timeout; raises UserFetchError on any network or HTTP failure; returns parsed JSON on success.",
  "class":  "volatile-logic"
}
```

**Gate 1:** CHANGED. Digest comparison: superset — all prior guarantees plus
bounded timeout and explicit failure surfacing. **Pass.**

**Gate 2:** 4.2 (hard timeout) now satisfied; previously was not. 4.6 (EAFP):
`try/except` at call site is correct. **Pass.**

**§6c narration (all that appears in chat):**
> `fetch_user` — CHANGED. Old: returned JSON, no timeout or failure handling.
> New: same, plus 5s timeout and `UserFetchError` on failure. Superset, pass.
> Closes the 4.2 gap.

---

## 10. One-Paragraph Quick Reference

> Before revising any artifact, decompose it into named units — functions,
> claims, lemmas, clauses, or process/resource boundaries, whatever the domain's
> natural grain is. For each unit, maintain a hash (detects change), a
> one-sentence digest (judges whether a change is safe), and — for any unit that
> executes or holds state — a class of `orchestrator` or `volatile-logic`. On
> revision, classify every unit as MISSING (hard fail), UNCHANGED (skip), or
> CHANGED (compare digests: superset passes, dropped capability is a hard-fail
> regression). Separately, for every `orchestrator`/`volatile-logic` unit, run
> the architectural gate: volatile logic must be sandboxed; every external
> execution needs a hard timeout; iterative state must be base+patch; every
> allocated resource needs unconditional cleanup including sibling-future
> cancellation on failure; no chimeric paradigm-mixing; EAFP over defensive
> pre-checks; no bolting working code onto a rotting monolith. A single failure
> on either gate is a hard fail, even if the other gate passes. Re-check only
> touched units per pass. Always emit the complete literal artifact with zero
> placeholders. In conversation, narrate only CHANGED or gate-failed units;
> never re-display unchanged content. Challenge any request that would force a
> Gate 2 violation. Halt and ask rather than guess whenever a unit's content,
> a digest comparison, or a class assignment is ambiguous.

---

## How to Apply This Skill

1. Identify the canonical baseline artifact (ask if ambiguous per §8) and run
   §1 atomization on it.
2. Build the §2 manifest for the baseline.
3. Make the requested revision.
4. Run §3 (Gate 1) on every touched unit. Untouched units are UNCHANGED by
   omission per §5 — do not re-derive them.
5. Run §4 (Gate 2) on every touched unit classed `orchestrator` or
   `volatile-logic`.
6. Emit per §6: full manifest (6a), full literal artifact with no placeholders
   (6b), narrate only CHANGED/failed units (6c).
7. If any unit is MISSING or fails Gate 2, treat as a hard fail — rebuild that
   unit before shipping.

---

## Automation Harness: `scripts/golden_unit_hash.py`

`scripts/golden_unit_hash.py` (v3.0.0) automates §1 atomization and the
hashing half of §2/§3 for the following languages and formats:

### Supported Languages

| Category | Languages / Formats |
|---|---|
| **Brace-delimited** | Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, C#, Kotlin, Swift, PHP, Scala, Dart, PowerShell |
| **End-keyword-delimited** | Ruby, Lua, Elixir |
| **Type-signature-anchored** | Haskell |
| **Data / Config** | TOML, YAML, JSON, SQL (CREATE TABLE/VIEW/PROCEDURE/FUNCTION/TRIGGER) |
| **Shell** | Bash / sh / zsh / ksh |
| **Any domain** | Manual JSON units (`--manual-units`) |

> **Note on Pygments:** Java, C, C++, C#, Kotlin, Swift, and Dart extraction
> requires [Pygments](https://pygments.org) (`pip install pygments`). All
> other languages use only the Python stdlib. The script raises a clear
> `ImportError` with install instructions if Pygments is missing for a
> requested language.

### Usage

```bash
# Compare baseline and candidate (auto-detects language from extension):
python3 scripts/golden_unit_hash.py --baseline old.py --candidate new.py

# Explicit language override:
python3 scripts/golden_unit_hash.py --baseline src.v --candidate src2.v --language haskell

# Manifest only (no comparison):
python3 scripts/golden_unit_hash.py --baseline old.go --manifest-only

# Non-code / unsupported domains (prose, math, contracts, protobuf, etc.):
python3 scripts/golden_unit_hash.py \
  --manual-units baseline_units.json \
  --manual-units-candidate candidate_units.json
# where each file is: [{"name": "Lemma 3.2", "content": "..."}]

# Version:
python3 scripts/golden_unit_hash.py --version
```

### Output

JSON to stdout with `baseline_manifest`, `candidate_manifest`, and `diff`
(per-unit MISSING / UNCHANGED / CHANGED / NEW verdicts by name, never by
line position).

**Stderr signals (CI-safe — stdout is pure JSON):**
- `[GUP v4 | script v3.0.0] UNCHANGED=N CHANGED=N NEW=N MISSING=N` — always
- `[REVIEW REQUIRED] NEW units — require §3 digest and §4 Gate 2 review: ...`
- `[HARD FAIL] MISSING units ...: ...` — exits 1

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | No MISSING units (NEW units present but require model review, not a script-level fail) |
| `1` | One or more MISSING units — hard fail |

### What the Script Does Not Do

The script does not perform the §3 digest comparison (whether a CHANGED unit's
new behavior is a semantic superset) and does not run the §4 architectural gate.
Both require reading and judgment. Treat the script's output as the *input* to
§3/§4, never as a substitute for them.
