# 4ndr0neering Performance-First Directives (PF-2026.1)

**Status:** Original, independently authored engineering directive. **Not** an ISO publication, implementation of ISO/IEC 5055, ISO certification, or an assertion that a pattern is globally fastest. Its only ISO relationship is the *conceptual distinction* between structural-weakness measurement and runtime performance behavior. Cite ISO/CISQ only when the actual mapping is supported by the official source; do not present this document as a verbatim reproduction of ISO rules.

## Precedence and execution

- `MUST` = release-gating procedural requirement, with evidence and explicit exceptions only when agreed in the acceptance contract.
- `SHOULD` = strong default, defeasible by profile/workload evidence; an unmeasured design preference is never a hard performance defect.
- `MAY` = a candidate optimization; test experimentally before adoption.
- Priority: **correctness, safety, security, and user-mandated semantics > explicit functional constraints > reproducible workload performance > structural simplicity > stylistic aesthetics**. Simplicity has independent maintenance value but does not establish runtime speed.
- States are **VERIFIED** (reproduced), **DEFECT** (demonstrated failed requirement), **UNVERIFIED** (inadequate/noisy coverage), **BLOCKED** (specific external/authority constraint). A plausible anti-pattern without reproducing impact is **HYPOTHESIS**, not DEFECT.

## 18 original numbered directives

| ID | Normative requirement | Detection and verification |
|---|---|---|
| PF-001 | **MUST** define the performance workload (representative input classes, distributions, data sizes, platform constraints, warm/cold state, concurrency, time budget). | Artifact: versioned workload contract with fingerprinted data and commands. |
| PF-002 | **MUST** preserve correctness, security and functional behavior before claiming a speedup. | Differential or golden tests; any mismatched output blocks performance PASS. |
| PF-003 | **MUST** record the baseline on the same declared host/workload and compare interleaved trials. | Paired A/B runs, warmups, source hashes, command hashes and environment. |
| PF-004 | **MUST** use explicit limits on regressions and absolute budgets; no universal threshold is inferred. | Workload-specific max regression, optional absolute deadline; separate tails/resource caps. |
| PF-005 | **MUST** keep evidence outcomes separate: green static scans, fast microbenchmarks, or clean installers do not certify end-to-end latency. | Independent correctness, static, performance, persistence and delivery gates. |
| PF-006 | **SHOULD** remove unnecessary work before selecting new abstractions or caching. | Profile expensive operations, algorithm complexity, repeated scans, extra serialization or rendering. |
| PF-007 | **SHOULD** minimize layers and dependencies only where the measured complexity/maintenance/latency tradeoff warrants it. | Record dependency reason; compare before/after startup, footprint, path length. |
| PF-008 | **SHOULD** expose simple direct hot-path operations to the optimizer where the runtime benefits. | Test dispatch tables/tagged unions/flat control flow **against** existing virtual dispatch or polymorphism. |
| PF-009 | **MAY** replace pointer-heavy object graphs with contiguous, compact, SoA/AoS or columnar representations based on access patterns. | Measure bytes touched, cache misses if available, allocation, traversal throughput. |
| PF-010 | **SHOULD** avoid redundant allocation and retained objects in hot paths without changing memory safety. | Allocation counts, GC pauses, peak live bytes, lifetime tests. |
| PF-011 | **SHOULD** batch remote calls, database operations, and disk I/O when semantics and consistency permit. | Query counts, network round trips, IO bytes, p95 latency, transaction correctness. |
| PF-012 | **SHOULD** test algorithmic complexity under growth in data size before optimizing instruction count. | Complexity curve, representative large data, worst-case inputs. |
| PF-013 | **MAY** add caches, pooling, prefetching or parallelism only after testing invalidation, footprint, contention, eviction, and cold-start cost. | Workload A/B including cold and contention cases; restore state after trials. |
| PF-014 | **MUST** isolate measured bottlenecks and use an explicit cost model: compute, memory, storage, network, contention or startup. | Profile/trace or bounded instrumented counters; do not infer hot paths from LOC. |
| PF-015 | **MUST** distinguish throughput, latency percentiles, startup, memory, energy and tail behavior; never present one metric as another. | Independent benchmark per acceptance budget; p95/p99 need adequate samples/load. |
| PF-016 | **MUST** confirm regression resistance across critical input classes and never trade away required accessibility/security/reliability. | Correctness and quality gates rerun after every optimization. |
| PF-017 | **SHOULD** prefer simple code and fewer dependencies at equal verified behavior/performance; **MUST NOT** blindly flatten code, ban interfaces, or duplicate logic. | Document why an abstraction benefits or costs the workload. DRY is not universally hostile to optimization. |
| PF-018 | **MUST** retain the slower fallback, rollback route, provenance, exact benchmark artifacts and outstanding uncertainties in the stop-and-go ledger. | Git-linked patch + lossless logs + next action; blocked hardware ≠ PASS. |

## Policy categories

1. `STRUCTURAL_RISK` (CISQ-inspired): known weakness families potentially detectable statically. Mapping to the public CWE list does **not** imply a tool implements ISO/IEC 5055 or finds every instance.
2. `MEASURED_REQUIREMENT`: a workload metric with explicit budget, environment and replayable benchmark. Only this can produce **verified runtime performance**.
3. `OPTIMIZATION_HYPOTHESIS`: data locality, simplified dispatch, batch processing, pooling, cache or removal of abstraction; rejected if slower or destabilizing.
4. `SIMPLICITY_CONSTRAINT`: suckless-style minimalism and explicitness, evaluated for maintainability and measured side-effects, not equivalent to peak throughput.

## Experiment protocol

1. Specify `baseline_command`, `candidate_command`, `fingerprints`, `workload_id`, `warmups >= 2`, `samples >= 7` and `max_regression_pct` in a contract. Explicitly fingerprint external datasets or pin their provenance when appropriate.
2. Run the instrument under the same workload with alternating AB / BA pairs. Record elapsed wall time and stdout digest; any difference in deterministic output is `DEFECT`, not a benchmark PASS.
3. Calculate a paired-bootstrap 95% interval on log duration ratios. **VERIFIED** only if its upper bound is no greater than the stated tolerance and any absolute median budget passes; **DEFECT** if its lower bound is above tolerance or the absolute budget fails; otherwise **UNVERIFIED_NOISE**. Intervals are sampling estimates, not strict guarantees.
4. Re-run after changes to the baseline, host, compiler flags, dataset, load or runtime. Never reuse a PASS from a different performance envelope.
5. Treat p95/p99, CPU cycles, energy, RSS, GC pressure and hardware counters as independent metrics. `4ndr0_perf.py` currently implements **wall-time paired samples** only, and does not certify these additional metrics; add suitable external counters and acceptance gates if required.
6. Diagnose noisy results (machine load, thermal scaling, caches, JIT, process startup), isolate the cause, rerun, and keep `UNVERIFIED` until conclusive.

## Anti-dogma controls

- A virtual call is not intrinsically a defect. A compiler can devirtualize; the operation may be outside hot paths; data layout and platform matter.
- A small function is not intrinsically slow: inlining and code size depend on compiler/runtime and workload.
- Contiguous layout is not universally faster (e.g. sparse access or costly copying); SoA versus AoS is workload-dependent.
- Reduced LOC is not a performance measurement. Removing necessary validation, instrumentation or error handling is forbidden.
- A cache can worsen latency by increasing memory pressure or invalidation overhead. No mandatory cache directive.
- Structural quality and runtime behavior are complementary, not substitutes; avoid calling a static scanner a benchmark.

## Source scope and non-affiliation

- ISO/IEC 5055:2021, official published abstract: https://www.iso.org/standard/80623.html and IEC catalog: https://webstore.iec.ch/en/publication/68831 . **Four source-code structural quality measures:** Security, Reliability, Performance Efficiency, Maintainability.
- CISQ public overview: https://www.it-cisq.org/standards/code-quality-standards/ ; public performance weaknesses: https://www.it-cisq.org/coding-rules/ . CISQ describes **15 parent** and **3 child** performance CWEs; our machine-readable listing is an *annotated public cross-reference*, not the ISO text.
- Suckless philosophy, simplicity/frugality: https://suckless.org/philosophy/ . This directive adopts simplicity as a design default, not a proven speedup.
- Casey Muratori, *“Clean” Code, Horrible Performance* (2023): https://www.computerenhance.com/p/clean-code-horrible-performance . His experiment supports testing flatter, data-aware designs in the demonstrated scenario, not universal performance claims.
