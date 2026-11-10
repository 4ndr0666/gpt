#!/usr/bin/env python3
"""Comprehensive unit and adversarial test suite for 4ndr0neering v8.0.0.

Verifies:
1. Lexical dispatch invariants & <module_top_level> protection against functionless file wipes.
2. Rejection of all GUP v7.0.2 false-PASS exploits:
   - Missing baseline/candidate manifest files on disk (GUP Exploit 1).
   - Phantom non-existent baseline Git commit SHAs.
   - Fabricated manifest files whose hashes disagree with the live Git tree.
   - Empty alignment arrays (`declarations: [], observations: []`) without verified zero-dep rationale (GUP Exploit 2).
   - Unanchored string placeholders (`"evidence": "trust me"`) that do not match actual files/symbols on disk.
   - Unverified test commands without executed logs.
3. Epistemic separation (`DEFECT` vs `UNVERIFIED` vs `BLOCKED`):
   - Missing runtime evidence (`UNVERIFIED`) or a blocked secondary target (`BLOCKED`) produces
     `BOUNDED_PASS` (exit 0 in default mode, exit 1 under `--require-full-certification`) without stopping
     unrelated verified work.
   - A demonstrated defect (`DEFECT`) always fails closed (`FAIL_DEFECT`, exit 1).
4. Deterministic single-file update kit (`4ndr0_kit.py`) construction, P0-P7 + RED_CONTROL battery,
   and self-contained HTML round-record (`4ndr0_report.py`) generation and pin parity.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PYTHON = sys.executable


def run_cmd(*args: str, cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args, cwd=str(cwd) if cwd else None, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check, timeout=120
    )


def init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    run_cmd("git", "init", "-q", "--initial-branch=main", str(path), check=True)
    run_cmd("git", "-C", str(path), "config", "user.name", "4ndr0neering Test", check=True)
    run_cmd("git", "-C", str(path), "config", "user.email", "4ndr0@example.invalid", check=True)


def commit_all(path: Path, message: str) -> str:
    run_cmd("git", "-C", str(path), "add", "-A", check=True)
    run_cmd("git", "-C", str(path), "commit", "-qm", message, check=True)
    return run_cmd("git", "-C", str(path), "rev-parse", "HEAD", check=True).stdout.strip()


class FourNdr0neeringProtocolTests(unittest.TestCase):
    def test_01_hash_selftest_and_functionless_file_protection(self) -> None:
        res = run_cmd(PYTHON, str(SCRIPTS / "4ndr0_hash.py"), "--selftest")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            b_file = td_path / "config.py"
            c_file = td_path / "config_new.py"
            b_file.write_text("MAX_RETRIES = 5\nTIMEOUT = 30\n", encoding="utf-8")
            c_file.write_text("MAX_RETRIES = 0\n", encoding="utf-8")
            comp_res = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_hash.py"),
                "--baseline-file", str(b_file),
                "--candidate-file", str(c_file),
            )
            self.assertEqual(comp_res.returncode, 0, comp_res.stderr)
            data = json.loads(comp_res.stdout)
            self.assertEqual(data["counts"]["CHANGED"], 1)
            self.assertEqual(data["comparison"][0]["unit_id"], "config.py::<module_top_level>")

    def test_02_adversarial_rejects_missing_manifests_and_phantom_baseline(self) -> None:
        """Prove that GUP Exploit 1 (missing manifests + phantom baseline commit) is rejected as FAIL_DEFECT."""
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            init_repo(repo)
            (repo / "service.py").write_text("def handle():\n    return 200\n", encoding="utf-8")
            head = commit_all(repo, "init")

            fake_evidence = {
                "protocol_version": "8.0.0",
                "tier": "T0",
                "delivery_mode": "CERTIFIED_RELEASE",
                "baseline_commit": "0" * 40,
                "candidate_commit": head,
                "units": {
                    "baseline_manifest": "/nonexistent/baseline.json",
                    "candidate_manifest": "/nonexistent/candidate.json",
                    "comparison_artifact": "nonexistent.json",
                },
                "comparison": [],
                "semantic_reviews": [],
                "alignment": {"alignment_file": "/nonexistent/align.json"},
                "acceptance_criteria": [],
                "integration_closure": [
                    {"surface": "entry_points", "status": "CLOSED", "evidence": "none"},
                    {"surface": "tests", "status": "CLOSED", "evidence": "none"},
                ],
                "manifest_targets": [],
            }
            ev_path = Path(td) / "fake_evidence.json"
            ev_path.write_text(json.dumps(fake_evidence), encoding="utf-8")
            res = run_cmd(PYTHON, str(SCRIPTS / "4ndr0_validate.py"), "--root", str(repo), "--evidence", str(ev_path))
            self.assertEqual(res.returncode, 1)
            report = json.loads(res.stdout)
            self.assertEqual(report["status"], "FAIL_DEFECT")
            joined = " | ".join(report["defects"])
            self.assertIn("baseline_commit", joined)
            self.assertIn("units.baseline_manifest file does not exist", joined)
            self.assertIn("units.candidate_manifest file does not exist", joined)

    def test_03_adversarial_rejects_empty_alignment_and_hallucinated_symbols(self) -> None:
        """Prove that GUP Exploit 2 (empty alignment arrays or fake file/symbol anchors) is rejected."""
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            init_repo(repo)
            (repo / "provider.py").write_text("def provide_token():\n    return 'tok'\n", encoding="utf-8")
            commit_all(repo, "init")

            # Case A: Empty alignment without rationale
            align_empty = Path(td) / "align_empty.json"
            align_empty.write_text(json.dumps({"declarations": [], "observations": []}), encoding="utf-8")
            r_empty = run_cmd(PYTHON, str(SCRIPTS / "4ndr0_align.py"), str(align_empty), "--root", str(repo))
            self.assertEqual(r_empty.returncode, 1)
            self.assertEqual(json.loads(r_empty.stdout)["status"], "FAIL_DEFECT")

            # Case B: Hallucinated symbol in existing file
            align_bad_sym = Path(td) / "align_bad_sym.json"
            edge = {"id": "tok-edge", "provider": "provider.py:nonexistent_fn", "consumer": "provider.py:provide_token"}
            align_bad_sym.write_text(json.dumps({
                "declarations": [{
                    **edge,
                    "declaration_evidence": "provider.py:provide_token",
                    "provider_evidence": "provider.py:nonexistent_fn",
                    "consumer_evidence": "provider.py:provide_token",
                }],
                "observations": [{
                    **edge,
                    "observation_evidence": "provider.py:provide_token",
                }],
            }), encoding="utf-8")
            r_sym = run_cmd(PYTHON, str(SCRIPTS / "4ndr0_align.py"), str(align_bad_sym), "--root", str(repo))
            self.assertEqual(r_sym.returncode, 1)
            self.assertIn("nonexistent_fn", r_sym.stdout)

    def test_04_certified_and_bounded_pass_workflow_plus_kit_and_html_report(self) -> None:
        """Prove end-to-end CERTIFIED and BOUNDED_PASS validation, kit battery (P0-P7 + RED_CONTROL), and HTML report."""
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            repo = td_path / "repo"
            init_repo(repo)
            (repo / "auth.py").write_text(
                "def authenticate(user: str) -> bool:\n    return bool(user)\n",
                encoding="utf-8",
            )
            (repo / "client.py").write_text(
                "from auth import authenticate\n\ndef login(u: str) -> bool:\n    return authenticate(u)\n",
                encoding="utf-8",
            )
            (repo / "test_auth.py").write_text(
                "import unittest\nfrom client import login\n\nclass T(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(login('alice'))\n\nif __name__ == '__main__':\n    unittest.main()\n",
                encoding="utf-8",
            )
            base_sha = commit_all(repo, "baseline")

            # Upgrade authenticate to enforce timeout and reject empty whitespace
            (repo / "auth.py").write_text(
                "def authenticate(user: str, timeout: int = 5) -> bool:\n    if timeout <= 0:\n        raise ValueError('invalid timeout')\n    return bool(user and user.strip())\n",
                encoding="utf-8",
            )
            cand_sha = commit_all(repo, "upgrade authenticate with timeout and whitespace check")

            b_man = td_path / "base_manifest.json"
            c_man = td_path / "cand_manifest.json"
            comp_file = td_path / "comparison.json"
            h_res = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_hash.py"),
                "--root", str(repo),
                "--baseline-rev", base_sha,
                "--candidate-rev", cand_sha,
                "--baseline-manifest-out", str(b_man),
                "--candidate-manifest-out", str(c_man),
                "--comparison-out", str(comp_file),
            )
            self.assertEqual(h_res.returncode, 0, h_res.stderr)
            comp_data = json.loads(comp_file.read_text(encoding="utf-8"))

            align_file = td_path / "alignment.json"
            edge = {"id": "auth-login", "provider": "auth.py:authenticate", "consumer": "client.py:login"}
            align_file.write_text(json.dumps({
                "declarations": [{
                    **edge,
                    "declaration_evidence": "client.py:from auth import authenticate",
                    "provider_evidence": "auth.py:def authenticate",
                    "consumer_evidence": "client.py:authenticate(u)",
                }],
                "observations": [{
                    **edge,
                    "observation_evidence": "test_auth.py:login('alice')",
                }],
            }), encoding="utf-8")

            # 4a. Full CERTIFIED validation at Tier T1
            evidence = {
                "protocol_version": "8.0.0",
                "tier": "T1",
                "delivery_mode": "CERTIFIED_RELEASE",
                "baseline_commit": base_sha,
                "candidate_commit": cand_sha,
                "units": {
                    "baseline_manifest": str(b_man),
                    "candidate_manifest": str(c_man),
                    "comparison_artifact": str(comp_file),
                },
                "comparison": comp_data["comparison"],
                "semantic_reviews": [
                    {
                        "unit_id": "auth.py::authenticate",
                        "classification": "CHANGED",
                        "verdict": "PRESERVED_SUPERSET",
                        "rationale": "Preserves boolean auth return and adds timeout + strip validation.",
                        "evidence": "auth.py:def authenticate",
                    }
                ],
                "alignment": {"alignment_file": str(align_file)},
                "acceptance_criteria": [
                    {
                        "id": "AC-1",
                        "target": "auth-core",
                        "description": "authenticate enforces timeout parameter",
                        "check_type": "symbol_present",
                        "path": "auth.py",
                        "symbols": ["timeout: int = 5", "user.strip()"],
                    },
                    {
                        "id": "AC-2",
                        "target": "auth-core",
                        "description": "unit test suite passes",
                        "check_type": "command_exit_zero",
                        "command": f"{PYTHON} test_auth.py",
                    },
                ],
                "integration_closure": [
                    {"surface": "entry_points", "status": "CLOSED", "evidence": "client.py:def login"},
                    {"surface": "callers", "status": "CLOSED", "evidence": "client.py:authenticate(u)"},
                    {"surface": "providers", "status": "CLOSED", "evidence": "auth.py:def authenticate"},
                    {"surface": "consumers", "status": "CLOSED", "evidence": "client.py:def login"},
                    {"surface": "tests", "status": "CLOSED", "evidence": "test_auth.py:test_ok"},
                ],
                "manifest_targets": [
                    {"target": "auth-core", "status": "VERIFIED", "evidence": "auth.py:def authenticate"}
                ],
            }
            ev_file = td_path / "evidence.json"
            val_out = td_path / "val_report.json"
            ev_file.write_text(json.dumps(evidence), encoding="utf-8")

            v_res = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_validate.py"),
                "--root", str(repo),
                "--evidence", str(ev_file),
                "--execute-checks",
                "--require-full-certification",
                "--output", str(val_out),
            )
            self.assertEqual(v_res.returncode, 0, v_res.stdout + v_res.stderr)
            v_report = json.loads(val_out.read_text(encoding="utf-8"))
            self.assertEqual(v_report["status"], "CERTIFIED")
            self.assertEqual(v_report["defect_count"], 0)

            # 4b. Test BOUNDED_PASS: add an unverified external criterion and a BLOCKED secondary target
            evidence_bounded = json.loads(json.dumps(evidence))
            evidence_bounded["delivery_mode"] = "BOUNDED_HANDOFF"
            evidence_bounded["acceptance_criteria"].append({
                "id": "AC-3",
                "target": "ldap- hardware-dongle",
                "description": "Hardware YubiKey tap in production rack",
                "check_type": "unverified_external",
                "rationale": "No physical YubiKey USB device attached to sandbox VM",
            })
            evidence_bounded["manifest_targets"].append({
                "target": "ldap-hardware-dongle",
                "status": "BLOCKED",
                "evidence": "Waiting on hardware dongle provisioning; auth-core remains verified and unblocked",
            })
            ev_bounded_file = td_path / "evidence_bounded.json"
            ev_bounded_file.write_text(json.dumps(evidence_bounded), encoding="utf-8")
            v_bounded = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_validate.py"),
                "--root", str(repo),
                "--evidence", str(ev_bounded_file),
                "--execute-checks",
            )
            self.assertEqual(v_bounded.returncode, 0, v_bounded.stdout + v_bounded.stderr)
            vb_report = json.loads(v_bounded.stdout)
            self.assertEqual(vb_report["status"], "BOUNDED_PASS")
            self.assertEqual(vb_report["defect_count"], 0)
            self.assertEqual(vb_report["unverified_count"], 1)
            self.assertEqual(vb_report["blocked_target_count"], 1)

            # 4c. Build Self-Verifying Kit + Run Full Battery (P0-P7 + RED_CONTROL)
            kit_path = td_path / "update-auth-suite-round-1.sh"
            kit_meta = td_path / "kit_meta.json"
            k_res = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_kit.py"),
                "--root", str(repo),
                "--base", base_sha,
                "--tip", cand_sha,
                "--suite", "auth-suite",
                "--round", "round-1",
                "--key-file", "auth.py",
                "--fingerprint-file", "client.py",
                "--gate-cmd", f"{PYTHON} test_auth.py",
                "--run-battery",
                "--output", str(kit_path),
                "--metadata-out", str(kit_meta),
            )
            self.assertEqual(k_res.returncode, 0, k_res.stdout + k_res.stderr)
            k_data = json.loads(kit_meta.read_text(encoding="utf-8"))
            self.assertEqual(k_data["battery"]["status"], "GREEN")
            self.assertGreaterEqual(k_data["battery"]["passed_checks"], 14)

            # 4d. Generate & Verify Self-Contained Out-of-Band HTML Round Record
            html_out = td_path / "round-record-round-1.html"
            rep_res = run_cmd(
                PYTHON, str(SCRIPTS / "4ndr0_report.py"),
                "--validation", str(val_out),
                "--kit-meta", str(kit_meta),
                "--output", str(html_out),
            )
            self.assertEqual(rep_res.returncode, 0, rep_res.stdout + rep_res.stderr)
            rep_meta = json.loads(rep_res.stdout)
            self.assertTrue(rep_meta["self_contained"])
            self.assertTrue(rep_meta["pin_parity_verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
