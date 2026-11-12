# 4ndr0neering v8.2.0 — Source-grounded engineering and performance-first directive

## Scope

New installable skill, replacing the narrower v8.0/v8.1 workflow while retaining existing v8.1 Git-grounded unit validation, alignment, dynamic pin handling, update kits, and round-record tools. This work **does not** edit 4ndr0prompts itself, resolve its historical HDL authority conflicts, or run any real-origin browser storage test.

## Independent design and references

- **Structural weakness side:** Public CISQ performance list has 15 parent + 3 child CWEs, consistent with CISQ descriptions and the crosswalk in `references/CISQ_PUBLIC_CWE_CROSSWALK.json`. Original, conditional mappings point to `PF-001`–`PF-018`. The tool does NOT reproduce the ISO standard, implement a conformant ISO analysis, or cover all CWEs. Sources: https://www.it-cisq.org/coding-rules/ ; https://www.it-cisq.org/standards/code-quality-standards-performance-efficiency/
- **ISO boundary:** ISO/IEC 5055:2021 is an international *automated source code quality measures* standard across security, reliability, performance efficiency, and maintainability. It is not a language-agnostic universally fastest implementation directive. Sources: https://www.iso.org/standard/80623.html ; https://webstore.iec.ch/en/publication/68831 .
- **Simplicity baseline:** https://suckless.org/philosophy/ . Apply frugality/clarity as code-design preferences; do not assert lower LOC means lower latency.
- **Performance aware candidate patterns:** https://www.computerenhance.com/p/clean-code-horrible-performance . Muratori's experimental counterexample motivates workload-specific tests of dispatch and layout, not a mandatory blanket ban on OOP, DRY or abstraction.

## New checks and rule types

| Asset | Behavior | Confidence boundary |
|---|---|---|
| `references/PERFORMANCE_DIRECTIVES.md` | 18 numbered independently authored MUST/SHOULD/MAY rules | A proposed engineering directive, NOT ISO conformance |
| `references/CISQ_PUBLIC_CWE_CROSSWALK.json` | 18 public CWE refs, original risk descriptions and suggested conditional mitigations | Public cross-reference, not full proprietary normative text |
| `scripts/4ndr0_perf.py run` | Runs executable, source-fingerprinted AB/BA workload commands; requires output parity; uses a paired bootstrap confidence interval and declared regression budget | Paired **wall-time** for declared workload only; no automatic CPU/memory/p95/energy certification |
| `scripts/4ndr0_perf.py scan` | Python AST nested-loop and resource-call heuristics | `HINTS_ONLY`, no ISO/CWE detection claim; other languages not scanned |
| `scripts/4ndr0_converge.py` | Immutable mandatory acceptance contract, real command execution, SHA-linked ledger, evidence file hashes, serialized controller access, fail-closed completion status | SHA chain is not a signed attestation against malicious full-file rewriting |
| `scripts/4ndr0_validate.py` v8.2 gating | Requires contract + verified ledger for `protocol_version=8.2.0` and exits nonzero if required acceptance open | v8.0/v8.1 evidence behavior remains supported |
| `scripts/4ndr0_skill_verify.py` | Validates all archive members and file hashes; fails on member injection/tampering | Archive integrity, not publisher authenticity |

## Executed regression and adverse controls

1. **26/26 v8.2 unit and adversarial tests:** reproducible measured faster/slower workloads, output differences, source fingerprint tampering, statistical noise, scanner non-certification, contract immutability, consecutive mitigation rounds, evidence/event tampering, user/external blockers, waiver bypass attempts, and required/optional release separation.
2. **4/4 inherited v8.1 GUP tests:** unit atomizer, phantom commits/manifests, fake alignment/file symbols, full certified/partial workflow, `P0-P7 + P1B + P1C + RED_CONTROL` Git update-kit battery, HTML record parity.
3. **1/1 real v8.2 Git integration:** executable valid T0 source-backed comparison rejected with missing acceptance ledger; after real executable criterion and verified ledger, the same candidate received `CERTIFIED`, zero defects, and `task_complete=true`. A worktree-dirt issue induced by interpreter bytecode was detected and mitigated with `python -B`; final clean-worktree run passes.
4. **4/4 JSON schema definition checks** (Draft 2020-12) and **2/2 template schema validation checks**. 
5. **Paired demo benchmark:** real `sh` commands, 9 A/B pairs plus warmups, source-fingerprinted and stdout-equal; `VERIFIED` against the demo-only regression limit. It is an orchestration smoke test, not performance evidence for a user application.
6. **Package integrity:** all 25 content files covered by in-archive manifest; archive verified, extracted directory verified, and mutated `SKILL.md` rejected. The zip itself must be pinned by its externally published SHA-256.

## Remaining boundaries

- No universal language-specific static CWE detector is supplied; Python AST heuristics do not imply 18-CWE coverage.
- Benchmark only measures process wall time, with nonzero exit codes on noise or mismatched outputs; p95/p99, memory, CPU cycles, energy and capacity require separate gates if mandatory.
- The installer can only be installed by an eligible host/user action. No account-level skill installation was executed.
- Historical application gaps (HDL authority semantics, real-origin IndexedDB/localStorage reload) remain unchanged and must be evaluated as mandatory criteria when the new skill is next applied to 4ndr0prompts.
- External hardware, Firefox/Safari and workload transport were not tested during skill development.

**Disposition:** Installable, source-verified skill version 8.2.0. The claim is successful *skill implementation tests*, not ISO accreditation or certification of any downstream software project.
