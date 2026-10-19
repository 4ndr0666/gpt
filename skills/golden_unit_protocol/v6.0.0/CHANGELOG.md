# Changelog

## 6.0.0 — 2026-10-15

### Added
- Large-radius repository mitigation before strict certification: trace entry points, loaders, callers, providers, deployment paths, tests, and runtime dependencies before narrow fixes.
- Mandatory integration-closure review for dead code, disconnected helpers, orphaned references, inert configuration, stubs, TODO/FIXME placeholders, and untested migration/deployment paths. The final validator hard-fails when any required integration surface or manifest target is omitted or unresolved.
- Canonical-source enforcement: active configuration must follow the explicitly declared canonical format; legacy files are not accepted as operational preservation merely because they were archived.
- Explicit baseline feature inventory and behavioral superset matrix, including edge cases, error paths, rollback, idempotency, and previously fixed defects.
- Iterative manifest-driven mitigation: broad-radius pass, target-scope rounds, affected integration tests, then final GUP scrutiny.
- Fail-closed inventory and validators with exact protocol validation, duplicate identity rejection, evidence-backed provider bindings, strict diff/review reconciliation, and durable atomic evidence output.
- Worktree cleanliness, exact commit identity, tracked-file hashes, untracked paths, and tracked diff fingerprint in repository inventory.

### Fixed
- Closed the certification-by-proxy path where a narrow passing gate could be mistaken for repository-wide operational completeness.
- Prevented any non-zero hash-script status from being accepted unless it is exactly explained by reviewed MISSING units.
- Required explicit user authorization and rationale for every removed baseline unit.
- Rejected phantom semantic review records, duplicate diff identities, invalid alignment results, and removal verdicts applied to non-missing units.
- Made inventory reject missing tracked files and dirty worktrees by default; `--allow-dirty` is an explicit non-certification capture mode.
- Made atomic output use unique same-directory temporary files, fsync before replace, and unconditional cleanup.
- Added executable package regression tests for atomizer invariants, deterministic/dirty inventory behavior, bidirectional alignment rejection, authorized removal review, omitted integration-surface rejection, durable evidence emission, and stale-inventory rejection.

### Compatibility
- Retained the v5.3 lexical atomizer behavior and self-test battery while advancing the protocol identity and atomizer package version.
- No baseline capability is intentionally removed by this protocol revision.
