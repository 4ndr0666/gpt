---
name: golden-unit-protocol
description: A strict, medium-agnostic regression-prevention and architectural-integrity protocol for revising an existing artifact (code, prose, math, schemas, systems orchestration, or contracts). Invoke this skill ONLY when the user explicitly references "the Golden-Unit Protocol," asks for a "golden-unit pass," or explicitly asks for unit-by-unit hash/digest-verified revision with regression and architectural-soundness guarantees. Do NOT use this for ordinary edit requests ("fix this bug," "clean up this doc") unless the user has invoked the protocol by name or asked for this specific level of rigor — it is intentionally heavyweight and not the default revision mode.
---

# The Golden-Unit Protocol v2

*A medium-agnostic regression-prevention and architectural-integrity protocol for LLM-driven revision — covering code, prose, mathematics, and systems orchestration alike.*

## 0. Purpose

This protocol makes two failure modes structurally difficult to commit:

1. **Silent regression** — losing a previously-working capability while revising.
2. **Architectural drift** — defaulting to fragile, host-mutating, chimeric, or over-defensive patterns because they are statistically common in training data, not because they are correct for the task.

It governs four things, kept deliberately separate so none of them get silently merged into "vibes":

1. **Atomization** — what counts as a unit.
2. **Verification** — how you prove nothing was lost.
3. **Architectural Soundness** — how you prove what *replaced* it isn't fragile.
4. **Emission & Narration** — how completely you produce the artifact, and what you actually show the person.

## 1. Atomization — Define the Unit Before Touching Anything

Decompose the canonical artifact into **named units**: the smallest pieces with independent identity in their own domain.

| Domain | Unit |
|---|---|
| Code (any language) | Function, method, class, exported constant, config block |
| Prose / documentation | Claim, numbered requirement, section, distinct assertion |
| Mathematics | Named lemma, theorem, equation, derivation step |
| Data / schema | Key, record, field, table definition |
| Systems orchestration | Process boundary, resource allocation, lifecycle stage (acquire → use → release) |
| Legal / contractual text | Clause, defined term, numbered provision |

A unit's identity is its **name**, never its position. `function pruneToPlaceholder`, `Lemma 3.2`, `the Docker container lifecycle in step 4` — these survive reordering. `lines 501–1000` does not, and has no meaning outside source code.

If the artifact has no natural named units, the smallest viable unit is the whole artifact. Do not invent boundaries the domain doesn't have.

## 2. The Manifest — Hash, Digest, *and* Architectural Class

For every unit, record four things — the fourth is new in v2:

```json
{
  "unit": "<stable name>",
  "hash": "<sha256 of the unit's literal content>",
  "digest": "<one sentence: what this unit does, asserts, or guarantees>",
  "class": "<orchestrator | volatile-logic | n/a>"
}
```

**`hash`** detects that something changed.
**`digest`** judges whether the change is safe — a hash mismatch alone is blind to meaning.
**`class`** exists only for units that execute, allocate, or hold state. It answers one question: *is this unit the durable orchestrator, or is it volatile logic that should be disposable?* This classification is what makes §4.1 (Isolation) and §4.3 (Immutable Lineage) checkable per-unit rather than left as a vague aspiration about the whole system.

Units with no execution/state behavior (a prose claim, a math lemma, a pure data record) get `class: "n/a"` and skip §4 entirely — the anti-patterns are about systems behavior, not about whether a paragraph is well-argued.

## 3. The Regression Check — Three-Way Classification

For every unit in baseline ∪ candidate:

- **MISSING** — present in baseline, absent in candidate → **automatic hard fail**. No exceptions, no "it was probably unused."
- **UNCHANGED** — hash matches → pass, skip, do not re-discuss.
- **CHANGED** — hash differs → **mandatory digest comparison**: does the new digest semantically contain everything the old one guaranteed, plus possibly more?
  - Superset/equivalent → pass.
  - Drops a capability, guarantee, error-handling path, or edge case → **regression, hard fail** — regardless of whether the candidate is cleaner, faster, or more elegant by any other measure.

This step requires actual reading and judgment, not just hash comparison. It cannot be merged into the hash check or skipped under time pressure — name it as a separate, mandatory step or it will get skipped.

## 4. The Architectural Soundness Check — Anti-Pattern Gate

**This runs on every unit classified `orchestrator` or `volatile-logic` in §2 — both newly-written units and any unit reclassified by a CHANGED verdict in §3.** It is not optional, and it is not satisfied by the regression check passing — a change can be a strict superset of prior behavior and *still* be architecturally unsound (e.g., it preserves every guarantee but now mutates the host directly to do so). Both gates must pass independently.

**4.1 — Isolation over host mutation.** Does this unit's volatile logic (untrusted, complex, or dependency-heavy execution — subprocess calls, transcodes, compilation, agent execution) run directly against the host filesystem/environment, or is it bounded inside a disposable sandbox (container, chroot, strictly-scoped temp tree)? Orchestrator units must never read global host state directly; they inject scoped input, execute inside the boundary, and extract only the explicit declared output.

**4.2 — Hard timeouts on every external execution.** Does every subprocess, container run, or external call have a system-level bounding timeout? An execution with no timeout is a unit that can hang the orchestrator indefinitely — this is a fail condition on its own, independent of whether the logic is otherwise correct.

**4.3 — Lineage is base + patch, not copy-and-accumulate.** When this unit tracks iterative state (evolutionary loops, multi-pass processing, repeated generation), does it apply diffs/patches to a pristine base, or does it copy entire directories/states per iteration? The latter is a fail: it causes unbounded storage growth and makes rollback undefined. Before any new iteration, state must be resettable to a known-pristine baseline, not "undone" piecemeal.

**4.4 — Ruthless resource reclamation.** Is every external resource this unit allocates (container, port, temp directory, thread, subprocess handle) bound to an unconditional cleanup path — a `finally`/POSIX trap/equivalent — that fires even on exception or interrupt? If this unit uses concurrency, does a single worker's failure trigger explicit cancellation of sibling futures, or are siblings left running toward a doomed result? Cleanup routines must tolerate "resource already gone" without surfacing that as an error — cleanup is unconditional, not best-effort.

**4.5 — No architectural chimeras.** Does this unit commit to one paradigm (e.g., purely async, purely synchronous, strictly declarative) or does it blend two incompatible ones (async event loop wrapping blocking calls; React hooks alongside direct DOM mutation; stream-copy mixed with frame-by-frame filtering)? If a chimera is detected, the fix is not to patch the seam — it is to pick one paradigm and rewrite the unit to commit to it fully. State the paradigm choice explicitly before writing the unit, and hold to it.

**4.6 — EAFP over defensive LBYL.** Does this unit run extensive pre-flight validation (existence checks, permission checks, alignment checks) before attempting the real operation, or does it attempt the operation directly and handle the resulting exception/exit-code/signal at the failure site? Excessive Look-Before-You-Leap logic is a fail condition — not because validation is wrong, but because duplicating the kernel/runtime's own error reporting in brittle pre-checks is what actually breaks under edge cases the pre-check didn't anticipate.

**4.7 — No tacking-on to a rotting monolith.** If the task is "integrate this clean, working piece into that large, struggling file," does the result preserve the working piece's simplicity, or does it bury it in wrappers and metadata-parsing scaffolding to fit the monolith's existing shape? When a provided solution is already correct and minimal, it is the architectural superior — restructure the surrounding system around it rather than degrading it to fit. A unit that has grown past doing one thing well is a unit that should be split into composable pieces connected by standard interfaces, not extended further in place.

**Any single "no" across 4.1–4.7, for a unit in the `orchestrator`/`volatile-logic` class, is a hard fail — discard the generation for that unit and rebuild it from the correct standard, the same severity as a §3 regression.**

## 5. The Trigger — Unit-Scoped, Not Count-Scoped

> Any time a named unit is touched, re-hash, re-digest, and — if its class warrants it — re-run the §4 architectural gate on **that unit only**. Units not touched are asserted UNCHANGED by omission. Do not re-derive the whole artifact's manifest unless explicitly performing a full audit.

The grain of re-checking is the domain's natural unit, never an arbitrary fixed-size window. A one-line fix inside a 2,000-line orchestration script re-checks one unit and its architectural class, not an artificial slice that happens to contain it.

## 6. The Emission Contract — Decoupled from the Narration Contract

Three separate obligations, never merged:

**6a. The Verification Artifact** — the full manifest (every unit, hash, digest, class) produced in full on every check. Always complete; it is small and structured regardless of artifact size.

**6b. The Emission Artifact** — the full literal artifact: every line, clause, or proof step, with zero placeholders, no "rest unchanged," no "for brevity." This binds to the *artifact*, not the *chat transcript* — a complete file delivered as a document satisfies this exactly as much as the same content typed into a conversation. Completeness of content and medium of delivery are different questions; only the first is non-negotiable.

**6c. The Narration** — only the CHANGED units (§3) and any unit that failed or required correction under the architectural gate (§4), shown as before/after with their digests and the specific directive(s) from §4 that were at issue. UNCHANGED units are never re-shown. Re-showing them is what buries real changes — and real architectural fixes — in noise.

> *Completeness of the artifact is mandatory. Completeness of the transcript is a different, weaker requirement.*

## 7. Behavioral Overrides

These bind the reviser's conduct, independent of any single unit's classification:

- **No apologies, no sycophancy in the correction path.** State the mechanism of failure and the fix. Gratitude for a correction is fine; performative self-criticism is not — it adds nothing to the next decision.
- **No hallucinated intent.** Treat the person's data, canonical source, and explicit instructions as fixed. Do not extrapolate beyond what's needed to complete the task.
- **No placeholders, ever**, per §6b — this is restated here because it is a behavioral discipline as much as an output rule.
- **Challenge architecturally unsound requests rather than silently complying.** If a request would force a §4 violation (e.g., "just write directly to the shared system directory over five hours, no sandbox"), say so explicitly, name the specific failure mode (TOCTOU, corruption-on-interrupt, unbounded mutation), and offer the compliant alternative — rather than either refusing outright or quietly building the unsound version.

## 8. Halt Conditions

Stop and ask, rather than guess, whenever:

- A unit's canonical content is missing, ambiguous, or contradicted by context.
- A §3 digest comparison is genuinely unclear (not obviously superset or regression).
- A §4 architectural classification is ambiguous (is this unit really volatile logic, or is it legitimately part of the durable orchestrator?).
- An instruction would require dropping a guarantee a unit previously held, or building a unit that fails §4 with no compliant alternative offered.

Guessing in any of these cases is itself a protocol violation.

## 9. Worked Example

A small trace of the manifest format applied to a single revision, to make §2–§3 concrete.

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
  "digest": "Fetches a user by id over HTTP and returns parsed JSON; no error handling on non-200 or network failure.",
  "class": "volatile-logic"
}
```

**Candidate unit** (after revision):

```python
def fetch_user(user_id, timeout=5):
    try:
        resp = requests.get(f"https://api.example.com/users/{user_id}", timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise UserFetchError(f"could not fetch user {user_id}") from e
```

```json
{
  "unit": "fetch_user",
  "hash": "d4e5f6...",
  "digest": "Fetches a user by id over HTTP with a bounded timeout, raises UserFetchError on any network or HTTP failure, returns parsed JSON on success.",
  "class": "volatile-logic"
}
```

**§3 verdict**: CHANGED (hash differs). Digest comparison: new digest is a strict superset — it still returns parsed JSON on success, and now additionally bounds the call and surfaces failure explicitly instead of letting a bad response propagate unhandled. **Pass.**

**§4 verdict** (class is `volatile-logic`, so the gate runs): 4.2 (hard timeout) — now satisfied, previously was not; this is a fix, not a regression. 4.6 (EAFP) — the `try`/`except` at the call site is EAFP, not a pre-flight check, so this passes. No chimera, no host mutation beyond the original's scope, no iterative state involved → n/a for 4.1, 4.3, 4.5. **Pass.**

**§6c narration for this unit** (this is *all* that gets shown in conversation for this unit):

> `fetch_user` — CHANGED. Old digest: fetched and returned JSON with no failure handling. New digest: same, plus a 5s timeout and an explicit `UserFetchError` on failure. Superset, pass. Architectural note: closes the 4.2 gap (no prior timeout) that would otherwise have been a hard fail on this unit's class.

Note what is *not* shown: the full baseline source, restated only to point out it's now superseded; any unit elsewhere in the same file that wasn't touched; apology for the original lacking a timeout.

## 10. One-Paragraph Form

For quick reference or re-embedding elsewhere:

> Before revising any artifact, decompose it into named units — functions, claims, lemmas, clauses, or process/resource boundaries, whatever the domain's natural grain is. For each unit needing one, maintain a hash (detects change), a one-sentence digest (judges whether a change is safe), and — for any unit that executes or holds state — a class of orchestrator or volatile-logic. On revision, classify every unit as MISSING (hard fail), UNCHANGED (skip), or CHANGED (compare digests: superset passes, dropped capability is a hard-fail regression). Separately, for every orchestrator/volatile-logic unit, run the architectural gate: volatile logic must be sandboxed not host-mutating; every external execution needs a hard timeout; iterative state must be base+patch, not copy-and-accumulate; every allocated resource needs unconditional cleanup including sibling-future cancellation on failure; no chimeric paradigm-mixing; EAFP execution over defensive pre-checks; no bolting working code onto a rotting monolith. A single failure on either gate is a hard fail, even if the other gate passes. Re-check only touched units per pass. Always emit the complete literal artifact with zero placeholders, but completeness of the artifact and completeness of the conversational transcript are separate requirements — only the former is mandatory. In conversation, narrate only CHANGED or gate-failed units with their digests and the specific directive at issue; never re-paste unchanged content. Challenge, rather than silently comply with, any request that would force an architectural-gate violation. Halt and ask rather than guess whenever a unit's content, a digest comparison, or a class assignment is ambiguous.

## How to apply this skill

1. On invocation, identify the canonical baseline artifact (ask if ambiguous per §8) and run §1 atomization on it.
2. Build the §2 manifest for the baseline.
3. Make the requested revision.
4. Run §3 on every touched unit (untouched units are UNCHANGED by omission per §5 — do not re-derive them).
5. Run §4 on every touched unit classed `orchestrator` or `volatile-logic`.
6. Emit per §6: full manifest (6a), full literal artifact with no placeholders (6b), and narrate only CHANGED/failed units (6c).
7. If any unit is MISSING or fails §4, treat as a hard fail — rebuild that unit, don't ship it with a caveat.

## Helper script: scripts/golden_unit_hash.py

For Python and JS/TS source files, `scripts/golden_unit_hash.py` automates the *hashing* half of §1–§3: it extracts named units (functions, classes, methods — qualified as `ClassName.method` to avoid collisions across classes), hashes each one's literal content, and reports MISSING / UNCHANGED / CHANGED / NEW by name.

```bash
python3 scripts/golden_unit_hash.py --baseline old.py --candidate new.py
```

For non-code domains (prose claims, math lemmas, contract clauses) there's no parser to lean on — supply units manually as JSON:

```bash
python3 scripts/golden_unit_hash.py \
  --manual-units baseline_units.json \
  --manual-units-candidate candidate_units.json
# where each file is: [{"name": "Lemma 3.2", "content": "..."}]
```

This script exits non-zero and prints to stderr if any unit is MISSING, so it's usable as a hard gate, not just a report.

**What this script does not and cannot do**: it does not perform the §3 digest comparison (whether a CHANGED unit's new behavior is a semantic superset) and it does not run the §4 architectural gate. Both require reading and judgment — that step stays with Claude, every time, on every CHANGED or NEW unit the script surfaces. Treat the script's output as the input to §3/§4, never as a substitute for them.
