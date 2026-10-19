---
name: 4NDR0666-engineering
version: 1.0.0
description: Construct, verify, and deliver self-verifying single-file update kits — a universal, zero-prior-knowledge specification for packaging a certified commit range into ONE file that applies itself with ONE command, ZERO operator decisions, fail-closed behavior, embedded payloads, multi-layer integrity pins, idempotent re-runs, and a mandatory pre-delivery battery.
allowed-tools: vm_shell
---

# THE SELF-VERIFYING UPDATE-KIT SPECIFICATION (SUK v1.0)
### Universal single-file delivery of certified change ranges — construction, verification, battery, and delivery law

**Classification:** UNIVERSAL ENGINEERING SPECIFICATION & PROMPT
**Enforcement:** STRICT / MANDATORY — every clause is load-bearing; deviation is a defect
**Scope:** Any git-governed repository whose work is certified by a local gate
(`npm run check`-class verification) and delivered to a human operator who
applies it to their own clone. Applies to the kit AUTHOR (you, the executor)
and to the kit BATTERY you must build before delivery.
**Intended reader:** an engineer or AI executor with ZERO prior knowledge of
any specific repository, lineage, or prior conversation. Everything required
is defined or derivable from this document plus the repository you point it
at.
**Field provenance:** distilled from a 10-round delivery lineage in which
loose-file delivery failed repeatedly (ambiguity, staleness, missing
authorization records, operator misinterpretation) and kit delivery
succeeded 100% of the time it was actually tested — including a 39-check
battery, a wire-download end-to-end execution, and a re-run idempotence
proof on a real certified tree.

---

## PART 0 — WHY THIS ARTIFACT CLASS EXISTS (the field record)

Between two parties — an EXECUTOR (agent/engineer who produces certified
work as local commits, never pushing) and an OPERATOR (the human who owns
the remote; their push is canon) — every historical failure of delivery
reduces to one of seven wounds:

1. **The placeholder wound.** Instructions like `git pull <downloaded>`
   demand interpretation. The operator asks "which git stash?", guesses
   wrong, or stalls. Where ambiguity can live, error will.
2. **The unit wound.** A certified change is usually not one file — the
   authorization records ride `tools/`, the inventory rides generated JSON,
   the docs regenerate. Delivering the headline file alone produces a tree
   that FAILS the operator's own gate, and the operator cannot tell a file
   defect from a missing-record defect. **The lawful unit of delivery is the
   COMMIT RANGE.**
3. **The split wound.** "Here is a bundle, here is a patch, here is a
   checksum" is three downloads, three paths, and three chances to mismatch.
4. **The trust wound.** The operator has no way to verify that bytes off the
   wire are the bytes the executor certified.
5. **The side-effect wound.** Applying an update to a tree with uncommitted
   WIP can destroy the operator's work (the `git stash --all` landmine
   sweeps ignored files like `node_modules`; a bare `git stash` on a dirty
   tree leaves the operator unsure what happened).
6. **The environment wound.** The operator may lack node, may run from an
   unexpected directory, may re-run the update after it already applied.
7. **The idempotence wound.** An update that half-applies or that damages
   the tree on re-run converts a success into a support incident.

The self-verifying update kit closes all seven simultaneously:

> **ONE file. ONE command. ZERO decisions.**
> The kit locates the repo, proves its own integrity, preserves the
> operator's WIP, applies the exact certified commit range as a true
> fast-forward, re-proves the result by content hash, runs the full
> certification gate, and reports the single remaining step — `git push` —
> which belongs to the operator alone.

---

## PART I — THE LAW (axioms; violation of any = the kit is defective)

**A1 · One file, one command, zero decisions.** The operator's total
interaction is: download one file, run one command, read the output, push
when told to. Every decision the kit needs is made BY THE KIT.

**A2 · The kit never trusts itself blindly.** Every layer of the kit — its
payload block, its decoded payload, its git semantics — is pinned by a
content hash, and at least one pin must be verifiable OUT OF BAND (on the
delivery page, committed somewhere the operator already trusts).

**A3 · Fail closed, always.** Any precondition that does not hold → the kit
stops, tells the operator EXACTLY what to do next (with copy-paste syntax),
and touches nothing. A failed kit must leave the repo byte-identical to how
it found it, except for its backup directory inside `.git/` (which git
status never shows).

**A4 · The law rides the commits.** If the round's authorization records
live in `tools/` or generated ledgers, they ride the payload. Never promise
that a loose file will pass the operator's gate when the gate reads ledgers.

**A5 · Idempotence is mandatory.** Re-running an applied kit must be GREEN
(re-verify only), never an error, never a second application. A crash at
ANY point inside the kit must leave a state the same kit can recover from
on re-run.

**A6 · The operator's push is canon; the kit NEVER pushes.** No network
mutation of the remote, ever, under any condition. The kit's final line
HANDS the push to the operator as the single remaining step.

**A7 · No untested kit ships.** The battery (Part V) is a precondition of
delivery, not an accessory. A kit whose battery has not run green on all
phases does not leave the building.

**A8 · Operator-facing text contains zero placeholders.** No
`<downloaded>`, no `<path>`, no `as appropriate`. If a value is unknown at
authoring time, the KIT resolves it at runtime — or fails closed printing
the exact re-run command with the value filled in from the runtime context.
(Exception: THIS spec is executor-facing and parameterizes freely — the
anti-placeholder law binds what the OPERATOR sees.)

**A9 · Everything the kit prints is either a fact it just verified, or an
instruction executable verbatim.** No narrative, no guesses, no
"you may want to".

**A10 · The kit is deterministic output of a persisted builder.** Same
inputs → byte-identical kit. The builder script is saved next to the
round's other scripts; the kit is never hand-edited after pins are
computed.

---

## PART II — THE ARTIFACT CONTRACT (what a compliant kit IS)

### II.1 Form

- A single `#!/usr/bin/env bash` file, `set -euo pipefail`, named
  `update-<suite>-<round>.sh` (the operator's own naming convention —
  discover it from the repo's delivery history and follow it).
- Two zones, in order:
  1. **SCRIPT ZONE** — the logic (typically 150–250 lines).
  2. **PAYLOAD ZONE** — begins AFTER the script's final `exit 0`, delimited
     by exact anchor lines `#__PAYLOAD_BEGIN__` and `#__PAYLOAD_END__` at
     column 0. The zone between the anchors is the payload, base64, wrapped
     at 76 columns, one trailing newline.
- The payload is the round's **git bundle**: `git bundle create
  <file> <base>..<tip>` — gzipped at max compression, then base64.
- Why embedded: applying the round must require **zero network downloads**
  beyond the kit itself (the operator may be offline; a second download is
  a second integrity surface and a second ambiguity).

### II.2 The mandatory header block (comment banner, top of file)

```
WHAT IT DOES — one paragraph: base -> tip, what the round is, what runs
USAGE — the exact command(s), including the optional path argument
SAFETY — WIP preservation, fail-closed, re-run safe, pins verified first
AFTER IT PRINTS THE GREEN RESULT LINE: git push
```

The header is part of the contract: an operator who reads ONLY the header
must know the full behavior and the full recovery story.

### II.3 The pin table (SCRIPT ZONE constants; every one mandatory)

| Pin | Meaning | Verified in |
|---|---|---|
| `PIN_BASE` | the full 40-char sha of the operator's pushed baseline the round is anchored to | G2 (HEAD match) + G3 (bundle verify output) |
| `PIN_TIP` | full sha of the round's tip commit | G2 (already-applied detection), G3 (post-merge HEAD), bundle list-heads |
| `PIN_TIP_TREE` | the TREE hash of `PIN_TIP^{tree}` — the certified content, independent of commit metadata | G4 |
| `PIN_BUNDLE_SHA` | sha256 of the decoded bundle file | G3 |
| `PIN_PAYLOAD_SHA` | sha256 of the EXACT bytes the marker-extraction produces (the b64 block as sed will slice it, byte-for-byte, including its final newline) | G3 |
| `PIN_<KEY>_SHA` | sha256 of any round-critical file the operator cares about (e.g. the canon script the round was about) | G4 |
| `KIT_SELF` | resolved absolute path of the kit itself | computed before any `cd` |

**The payload-pin subtlety (this exact defect class exists in the field):**
the pin must be computed over the bytes BETWEEN the anchors as the kit's
own `sed -n '/^#__PAYLOAD_BEGIN__$/,/^#__PAYLOAD_END__$/p' | sed '1d;$d'`
extraction yields them — not over the pre-wrap base64, not over the gzip
stream. Author the builder to derive the payload bytes the same way the
kit extracts them (Part IV), or the kit fails its own G3 on first run.

### II.4 Out-of-band pins (delivery-side, not in the kit)

The kit's own sha256 is printed on the delivery page (Part VIII) and —
where the channel allows — in the delivery message. This is the
chain-of-trust head: everything else the kit verifies descends from the
operator's decision to trust that one published hash.

### II.5 Runtime contract

- **No writes outside**: the repo's `.git/` (backup dir, temp branch) and
  the OS temp dir (payload staging). Zero writes to the worktree outside
  the merge itself.
- **No network**: the payload is embedded; the only network act the kit may
  perform is `npm install` IF node_modules is absent AND the gate requires
  it — and that path must be disclosed in the header and skippable (node
  absent → defer, II.7).
- **Traps**: `trap cleanup EXIT` removes the temp dir and deletes the
  incoming temp branch (`|| true` — cleanup must never mask the exit code).

### II.6 Exit codes

- `0` with `KIT RESULT: GREEN` (or `GREEN (already applied …)`): success.
- `1` with `[KIT-FAIL] <reason>` on stderr plus the fixed line "Nothing was
  left half-applied. Fix the above and re-run this kit.": every failure
  path exits through the SAME fail function. No other exit codes, no naked
  `exit`, no fall-through past G5 (a kit that falls into its payload
  block after G5 prints garbage errors — this exact defect shipped once
  and was caught by the battery: `exit 0` BEFORE `#__PAYLOAD_BEGIN__` is
  mandatory).

### II.7 Environment tolerance

- Requires: bash, git, sha256sum, base64, gunzip, sed, date — feature-detect
  all in G0 and fail closed naming the missing tool and the install act.
- node/npm OPTIONAL: absent → apply + hash-verify now, DEFER the gate,
  print the exact deferred commands in the GREEN line itself.
- The kit must run correctly when invoked from ANY working directory (the
  operator will run it from Downloads), with a path-bearing filename, with
  spaces in the repo path, and when renamed.

---

## PART III — THE PHASE ARCHITECTURE (G0 → G5)

Phases are strictly ordered. Each phase states ENTRY CONDITIONS, ACTIONS,
and FAILURE SEMANTICS. Phase numbering is part of the operator's existing
kit convention — adopt it, do not invent new letters.

### G0 · Environment

- ENTRY: none (always runs).
- ACTIONS: resolve `KIT_SELF` before any `cd`; feature-detect every
  required tool; probe node (`command -v node`) → set `HAVE_NODE`; print
  the kit's own sha256 ("compare with the delivery page pin") so the
  operator's terminal itself becomes a verification surface.
- FAIL: missing tool → name it, name the install act, exit 1. Nothing
  touched.

### G1 · Locate the repository

- ENTRY: G0 green.
- ACTIONS, in precedence order:
  1. Explicit argument: `bash update-…sh /full/path/to/repo`.
  2. Current directory, IF it fingerprints as the suite: the repo's own
     `package.json` name AND a signature file (e.g. `tools/validate.mjs`)
     both present.
  3. Autodiscovery over a fixed candidate list
     (`$HOME/{userscripts,src/userscripts,repos/userscripts,github/
     userscripts,code/userscripts,dev/userscripts,Documents/userscripts,
     Downloads/userscripts}` — extend from the operator's known layout).
- FAIL: not found → exit 1 printing the EXACT re-run syntax with the kit's
  resolved path filled in:
  `bash "<KIT_SELF>" /full/path/to/<repo>`.
  A candidate that fingerprints wrong → name the failed fingerprint test
  ("package.json mismatch", "missing tools/validate.mjs").
- WHY BOTH fingerprints: a path argument defends against applying the
  round to the WRONG repo that happens to be a git repo; the fingerprint
  pair defends against applying it to a DIRECTORY that merely has the
  right name.

### G2 · Baseline verification (the fork)

- ENTRY: repo located.
- ACTIONS: read branch (`git symbolic-ref --short HEAD`; empty = detached
  → fail with `git checkout main` + re-run syntax). Then fork:
  - HEAD == `PIN_TIP` → `ALREADY=1` (skip G2.5/G3; G4 gate re-runs).
  - HEAD == `PIN_BASE` → proceed (the normal path).
  - anything else → fail: print actual HEAD, the pinned base, the base's
    commit subject, and the DO-NOT-FORCE instruction ("If you have newer
    local commits, do NOT force anything — report this to the executor").
- FAILURE SEMANTICS: this is the single most important fail-closed gate.
  An operator ahead of base has work the kit CANNOT see; any destructive
  move would be data loss. The kit is explicitly forbidden from
  `reset`/`checkout --`/`clean` under any circumstance.

### G2.5 · WIP preservation (only when tree is dirty AND not ALREADY)

- ENTRY: G2 passed on the normal path; `git status --porcelain` non-empty.
- ACTIONS:
  1. `BK=".git/kit-backups/<timestamp>"`; `mkdir -p` it (inside `.git/`
     so it never pollutes status or the worktree).
  2. `git stash push --include-untracked -m "<kit> WIP backup <ts>"` —
     **plain scoped stash, NEVER `--all`** (the `--all` landmine sweeps
     ignored files: node_modules, build outputs, editor state).
  3. Write `RESTORE-INSTRUCTIONS.txt` into `BK` with the three lawful
     next acts: `git stash list` (see it) · `git stash pop` (restore) ·
     do nothing (keep as backup).
  4. Re-assert clean; if still dirty → fail ("aborting rather than
     guessing") — a stash that leaves residue means ignored-but-tracked
     oddities the kit must not reason about.
- NOTE: untracked files are stashed (so the merge cannot collide with
  them) and the G5 report says so explicitly.

### G3 · Payload verification, then application

- ENTRY: baseline verified (or skipped via ALREADY).
- VERIFY (all before ANY mutation of the repo):
  1. Slice the payload: `sed -n '/^#__PAYLOAD_BEGIN__$/,/^#__PAYLOAD_END__$/p'
     "$KIT_SELF" | sed '1d;$d' > "$TMP/payload.b64"` (marker-anchored —
     rename-safe, line-number-free).
  2. `sha256sum -c` against `PIN_PAYLOAD_SHA` → corrupted-kit exit with
     "re-download it" (the kit CANNOT repair its own corruption).
  3. `base64 -d | gunzip > $TMP/range.bundle`; sha256 vs `PIN_BUNDLE_SHA`.
  4. `git bundle verify` → must succeed AND its output must contain
     `PIN_BASE` (the bundle requires the operator's own baseline — this
     is the cryptographic handshake with the operator's repo) and
     `PIN_TIP`.
  5. `git bundle list-heads` → must be EXACTLY
     `<PIN_TIP> refs/heads/<round>` (one ref, the right one).
- APPLY (only after all five pins hold):
  1. `git fetch <bundle> refs/heads/<round>:refs/heads/<round>-incoming`
  2. `git merge --ff-only <round>-incoming` — true fast-forward: the
     operator's history and the round's commit messages are preserved,
     nothing rewritten. (If the merge cannot fast-forward, git itself
     refuses — that is the desired fail-closed.)
  3. Delete the temp branch; assert HEAD == `PIN_TIP`; fail otherwise.
- WHY fetch-to-temp-branch instead of `git pull <bundle> <ref>`: the temp
  branch makes the incoming ref visible, deletable, and collision-proof;
  `pull` semantics on bundles differ across git versions.

### G4 · Proof of exactness + the gate

- ENTRY: HEAD == `PIN_TIP` (freshly merged or ALREADY).
- PROOF (content, not metadata):
  1. `git rev-parse 'HEAD^{tree}'` == `PIN_TIP_TREE` — the tree IS the
     certified tree, independent of timestamps/authorship in commits.
  2. sha256 of every `PIN_<KEY>_SHA` file == pin (e.g. the canon script
     the round was about: "your file, byte-identical").
- GATE (only if `HAVE_NODE`):
  1. `npm install` IF `node_modules` absent (fail → "resolve network/npm,
     then re-run" — the apply already stands; re-run takes the ALREADY
     path).
  2. `npm run check` → assert the certification line (e.g.
     `GUP VERIFICATION: CERTIFIED`), log preserved at the temp path and
     the path printed on failure.
  3. `npm run docs` → assert its count line.
  4. `npm run check` AGAIN → same certification. **The order check → docs
     → check is itself a mitigation**: docs generation can drift generated
     files (the doc-drift class); the final check proves idempotence.
  5. Zero-drift assertion: `git status --porcelain
     --untracked-files=no` must be EMPTY after the gate — a gate that
     dirties the tree it certifies is a defect, not a pass.
- DEFER (`HAVE_NODE=0`): print the exact deferred command block; the
  GREEN line itself carries the reminder.

### G5 · Report

- ACTIONS: print applied commits (`git log --oneline --reverse
  <base>..<HEAD>` — the operator SEES what entered their history); the
  proof pins; stash state + restore pointers; the **canon-identity note**:
  if the stashed WIP contains a file whose sha equals the round's pin
  (check `git show "stash@{0}:<path>" | sha256sum`), say so — restoring it
  is a no-op, drop-or-keep both fine (this prevents the exact confusion
  where an operator's stashed manual placement of the delivered file
  reads as "my work was lost"); untracked-file count (left untouched);
  the GREEN line with the single remaining step: `git push`.
- The kit ends `exit 0`. THE PAYLOAD BLOCK MUST NEVER EXECUTE.

---

## PART IV — DETERMINISTIC CONSTRUCTION (the builder)

The kit is GENERATED, never hand-written in final form. Persist a builder
script (Python or bash) that:

1. Reads the round bundle from its verified location; **asserts its sha256
   against the round's recorded pin before embedding** (the builder is
   itself fail-closed: if the bundle drifted, abort — never embed
   unverified bytes).
2. `gzip.compress(payload, 9)` → `base64.b64encode` → wrap at 76 columns →
   join with `\n` + ONE trailing newline. **This byte string is what
   `PIN_PAYLOAD_SHA` hashes.** (Compute the pin AFTER building the exact
   b64 block; deriving it any other way is the classic builder defect.)
3. `git rev-parse <tip>^{tree}` in the certified repo → `PIN_TIP_TREE`.
4. Reads a TEMPLATE (the script zone with `__PIN_*__` placeholders);
   substitutes the computed pins; **asserts no `__PIN_` substring
   survives** (an unresolved placeholder inside the kit is a corrupted
   kit — this is A8 applied to yourself).
5. Splices the payload between the anchor lines; writes the kit to BOTH
   staging locations (delivery page dir + download dir); prints kit size,
   pins, and kit sha256 for the delivery page.
6. Re-runs produce byte-identical output (gzip is deterministic for a
   fixed input and level; no timestamps are embedded in the script zone —
   timestamps appear only in RUNTIME output like backup dir names).

**Round inputs** (what the author assembles BEFORE building): the
operator's current pushed baseline sha (fetch their remote; NEVER assume
your last known state — the operator pushes without warning); the round's
tip commit (your local range, gates green); the per-round file pins the
operator cares about; the suite's kit naming convention.

---

## PART V — THE BATTERY LAW (the kit ships only after its battery is green)

The battery is a persisted, re-runnable script (bash preferred; the
operator's convention is `<round>-kit-battery.sh`) that constructs THROWAWAY
test repos and drives the kit through every lawful and unlawful path.

### V.1 Test-repo construction law

- Build test repos **from a git bundle of the accepted baseline, NEVER
  from the authoring clone** (the authoring clone carries your local
  branches, reflog, and ahead-state — a battery that reads it lies about
  the operator's world).
- **A bundle does not carry a working HEAD ref by default** — cloning from
  a bare range bundle lands nowhere. Either create the bundle with an
  explicit HEAD ref or `git clone <bundle> t && git -C t checkout -B main
  <PIN_BASE>`. (This exact harness defect shipped once: 14/25 checks
  green on a battery testing the wrong state.)
- The dirty-tree scenario (P2) must replicate the OPERATOR'S EXACT
  situation, not a generic one — e.g. the canon file replaced by the
  delivered bytes + an edited README + one untracked file.

### V.2 The mandatory phases (P0–P7; a battery with fewer phases is
non-compliant)

| Phase | Scenario | Asserted outcome |
|---|---|---|
| **P0** | Self-integrity | kit's internal payload pin == sha of the actual embedded block; decoded block == the ORIGINAL bundle byte-identical. **Expectations are DERIVED from the kit's internal pins** (parse them out), never hardcoded in the battery — hardcoded expectations go stale the moment the kit is rebuilt and turn the battery into a liar |
| **P1** | Pristine apply | fresh baseline clone → kit → all phases green + gate CERTIFIED + commit count/HEAD correct + tree & canon pins verified |
| **P2** | Operator's exact dirty tree | WIP present → stash-backup created + RESTORE-INSTRUCTIONS on disk + identity note printed when applicable + `git stash pop` restores EVERY byte (lossless round-trip proof) |
| **P3** | Wrong baseline | HEAD = something else → fail-closed, repo byte-untouched, message contains the actual HEAD |
| **P4** | No repo | PATH containing no repo (or a wrong-directory argument) → fail-closed, message contains the EXACT re-run syntax |
| **P5** | node absent | restricted PATH without node → APPLIED + HASH-VERIFIED, gate DEFERRED with exact commands |
| **P6** | Re-run | run kit twice → second run: already-applied + full gate green, no double-apply |
| **P7** | Authoring repo untouched | the repo the kit was built from is byte-identical before/after the whole battery |

### V.3 Battery discipline

- The battery's own defects are kit defects: when the battery fails, FIRST
  determine whether the kit or the harness is wrong (the bundle-HEAD
  defect above looked like a kit failure and was a harness failure —
  misdiagnosis produces a "fixed" kit that is actually broken).
- Every battery run is archived as evidence (`<round>-kit-battery.txt`)
  and staged with the delivery.
- **Red control discipline**: wherever possible, prove the battery can
  FAIL — run one known-bad input (corrupt one byte of a kit copy; expect
  the P0 pin failure specifically) so a battery that always says GREEN is
  exposed as such.
- **Wire-download proof**: before delivery, download the kit back over
  the actual delivery channel and execute THAT copy (P1 again) — the
  bytes the operator receives are the bytes the battery tested.

---

## PART VI — THE NESTED FAILURE LADDERS (adversarial depth analysis)

Each ladder is: **[L1] failure → mitigation → [L2] the mitigation breaks →
mitigation → [L3] THAT breaks → mitigation.** Author-time obligation:
for every mitigation you add, spend at least one full adversarial pass
trying to break it BEFORE the operator does. When you find the break,
add the next rung. The ladders below are the field-proven core; extend
them per-round.

### Ladder 1 — Corrupted or substituted kit bytes

- **[L1] The kit file is corrupted in transit (truncated download, disk
  rot, FTP ASCII-mangling).**
  Mitigation: G3 verifies `PIN_PAYLOAD_SHA` over the extracted b64 block;
  a corrupt file fails pin #2 before touching the repo, with
  "re-download it."
- **[L2] The corruption is CONSISTENT — an attacker (or a bad proxy)
  rebuilt the kit with its own payload and recomputed all internal pins.**
  Internal pins prove nothing against an attacker who authored them.
  Mitigation: the kit's own sha256 is published OUT OF BAND on the
  delivery page (a channel the kit cannot rewrite), and G0 prints the
  running file's hash so the operator's terminal is a comparison
  surface. Trust anchors: page pin + operator's own git objects —
  BOTH must lie simultaneously for a bad kit to pass G3.
- **[L3] The operator will not manually compare a 64-char hash.**
  Mitigation: make the comparison unnecessary for SAFETY even when
  skipped for CONVENIENCE: G4's tree-hash pin (`PIN_TIP_TREE`) and the
  `git bundle verify` against the operator's OWN baseline mean a
  substituted payload that doesn't produce the certified tree fails
  closed AFTER the pins — the only thing a non-comparing operator risks
  is running a kit that refuses to work, not one that damages the repo.
  Substitution safety ≠ substitution detection; the kit guarantees the
  former and enables the latter.
- **[L4] The operator's delivery PAGE itself serves stale bytes** (this
  shipped THREE times in the field as the `.txt` mirror serving the
  previous round's file).
  Mitigation: the delivery protocol (Part VIII) wire-proofs EVERY
  artifact every round: download over HTTP from both endpoints, `cmp`
  against the staged file, byte-for-byte. Visual inspection is never
  proof; curl|cmp is.

### Ladder 2 — The operator's uncommitted work (the WIP minefield)

- **[L1] Applying a fast-forward over a dirty tree can collide with or
  bury the operator's WIP.**
  Mitigation: G2.5 stashes before the merge, with the backup directory
  and RESTORE-INSTRUCTIONS.
- **[L2] The naive fix `git stash --all` sweeps ignored files —
  `node_modules`, build outputs, editor state — into the stash where the
  operator will never find them.**
  Mitigation: plain `git stash push --include-untracked` (tracked +
  untracked, NOT ignored); the G5 report names the stash message; the
  instructions file names the three lawful acts.
- **[L3] The operator's WIP edits files the round also changed →
  `git stash pop` after the round CONFLICTS, and the operator reads the
  conflict as "the kit broke my repo."**
  Mitigation: (a) the stash is never auto-dropped — it survives as a
  backup until the operator acts; (b) G5 prints the applied-commit list
  so the collision surface is visible BEFORE the pop; (c) the battery's
  P2 proves the lossless round-trip on the exact dirty-tree scenario;
  (d) RESTORE-INSTRUCTIONS offers "do nothing" as a first-class act.
- **[L4] The stashed WIP contains the very file the round delivers
  (the operator had manually placed the previous round's deliverable
  into their tree — this exact scenario occurred).**
  Mitigation: G5's canon-identity note — hash `stash@{0}:<path>` against
  the round pin; if equal, SAY SO: "restoring it is a no-op; drop or
  keep, both fine." An unexplained stash that silently contains the
  delivered file reads as lost work.
- **[L5] The stash entry itself is lost** (operator runs `git stash
  clear` or `git gc --prune=now` in panic).
  Mitigation: the backup directory inside `.git/kit-backups/<ts>/` also
  carries the instructions and the timestamp; the stash MESSAGE is
  round-branded so `git log -g` and reflog forensics can reconstruct.
  (Reflog keeps stashes reachable ~30 days by default — disclose this
  window in the instructions file.)

### Ladder 3 — Wrong repo, wrong state

- **[L1] The kit applies the round to the wrong repository** (operator
  has three clones; the PATH variable finds the wrong one).
  Mitigation: the G1 fingerprint pair (package.json name + signature
  file) plus the G2 baseline pin — a wrong clone will not be at
  `PIN_BASE`.
- **[L2] The right repo, but detached HEAD or another branch.**
  Mitigation: branch check fails closed with the exact
  `git checkout main` + re-run syntax.
- **[L3] The repo is AHEAD of baseline — the operator has newer local
  commits the executor has never seen.**
  Mitigation: fail with DO-NOT-FORCE and a report instruction. The kit
  is forbidden from reset/checkout/clean; an ahead tree is INVISIBLE
  work, and the only lawful move is to stop. (The successor protocol:
  the executor fetches, rebases the round onto the operator's new
  baseline, and ships a NEW kit — never mutates the old one.)
- **[L4] The repo is BEHIND — the operator's local main is at the
  baseline, but their origin/main has moved** (they pulled elsewhere).
  Out of scope by design: the kit anchors to the LOCAL HEAD pin. If
  local HEAD == base, the round applies cleanly; the push later
  fast-forwards or the operator's own git handles the divergence.
  Disclose in the kit header that the anchor is the local baseline sha.

### Ladder 4 — Partial application and crash recovery

- **[L1] The kit dies mid-G3 — after fetch, before/during merge.**
  Mitigation: the EXIT trap deletes the temp branch; a fetch touches no
  working files; merge --ff-only is a single ref move — the tree was
  never half-updated. Re-run: HEAD is still `PIN_BASE` (normal path
  runs again) or `PIN_TIP` (ALREADY path re-verifies).
- **[L2] The kit dies mid-G2.5 — after the stash, before the merge.**
  The tree is clean; the WIP is in the stash. Mitigation: re-run sees a
  clean tree, skips G2.5, applies the round; G5 reports the stash state
  (it prints stash pointers on EVERY run when a kit-brand stash exists —
  not only the run that created it). The RESTORE-INSTRUCTIONS file is
  already on disk from the first run.
- **[L3] The kit dies mid-G4 gate (npm install network hang, node
  crash).**
  Mitigation: the apply stands; re-run takes the ALREADY path and
  re-runs ONLY the gate. The deferred-gate mode (P5) proves the split
  works. No path in the kit deletes the applied range.
- **[L4] Two kits run CONCURRENTLY in the same repo** (operator opens
  two terminals, pastes twice, impatient).
  Mitigation (mandatory in new kits; the field-proven kit predates
  it): acquire `flock` on `.git/kit.lock` at G0; second instance exits
  with "another kit instance is running; let it finish." Without it:
  the baseline fork makes double-apply largely self-correcting (second
  run sees ALREADY), but two interleaved G2.5 stashes are unrecoverable
  ambiguity — hence the lock.

### Ladder 5 — The gate itself lies

- **[L1] `npm run check` passes but the tree drifted** (generated files
  wrote during the gate).
  Mitigation: the zero-drift assertion after the FINAL check; check →
  docs → check ordering so doc-drift is caught inside the same run
  (inventory feeds docs; the [C]-class failures are the gate's own
  coaching for running docs in between).
- **[L2] The gate emits the certification string but non-zero-dependently
  (string present earlier in the log, e.g. inside a changelog).**
  Mitigation: assert the certification line appears in the LAST N lines
  of the gate output AND the gate's exit code is zero (set -e handles
  the code; the tail-window grep handles the string).
- **[L3] The gate is green but on the WRONG tree** (operator moved
  HEAD between phases — pathological but seen in the field as manual
  interference).
  Mitigation: G4 re-derives `HEAD^{tree}` == `PIN_TIP_TREE` AFTER the
  gate, inside the same phase sequence; the tree pin is the last word.

### Ladder 6 — Environment and portability

- **[L1] The operator has no node** (or a broken npm).
  Mitigation: P5 defer path — apply + hash-verify now, gate deferred
  with exact commands in the GREEN line.
- **[L2] The operator's coreutils differ** (BSD vs GNU: `sha256sum`
  absent, `base64` needs no `-w`, `sed -z` missing).
  Mitigation: G0 feature-detects and names the missing binary; the
  implementation uses only POSIX-shaped constructs; where a tool name
  differs (macOS `shasum -a 256`), the kit detects and aliases at G0 —
  never mid-phase.
- **[L3] The kit is executed in a way with no `$0` file** (`curl … |
  bash` — stdin execution; `bash < scriptfile` variants).
  Mitigation (mandatory in new kits): G0 asserts `$0` resolves to a
  readable file; else fail with "download the file first, then run:
  bash update-<suite>-<round>.sh" — a piped kit cannot read its own
  payload zone.
- **[L4] Pathological paths: spaces, unicode, symlinked repo dirs.**
  Mitigation: `KIT_SELF` resolution via `cd dirname + pwd` (dereferences
  symlinks); ALL git invocations use `-C "$REPO_DIR"`; every variable is
  quoted; marker-anchored payload slicing (not line numbers, which
  authoring edits shift).

### Ladder 7 — The bundle and its objects

- **[L1] The bundle was built against a different baseline than the
  operator's HEAD.**
  Mitigation: `git bundle verify` names the required base; G3 asserts
  the required base == `PIN_BASE` == the operator's HEAD.
- **[L2] The bundle carries extra refs** (authoring state leaked: your
  local branches, a stale HEAD pointer).
  Mitigation: `git bundle list-heads` must be EXACTLY one ref
  (`<tip> refs/heads/<round>`); build bundles with the explicit
  single-ref syntax `git bundle create F <base>..<tip>` — never `--all`.
- **[L3] The bundle's OBJECTS are fine but its HISTORY doesn't
  fast-forward onto the operator's baseline** (rebased tip over a
  different base than verified).
  Mitigation: `merge --ff-only` refuses — by construction. The G3
  post-assert `HEAD == PIN_TIP` catches any residual confusion.

### Ladder 8 — Semantic delivery failures (bytes right, meaning wrong)

- **[L1] The kit applies and certifies, but the operator's MENTAL model
  breaks** ("which of my three copies is production?", "did my WIP
  survive?", "why does check fail on MY other machine?").
  Mitigation: G5's report is a NARRATIVE of state: what entered, what
  is stashed where, what was left untouched, what the single remaining
  step is. The kit's job is not just a correct repo — it is a CALM
  operator.
- **[L2] The operator expects the delivered FILE to appear somewhere**
  (their prior mental model was file-download delivery).
  Mitigation: G4's per-file pin prints the path + "your file,
  byte-identical" — the operator learns WHERE their artifact lives in
  the tree (`canon/_sovereign/…`), converting a file-shaped expectation
  into a tree-shaped fact.
- **[L3] The operator runs their gate on a DIFFERENT machine than the
  kit ran on** (applied at the desktop, checks on the laptop — the
  divergence class).
  Mitigation: out of kit scope BY DESIGN — but the G5 deferred-gate
  block and the header's SAFETY section both teach the invariant: the
  KIT runs the gate so the operator doesn't have to; if they do anyway,
  the tree pin is the cross-machine truth (commit the range, clone
  elsewhere, `git rev-parse HEAD^{tree}` must match the page pin).

### Ladder 9 — Delivery-channel failure (the executor's side)

- **[L1] The executor's session dies at the delivery boundary** (the
  most expensive failure in the field record — thrice).
  Mitigation: the durable artifacts (delivery page, pins, worklog,
  staged files) ARE the delivery; the chat response only POINTS. Write
  the ledger entry BEFORE staging; keep the final response SHORT and
  link-first so it survives any context window.
- **[L2] The staged page/links are correct but unreachable**
  (dev server died, port map changed, VM moved).
  Mitigation: the run book's port probe FIRST; re-initialize the
  delivery app if needed; re-verify the preview URL answers before
  claiming delivery.
- **[L3] The browser renders but the LINKS 404** (staged path ≠ linked
  path — filename typos with spaces are the classic).
  Mitigation: the browser-render proof CLICKS every artifact link
  (HTTP 200 asserted per link), and the wire-download proof pulls the
  actual bytes. A page that renders but whose links are dead is a
  failed delivery.

### Ladder 10 — The battery rot

- **[L1] The battery passes but tests stale expectations** (kit was
  rebuilt; battery still pins the old kit sha).
  Mitigation: P0 derives expectations from the KIT'S OWN internal pins,
  parsed out of the shipped file — the battery can only test "the kit
  as it is," never "the kit as it was."
- **[L2] The battery's test repos are subtly the authoring world**
  (cloned from the working clone, carrying ahead-state).
  Mitigation: test repos built from a bundle of the accepted baseline;
  the P7 authoring-repo-untouched assertion catches leakage.
- **[L3] The battery is green but UNRUN against the wire copy.**
  Mitigation: the wire-download execution proof — the delivered bytes
  run P1 again, on a fresh clone, from the actual channel.

### Ladder 11 — Trust-anchor collapse

- **[L1] The operator's baseline is NOT what the executor believes**
  (their local tree diverges from their pushed remote — held commits).
  Mitigation: kits depend on ZERO held copies: every pin is either in
  the operator's own pushed history or embedded in the kit itself.
  When the operator's GitHub is the source of truth, the round's base
  is FETCHED fresh at authoring time (all refs, not just main — PR
  heads can carry work).
- **[L2] The operator's git history is IMMUTABLE-held** (local-only
  commits that no remote ref can reach — the field record contains
  exactly such a commit; 28 refs fetched, unreachable).
  Mitigation: acknowledged, not solved: the kit's G3 verifies the
  bundle against the operator's LOCAL baseline objects, which is the
  only authority that can vouch for held history. The DO-NOT-FORCE
  clause at G2 is the respect this immutability demands.

### Ladder 12 — Semantic drift between rounds

- **[L1] Round N+1's kit quietly assumes round N applied** (base = N's
  tip, but the operator never ran N).
  Mitigation: the G2 fork handles it mechanically (HEAD = base-1 ≠
  base → fail with DO-NOT-FORCE + report). The AUTHOR-side discipline:
  every kit's WHAT-IT-DOES states its exact base anchor; the delivery
  page lists rounds in order with their bases.
- **[L2] The operator cherry-applied PART of a past round** (patched
  some files, not the commits).
  Mitigation: same G2 fork — a tree at partial state is at neither pin.
  The kit never guesses; the operator reports; the executor re-derives
  a fresh kit against the ACTUAL pushed state. That re-derivation is
  cheap BECAUSE the builder is deterministic and the ledger carries the
  state.

---

## PART VII — CONSTRUCTION PROCEDURE (the ordered walkthrough)

Execute in order; do not skip. Each step's output feeds the next.

1. **Freeze the round.** The round's commits exist locally; gates green
   (`check` → `docs` → `check`, CERTIFIED, docs full count, tree clean
   after). If the tree is dirty or gates red, there is no round to ship.
2. **Fetch the operator's truth.** `git fetch origin --prune` (and
   `git ls-remote` / fetch all refs where PR heads matter). The round's
   BASE is the operator's CURRENT pushed baseline — not your memory of
   it. If they pushed past your last-known base: rebase the round onto
   their new baseline, re-run gates, regenerate inventory — then
   continue. (Deterministic regeneration tools make this cheap; never
   hand-merge.)
3. **Build the round bundle.** `git bundle create <round>.bundle
   <base>..<tip>` — single ref (`refs/heads/<round>` = tip). Verify:
   `git bundle verify` names base == the fetched baseline; `list-heads`
   shows exactly one ref.
4. **Record the trust pins.** bundle sha256; `tip^{tree}`; the per-file
   pins the operator cares about (the round's headline canon file(s)).
   These go into BOTH the kit and the delivery page.
5. **Author the template.** The SCRIPT ZONE with `__PIN_*__`
   placeholders per Part III. If a prior round's template exists, derive
   from it (convention stability is itself an operator comfort); update
   WHAT-IT-DOES with THIS round's story.
6. **Run the builder.** It asserts the bundle pin, computes the payload
   pin over the exact extractable bytes, substitutes, splices, asserts
   no placeholder survives, writes both staging locations, prints the
   kit sha256.
7. **Write the battery.** Per Part V, all phases; P0 derives
   expectations from the kit's own pins. Include the operator's exact
   dirty-tree scenario.
8. **Run the battery.** ALL green, or fix and re-run from step 5. Archive
   the evidence file.
9. **Stage the delivery.** Kit + battery evidence + round record into the
   delivery page's directory; the page gains the round's section with
   the kit's sha256, usage block, and links.
10. **Wire-proof.** Download the kit over the delivery channel; `cmp`
    against the staged file; execute the WIRE copy against a fresh
    baseline clone (a second P1 — the bytes the operator gets).
11. **Browser-render proof.** The delivery page renders; every link
    answers 200 (the .sh link may trigger a browser download instead of
    a render — that is EXPECTED for shell files; the wire-download
    execution is the render proof for this artifact type).
12. **Ledger.** Append the round's worklog entry (gates, battery,
    artifacts, pins, lessons) BEFORE the delivery response. Then respond
    SHORT, link-first.

---

## PART VIII — DELIVERY PROTOCOL (the run book; referenced, never altered)

The standing verification protocol of the lineage, in order, per round:

1. **Port probe** — the delivery endpoints answer (both the gateway and
   upstream; a down upstream with a live gateway serves 502s that look
   alive).
2. **File-delivery endpoint** — every staged artifact serves HTTP 200
   with byte-exact content (curl + cmp against the staged file, from
   each endpoint).
3. **Share** — the preview URL is the delivery surface; the chat response
   points at it (short, link-first — it must survive context death).
4. **Browser-render proof** — a real browser loads the page, the round
   section renders, artifact links click through (or download, for
   shell files).
5. **IM-layer delivery** — the response itself.

The delivery page carries the out-of-band pins: kit sha256, bundle sha,
tree hash, per-file pins. **The page is the trust anchor the kit's G0
hash print refers to.**

---

## PART IX — CHECKLISTS & COMPLIANCE VERDICT

### IX.1 Pre-flight (before building)

- [ ] Round frozen: gates CERTIFIED, docs full, tree clean (after
      NUL-safe mode normalization if the filesystem flips modes)
- [ ] Operator's pushed baseline FETCHED fresh (all refs)
- [ ] Round rebased onto their actual baseline if they moved
- [ ] Bundle single-ref, base-anchored, verified
- [ ] Pins recorded (bundle / tip / tip-tree / per-file)
- [ ] Template placeholders present for every pin

### IX.2 Battery gate (before delivery)

- [ ] P0 internal-pin derivation (no hardcoded kit expectations)
- [ ] P1 pristine apply + full gate
- [ ] P2 operator's EXACT dirty tree + lossless stash round-trip
- [ ] P3 wrong baseline fail-closed, repo untouched
- [ ] P4 no repo fail-closed with exact re-run syntax
- [ ] P5 node-absent defer path
- [ ] P6 re-run idempotence
- [ ] P7 authoring repo untouched
- [ ] Red control: one known-bad input fails the battery correctly
- [ ] Evidence archived

### IX.3 Delivery gate (before responding)

- [ ] Kit sha256 on the page == staged file == builder output
- [ ] Both endpoints serve the kit byte-exact over the wire
- [ ] Wire-copy execution GREEN on a fresh clone
- [ ] Page section renders; links 200
- [ ] Worklog appended (gates → battery → delivery, in that order)
- [ ] Response drafted SHORT and link-first

### IX.4 Compliance verdict

A kit is **COMPLIANT** iff: every axiom A1–A10 holds; every phase
G0–G5 implements its contract; the battery ran green on all mandatory
phases including the red control; the wire-copy execution is green; the
delivery protocol completed. Anything less is a defective kit — it does
not ship, regardless of deadline. **A kit that has not been tested is
not a kit; it is a hypothesis.**

---

## PART X — FIELD-PROVEN LINEAGE & LESSONS LEDGER

The artifact class this spec encodes was proven in a live lineage:
a suite governed by a certification gate (`npm run check` → GUP
VERIFICATION: CERTIFIED, 100/100), an operator applying rounds to their
own clone, and ten rounds of delivery-failure archaeology before the kit
form emerged. The proving round shipped an 82 KB kit embedding a
53,637 B bundle (9 commits), battery 39/39 across 8 phase families,
wire-download execution green on a fresh clone, and a re-run idempotence
proof — after which the operator's application path became literally:

```
bash update-<suite>-<round>.sh      # from anywhere
# read the GREEN line
git push
```

**The lessons ledger (each one a shipped defect or near-miss, distilled
into the clauses above):**

1. `exit 0` before the payload block, or bash falls through into base64
   after G5 and the operator sees garbage errors after success.
2. Test-repo bundles need a HEAD ref (or `clone` + `checkout -B main
   <sha>`), or the battery tests the wrong state and calls it green.
3. Battery expectations derive from the kit's internal pins, never
   hardcoded — rebuilt kits turn hardcoded batteries into liars.
4. The payload pin hashes the EXACT extractable bytes (post-wrap,
   post-newline), not the pre-wrap encoding.
5. Plain `git stash push --include-untracked`; NEVER `--all`.
6. `git pull <bundle> <ref>` semantics vary by git version —
   fetch-to-temp-branch + `merge --ff-only` does not.
7. `gup_validate.py`-class tools hang without stdin detached — run with
   `< /dev/null`.
8. Mode noise recurs (filesystem events flip 100644→100755); normalize
   NUL-safely (`git ls-tree -z` + `${rec#*$'\t'}`; awk field-splitting
   eats space-bearing paths) before ANY tree-clean claim.
9. The `.txt`/mirror channel served stale bytes three separate rounds —
   wire-proof every artifact, every round, both endpoints.
10. Announce after gates pass; never promise the next artifact before it
    exists on disk.
11. Every operator instruction must be executable VERBATIM with zero
    interpretation — one file, one command, edge cases handled BY THE
    ARTIFACT, not by the human. Where ambiguity can live, error will.
12. The durable artifacts are the delivery; the response only points.
    Keep it short enough to survive context death.
13. `git bundle verify` + list-heads single-ref assert closes the
    extra-refs leak (authoring branches riding inside the payload).
14. The G5 canon-identity note prevents "my work was lost" reads when
    the stash contains the delivered file itself.
15. `npm run check` runs the build first — the TREE is what gets
    certified; delivering a hand-built "production" file inverts the
    trust model. The commit range is the lawful delivery unit; the kit
    is its carrier.

**End of specification.** Built as a complete literal artifact: zero
placeholders in any operator-facing path, every clause derived from a
reproducible field event, and every mitigation broken at least once on
paper before being trusted.
