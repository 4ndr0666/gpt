# Golden Unit Protocol v5.2 — Skill Package Reference

## 1. Purpose

This directory contains the complete **Golden Unit Protocol (GUP) v5.2** skill package.

GUP is a strict regression-prevention, architectural-integrity, and production-readiness protocol for revising existing artifacts without allowing behavioral drift, feature loss, hidden failure, duplicated authority, or incomplete cleanup.

Version 5.2 is the successor to the supplied GUP v5.0 skill package. It preserves the original GUP machinery and incorporates the validated engineering controls established during the repository audit.

The package also bundles **GUP-O.M.A. (Omnipresent Machine Assurance)** as its machine-level assurance extension.

---

## 2. Package Architecture

```text
gup-v5.2.skill
├── SKILL.md
├── VERSION
├── CHANGELOG.md
├── golden_unit_hash.py
├── scripts/
│   └── golden_unit_hash.py
└── gup-oma/
    ├── SKILL.md
    ├── oma_assurance.py
    └── scripts/
        └── oma_assurance.py
```

### Core

`SKILL.md` is the authoritative GUP v5.2 protocol.

`golden_unit_hash.py` is the executable Golden-Unit hashing/classification engine.

`scripts/golden_unit_hash.py` is the mirrored executable copy retained as part of the package structure inherited from the original skill.

### Bundled Extension

`gup-oma/SKILL.md` defines the O.M.A. extension.

`gup-oma/oma_assurance.py` provides the executable O.M.A. assurance harness.

`gup-oma/scripts/oma_assurance.py` is the mirrored O.M.A. executable copy.

---

## 3. Version Lineage

| Component | Version | Role |
|---|---:|---|
| Golden Unit Protocol | **v5.2** | Core protocol |
| Golden Unit Hash Engine | **v2.1.0** | Core executable |
| GUP-O.M.A. | **v1.1.0** | Bundled machine-assurance extension |

The original supplied skill was GUP v5.0. This package is an actual protocol revision, not a rename of O.M.A.

O.M.A. remains logically subordinate to GUP: repository certification is a prerequisite for machine-level assurance.

---

## 4. What v5.2 Adds

GUP v5.2 incorporates the controls proven necessary during the audit:

- Repository-wide integrity boundaries in addition to named-unit verification.
- Explicit feature-preservation and behavioral-superset enforcement.
- Validated feature loss classified as **CRITICAL**.
- Explicit failure propagation rather than masked failures or unsafe defaults.
- Transaction-local cleanup ownership.
- Atomic replacement and rollback requirements.
- Idempotence requirements.
- A formal non-mutating validation/dry-run boundary.
- Legacy and duplicate implementation detection.
- Installer fail-closed requirements.
- Runtime, dependency, reachability, and lifecycle verification.
- Evidence retention and integrity requirements.
- Change-based revalidation.
- Explicit separation between repository certification and machine certification.
- Bounded machine assurance through GUP-O.M.A.
- Prohibition on fabricated compatibility or certification claims.

These controls are additive to the original GUP architecture; they are not intended to weaken or bypass existing gates.

---

## 5. Golden-Unit Engine

The core executable classifies named units using four states:

```text
MISSING
UNCHANGED
CHANGED
NEW
```

The engine supports the source-unit mechanisms defined by the GUP protocol, including Python AST analysis, conservative JavaScript/TypeScript handling, and manual JSON units.

### Important semantics

- `MISSING` is a hard failure.
- `CHANGED` requires architectural/behavioral review.
- `NEW` is surfaced for review and is not silently treated as equivalent to an existing unit.
- Duplicate stable unit identities are rejected rather than silently overwritten.
- Hashing is not a substitute for semantic review or the architectural gate.

The hash engine therefore acts as a deterministic evidence component, not as a claim that textual or structural identity alone proves correctness.

---

## 6. GUP Execution Model

GUP v5.2 follows the established multi-stage model:

```text
Baseline
   │
   ▼
Inventory / Unit Discovery
   │
   ▼
Golden-Unit Classification
   │
   ▼
Architectural / Behavioral Review
   │
   ▼
Implementation
   │
   ▼
Failure / Transaction / Cleanup Review
   │
   ▼
Regression + Runtime Verification
   │
   ▼
Feature-Superset Verification
   │
   ▼
Certification
   │
   └──────────────► O.M.A. machine assurance
```

A passing hash comparison does not authorize a change by itself. All required GUP gates remain authoritative.

---

## 7. Engineering Doctrine

The package operates under the following principles.

### Blind Execution

Generated or modified code is treated as potentially fragile until exercised.

### EAFP

Prefer robust execution with explicit failure propagation over brittle precondition choreography that can race or become stale.

### No Failure Masking

Do not convert unrecoverable errors into success, empty values, generic fallbacks, or suppressed output.

A tolerated failure must be explicitly classified as normal, bounded behavior.

### Atomicity

State-changing operations must either complete as a coherent transaction or restore the prior state.

### Idempotence

Repeating a successful operation must not progressively corrupt, duplicate, or degrade state.

### Cleanup

Temporary state, traps, locks, processes, mounts, and staging artifacts must have deterministic ownership and unconditional cleanup.

### Single Authority

Duplicate implementations, stale compatibility paths, shadowed functions, and competing configuration authorities are defects unless explicitly justified.

### No Placeholders

No TODO/FIXME/stub/placeholder implementation may be accepted as completed production work.

---

## 8. Baseline and Feature Preservation

Every revision of an established artifact requires an explicit baseline.

The baseline defines the feature and behavior set that must survive the revision.

The required relation is:

```text
Current capability set ⊇ Stable baseline capability set
```

A validated loss of an existing capability is **CRITICAL** unless explicitly authorized as a deliberate breaking change with its corresponding protocol treatment.

The protocol therefore distinguishes:

- implementation changes,
- intentional additions,
- refactors,
- behavioral changes,
- regressions,
- feature loss,
- unreachable capabilities,
- and undocumented authority changes.

---

## 9. Repository vs. Machine Certification

GUP v5.2 makes a strict distinction:

### Repository certification

Answers:

> Does the artifact satisfy its defined integrity, regression, architectural, transactional, lifecycle, installer, and capability-preservation requirements?

### Machine certification

Answers:

> Has the artifact actually been exercised and reproduced on a declared machine/support class?

A repository can be GUP-certified without being universally certified across all hardware.

This distinction prevents unsupported claims such as "works on every Arch machine" when only one machine or one hardware class has been exercised.

---

# 10. GUP-O.M.A.

O.M.A. is bundled because repository correctness and machine correctness are related but distinct assurance problems.

**O.M.A. means Omnipresent Machine Assurance.**

Its governing rule is:

> Never certify what was not defined, exercised, observed, recovered, and reproduced.

O.M.A. does not make an unbounded universal defect-free claim possible. It establishes evidence-backed certification over an explicitly declared Arch Linux support envelope.

---

## 11. O.M.A. Support Envelope

A machine certification envelope may include:

- Architecture.
- Arch Linux release state.
- Kernel versions.
- Firmware/UEFI state.
- CPU class.
- GPU and driver class.
- Display topology.
- Wayland compositor/session.
- Desktop/session environment.
- Package state.
- Network state.
- Filesystem/storage conditions.
- Locale/timezone.
- Power and reboot behavior.
- Lifecycle and concurrency conditions.
- Recovery behavior.

A certification record must identify the exercised envelope rather than extrapolating beyond it.

---

## 12. O.M.A. Certification Levels

| Level | Meaning |
|---|---|
| **O.M.A.-0** | Envelope declared |
| **O.M.A.-1** | Matrix verified |
| **O.M.A.-2** | Adversarial verification completed |
| **O.M.A.-3** | Reproducibility independently verified |
| **O.M.A.-4** | Production certification |

O.M.A.-4 must never be inferred merely because GUP passed.

---

## 13. O.M.A. Executable Harness

The bundled executable is intended to collect machine evidence and enforce the machine-side assurance boundary.

Typical operations include:

```bash
python3 gup-oma/oma_assurance.py --help
```

Use the executable's current `--help` output as the authoritative command-line interface if options are extended in a later package revision.

The harness is designed to preserve evidence even when an individual probe fails, while ensuring that probe failure cannot be silently converted into certification success.

---

## 14. Recommended Use With an Arch Repository

For a live Arch repository update:

1. Establish the stable repository baseline.
2. Run the complete GUP verification process.
3. Inspect and preserve the baseline commit/reference.
4. Perform non-mutating validation first.
5. Apply the controlled change.
6. Verify transactional cleanup and rollback semantics.
7. Re-run Golden Units.
8. Verify capability superset.
9. Verify runtime/reachability/lifecycle behavior.
10. Collect O.M.A. machine evidence.
11. Record the exact machine, kernel, driver, session, package, and repository state.
12. Reproduce on additional declared machine classes where required.
13. Do not claim a higher O.M.A. level than the evidence supports.

---

## 15. Artifact Integrity Expectations

The `.skill` package is itself a production artifact.

Before distributing a new version:

- Validate ZIP/package integrity.
- Verify required files exist.
- Validate YAML frontmatter.
- Run syntax/compile checks on executable components.
- Verify mirrored executable copies remain synchronized.
- Exercise version reporting.
- Exercise intentional failure paths.
- Check for duplicate or orphaned protocol components.
- Verify the changelog and version metadata agree.
- Confirm no placeholders or temporary development artifacts remain.

---

## 16. Updating the Skill

A future GUP revision should not be produced by editing only the visible Markdown.

The revision process is:

```text
1. Identify the current authoritative package.
2. Preserve the existing feature set.
3. Establish the previous version as baseline.
4. Identify intended protocol changes.
5. Implement executable changes where the protocol requires automation.
6. Update companion documentation.
7. Run the GUP verification gates.
8. Verify the capability superset.
9. Validate package structure.
10. Re-run executable negative-path tests.
11. Update VERSION and CHANGELOG.
12. Produce a new .skill package.
13. Independently inspect the final package.
```

A version number must correspond to a real protocol revision. Do not increment the version merely to rename or repack an unchanged artifact.

---

## 17. Change Classification

At minimum, changes should be classified as:

- **NEW** — new capability.
- **CHANGED** — existing behavior or implementation materially changed.
- **UNCHANGED** — preserved.
- **MISSING** — baseline capability absent.
- **CRITICAL** — validated regression, feature loss, unsafe failure masking, broken cleanup, or other release-blocking defect.

`MISSING` and validated critical regressions must block certification.

---

## 18. Certification Evidence

A meaningful certification record should contain enough information for another operator to determine:

- What artifact was tested.
- Which version was tested.
- Which baseline was used.
- Which machine/support class was tested.
- Which kernel/firmware/driver/session state existed.
- Which tests were executed.
- Which tests passed or failed.
- What mutations were permitted.
- What recovery was exercised.
- What evidence was retained.
- Whether reproduction occurred.
- Which certification level is actually justified.

Evidence must be reproducible and attributable to the tested state.

---

## 19. Safety Boundary

The protocol does not authorize destructive testing on an operator's primary machine merely to obtain a higher certification level.

Destructive fault injection, power-loss simulation, recovery tests, and similar adversarial operations require an explicitly provisioned disposable/recovery environment.

A live production workstation may be used for non-destructive validation and ordinary deployment verification, but that does not make it an acceptable target for arbitrary destructive experiments.

---

## 20. Universal-Certification Constraint

No finite test matrix can mathematically prove defect-free operation over an unbounded and continuously changing universe of Arch hardware, firmware, kernels, drivers, packages, displays, peripherals, and user environments.

Accordingly:

```text
Universal claim
    ↓
Unsupported

Bounded declared support envelope
    ↓
Exercised + observed + recovered + reproduced
    ↓
Evidence-backed certification
```

The correct objective is therefore **bounded, reproducible assurance**, not an unverifiable universal guarantee.

---

## 21. Relationship to the Repository Audit

This package was produced as the next GUP revision following a production-readiness audit of an Arch Linux Hyprland repository.

The audit established the need for:

- strict baseline comparison,
- feature-superset verification,
- removal of legacy duplicate implementations,
- hardened transaction boundaries,
- explicit process lifecycle handling,
- installer fail-closed behavior,
- non-mutating dry-run validation,
- runtime/reachability verification,
- evidence retention,
- and machine-level assurance.

Those findings informed GUP v5.2 and the bundled O.M.A. extension.

The package itself does **not** constitute certification of any particular repository or machine. It is the protocol and executable tooling used to perform that certification.

---

## 22. Future Reference

When this directory is used by another operator or future revision:

- Treat `SKILL.md` as the GUP protocol authority.
- Treat `VERSION` as the package version authority.
- Treat `CHANGELOG.md` as the revision-history authority.
- Treat the executable scripts as operational components, not documentation examples.
- Treat `gup-oma/` as the bundled machine-assurance extension.
- Preserve the distinction between repository certification and machine certification.
- Never infer certification from the existence of the package.
- Never silently weaken a gate to make a failing artifact pass.
- Never claim an environment was tested when it was not.

---

## 23. Prime Directive

> **Never certify what was not defined, exercised, observed, recovered, and reproduced.**
