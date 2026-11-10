# 4ndr0neering (v8.0.0)

> **Universal, evidence-based systems engineering protocol and self-verifying delivery directive.**  
> Unifies, hardens, and supersedes `golden-unit-protocol` (GUP v7.0.2) and `andr0666-engineering` (SUK v1.2) by coupling file-anchored verification and proportionate tiers with deterministic update kits and out-of-band HTML attestation records.

---

## 1. Why 4ndr0neering Exists

The combination of GUP v7.0.2 and SUK v1.2 suffered from a structural paradox:
- **Prose maximalism:** Strict prose rules (GUP §8 and Execution Order Step 2) halted work (`BLOCKED`) when an agent could not produce impossible static proof of behavioral supersets or execute unavailable host/hardware runtimes.
- **Validator vacuity:** Bundled scripts (`gup_validate.py`, `gup_alignment.py`) checked only string non-emptiness, silently returning `status: PASS` on nonexistent manifest files, phantom Git commits (`0000...`), empty alignment arrays, or fake test commands.
- **Delivery paralysis:** SUK v1.2 permitted no delivery if a worktree had partial work or deferred runtime gates, leaving agents no safe path to hand off unblocked progress.

**4ndr0neering closes this gap with four core design invariants:**
1. **Checks Tied to Actual Files:** Every manifest unit, alignment edge, and acceptance criterion verifies actual files, AST/lexical symbols, and command exit logs on disk.
2. **Defect vs. Missing-Evidence Separation:** Evaluates claims across four explicit epistemic states:
   - `VERIFIED`: Proven by file bytes, AST symbols, or executed test logs.
   - `UNVERIFIED`: Cannot be tested in the current environment (e.g., physical hardware, external API). Bounds claims without halting.
   - `BLOCKED`: A specific target awaits upstream authorization. Scoped strictly to that target.
   - `DEFECT`: A broken invariant or failing test. Halts certification of that target.
3. **Proportionate Verification Tiers:** Matches rigor to blast radius instead of forcing 9-surface ceremony onto micro-fixes:
   - `T0` (Micro / Patch): 1–2 files, unit hash comparison, entry points + tests closure.
   - `T1` (Module / Feature): Multi-file feature, file-anchored bidirectional alignment, callers/providers/consumers closure.
   - `T2` (Cross-Cutting / Migration): Full repository unit comparison, all 9 integration surfaces.
   - `T3` (Release / Delivery): Full `T2` + deterministic update kit + P0–P7/Red Control battery + HTML round record.
4. **Lawful Three-Rung Delivery:** Unfinished work can be packaged safely as a `WIP_CHECKPOINT` or `BOUNDED_HANDOFF` (`Class H` kit) with explicit `bounded_claims`, while certified work ships via `CERTIFIED_RELEASE` (`Class U` or `Class F` kit).

---

## 2. Repository Layout & Architecture

```text
skills/4ndr0neering/
├── SKILL.md                                 # Skill trigger metadata & operational directive
├── scripts/
│   ├── 4ndr0_hash.py                        # Context-aware unit atomizer (Python AST, JS/TS, Bash, JSON)
│   ├── 4ndr0_align.py                       # File- & symbol-anchored bidirectional alignment verifier
│   ├── 4ndr0_validate.py                    # Proportionate multi-tier validator & live Git cross-checker
│   ├── 4ndr0_kit.py                         # Deterministic update-kit builder & P0–P7/Red Control battery
│   └── 4ndr0_report.py                      # Self-contained zero-external-request HTML round-record builder
├── schemas/
│   ├── 4ndr0-evidence.schema.json           # JSON Schema for evidence validation
│   └── 4ndr0-alignment.schema.json          # JSON Schema for bidirectional alignment
├── references/
│   └── CRITIQUE-AND-ADVERSARIAL-DESIGN.md   # Complete forensic audit of GUP v7.0.2 & SUK v1.2
└── tests/
    └── test_4ndr0_suite.py                  # Unit, exploit-regression, and E2E battery tests
```

---

## 3. Bundled Executables & Usage

### 3.1 `4ndr0_hash.py` (Atomizer & Comparator)
Atomizes source code into named stable units using Python's `ast` module, a lexically context-aware JS/TS/Bash parser, or JSON key extractors.
- **Top-Level Protection:** Automatically synthesizes a `<module_top_level>` unit for module-scope statements, constants, and configs, preventing zero-unit blindness on functionless files.
- **Lexical Dispatch:** Inactive regions (`#` comments, quotes, regex literals, heredocs) are structurally inert; braces inside them cannot leak into parser state.

```bash
# Compare working tree or revision against baseline
python3 scripts/4ndr0_hash.py --root . \
  --baseline-rev <BASE_COMMIT> \
  --candidate-rev HEAD \
  --baseline-manifest-out /tmp/base-manifest.json \
  --candidate-manifest-out /tmp/cand-manifest.json \
  --comparison-out /tmp/comparison.json

# Run built-in lexical invariant battery
python3 scripts/4ndr0_hash.py --selftest
```

### 3.2 `4ndr0_align.py` (File-Anchored Alignment)
Verifies that every declared dependency or capability maps to an observed use, and that every observed dependency is declared.
- **Zero-Dependency Guard:** Rejects `declarations: []` and `observations: []` unless `zero_dependency_rationale` and non-empty `scope_files` exist and pass file verification.
- **Disk Anchoring:** Validates every `path:symbol` reference in `provider`, `consumer`, and `*_evidence` against actual files on disk.

```bash
python3 scripts/4ndr0_align.py /path/to/alignment.json \
  --root . \
  --strict-certified \
  --output /tmp/align-report.json
```

### 3.3 `4ndr0_validate.py` (Proportionate Validator)
The central evidence gate. Cross-checks commits via `git cat-file -e`, live-recomputes unit manifests from Git trees, evaluates explicit `acceptance_criteria`, and enforces integration closure according to the declared tier (`T0`–`T3`).

```bash
python3 scripts/4ndr0_validate.py --root . \
  --evidence /path/to/evidence.json \
  --execute-checks \
  --require-full-certification \
  --output /tmp/val-report.json
```

Status outcomes:
- `CERTIFIED`: 0 defects, 0 unverified claims, 0 blocked targets. Exits `0`.
- `BOUNDED_PASS`: 0 defects on completed work; unverified runtime checks or blocked targets recorded in `bounded_claims`. Exits `0` (or `1` under `--require-full-certification`).
- `FAIL_DEFECT`: One or more demonstrated defects. Exits `1`.

### 3.4 `4ndr0_kit.py` (Kit Builder & Battery Runner)
Builds a self-contained, single-file Bash update kit (`update-<suite>-<round>.sh`) embedding a compressed, base64-encoded Git bundle.
- **Concurrency & Stash Protection:** Enforces a `.git/kit.lock` mutex, verifies baseline commit identity, and preserves uncommitted work using scoped `git stash push --include-untracked` (never `--all`).
- **Battery Invariant:** With `--run-battery`, drives throwaway test repos through phases `P0`–`P7` plus a newline-anchored payload `RED_CONTROL` corruption test.

```bash
python3 scripts/4ndr0_kit.py --root . \
  --base <BASE_COMMIT> --tip HEAD \
  --suite my-project --round v1.0.0 \
  --key-file src/main.py --fingerprint-file package.json \
  --gate-cmd "pytest" \
  --kit-class U --delivery-mode CERTIFIED_RELEASE --epistemic-status CERTIFIED \
  --run-battery \
  --output /tmp/update-my-project-v1.sh \
  --metadata-out /tmp/kit-meta.json
```

### 3.5 `4ndr0_report.py` (HTML Round-Record Builder)
Emits an out-of-band, single-file HTML evidence attestation page using dark terminal design tokens.
- **Zero External Requests:** All styles are inline; no CDN fonts, scripts, or external images.
- **Pin Parity:** Mechanically derives all pins (`PIN_KIT_SHA`, `PIN_BUNDLE_SHA`, `PIN_TIP_TREE`) directly from validator and kit metadata JSON, running a self-containment and pin-parity audit before output.

```bash
python3 scripts/4ndr0_report.py \
  --validation /tmp/val-report.json \
  --kit-meta /tmp/kit-meta.json \
  --output /tmp/round-record-v1.html
```

---

## 4. End-to-End Workflow

```text
[Select Tier: T0 - T3]
         │
         ▼
[Define Acceptance Criteria] ──► (file_exists | symbol_present | command_exit_zero | unverified_external)
         │
         ▼
[Implement & Commit Range]   ──► Clean atomic Git commits
         │
         ▼
[4ndr0_hash.py]              ──► Extract baseline & candidate unit manifests; compare
         │
         ▼
[4ndr0_align.py]             ──► Verify bidirectional alignment against files on disk
         │
         ▼
[4ndr0_validate.py]          ──► Epistemic verdict: CERTIFIED, BOUNDED_PASS, or FAIL_DEFECT
         │
    ┌────┴────────────────────────┐
    ▼                             ▼
(CERTIFIED)                  (BOUNDED_PASS)
    │                             │
[4ndr0_kit.py (Class U)]     [4ndr0_kit.py (Class H)]
    │                             │
    └──────────────┬──────────────┘
                   ▼
         [Run P0-P7 Battery]
                   │
                   ▼
         [4ndr0_report.py]   ──► Out-of-band HTML round record
                   │
                   ▼
         [Operator: git push]
```

---

## 5. Applying an Update Kit (`update-<suite>-<round>.sh`)

The self-verifying update kit requires **one command and zero operator decisions**:

```bash
bash update-<suite>-<round>.sh /path/to/your/repo
```

1. **Self-Verification (G0):** Prints its SHA-256 hash. Compare this with the published hash on the HTML round-record page.
2. **Repository & Baseline Check (G1–G2):** Resolves the target repository and checks `HEAD == PIN_BASE`. If your branch has newer unpushed commits, it fails closed with `DO NOT FORCE`.
3. **WIP Preservation (G2.5):** If uncommitted changes exist, stashes them with `--include-untracked` and writes restore instructions to `.git/kit-backups/<timestamp>/`.
4. **Fast-Forward Merge (G3):** Verifies bundle pins and fast-forwards your branch to `PIN_TIP`.
5. **Exactness Proof & Gate (G4):** Asserts tree hash matches `PIN_TIP_TREE` and executes the configured test gate.
6. **Result Line:** Prints `KIT RESULT: GREEN`. The single remaining step belongs to you:
   ```bash
   git push
   ```
