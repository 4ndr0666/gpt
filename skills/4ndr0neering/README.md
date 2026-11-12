# 4ndr0neering v8.2.0 — Performance-First Convergence Directive

An installable `.skill` file containing the original performance directive `PF-001`–`PF-018`, the public CISQ performance CWE crosswalk (15 parents and 3 children), a source-fingerprinted paired wall-time benchmark runner, immutable stop-and-go acceptance ledger, v8.1 GUP compatibility tools, schemas, and adversarial tests.

## Install and use

Load `4ndr0neering_v8.2.0.skill` through the ChatGPT skill installation mechanism supported by your account, or unzip into a local skills directory and point your agent at `SKILL.md`. This package cannot install itself into your account.

Run locally from the extracted skill directory:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/4ndr0_skill_verify.py path/to/4ndr0neering_v8.2.0.skill
python3 scripts/4ndr0_perf.py run --root . \
  --contract examples/demo-performance.contract.json \
  --output /tmp/demo-performance-result.json
```

The demonstration uses shell process elapsed time only; it does not benchmark 4ndr0prompts or any real workload. For a real codebase, replace the template `examples/acceptance.contract.json`, supply actual test commands and baseline/candidate source fingerprints, seal the contract with `4ndr0_converge.py init`, then run and evaluate gates.

## Distinct assurance planes

`4ndr0_validate.py` checks Git-grounded unit/semantic evidence and delivery. The v8.2.0 controller checks whether **mandatory requirements actually passed**. Its exit code is nonzero if any required outcome is failed, pending, unverified, or blocked. Performance is a separate gate and never implied by structural simplification or self-verifying installation.

ISO/IEC 5055:2021 is a published standard for **automated source-code quality measures**. It does not prescribe a universal fastest design. The bundled original rulebook draws on public CISQ weakness categories and performance-aware design literature; it is **not** an ISO-conformity implementation. The scanner currently supports Python AST **hints**, not complete CWE detection across arbitrary languages. Runtime benchmark supports paired wall time, not p99, energy or memory certification.

## Explicit release limitations

This deliverable is a new **engineering skill**, not an application performance retrofit. It does not fix unresolved 4ndr0prompts HDL authority mismatches or execute its browser persistence test. Prior unresolved acceptance criteria remain unresolved until separately satisfied by actual application tests or a user decision.

Keep acceptance `contract.json` versioned. Add `.4ndr0/` and interpreter/test byproducts to the repository `.gitignore` before Git clean-worktree checks, or archive their hashes in a dedicated audit commit. These are operational examples, not a blanket instruction to ignore source or required test fixtures.
