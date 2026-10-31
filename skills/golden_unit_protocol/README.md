# Golden Unit Protocol — Skill Directory Reference

*(Revision 2026-10-19: replaces the v5.2-era README, which described a
package layout this directory no longer has. The v5.2-era document remains
in git history. Scoped to THIS directory only — it is not a repo-wide
reference.)*

## 1. Current contents

```text
skills/golden_unit_protocol/
├── README.md                       this file
├── golden-unit-protocol.skill      CANONICAL — GUP v7.0.1 (see §2)
└── gemini/v7.0.0/                  Gemini-surface variant of GUP v7.0.0
```

The **O.M.A. (Omnipresent Machine Assurance)** extension no longer rides
inside the GUP package. It is its own skill:
[`skills/omnipresent_machine_assurance/oma-v1.1.skill`](../omnipresent_machine_assurance/).
This mirrors the assurance doctrine itself: single authority, no duplicate
implementations. In the v5.2 era O.M.A. was bundled as `gup-oma/`; the
bundle-era description is preserved in git history.

## 2. Canonical artifact

| Field | Value |
|---|---|
| File | `golden-unit-protocol.skill` |
| Version | **v7.0.1** (2026-10-19) |
| Bytes | 66,241 |
| SHA-256 | `d88eea0718cfcd43ae0c65b713c1185bf50e8b49126a880605b41d11da8c8cd2` |
| Package | ZIP, 15 entries (SKILL.md + executables + tests) |

The digest is the identity (Tier 1): any copy whose sha256 matches IS the
artifact. This version is also registered as pin A11 in the 4NDR0MEDA
pin-chain (`reference/` staging there), byte-verified against this
directory on 2026-10-19.

## 3. Version lineage

| Version | Status | Notes |
|---|---|---|
| v5.0 | superseded | the originally supplied skill package |
| v5.2 | superseded | audit-hardened revision; bundled GUP-O.M.A. v1.1.0; the era the previous README described |
| v7.0.0 | superseded | chat-surface operations era; consumed version preserved in 4NDR0MEDA `reference/` (pin A7, `6ab62d44…`) |
| **v7.0.1** | **current** | 2026-10-19 revision under explicit operator authorization — see §4 |

## 4. What v7.0.1 adds over v7.0.0

Twenty-two surgical patches, additive and cosmetic — no gate weakened, no
baseline capability removed (GUP's own superset rule applied to itself):

- **Appendix E — Continuity & Rehydration Annex**: the protocol now treats
  continuity as a first-class dimension (session-death recovery, worklog
  re-ingest, state-echo discipline) — field-proven across three context
  deaths and one platform-deletion event in the source collaboration.
- **0.3.13 Canonical Homes**: single-source-of-truth rule per document
  class, cross-referenced by commit hash, never URL.
- **D5 scope clause**: resolves the EAFP-vs-fail-closed tension — EAFP
  governs I/O ergonomics; fail-closed governs verification and trust
  boundaries. They are different layers; neither overrides the other.
- **Out-of-band evidence rule**: a delivered artifact's digest is stated
  in-channel (out-of-band pin) at delivery; wire self-attestation alone
  never certifies receipt.
- **§7.5 reservation slots**: numbered-but-unsassigned section slots so
  future sections do not renumber existing text that other tools cite.
- Internal-consistency repairs: §5 numbering order, phantom Appendix-A
  references (D10/D12/D14), stale "GUP v5" label, §9 scripts/ path.

## 5. Doctrine (unchanged core)

The engineering doctrine is stable across versions: blind execution is
fragile until exercised; no failure masking; atomicity; idempotence;
deterministic cleanup ownership; single authority; no placeholders;
feature superset over baseline; repository certification is distinct from
machine certification; bounded declared envelopes over universal claims.

**Prime Directive (unchanged since v5.2):**

> Never certify what was not defined, exercised, observed, recovered, and
> reproduced.

## 6. Updating this skill

Per the protocol's own revision discipline: a version number must
correspond to a real protocol revision; the previous version is the
baseline; the capability superset must survive; VERSION/CHANGELOG must
agree with the package; negative-path tests re-run before release. The
v7.0.1 revision itself was produced by exactly this process — full review
memo: `protocol-review-2026-10-19.md` (digest `93268708…c4098`) in the
4NDR0MEDA record.
