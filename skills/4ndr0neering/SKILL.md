---
name: 4ndr0neering
description: Unified, evidence-based engineering protocol and self-verifying delivery directive replacing golden-unit-protocol (GUP) and andr0666-engineering (SUK). Use when executing code changes, audits, refactoring, migrations, regression verification, or packaging work into self-verifying single-file update kits and HTML round records with executable file-tied checks, explicit acceptance criteria, defect vs. missing-evidence separation, and proportionate verification.
allowed-tools: execute_bash view_file write_to_file
---
# 4ndr0neering Unified Engineering Protocol (v8.0.0)

An evidence-backed software engineering, regression-prevention, and self-verifying delivery protocol that unifies and replaces `golden-unit-protocol` (GUP v7.0.2) and `andr0666-engineering` (SUK v1.2). It pairs executable validators tied to actual files on disk with proportionate verification tiers and a clear path from unfinished work to delivery.

## When to Use

- Executing feature implementation, bugfixes, refactoring, or repository migrations requiring zero silent regressions.
- Auditing codebases, verifying bidirectional dependency/capability alignment, or validating acceptance criteria against real files and test logs.
- Packaging completed or partially completed engineering rounds into deterministic, single-file self-verifying update kits (`update-<suite>-<round>.sh`) and self-contained HTML round-record pages.
- Replacing GUP or SUK workflows where missing runtime proof or blocked secondary targets must bound claims rather than halting unrelated work.

## Core Operational Principles

1. **Checks Tied to Actual Files:** Every unit manifest, semantic review, alignment edge, integration surface, and acceptance criterion must resolve to real files, AST/lexical symbols, Git objects, or executed command logs on disk. String-only placeholders (`"evidence": "ok"`) are rejected by the validator.
2. **Demonstrated Defect vs. Missing Evidence:** Never conflate a demonstrated defect with missing evidence. Use four distinct epistemic states:
   - `VERIFIED`: Checked against actual repository bytes, symbols, or executed command logs with zero errors.
   - `UNVERIFIED`: Cannot be conclusively tested in the current environment (for example, missing host hardware, external network service, or unrunnable GUI check). Bounds the claim without halting work.
   - `BLOCKED`: A specific target cannot proceed due to missing upstream input or user authorization. Scoped strictly to that target so unrelated targets proceed.
   - `DEFECT`: An invariant, file check, symbol check, unit superset guarantee, or test was evaluated and failed. Blocks delivery of the broken target until fixed or explicitly disclosed in a diagnostic handoff.
3. **Uncertainty Bounds Claims Without Stopping Unrelated Work:** When Target A is `VERIFIED` and Target B is `UNVERIFIED` or `BLOCKED`, complete Target A, record the exact boundary on Target B, and emit `BOUNDED_PASS` rather than halting the entire session or fabricating a pass.
4. **Proportionate Verification Tiers:** Match verification overhead to change blast radius instead of forcing heavyweight ceremony onto minor edits:
   - **Tier `T0` (Micro / Patch):** Single-file bugfix, config tweak, or pure helper (1-2 files, no new external dependencies). Requires `entry_points` and `tests` closure plus unit hash comparison on touched files.
   - **Tier `T1` (Module / Feature):** Multi-function or multi-file feature within an existing module boundary. Requires `entry_points`, `callers`, `providers`, `consumers`, and `tests` closure plus file-anchored alignment on touched modules.
   - **Tier `T2` (Cross-Cutting / Migration):** Architectural refactor, schema migration, or loader change. Requires all 9 integration surfaces (`entry_points`, `loaders`, `callers`, `providers`, `consumers`, `configuration_paths`, `install_migration_paths`, `tests`, `runtime_dependencies`) and full repository unit comparison.
   - **Tier `T3` (Release / Self-Verifying Kit Delivery):** Full `T2` verification plus deterministic single-file update kit (`4ndr0_kit.py`), automated `P0-P7 + RED_CONTROL` battery execution, and self-contained HTML round-record generation (`4ndr0_report.py`).
5. **Architectural Soundness (Gate 2 Directives):**
   - Declare a single paradigm per module; do not mix incompatible concurrency or DOM models.
   - Enforce explicit timeouts on all subprocesses and external I/O.
   - Bind temporary directories, containers, locks, and background workers to unconditional `finally` or POSIX `trap` cleanup.
   - Use EAFP (`try`/`except` specific exceptions) on data paths, and fail-closed precondition checks at trust boundaries (installers, kits, destructive Git operations).
   - Emit complete, runnable files with zero `TODO` stubs or ellipses.

## Bundled Executable Tooling

All protocol checks are implemented as deterministic Python 3 standard-library scripts in `scripts/`:

- `scripts/4ndr0_hash.py`: Lexically context-aware unit atomizer and comparator for Python (AST), JS/TS, Bash, JSON, and generic files. Includes a `<module_top_level>` unit so functionless files are never ignored, and outputs the exact manifest schema consumed by `4ndr0_validate.py`.
- `scripts/4ndr0_align.py`: File- and symbol-anchored bidirectional dependency/capability alignment validator. Rejects empty alignment data unless `zero_dependency_rationale` and `scope_files` are verified on disk, and checks every `path:symbol` reference in `--root`.
- `scripts/4ndr0_validate.py`: Proportionate validator that verifies Git commits via `git cat-file -e`, cross-checks manifests against live repository files, evaluates explicit `acceptance_criteria`, and outputs `CERTIFIED`, `BOUNDED_PASS`, or `FAIL_DEFECT`.
- `scripts/4ndr0_kit.py`: Deterministic builder and `P0-P7 + RED_CONTROL` throwaway-repo battery runner for self-verifying single-file bash kits (`Class F` First-Delivery, `Class U` Fast-Forward Update, `Class H` Bounded Handoff).
- `scripts/4ndr0_report.py`: Mechanically derived, single-file, zero-external-request HTML round-record generator and pin-parity verifier.

## Step-by-Step Workflow

### Step 1: Select Tier, Establish Git Baseline, and Define Acceptance Criteria

1. Inspect the repository root (`git status --porcelain=v1`, `git rev-parse HEAD`). Initialize Git if absent and record the baseline commit SHA.
2. Choose the verification tier (`T0`, `T1`, `T2`, or `T3`) proportionate to the task's blast radius.
3. Define explicit, testable acceptance criteria (`file_exists`, `symbol_present`, `command_exit_zero`, or `unverified_external`) before or alongside implementation.

### Step 2: Implement Changes and Atomize Baseline vs. Candidate

1. Implement changes cleanly in focused commits while preserving baseline behavioral guarantees.
2. Extract and compare baseline and candidate unit manifests directly from Git revisions:

```bash
python3 scripts/4ndr0_hash.py --root /path/to/repo   --baseline-rev <BASE_SHA>   --candidate-rev HEAD   --baseline-manifest-out /tmp/base-manifest.json   --candidate-manifest-out /tmp/cand-manifest.json   --comparison-out /tmp/comparison.json
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
python3 scripts/4ndr0_validate.py --root /path/to/repo   --evidence /tmp/evidence.json   --execute-checks   --output /tmp/validation-report.json
```

2. Interpret the validation status:
   - `CERTIFIED`: Zero defects, zero unverified claims, zero blocked targets. Ready for `CERTIFIED_RELEASE` (`Class U` or `Class F` kit).
   - `BOUNDED_PASS`: Zero defects on completed work, with one or more `UNVERIFIED` claims or scoped `BLOCKED` targets explicitly recorded in `bounded_claims`. Ready for `BOUNDED_HANDOFF` (`Class H` kit).
   - `FAIL_DEFECT`: One or more demonstrated defects exist. Fix the defect before claiming completion, or if delivering an emergency diagnostic checkpoint, disclose the exact `defects` list.

### Step 5: Path from Unfinished or Certified Work to Delivery (`T3` / Kit & Round Record)

Follow the three-rung delivery ladder based on current work completion:

1. **Rung 1 - `WIP_CHECKPOINT` (Unfinished Work in Progress):** Commit safe intermediate units to a working branch or use `delivery_mode: "WIP_CHECKPOINT"` to record verified vs. remaining targets in the evidence ledger.
2. **Rung 2 - `BOUNDED_HANDOFF` (`Class H` Kit):** When all completed targets have zero defects (`BOUNDED_PASS`) but some runtime checks or secondary targets remain `UNVERIFIED` or `BLOCKED`, build a `Class H` self-verifying handoff kit with `--delivery-mode BOUNDED_HANDOFF --epistemic-status BOUNDED_PASS`.
3. **Rung 3 - `CERTIFIED_RELEASE` (`Class U` / `Class F` Kit):** When validation returns `CERTIFIED`, build a `Class U` (or `Class F`) kit and run the mandatory `P0-P7 + RED_CONTROL` battery and HTML round-record generator:

```bash
python3 scripts/4ndr0_kit.py --root /path/to/repo   --base <BASE_SHA> --tip HEAD   --suite <suite-name> --round <round-id>   --key-file <primary-changed-file>   --fingerprint-file <repo-anchor-file>   --gate-cmd "<test-command>"   --kit-class U --delivery-mode CERTIFIED_RELEASE --epistemic-status CERTIFIED   --run-battery   --output /tmp/update-<suite>-<round>.sh   --metadata-out /tmp/kit-meta.json

python3 scripts/4ndr0_report.py   --validation /tmp/validation-report.json   --kit-meta /tmp/kit-meta.json   --output /tmp/round-record-<round>.html
```

## Gotchas

- **Never hand-write unit manifests or HTML pins:** `4ndr0_validate.py` recomputes live unit hashes from Git trees and rejects synthetic manifests whose hashes or unit IDs do not match the repository. `4ndr0_report.py` diffs every pin in the HTML against `kit-meta.json`.
- **File anchors must exist inside `--root`:** Every `evidence` string in `semantic_reviews`, `integration_closure`, `manifest_targets`, and `alignment.json` is parsed as `<rel_path>` or `<rel_path>:<symbol_substring>`. If a check cannot be anchored to a local file because it depends on an absent external runtime, prefix it with `runtime-unverified:<reason>` so the validator classifies it as `UNVERIFIED` (`BOUNDED_PASS`) rather than `DEFECT`.
- **Detailed critique and adversarial design reference:** See `references/CRITIQUE-AND-ADVERSARIAL-DESIGN.md` for the full forensic audit of GUP v7.0.2 and SUK v1.2 and the 8 adversarial attack vectors closed by this skill.
