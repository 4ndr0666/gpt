---
name: golden-unit-protocol
description: A strict, medium-agnostic regression-prevention and architectural-integrity protocol for revising an existing artifact (code, prose, math, schemas, systems orchestration, or contracts). Invoke this skill ONLY when the user explicitly references "the Golden-Unit Protocol," asks for a "golden-unit pass," or explicitly asks for unit-by-unit hash/digest-verified revision with regression and architectural-soundness guarantees. Do NOT use this for ordinary edit requests ("fix this bug," "clean up this doc") unless the user has invoked the protocol by name or asked for this specific level of rigor — it is intentionally heavyweight and not the default revision mode.
allowed-tools: vm_shell
---

# The Golden-Unit Protocol v4

*A medium-agnostic, zero-drift regression-prevention and architectural-integrity
protocol for LLM-driven revisions across code, prose, mathematics, data schemas,
systems orchestration, and legal contracts.*

---

## 0. Purpose & Core Guarantees

The Golden-Unit Protocol makes two failure modes structurally difficult to commit:

1. **Silent Regression** — silently dropping a previously working capability,
   edge-case handler, or contract guarantee during refactoring.
2. **Architectural Drift** — defaulting to fragile, host-mutating, chimeric, or
   over-defensive patterns that are statistically common in training data rather
   than architecturally sound.

The protocol separates verification into four explicit, independently-verifiable
phases — kept deliberately separate so none of them get silently merged into
"vibes":

1. **Atomization** — what counts as a unit.
2. **Verification** — how you prove nothing was lost.
3. **Architectural Soundness** — how you prove what replaced it isn't fragile.
4. **Emission & Narration** — how completely you produce the artifact, and what
   you actually show the person.

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
| **Code** (Python, JS, C++, Go, Rust, etc.) | Function, method, class, exported constant, config block | `[Module.]Class.method` or `[Module.]function_name` |
| **Prose / Documentation** | Claim, requirement, section, distinct assertion | `Section_X.Claim_Y` or `Req_Z` |
| **Mathematics** | Lemma, theorem, equation, derivation step | `Theorem_A`, `Lemma_B.Step_C` |
| **Data / Schema** | Key, record, field, table definition | `Table.field_name` or `Schema.key` |
| **Systems Orchestration** | Process boundary, resource allocation, lifecycle stage | `Service.Lifecycle_Stage` (e.g., `Docker.acquire`) |
| **Legal / Contractual Text** | Clause, defined term, numbered provision | `Clause_X.Y` or `Term_Z` |

### Boundary Resolution Rules

1. **Name-Based Identity**: A unit's identity is strictly its **stable name**,
   never its character position or line index. Names survive reordering and
   refactoring. `lines 501–1000` does not, and is explicitly prohibited as a
   unit boundary.
2. **Nested Scope Qualification**: Methods inside classes must be qualified as
   `ClassName.method_name` to prevent namespace collisions across unrelated
   classes.
3. **Atomic Fallback**: If an artifact lacks natural sub-units, the entire
   artifact is treated as a single unit. Do not manufacture artificial boundaries
   that conflict with domain idioms.

---

## 2. The Manifest — Hash, Digest, and Architectural Class

Every unit in the baseline and candidate manifests is recorded as a JSON object
with four mandatory fields:

```json
{
  "unit": "<stable_qualified_name>",
  "hash": "<sha256_of_literal_unit_content>",
  "digest": "<one sentence: what this unit does, asserts, handles, or guarantees>",
  "class": "<orchestrator | volatile-logic | n/a>"
}
```

### Field Definitions & Semantics

**`unit`** — Unique, qualified stable identifier per §1 naming conventions.

**`hash`** — SHA-256 of the literal unit content. Detects structural change
instantly. Hash equality does not imply behavioral equivalence — that requires
the digest comparison in §3.

**`digest`** — A single, rigorous sentence capturing the behavioral guarantee or
contract. A hash mismatch detects *change*; the digest evaluates *safety*.

**`class`** — Operational classification. Answers exactly one question: is this
unit the durable orchestrator, or is it volatile logic that should be disposable?

- `orchestrator`: Durable control flow, lifecycle management, state transitions,
  or dispatch logic. These units persist across the system's lifetime.
- `volatile-logic`: High-complexity, dependency-heavy, untrusted, or
  execution-heavy logic (subprocesses, parsing, network I/O, compilation, agent
  execution). These units must be disposable and sandboxed.
- `n/a`: Non-executing units — prose claims, math derivations, pure data
  schemas. Units with `class: "n/a"` skip Gate 2 (§4) entirely. The
  architectural anti-patterns are about systems behavior, not about whether a
  paragraph is well-argued.

---

## 3. Gate 1 — Regression Verification (Three-Way Classification)

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

**MISSING** — present in baseline, absent in candidate → automatic hard fail.
No exceptions. No assumption of "probably unused" or "implicitly redundant."

**UNCHANGED** — hashes match → pass. Do not re-discuss or re-display in
narration. Silence on an UNCHANGED unit is the correct narration for it.

**CHANGED** — hashes differ → mandatory digest comparison. Does the candidate
digest preserve all baseline behavioral guarantees, edge-case handlers, and
output constraints — while potentially adding capabilities?
- Superset or equivalent → **pass**.
- Drops any capability, error-handling path, bounds check, or edge-case
  guarantee → **regression hard fail**, regardless of whether the candidate is
  cleaner, faster, or more elegant.

This step requires reading and judgment. It cannot be merged into the hash check
or skipped under time pressure. Name it as a separate, mandatory step or it will
be skipped.

---

## 4. Gate 2 — Architectural Soundness Firewall

Runs on every unit classified `orchestrator` or `volatile-logic` that is either
newly written or carries a `CHANGED` verdict from Gate 1.

**Any single violation across 4.1–4.7 is a hard fail — discard and rebuild the
unit from the correct standard. Gate 2 failure has the same severity as a §3
regression. Gate 2 runs independently of Gate 1; a Gate 1 pass does not satisfy
or reduce Gate 2 requirements.**

**4.1 — Isolation over host mutation.**
Does this unit's volatile logic (untrusted, complex, or dependency-heavy
execution — subprocess calls, transcodes, compilation, agent execution) run
directly against the host filesystem/environment, or is it bounded inside a
disposable sandbox (container, chroot, strictly-scoped temp tree)? Orchestrator
units must never read global host state directly; they inject scoped input,
execute inside the boundary, and extract only the explicit declared output.

**4.2 — Hard timeouts on every external execution.**
Does every subprocess, container run, HTTP request, or external call have an
explicit, system-enforced timeout? An execution with no timeout is a unit that
can hang the orchestrator indefinitely — this is a standalone fail condition,
independent of whether the logic is otherwise correct.

**4.3 — Base + patch lineage.**
When this unit tracks iterative state (evolutionary loops, multi-pass processing,
repeated generation), does it apply diffs/patches to a pristine base — or does
it copy entire directories or state objects per iteration? The latter causes
unbounded storage growth and makes rollback undefined. State must be resettable
to a known-pristine baseline; never "undone" piecemeal.

**4.4 — Ruthless resource reclamation.**
Is every resource this unit allocates (container, port, temp directory, thread,
subprocess handle, file descriptor) bound to an unconditional cleanup path —
a `finally`/POSIX trap/equivalent — that fires on success, exception, and
cancellation? If the unit uses concurrency, does a single worker failure trigger
explicit cancellation of all sibling futures? Do cleanup routines tolerate
"resource already released" idempotently, without surfacing that as an error?

**4.5 — No architectural chimeras.**
Does this unit commit fully to one execution paradigm (purely async, purely
synchronous, strictly declarative) or does it blend two incompatible ones (async
event loop wrapping blocking calls; React hooks alongside direct DOM mutation;
stream-copy mixed with frame-by-frame filtering)? If a chimera is detected, the
fix is not to patch the seam — it is to declare one paradigm and rewrite the
unit to commit to it fully.

**4.6 — EAFP over defensive LBYL.**
Does this unit attempt operations directly and handle resulting exceptions at the
failure site, or does it run extensive pre-flight checks that duplicate the
kernel's or runtime's own error reporting? Defensive pre-checks that mirror what
the OS will report anyway are what break under edge cases the pre-check didn't
anticipate.

**4.7 — No tacking-on to a rotting monolith.**
If the task is "integrate this clean, working piece into that large, struggling
file," does the result preserve the working piece's simplicity, or does it bury
it in wrappers and metadata-parsing scaffolding to fit the monolith's existing
shape? When a provided solution is already correct and minimal, it is the
architectural superior — restructure the surrounding system around it rather than
degrading it to fit. A unit that has grown past doing one thing well must be
split into composable pieces connected by clean interfaces, not extended further
in place.

---

## 5. Trigger Scope — Unit-Scoped, Not File-Scoped

Any time a named unit is touched, re-hash, re-digest, and — if its class warrants
it — re-run Gate 2 on **that unit only**. Units not touched are asserted
UNCHANGED by omission. Do not re-derive the whole artifact's manifest unless
explicitly performing a full audit.

The grain of re-checking is the domain's natural unit, never an arbitrary
fixed-size window. A one-line fix inside a 2,000-line orchestration script
re-checks one unit and its architectural class — not an artificial slice that
happens to contain it.

---

## 6. Emission & Narration — Three Decoupled Contracts

Three separate obligations, never merged:

**6a. The Verification Artifact** — the full manifest (`unit`, `hash`, `digest`,
`class`) for every unit evaluated during the session. Always complete; it is
small and structured regardless of artifact size.

**6b. The Emission Artifact** — the full literal artifact: every line, clause, or
proof step, with zero placeholders, no "rest unchanged," no "for brevity"
truncations. This binds to the *artifact*, not the *chat transcript* — a complete
file delivered as a document satisfies this exactly as much as the same content
typed into a conversation. Completeness of content and medium of delivery are
different questions; only the first is non-negotiable.

**6c. The Narration** — only the CHANGED units (§3) and any unit that failed or
required correction under Gate 2 (§4), shown as before/after with their digests
and the specific directive(s) at issue. UNCHANGED units are **never** re-shown.
Re-showing them is what buries real changes — and real architectural fixes — in
noise.

> *Completeness of the artifact (6b) is mandatory.*
> *Completeness of the transcript (6c) is a different, weaker requirement.*

---

## 7. Behavioral Overrides

These bind the reviser's conduct, independent of any single unit's classification:

1. **No apologies, no sycophancy in the correction path.** State the mechanism of
   failure and the fix directly. Gratitude for a correction is fine; performative
   self-criticism is not — it adds nothing to the next decision.
2. **No hallucinated intent.** Treat the person's data, canonical source, and
   explicit instructions as fixed. Do not extrapolate beyond what is strictly
   necessary to complete the task.
3. **No placeholders, ever**, per §6b — this is restated here because it is a
   behavioral discipline as much as an output rule.
4. **Challenge architecturally unsound requests rather than silently complying.**
   If a request would force a §4 violation, name the specific directive, explain
   the failure mode (TOCTOU, corruption-on-interrupt, unbounded mutation, etc.),
   and offer the compliant alternative — rather than either refusing outright or
   quietly building the unsound version.

---

## 8. Halt Conditions

Stop and ask, rather than guess, whenever:

- A unit's canonical content is missing, ambiguous, or contradicted by context.
- A §3 digest comparison is genuinely unclear (not obviously superset or
  regression).
- A §4 architectural classification is ambiguous (is this unit really volatile
  logic, or is it legitimately part of the durable orchestrator?).
- An instruction would require dropping a guarantee a unit previously held, or
  building a unit that fails §4 with no compliant alternative offered.

Guessing in any of these cases is itself a protocol violation.

---

## 9. Worked Example

A single unit traced through the full pipeline to make §2–§4 concrete.

**Baseline unit** (Python function, before):

```python
def fetch_user(user_id):
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    return resp.json()
```

```json
{
  "unit": "fetch_user",
  "hash": "a1b2c3...",
  "digest": "Fetches a user by id over HTTP and returns parsed JSON; no timeout, no error handling on non-200 or network failure.",
  "class": "volatile-logic"
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
  "unit": "fetch_user",
  "hash": "d4e5f6...",
  "digest": "Fetches a user by id over HTTP with a bounded timeout; raises UserFetchError on any network or HTTP failure; returns parsed JSON on success.",
  "class": "volatile-logic"
}
```

**Gate 1 verdict:** CHANGED (hash differs). Digest comparison: the candidate is a
strict superset — it still returns parsed JSON on success, and now additionally
bounds the call and surfaces failure explicitly. **Pass.**

**Gate 2 verdict** (class is `volatile-logic`, so the gate runs):
- 4.2 (hard timeout): now satisfied; previously was not — this is a fix, not a
  regression.
- 4.6 (EAFP): the `try/except` at the call site is EAFP, not a pre-flight check.
  Pass.
- 4.1, 4.3, 4.5: no sandbox, iterative state, or paradigm-mixing involved — n/a.

**Pass.**

**§6c narration for this unit** (this is *all* that appears in chat for this
unit):

> `fetch_user` — CHANGED. Old digest: fetched and returned JSON with no timeout
> or failure handling. New digest: same, plus 5s timeout and explicit
> `UserFetchError` on failure. Superset, pass. Closes the 4.2 gap that would
> otherwise have been a hard fail on this unit's class.

Note what is *not* shown: the full baseline source; any unit elsewhere in the
same file that wasn't touched; an apology for the original lacking a timeout.

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
> the architectural gate: volatile logic must be sandboxed, not host-mutating;
> every external execution needs a hard timeout; iterative state must be
> base+patch, not copy-and-accumulate; every allocated resource needs
> unconditional cleanup including sibling-future cancellation on failure; no
> chimeric paradigm-mixing; EAFP over defensive pre-checks; no bolting working
> code onto a rotting monolith. A single failure on either gate is a hard fail,
> even if the other gate passes. Re-check only touched units per pass. Always emit
> the complete literal artifact with zero placeholders. In conversation, narrate
> only CHANGED or gate-failed units with their digests and the specific directive
> at issue; never re-display unchanged content. Challenge any request that would
> force a Gate 2 violation. Halt and ask rather than guess whenever a unit's
> content, a digest comparison, or a class assignment is ambiguous.

---

## How to Apply This Skill

1. On invocation, identify the canonical baseline artifact (ask if ambiguous per
   §8) and run §1 atomization on it.
2. Build the §2 manifest for the baseline.
3. Make the requested revision.
4. Run §3 (Gate 1) on every touched unit. Untouched units are UNCHANGED by
   omission per §5 — do not re-derive them.
5. Run §4 (Gate 2) on every touched unit classed `orchestrator` or
   `volatile-logic`.
6. Emit per §6: full manifest (6a), full literal artifact with no placeholders
   (6b), and narrate only CHANGED/failed units (6c).
7. If any unit is MISSING or fails Gate 2, treat as a hard fail — rebuild that
   unit; do not ship it with a caveat.

---

## Automation Harness: `scripts/golden_unit_hash.py`

For Python and JS/TS source files, `scripts/golden_unit_hash.py` automates the
*hashing* half of §1–§3: it extracts named units (functions, classes, methods —
qualified as `ClassName.method` to avoid collisions), hashes each unit's literal
content, and reports MISSING / UNCHANGED / CHANGED / NEW by name — never by line
position.

```bash
# Compare baseline and candidate:
python3 scripts/golden_unit_hash.py --baseline old.py --candidate new.py

# Manifest only (no comparison):
python3 scripts/golden_unit_hash.py --baseline old.py --manifest-only

# Non-code domains (prose, math, schemas, contracts):
python3 scripts/golden_unit_hash.py \
  --manual-units baseline_units.json \
  --manual-units-candidate candidate_units.json
# where each file is: [{"name": "Lemma 3.2", "content": "..."}]
```

The script exits non-zero and prints to `stderr` if any unit is MISSING — usable
as a hard gate in CI, not just a report. It also summarizes NEW units to `stderr`
so newly introduced units are always surfaced explicitly for digest and Gate 2
review.

**What the script does not and cannot do:** it does not perform the §3 digest
comparison (whether a CHANGED unit's new behavior is a semantic superset) and it
does not run the §4 architectural gate. Both require reading and judgment — those
steps stay with the model, every time, on every CHANGED or NEW unit the script
surfaces. Treat the script's output as the *input* to §3/§4, never as a
substitute for them.
