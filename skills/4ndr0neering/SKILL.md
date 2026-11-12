---
name: 4ndr0neering
description: Evidence-driven engineering convergence and performance-first directive unifying GUP, 4ndr0neering, and suckless/data-oriented design. Use when implementing or revising code, profiling performance, remediating ISO/IEC 5055-inspired structural weaknesses, defining benchmark gates, preventing regressions, verifying acceptance contracts, or producing self-verifying updates. Enforces immutable mandatory criteria, stepwise mitigation, source-anchored performance measurement, and bounded/certified delivery without conflating installation success with product acceptance.
allowed-tools: execute_bash view_file write_to_file
---
# 4ndr0neering Convergence + Performance-First Engineering Protocol (v8.2.0)

A bounded, executable source-grounded engineering discipline unifying `golden-unit-protocol` (GUP), original 4ndr0neering, and an **original** performance-first directive. It retains the v8.1 lineage-adaptive Git kit and unit verification, and adds an immutable acceptance ledger and workload-specific performance gates. The design draws conceptually on public CISQ performance weaknesses, suckless simplicity/frugality, and Casey Muratori's performance-aware data-layout arguments. **It is not an ISO/IEC 5055 publication, conformant implementation, certified audit, or proof that any coding idiom is universally optimal.**

## When to Use

- Executing feature implementation, bugfixes, refactoring, or repository migrations requiring zero silent regressions.
- Auditing codebases, verifying bidirectional dependency/capability alignment, or validating acceptance criteria against real files and test logs.
- Packaging completed or partially completed engineering rounds into deterministic, single-file self-verifying update kits (`update-<suite>-<round>.sh`) and self-contained HTML round-record pages that adapt cleanly to moving-HEAD and cross-lineage host repositories.
- Replacing GUP or SUK workflows where missing runtime proof, blocked secondary targets, or changing host commit pins must be handled deterministically rather than halting work or failing on synthetic sandbox commit SHAs.
- Applying an original, language-agnostic performance-first doctrine with **conditional** hot-path specialization, data locality, bounded resource use, and direct simplicity, with no unmeasured universal speed claims.
- Running mandatory stop-and-go acceptance rounds until all required gates pass or a documented external/user-authority checkpoint is unavoidable.

## Core Operational Principles

1. **Checks Tied to Actual Files:** Every unit manifest, semantic review, alignment edge, integration surface, and acceptance criterion must resolve to real files, AST/lexical symbols, Git objects, or executed command logs on disk. String-only placeholders (`"evidence": "ok"`) are rejected by the validator.
2. **Demonstrated Defect vs. Missing Evidence:** Never conflate a demonstrated defect with missing evidence. Use four distinct epistemic states:
   - `VERIFIED`: Checked against actual repository bytes, symbols, or executed command logs with zero errors.
   - `UNVERIFIED`: Cannot be conclusively tested in the current environment (for example, missing host hardware, external network service, or unrunnable GUI check). Bounds the claim without halting work.
   - `BLOCKED`: A specific target cannot proceed due to missing upstream input or user authorization. Scoped strictly to that target so unrelated targets proceed.
   - `DEFECT`: An invariant, file check, symbol check, unit superset guarantee, or test was evaluated and failed. Blocks delivery of the broken target until fixed or explicitly disclosed in a diagnostic handoff.
3. **Uncertainty Bounds Claims Without Stopping Unrelated Work:** When Target A is `VERIFIED` and Target B is `UNVERIFIED` or `BLOCKED`, complete Target A, record the exact boundary on Target B, and emit `BOUNDED_PASS` as **legacy evidence-scope status only**, never as v8.2 task completion; the v8.2 acceptance controller still exits nonzero while mandatory gates remain open.
4. **Content-Addressed & Lineage-Adaptive Pinning (Moving-HEAD & Sandbox-to-Host Resilience):**
   - Commit SHAs (`PIN_BASE`, `PIN_TIP`, `PIN_TIP_TREE`) change whenever an operator commits to other files in a monorepo or when a kit is authored inside an isolated sandbox VM from uploaded files rather than a full clone of the operator's `.git` history.
   - `4ndr0_kit.py` embeds **both** build-lineage pins (`PIN_BASE`, `PIN_TIP`, `PIN_TIP_TREE`) in a prerequisite-free Git bundle **and** content-addressed file pins (`PIN_KEY_BASE_SHA` and `PIN_KEY_SHA`):
     - **Fast-Forward Lineage Mode (`HEAD == PIN_BASE`):** Fast-forwards `HEAD` directly to `PIN_TIP` and verifies `PIN_TIP_TREE`.
     - **Dynamic Content-Pinned Mode (`HEAD != PIN_BASE`):** When the operator's `HEAD` has advanced on other files while `PIN_KEY_FILE` still matches `PIN_KEY_BASE_SHA`, or when the kit was authored in a sandbox VM (`PIN_BASE` absent from the host's `.git/objects`) or targets a subdirectory (e.g. `bash update-suite-round-1.sh scr`), the kit unpacks and verifies the bundle (`PIN_PAYLOAD_SHA`, `PIN_BUNDLE_SHA`, `PIN_TIP`, `PIN_TIP_TREE`) inside an isolated temporary staging repository, backs up any prior file state, applies the verified candidate blobs onto the operator's active branch, verifies `PIN_KEY_SHA` and `GATE_CMD`, and commits cleanly.
     - **Conflicting Edit Fail-Closed (`P3`):** In same-lineage repositories where `HEAD != PIN_BASE` and `PIN_KEY_FILE` itself has diverged (`!= PIN_KEY_BASE_SHA` and `!= PIN_KEY_SHA`), the kit fails closed (`exit 1`, `DO NOT FORCE`) without touching `HEAD`.
     - **Canvas / Clipboard Trailing-Newline Immunity:** Kits are emitted without a trailing newline after `#__PAYLOAD_END__` so browser/Canvas downloads preserve `PIN_KIT_SHA` byte-for-byte.
5. **Proportionate Verification Tiers:** Match verification overhead to change blast radius instead of forcing heavyweight ceremony onto minor edits:
   - **Tier `T0` (Micro / Patch):** Single-file bugfix, config tweak, or pure helper (1-2 files, no new external dependencies). Requires `entry_points` and `tests` closure plus unit hash comparison on touched files.
   - **Tier `T1` (Module / Feature):** Multi-function or multi-file feature within an existing module boundary. Requires `entry_points`, `callers`, `providers`, `consumers`, and `tests` closure plus file-anchored alignment on touched modules.
   - **Tier `T2` (Cross-Cutting / Migration):** Architectural refactor, schema migration, or loader change. Requires all 9 integration surfaces (`entry_points`, `loaders`, `callers`, `providers`, `consumers`, `configuration_paths`, `install_migration_paths`, `tests`, `runtime_dependencies`) and full repository unit comparison.
   - **Tier `T3` (Release / Self-Verifying Kit Delivery):** Full `T2` verification plus deterministic single-file update kit (`4ndr0_kit.py`), automated `P0-P7 + P1B (Moving-HEAD) + P1C (Cross-Lineage Subdir) + RED_CONTROL` battery execution, and self-contained HTML round-record generation (`4ndr0_report.py`).
6. **Architectural Soundness (Gate 2 Directives):**
   - Declare a single paradigm per module; do not mix incompatible concurrency or DOM models.
   - Enforce explicit timeouts on all subprocesses and external I/O.
   - Bind temporary directories, containers, locks, and background workers to unconditional `finally` or POSIX `trap` cleanup.
   - Use EAFP (`try`/`except` specific exceptions) on data paths, and fail-closed precondition checks at trust boundaries (installers, kits, destructive Git operations).
   - Emit complete, runnable files with zero `TODO` stubs or ellipses.

## Mandatory v8.2 Rules: Completion, Provenance, Performance

**Use the independent rulebook:** `references/PERFORMANCE_DIRECTIVES.md` (PF-001–PF-018). `references/CISQ_PUBLIC_CWE_CROSSWALK.json` contains a public **18-CWE** cross-reference (15 parents, 3 children) and conditional investigation paths; it does not reprint the ISO standard or assert static-analysis coverage beyond the available detector.

### GUP-C01 — Immutability of mandatory acceptance

Write `schemas/4ndr0-convergence-contract.schema.json`-shaped `contract.json` **before** implementation. Every user-mandated outcome has `mandatory: true`, a quality `gate`, an owner, and an executable `command` where engineer-owned. The ledger binds the full contract by SHA-256. **Do not** remove, weaken, silently waive, or rename required criteria to obtain a green release. A genuine conflicting-user-authority decision must be explicitly requested, not inferred. Contract changes require a newly versioned acceptance baseline. `BOUNDED_PASS` in legacy GUP evidence is never synonymous with completion when mandatory gates remain open.

### GUP-C02 — Stop-and-go convergence

At each round, inspect failure evidence, identify an *actionable* root cause, patch the smallest sufficient surface, run acceptance and regression checks, record the result, and continue. Emit next-action status from the ledger: `MITIGATE_AND_RETEST`, `EXECUTE_OR_REPLAN_REQUIRED_GATES`, `EXECUTE_ON_SUPPORTED_EXTERNAL_HOST`, `REQUEST_NARROW_USER_DECISION`, or `DELIVER_CERTIFIED_RELEASE`. Stop only when all mandatory gates pass or a specific user/external blocker prevents further legitimate progress. A diagnostic handoff is permitted but exits nonzero and is labeled incomplete.

### GUP-C03 — Separate five verification planes

Track **functional behavior**, **structural/static risk**, **measured runtime performance**, **persistent/integration behavior**, and **update-kit integrity** separately. A green Git kit/CRC, static CWE-style scan, or unit hash cannot satisfy a runtime-performance or real-browser-persistence criterion. Contract an HTTP-origin reload if persistence is mandatory; a `file://` mock or state-reset simulation is not equivalent.

### GUP-C04 — Performance: simple by default, workload-driven in hot paths

- Treat the **suckless** values simplicity, clarity, frugality, removal of needless layers and dependencies as a *default design constraint*, not proof of speed. Do not delete required safeguards, behavior, error handling, or observability.
- Review structural risks (resource lifetime, expensive calls in loops, N+1 queries, repeated scans, unnecessary allocations, data access bypass) using the public CISQ 18-CWE cross-reference. The bundled `scan` currently supports **Python AST hints**; other languages require external analyzers or human review. Hints are **not verified defects**.
- Use data-oriented design as a **testable candidate**: change layout, batch operations, specialize dispatch or collapse abstraction **only** if a workload profile supports it. Small functions, DRY, OOP, caches, and virtual dispatch are not universally slow; explicit code is not inherently fast.
- For a required performance acceptance criterion, define source-fingerprinted baseline and candidate commands, realistic input, host envelope, warmups, samples, allowable regression, and correctness parity. Only `4ndr0_perf.py run` can establish this tool's **paired wall-time** PASS; CI width/noise and output differences force non-PASS. Other metrics (memory, energy, throughput, tails, I/O) must have independent instruments and gates.

### GUP-C05 — Provenance and external blockers

Require authentic baseline code and reproducible execution logs. If the environment blocks `localhost` or hardware, preserve the actual failure and run on an authorized host if available. Do not substitute dry runs or mock/local volatile storage. If no authorized runtime exists, keep the mandatory gate `BLOCKED` and the overall task **incomplete**.

### GUP-C06 — Fail-closed certification

Protocol `8.2.0` requires both `--convergence-contract` and `--convergence-ledger` in the legacy validator. It reads the verified hash-linked controller ledger. A required gate in `DEFECT`, `UNVERIFIED`, `BLOCKED`, or `PENDING` prevents a successful exit, even if legacy evidence says `BOUNDED_PASS`. For older GUP 8.0/8.1 evidence, legacy compatibility is preserved; start new tasks with v8.2 acceptance.

## New Executable Commands (v8.2)

1. `python3 scripts/4ndr0_converge.py init --root <repo> --contract <contract.json> --ledger <repo>/.4ndr0/ledger.json`: seal the mandatory criteria.
2. `python3 scripts/4ndr0_perf.py scan --root <repo> --output <repo>/.4ndr0/perf-hints.json`: optional *advisory-only* Python AST scan; never claim ISO conformity or verified speed from it.
3. `python3 scripts/4ndr0_perf.py run --root <repo> --contract <perf.contract.json> --output <repo>/.4ndr0/perf-result.json`: execute fingerprint-pinned paired benchmark. Exit `0` only on verified permitted wall-time behavior **and stdout equivalence**; `1` on defect/uncertain execution, `2` on invalid contract.
4. `python3 scripts/4ndr0_converge.py run --root <repo> --contract <contract.json> --ledger <repo>/.4ndr0/ledger.json --all`: actively run every executable criterion (including performance command); append hashed evidence. Evaluate with `evaluate` instead of `run` to inspect without executing.
5. `python3 scripts/4ndr0_converge.py evaluate --root <repo> --contract <contract.json> --ledger <repo>/.4ndr0/ledger.json --output <repo>/.4ndr0/status.json`: return `0` **only** when mandatory criteria are verified; otherwise `1`; evidence alteration or schema problems `2`. `verify` recomputes the chain and evidence hashes.
6. `python3 scripts/4ndr0_validate.py --root <repo> --evidence <gup-evidence.json> --execute-checks --convergence-contract <contract.json> --convergence-ledger <repo>/.4ndr0/ledger.json --output <gup-validation.json>`: v8.2 ties traditional GUP verification to actual acceptance completion.

Git hygiene: commit the acceptance contract as source; place generated ledger, lock, logs and benchmark reports under a separately ignored `.4ndr0/` directory (or explicitly stage immutable evidence in a separate audit commit), so application Git clean-worktree checks are meaningful. Disable incidental test artifacts such as `__pycache__` (`python3 -B`) or ignore them explicitly.

Note: example contracts in `examples/` are **templates only** and refer to project-specific files. Replace those paths and supply real performance fingerprints before execution. The controller's hash chain detects accidental post-record modification but is not a cryptographic signature against a malicious operator who can rewrite all files and hashes; commit/attest the final evidence separately.

## Bundled Executable Tooling

All protocol checks are implemented as deterministic Python 3 standard-library scripts in `scripts/`:

- `scripts/4ndr0_hash.py`: Lexically context-aware unit atomizer and comparator for Python (AST), JS/TS, Bash, JSON, and generic files. Includes a `<module_top_level>` unit so functionless files are never ignored, and outputs the exact manifest schema consumed by `4ndr0_validate.py`.
- `scripts/4ndr0_align.py`: File- and symbol-anchored bidirectional dependency/capability alignment validator. Rejects empty alignment data unless `zero_dependency_rationale` and `scope_files` are verified on disk, and checks every `path:symbol` reference in `--root`.
- `scripts/4ndr0_validate.py`: Proportionate validator that verifies Git commits via `git cat-file -e`, cross-checks manifests against live repository files, evaluates explicit `acceptance_criteria`, and outputs `CERTIFIED`, `BOUNDED_PASS`, or `FAIL_DEFECT`.
- `scripts/4ndr0_kit.py`: Content-addressed & lineage-adaptive builder and `P0-P7 + P1B + P1C + RED_CONTROL` throwaway-repo battery runner for self-verifying single-file bash kits (`Class F` First-Delivery, `Class U` Update, `Class H` Bounded Handoff).
- `scripts/4ndr0_report.py`: Mechanically derived, single-file, zero-external-request HTML round-record generator and pin-parity verifier.
- `scripts/4ndr0_perf.py`: Original workload-specific paired wall-time measurement with source fingerprints, alternating order, bootstrap uncertainty interval, output parity, and an explicitly partial Python AST static scanner.
- `scripts/4ndr0_converge.py`: Durable acceptance controller with serialized execution, immutable contract SHA, artifact-hash/round chain, strict completion exit codes, and narrow authority checkpoints.

## Step-by-Step Workflow

### Step 1: Select Tier, Establish Git Baseline, and Define Acceptance Criteria

1. Inspect the repository root (`git status --porcelain=v1`, `git rev-parse HEAD`). Initialize Git if absent and record the baseline commit SHA.
2. Choose the verification tier (`T0`, `T1`, `T2`, or `T3`) proportionate to the task's blast radius.
3. Define explicit, testable acceptance criteria (`file_exists`, `symbol_present`, `command_exit_zero`, or `unverified_external`) before or alongside implementation. **For v8.2 tasks, seal the stronger convergence contract before work starts; a legacy acceptance `unverified_external` does not satisfy mandatory runtime behavior.**

### Step 2: Implement Changes and Atomize Baseline vs. Candidate

1. Implement changes cleanly in focused commits while preserving baseline behavioral guarantees.
2. Extract and compare baseline and candidate unit manifests directly from Git revisions:

```bash
python3 scripts/4ndr0_hash.py --root /path/to/repo \
  --baseline-rev <BASE_SHA> \
  --candidate-rev HEAD \
  --baseline-manifest-out /tmp/base-manifest.json \
  --candidate-manifest-out /tmp/cand-manifest.json \
  --comparison-out /tmp/comparison.json
```

3. Review every `CHANGED`, `NEW`, and `MISSING` unit. Any `MISSING` unit is a `DEFECT` unless accompanied by `AUTHORIZED_REMOVAL` and `user_authorization: true`. If a changed unit's runtime equivalence cannot be tested in the current environment, mark its semantic verdict as `UNVERIFIED_BEHAVIOR` with a file-anchored static rationale rather than halting unrelated work.

### Step 3: Verify Bidirectional Alignment Against Real Files

1. Author `alignment.json` mapping each declared dependency or capability edge (`id`, `provider`, `consumer`) to concrete `path:symbol` anchors in `declaration_evidence`, `provider_evidence`, `consumer_evidence`, and `observation_evidence` (or provide `zero_dependency_rationale` + `scope_files` for standalone `T0` changes).
2. Run the alignment verifier:

```bash
python3 scripts/4ndr0_align.py /tmp/alignment.json --root /path/to/repo --output /tmp/align-report.json
```

### Step 4: Run Proportionate Validation and Evaluate Epistemic State

1. Assemble `evidence.json` conforming to `schemas/4ndr0-evidence.schema.json` and run `4ndr0_validate.py`:

```bash
python3 scripts/4ndr0_validate.py --root /path/to/repo \
  --evidence /tmp/evidence.json \
  --execute-checks \
  --output /tmp/validation-report.json
```

2. For `protocol_version: "8.2.0"`, also pass `--convergence-contract ... --convergence-ledger ...` as above. The older GUP status reports *evidence scope*, not task-completion eligibility; its v8.2 exit is nonzero while mandatory work remains open.
3. Interpret the validation status:
   - `CERTIFIED`: Zero defects, zero unverified claims, zero blocked targets. Ready for `CERTIFIED_RELEASE` (`Class U` or `Class F` kit).
   - `BOUNDED_PASS`: Zero defects on completed work, with one or more `UNVERIFIED` claims or scoped `BLOCKED` targets explicitly recorded in `bounded_claims`. Ready for `BOUNDED_HANDOFF` (`Class H` kit).
   - `FAIL_DEFECT`: One or more demonstrated defects exist. Fix the defect before claiming completion, or if delivering an emergency diagnostic checkpoint, disclose the exact `defects` list.

### Step 5: Path from Unfinished or Certified Work to Delivery (`T3` / Kit & Round Record)

Follow the three-rung delivery ladder based on current work completion:

1. **Rung 1 - `WIP_CHECKPOINT` (Unfinished Work in Progress):** Commit safe intermediate units to a working branch or use `delivery_mode: "WIP_CHECKPOINT"` to record verified vs. remaining targets in the evidence ledger.
2. **Rung 2 - `BOUNDED_HANDOFF` (`Class H` Kit):** When completed subtargets have zero demonstrated defects but runtime checks or mandatory targets remain `UNVERIFIED`/`BLOCKED`, build a diagnostic `Class H` kit with claims explicitly bounded. **The v8.2 convergence ledger stays incomplete and the validator/controller exits nonzero; no user acceptance or product certification is implied.**
3. **Rung 3 - `CERTIFIED_RELEASE` (`Class U` / `Class F` Kit):** When validation returns `CERTIFIED`, build a `Class U` (or `Class F`) kit (always passing `--key-file <primary-changed-file>` so `PIN_KEY_BASE_SHA` and `PIN_KEY_SHA` enable dynamic moving-HEAD and cross-lineage adaptation) and run the mandatory `P0-P7 + P1B + P1C + RED_CONTROL` battery and HTML round-record generator:

```bash
python3 scripts/4ndr0_kit.py --root /path/to/repo \
  --base <BASE_SHA> --tip HEAD \
  --suite <suite-name> --round <round-id> \
  --key-file <primary-changed-file> \
  --fingerprint-file <repo-anchor-file> \
  --gate-cmd "<test-command>" \
  --kit-class U --delivery-mode CERTIFIED_RELEASE --epistemic-status CERTIFIED \
  --run-battery \
  --output /tmp/update-<suite>-<round>.sh \
  --metadata-out /tmp/kit-meta.json

python3 scripts/4ndr0_report.py \
  --validation /tmp/validation-report.json \
  --kit-meta /tmp/kit-meta.json \
  --output /tmp/round-record-<round>.html
```

## Gotchas

- **Always pass `--key-file` to `4ndr0_kit.py`:** Passing `--key-file` embeds both `PIN_KEY_BASE_SHA` and `PIN_KEY_SHA`, allowing the generated kit to adapt seamlessly when the operator's repository `HEAD` has moved on other files or has an independent Git history (e.g. when the kit was built in a sandbox VM from uploaded files or applied to a monorepo subdirectory like `scr/`).
- **Never hand-write unit manifests or HTML pins:** `4ndr0_validate.py` recomputes live unit hashes from Git trees and rejects synthetic manifests whose hashes or unit IDs do not match the repository. `4ndr0_report.py` diffs every pin in the HTML against `kit-meta.json`.
- **File anchors must exist inside `--root`:** Every `evidence` string in `semantic_reviews`, `integration_closure`, `manifest_targets`, and `alignment.json` is parsed as `<rel_path>` or `<rel_path>:<symbol_substring>`. If a check cannot be anchored to a local file because it depends on an absent external runtime, prefix it with `runtime-unverified:<reason>` so the validator classifies it as `UNVERIFIED` (`BOUNDED_PASS`) rather than `DEFECT`.

## Source-backed design boundaries

Read `references/PERFORMANCE_DIRECTIVES.md` and the public crosswalk before performance reviews. ISO/IEC 5055:2021 measures structural weaknesses across four software quality characteristics, including performance efficiency; it does **not** specify universally optimal cache/layout/dispatch rules. Public source links are embedded in both references. v8.2 is independently authored and does not assert external ISO/CISQ certification or complete CWE detection. Always retain the original v8.1 Git-kit and adversarial properties when changing this protocol.
