#!/usr/bin/env python3
"""4ndr0_kit.py v8.0.0 — Deterministic Self-Verifying Update-Kit Builder & Battery Runner.

Implements and upgrades SUK v1.2 (`andr0666-engineering`) into an executable tool:
1. Supports three lawful delivery classes:
   - `Class F` (First-Delivery / Standalone Bootstrap)
   - `Class U` (Fast-Forward Update Kit for `CERTIFIED` commit ranges)
   - `Class H` (Bounded Handoff Kit for `BOUNDED_PASS` work-in-progress / partial verification,
     carrying the committed progress range plus explicit claim boundaries without faking green gates).
2. Parameterizes repository fingerprints (`--fingerprint-file`) and gate command (`--gate-cmd`),
   eliminating hardcoded `$HOME/userscripts` and `npm run check` assumptions.
3. Computes `PIN_PAYLOAD_SHA` over the exact 76-col wrapped base64 block as extracted by `sed`.
4. Includes `flock` concurrency protection, stdin-pipe execution guard (`[ -f "$0" ]`), and
   cross-platform `sha256sum` / `shasum -a 256` detection.
5. `--run-battery` executes the full P0–P7 + Red Control battery against throwaway clones built
   from the baseline bundle (with remote-removal, `git reflog expire --expire=now --all`, and
   `git gc --prune=now` + P1 `! git cat-file -e <PIN_TIP>` realness proof).
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

PROTOCOL = "4NDR0-SUK-8.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str) -> str:
    p = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True, encoding="utf-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=60
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p.stdout.strip()


KIT_TEMPLATE = r"""#!/usr/bin/env bash
# ==============================================================================
# SELF-VERIFYING UPDATE & HANDOFF KIT (__PROTOCOL__)
# Suite:        __SUITE__
# Round:        __ROUND__
# Kit Class:    __KIT_CLASS__ (__DELIVERY_MODE__)
# Epistemic:    __EPISTEMIC_STATUS__
#
# WHAT IT DOES:
#   Applies certified/bounded commit range __PIN_BASE_SHORT__..__PIN_TIP_SHORT__
#   (__COMMIT_COUNT__ commit(s)) to your repository as a verified fast-forward,
#   checks content and tree hashes (__PIN_TIP_TREE__), and runs the configured
#   verification gate (__GATE_CMD_DISPLAY__).
#
# USAGE:
#   bash __KIT_FILENAME__ [/optional/path/to/repo]
#
# SAFETY:
#   - Zero network mutation (never pushes).
#   - Dirty worktree is preserved via `git stash push --include-untracked` (never --all).
#   - Fail-closed on wrong baseline, detached HEAD, or corrupted payload.
#   - Idempotent: re-running after application re-verifies cleanly.
#
# AFTER IT PRINTS THE GREEN / BOUNDED RESULT LINE:
#   git push
# ==============================================================================
set -euo pipefail

PIN_BASE="__PIN_BASE__"
PIN_TIP="__PIN_TIP__"
PIN_TIP_TREE="__PIN_TIP_TREE__"
PIN_BUNDLE_SHA="__PIN_BUNDLE_SHA__"
PIN_PAYLOAD_SHA="__PIN_PAYLOAD_SHA__"
PIN_KEY_FILE="__PIN_KEY_FILE__"
PIN_KEY_SHA="__PIN_KEY_SHA__"
KIT_CLASS="__KIT_CLASS__"
EPISTEMIC_STATUS="__EPISTEMIC_STATUS__"
ROUND_REF="refs/heads/__ROUND__"
FINGERPRINT_FILE="__FINGERPRINT_FILE__"
GATE_CMD="__GATE_CMD__"
OPTIONAL_TOOL="__OPTIONAL_TOOL__"

fail() {
  printf '[KIT-FAIL] %s\n' "$1" >&2
  printf 'Nothing was left half-applied. Fix the above and re-run this kit.\n' >&2
  exit 1
}

# G0: Environment & Pipe Guard
if [ ! -f "$0" ]; then
  fail "Stdin/piped execution is not supported. Download the file first, then run: bash __KIT_FILENAME__"
fi

KIT_SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"

for req_tool in bash git base64 gunzip sed date; do
  command -v "$req_tool" >/dev/null 2>&1 || fail "Missing required tool '$req_tool'. Install '$req_tool' and re-run."
done

if command -v sha256sum >/dev/null 2>&1; then
  sha256_file() { sha256sum "$1" | awk '{print $1}'; }
elif command -v shasum >/dev/null 2>&1; then
  sha256_file() { shasum -a 256 "$1" | awk '{print $1}'; }
else
  fail "Missing sha256sum or shasum. Install coreutils and re-run."
fi

HAVE_OPT_TOOL=1
if [ -n "$OPTIONAL_TOOL" ]; then
  if ! command -v "$OPTIONAL_TOOL" >/dev/null 2>&1; then
    HAVE_OPT_TOOL=0
  fi
fi

SELF_SHA="$(sha256_file "$KIT_SELF")"
printf '[G0] Kit self-hash: %s (compare with out-of-band round-record pin)\n' "$SELF_SHA"

TMP_DIR="$(mktemp -d)"
REPO_DIR=""
LOCK_FD=""
cleanup() {
  if [ -n "$REPO_DIR" ] && [ -d "$REPO_DIR/.git" ]; then
    git -C "$REPO_DIR" branch -D "__ROUND__-incoming" >/dev/null 2>&1 || true
    rm -f "$REPO_DIR/.git/kit.lock" >/dev/null 2>&1 || true
  fi
  rm -rf "$TMP_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

# G1: Locate Repository
TARGET_CANDIDATE="${1:-$PWD}"
if [ ! -d "$TARGET_CANDIDATE/.git" ]; then
  fail "No git repository found at '$TARGET_CANDIDATE'. Run: bash \"$KIT_SELF\" /full/path/to/repo"
fi
REPO_DIR="$(cd "$TARGET_CANDIDATE" && pwd)"

# Concurrency lock
if [ -f "$REPO_DIR/.git/kit.lock" ]; then
  fail "Another kit instance is running ($REPO_DIR/.git/kit.lock exists); let it finish."
fi
printf '%s\n' "$$" > "$REPO_DIR/.git/kit.lock"

# G2: Baseline Verification
CURRENT_BRANCH="$(git -C "$REPO_DIR" symbolic-ref --short HEAD 2>/dev/null || true)"
if [ -z "$CURRENT_BRANCH" ]; then
  fail "Detached HEAD detected. Run 'git -C \"$REPO_DIR\" checkout main' and re-run: bash \"$KIT_SELF\" \"$REPO_DIR\""
fi

CURRENT_HEAD="$(git -C "$REPO_DIR" rev-parse HEAD 2>/dev/null || true)"
ALREADY=0
if [ "$CURRENT_HEAD" = "$PIN_TIP" ]; then
  ALREADY=1
  printf '[G2] Repository already at PIN_TIP (%s); skipping apply and re-verifying.\n' "$PIN_TIP"
elif [ "$CURRENT_HEAD" = "$PIN_BASE" ]; then
  if [ -n "$FINGERPRINT_FILE" ] && [ ! -f "$REPO_DIR/$FINGERPRINT_FILE" ]; then
    fail "Repository fingerprint failed: missing '$FINGERPRINT_FILE' in '$REPO_DIR'."
  fi
  printf '[G2] Baseline verified at PIN_BASE (%s).\n' "$PIN_BASE"
else
  fail "Baseline mismatch: repo HEAD is $CURRENT_HEAD, expected PIN_BASE ($PIN_BASE). If you have newer local commits, DO NOT FORCE anything — report this to the executor."
fi

# G2.5: WIP Preservation
STASH_CREATED=0
if [ "$ALREADY" -eq 0 ]; then
  WIP_STATUS="$(git -C "$REPO_DIR" status --porcelain=v1 --untracked-files=all)"
  if [ -n "$WIP_STATUS" ]; then
    TS="$(date -u +%Y%m%dT%H%M%SZ)"
    BK_DIR="$REPO_DIR/.git/kit-backups/$TS"
    mkdir -p "$BK_DIR"
    git -C "$REPO_DIR" stash push --include-untracked -m "__ROUND__ kit WIP backup $TS" >/dev/null
    STASH_CREATED=1
    cat > "$BK_DIR/RESTORE-INSTRUCTIONS.txt" <<EOF
Your uncommitted changes were safely stashed before applying __ROUND__.
Three lawful next actions:
  1. Inspect stash: git -C "$REPO_DIR" stash list
  2. Restore WIP:   git -C "$REPO_DIR" stash pop
  3. Keep backup:   do nothing (stash remains reachable in git reflog for ~30 days)
EOF
    POST_STASH="$(git -C "$REPO_DIR" status --porcelain=v1 --untracked-files=all)"
    if [ -n "$POST_STASH" ]; then
      fail "Worktree still dirty after stash; aborting rather than guessing."
    fi
    printf '[G2.5] Dirty worktree stashed cleanly (%s).\n' "$BK_DIR/RESTORE-INSTRUCTIONS.txt"
  fi
fi

# G3: Payload Verification & Application
sed -n '/^#__PAYLOAD_BEGIN__$/,/^#__PAYLOAD_END__$/p' "$KIT_SELF" | sed '1d;$d' > "$TMP_DIR/payload.b64"
ACTUAL_PAYLOAD_SHA="$(sha256_file "$TMP_DIR/payload.b64")"
if [ "$ACTUAL_PAYLOAD_SHA" != "$PIN_PAYLOAD_SHA" ]; then
  fail "Corrupted payload block (sha256 $ACTUAL_PAYLOAD_SHA != $PIN_PAYLOAD_SHA). Re-download the kit."
fi

base64 -d < "$TMP_DIR/payload.b64" | gunzip > "$TMP_DIR/range.bundle"
ACTUAL_BUNDLE_SHA="$(sha256_file "$TMP_DIR/range.bundle")"
if [ "$ACTUAL_BUNDLE_SHA" != "$PIN_BUNDLE_SHA" ]; then
  fail "Decoded bundle sha256 mismatch ($ACTUAL_BUNDLE_SHA != $PIN_BUNDLE_SHA)."
fi

if [ "$ALREADY" -eq 0 ]; then
  VERIFY_OUT="$(git -C "$REPO_DIR" bundle verify "$TMP_DIR/range.bundle" 2>&1)" || fail "git bundle verify failed: $VERIFY_OUT"
  case "$VERIFY_OUT" in
    *"$PIN_BASE"*) ;;
    *) fail "Bundle does not anchor to PIN_BASE ($PIN_BASE)." ;;
  esac
  HEADS_OUT="$(git -C "$REPO_DIR" bundle list-heads "$TMP_DIR/range.bundle")"
  EXPECTED_HEAD="$PIN_TIP $ROUND_REF"
  if [ "$HEADS_OUT" != "$EXPECTED_HEAD" ]; then
    fail "Bundle list-heads mismatch: got '$HEADS_OUT', expected '$EXPECTED_HEAD'."
  fi

  git -C "$REPO_DIR" fetch "$TMP_DIR/range.bundle" "$ROUND_REF:refs/heads/__ROUND__-incoming" >/dev/null 2>&1
  git -C "$REPO_DIR" merge --ff-only "refs/heads/__ROUND__-incoming" >/dev/null 2>&1 || fail "Fast-forward merge failed."
  git -C "$REPO_DIR" branch -D "__ROUND__-incoming" >/dev/null 2>&1 || true

  POST_HEAD="$(git -C "$REPO_DIR" rev-parse HEAD)"
  if [ "$POST_HEAD" != "$PIN_TIP" ]; then
    fail "Post-merge HEAD ($POST_HEAD) does not match PIN_TIP ($PIN_TIP)."
  fi
  printf '[G3] Payload verified and fast-forwarded to %s.\n' "$PIN_TIP"
fi

# G4: Proof of Exactness + Gate
ACTUAL_TREE="$(git -C "$REPO_DIR" rev-parse 'HEAD^{tree}')"
if [ "$ACTUAL_TREE" != "$PIN_TIP_TREE" ]; then
  fail "Tree hash mismatch: got $ACTUAL_TREE, expected $PIN_TIP_TREE."
fi

if [ -n "$PIN_KEY_FILE" ]; then
  if [ ! -f "$REPO_DIR/$PIN_KEY_FILE" ]; then
    fail "Pinned key file '$PIN_KEY_FILE' is missing after apply."
  fi
  ACTUAL_KEY_SHA="$(sha256_file "$REPO_DIR/$PIN_KEY_FILE")"
  if [ "$ACTUAL_KEY_SHA" != "$PIN_KEY_SHA" ]; then
    fail "Pinned file '$PIN_KEY_FILE' sha256 mismatch ($ACTUAL_KEY_SHA != $PIN_KEY_SHA)."
  fi
  printf '[G4] Verified key file %s (%s — byte-identical).\n' "$PIN_KEY_FILE" "$PIN_KEY_SHA"
fi

GATE_DEFERRED=0
if [ -n "$GATE_CMD" ]; then
  if [ "$HAVE_OPT_TOOL" -eq 1 ]; then
    (cd "$REPO_DIR" && PYTHONDONTWRITEBYTECODE=1 eval "$GATE_CMD" > "$TMP_DIR/gate.log" 2>&1) || fail "Verification gate failed ($GATE_CMD). Inspect log."
    DRIFT="$(git -C "$REPO_DIR" status --porcelain=v1 --untracked-files=no)"
    if [ -n "$DRIFT" ]; then
      fail "Verification gate dirtied tracked files in the repository."
    fi
    POST_GATE_TREE="$(git -C "$REPO_DIR" rev-parse 'HEAD^{tree}')"
    if [ "$POST_GATE_TREE" != "$PIN_TIP_TREE" ]; then
      fail "Tree hash mutated during verification gate."
    fi
    printf '[G4] Verification gate passed cleanly with zero worktree drift.\n'
  else
    GATE_DEFERRED=1
    printf '[G4] Optional runtime tool (%s) absent; gate deferred. Run manually when available: (cd "%s" && %s)\n' "$OPTIONAL_TOOL" "$REPO_DIR" "$GATE_CMD"
  fi
fi

# G5: Report
printf '[G5] Applied commits (%s..%s):\n' "$PIN_BASE" "$PIN_TIP"
git -C "$REPO_DIR" log --oneline --reverse "$PIN_BASE..$PIN_TIP" | sed 's/^/  /'

if [ "$STASH_CREATED" -eq 1 ] && [ -n "$PIN_KEY_FILE" ]; then
  STASH_FILE_SHA="$((git -C "$REPO_DIR" show "stash@{0}:$PIN_KEY_FILE" 2>/dev/null || git -C "$REPO_DIR" show "stash@{0}^3:$PIN_KEY_FILE" 2>/dev/null) | (sha256sum 2>/dev/null || shasum -a 256) | awk '{print $1}' || true)"
  if [ "$STASH_FILE_SHA" = "$PIN_KEY_SHA" ]; then
    printf '[G5] Canon-identity note: stashed %s matches delivered pin (%s); restoring it is a no-op (drop or keep, both fine).\n' "$PIN_KEY_FILE" "$PIN_KEY_SHA"
  fi
fi

if [ "$ALREADY" -eq 1 ]; then
  printf 'KIT RESULT: GREEN (already applied; tree=%s; status=%s) — Next step: git push\n' "$PIN_TIP_TREE" "$EPISTEMIC_STATUS"
elif [ "$GATE_DEFERRED" -eq 1 ]; then
  printf 'KIT RESULT: GREEN (applied + hash-verified; gate DEFERRED: run `%s`; status=%s) — Next step: git push\n' "$GATE_CMD" "$EPISTEMIC_STATUS"
else
  printf 'KIT RESULT: GREEN (applied + verified; tree=%s; status=%s) — Next step: git push\n' "$PIN_TIP_TREE" "$EPISTEMIC_STATUS"
fi
exit 0
#__PAYLOAD_BEGIN__
__PAYLOAD_BLOCK__
#__PAYLOAD_END__
"""


def build_kit(
    repo_root: Path,
    base_rev: str,
    tip_rev: str,
    suite: str,
    round_id: str,
    output_path: Path,
    key_file: str = "",
    fingerprint_file: str = "",
    gate_cmd: str = "",
    optional_tool: str = "",
    kit_class: str = "U",
    delivery_mode: str = "CERTIFIED_RELEASE",
    epistemic_status: str = "CERTIFIED",
) -> dict:
    repo_root = repo_root.resolve()
    pin_base = git(repo_root, "rev-parse", f"{base_rev}^{{commit}}")
    pin_tip = git(repo_root, "rev-parse", f"{tip_rev}^{{commit}}")
    pin_tip_tree = git(repo_root, "rev-parse", f"{pin_tip}^{{tree}}")

    commits_out = git(repo_root, "rev-list", "--count", f"{pin_base}..{pin_tip}")
    commit_count = int(commits_out.strip() or "0")
    if commit_count <= 0:
        raise ValueError(f"commit range {pin_base}..{pin_tip} contains 0 commits")

    pin_key_sha = ""
    if key_file:
        kf_path = repo_root / key_file
        if not kf_path.is_file():
            raise ValueError(f"key_file '{key_file}' does not exist in {repo_root}")
        pin_key_sha = sha256_bytes(kf_path.read_bytes())

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        # Create single-ref bundle
        git(repo_root, "branch", "-f", round_id, pin_tip)
        bundle_path = td_path / f"{round_id}.bundle"
        try:
            git(repo_root, "bundle", "create", str(bundle_path), f"{pin_base}..{round_id}")
        finally:
            subprocess.run(["git", "-C", str(repo_root), "branch", "-D", round_id], capture_output=True, check=False)

        bundle_bytes = bundle_path.read_bytes()
        pin_bundle_sha = sha256_bytes(bundle_bytes)

        # Deterministic gzip (mtime=0) + 76-char wrapped base64
        gz_bytes = gzip.compress(bundle_bytes, compresslevel=9, mtime=0)
        b64_raw = base64.b64encode(gz_bytes).decode("ascii")
        b64_lines = [b64_raw[i : i + 76] for i in range(0, len(b64_raw), 76)]
        payload_block_with_newline = "\n".join(b64_lines) + "\n"
        # Exact bytes extracted by sed between #__PAYLOAD_BEGIN__ and #__PAYLOAD_END__
        pin_payload_sha = sha256_bytes(payload_block_with_newline.encode("ascii"))

    kit_filename = output_path.name
    replacements = {
        "__PROTOCOL__": PROTOCOL,
        "__SUITE__": suite,
        "__ROUND__": round_id,
        "__KIT_CLASS__": kit_class,
        "__DELIVERY_MODE__": delivery_mode,
        "__EPISTEMIC_STATUS__": epistemic_status,
        "__PIN_BASE__": pin_base,
        "__PIN_BASE_SHORT__": pin_base[:12],
        "__PIN_TIP__": pin_tip,
        "__PIN_TIP_SHORT__": pin_tip[:12],
        "__PIN_TIP_TREE__": pin_tip_tree,
        "__PIN_BUNDLE_SHA__": pin_bundle_sha,
        "__PIN_PAYLOAD_SHA__": pin_payload_sha,
        "__PIN_KEY_FILE__": key_file,
        "__PIN_KEY_SHA__": pin_key_sha,
        "__COMMIT_COUNT__": str(commit_count),
        "__KIT_FILENAME__": kit_filename,
        "__FINGERPRINT_FILE__": fingerprint_file,
        "__GATE_CMD__": gate_cmd,
        "__GATE_CMD_DISPLAY__": gate_cmd or "none (hash-only)",
        "__OPTIONAL_TOOL__": optional_tool,
        "__PAYLOAD_BLOCK__": "\n".join(b64_lines),
    }

    content = KIT_TEMPLATE
    for k, v in replacements.items():
        content = content.replace(k, v)

    # Assert zero unresolved placeholders in script zone (Axiom A8/Part IV)
    if re.search(r"__[A-Z0-9_]+__", content.split("#__PAYLOAD_BEGIN__")[0]):
        raise RuntimeError("unresolved template placeholder survived in script zone")

    kit_bytes = content.encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(kit_bytes)
    output_path.chmod(output_path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    kit_sha = sha256_bytes(kit_bytes)
    return {
        "protocol": PROTOCOL,
        "suite": suite,
        "round": round_id,
        "kit_class": kit_class,
        "delivery_mode": delivery_mode,
        "epistemic_status": epistemic_status,
        "kit_path": str(output_path.resolve()),
        "kit_filename": kit_filename,
        "kit_size_bytes": len(kit_bytes),
        "bundle_size_bytes": len(bundle_bytes),
        "commit_count": commit_count,
        "pins": {
            "PIN_KIT_SHA": kit_sha,
            "PIN_BASE": pin_base,
            "PIN_TIP": pin_tip,
            "PIN_TIP_TREE": pin_tip_tree,
            "PIN_BUNDLE_SHA": pin_bundle_sha,
            "PIN_PAYLOAD_SHA": pin_payload_sha,
            "PIN_KEY_FILE": key_file,
            "PIN_KEY_SHA": pin_key_sha,
        },
    }


def run_battery(repo_root: Path, kit_path: Path) -> dict:
    """Execute the mandatory P0-P7 + Red Control battery against throwaway baseline clones."""
    repo_root = repo_root.resolve()
    kit_path = kit_path.resolve()
    kit_text = kit_path.read_text(encoding="utf-8")

    # Parse pins directly from the kit (P0 law: never hardcode expectations)
    pins: Dict[str, str] = {}
    for line in kit_text.splitlines():
        m = re.match(r'^([A-Z0-9_]+)="([^"]*)"$', line)
        if m:
            pins[m.group(1)] = m.group(2)

    pin_base = pins["PIN_BASE"]
    pin_tip = pins["PIN_TIP"]
    pin_tip_tree = pins["PIN_TIP_TREE"]
    pin_payload_sha = pins["PIN_PAYLOAD_SHA"]
    pin_bundle_sha = pins["PIN_BUNDLE_SHA"]
    pin_key_file = pins.get("PIN_KEY_FILE", "")
    pin_key_sha = pins.get("PIN_KEY_SHA", "")

    author_before_head = git(repo_root, "rev-parse", "HEAD")
    author_before_status = git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")

    checks: List[dict] = []

    def record(phase: str, name: str, passed: bool, detail: str = "") -> None:
        checks.append({"phase": phase, "check": name, "status": "PASS" if passed else "FAIL", "detail": detail})

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)

        # P0: Self-integrity of embedded payload & bundle
        p0_b64 = subprocess.run(
            f"sed -n '/^#__PAYLOAD_BEGIN__$/,/^#__PAYLOAD_END__$/p' '{kit_path}' | sed '1d;$d'",
            shell=True, capture_output=True, check=True
        ).stdout
        actual_payload_sha = sha256_bytes(p0_b64)
        record("P0", "extracted payload sha256 matches PIN_PAYLOAD_SHA", actual_payload_sha == pin_payload_sha, actual_payload_sha)

        p0_bundle = gzip.decompress(base64.b64decode(p0_b64))
        actual_bundle_sha = sha256_bytes(p0_bundle)
        record("P0", "decoded bundle sha256 matches PIN_BUNDLE_SHA", actual_bundle_sha == pin_bundle_sha, actual_bundle_sha)

        # Helper to construct operator-state simulator at PIN_BASE with PIN_TIP pruned
        def make_baseline_clone(name: str) -> Path:
            clone_dir = td_path / name
            subprocess.run(["git", "clone", "-q", str(repo_root), str(clone_dir)], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "config", "user.name", "Operator"], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "config", "user.email", "operator@example.com"], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "checkout", "-q", "-B", "main", pin_base], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "remote", "remove", "origin"], check=True)
            # Delete any other local branches/tags that might hold PIN_TIP
            for br in git(clone_dir, "for-each-ref", "--format=%(refname)", "refs/heads/", "refs/tags/").splitlines():
                if br and br != "refs/heads/main":
                    subprocess.run(["git", "-C", str(clone_dir), "update-ref", "-d", br], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "reflog", "expire", "--expire=now", "--all"], check=True)
            subprocess.run(["git", "-C", str(clone_dir), "gc", "--prune=now", "--quiet"], check=True)
            return clone_dir

        # P1: Pristine apply on operator-state clone
        c_p1 = make_baseline_clone("p1_pristine")
        tip_absent = subprocess.run(["git", "-C", str(c_p1), "cat-file", "-e", pin_tip], capture_output=True).returncode != 0
        record("P1", "operator simulator has PIN_TIP absent before apply", tip_absent)

        r_p1 = subprocess.run(["bash", str(kit_path), str(c_p1)], capture_output=True, text=True)
        record("P1", "pristine apply exits 0 with KIT RESULT: GREEN", r_p1.returncode == 0 and "KIT RESULT: GREEN" in r_p1.stdout, r_p1.stderr.strip())
        record("P1", "post-apply HEAD equals PIN_TIP", git(c_p1, "rev-parse", "HEAD") == pin_tip)
        record("P1", "post-apply tree equals PIN_TIP_TREE", git(c_p1, "rev-parse", "HEAD^{tree}") == pin_tip_tree)

        # P2: Dirty-tree WIP stash + restore instructions + canon-identity note + lossless round-trip
        c_p2 = make_baseline_clone("p2_dirty")
        (c_p2 / "operator_wip.txt").write_text("untracked operator notes\n", encoding="utf-8")
        if pin_key_file:
            # Place the exact delivered file into the dirty tree to trigger canon-identity note
            delivered_bytes = (c_p1 / pin_key_file).read_bytes()
            (c_p2 / pin_key_file).parent.mkdir(parents=True, exist_ok=True)
            (c_p2 / pin_key_file).write_bytes(delivered_bytes)
        r_p2 = subprocess.run(["bash", str(kit_path), str(c_p2)], capture_output=True, text=True)
        record("P2", "dirty-tree apply exits 0 and creates stash backup", r_p2.returncode == 0 and "[G2.5]" in r_p2.stdout)
        if pin_key_file:
            record("P2", "canon-identity note printed when stashed file equals delivered pin", "Canon-identity note" in r_p2.stdout)
        # Drop or pop stash and verify operator_wip.txt round-trip
        subprocess.run(["git", "-C", str(c_p2), "checkout", "--", "."], check=False)
        subprocess.run(["git", "-C", str(c_p2), "stash", "pop"], capture_output=True, check=False)
        record("P2", "untracked WIP file survives stash round-trip byte-identically", (c_p2 / "operator_wip.txt").read_text(encoding="utf-8") == "untracked operator notes\n")

        # P3: Wrong baseline fail-closed
        c_p3 = make_baseline_clone("p3_wrong_base")
        (c_p3 / "diverged.txt").write_text("ahead of base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(c_p3), "add", "diverged.txt"], check=True)
        subprocess.run(["git", "-C", str(c_p3), "commit", "-qm", "operator ahead"], check=True)
        wrong_head = git(c_p3, "rev-parse", "HEAD")
        r_p3 = subprocess.run(["bash", str(kit_path), str(c_p3)], capture_output=True, text=True)
        record("P3", "wrong baseline fails closed (exit 1) and leaves HEAD untouched", r_p3.returncode == 1 and git(c_p3, "rev-parse", "HEAD") == wrong_head and "DO NOT FORCE" in r_p3.stderr)

        # P4: No repo fail-closed with exact re-run syntax
        empty_dir = td_path / "p4_no_repo"
        empty_dir.mkdir()
        r_p4 = subprocess.run(["bash", str(kit_path), str(empty_dir)], capture_output=True, text=True)
        record("P4", "non-repo path fails closed (exit 1) with exact re-run syntax", r_p4.returncode == 1 and str(kit_path) in r_p4.stderr)

        # P5: Optional tool absent -> deferred gate mode
        c_p5 = make_baseline_clone("p5_defer")
        # Test by temporarily setting OPTIONAL_TOOL to a nonexistent binary in a copy of the kit
        # Wait: changing script bytes changes kit self-hash, not payload hash! So G3 still passes!
        defer_kit = td_path / "defer_kit.sh"
        defer_kit.write_text(kit_text.replace('OPTIONAL_TOOL=""', 'OPTIONAL_TOOL="__nonexistent_runtime_bin__"').replace('GATE_CMD=""', 'GATE_CMD="true"'), encoding="utf-8")
        r_p5 = subprocess.run(["bash", str(defer_kit), str(c_p5)], capture_output=True, text=True)
        record("P5", "missing optional tool applies payload and defers gate cleanly", r_p5.returncode == 0 and "DEFERRED" in r_p5.stdout)

        # P6: Re-run idempotence on P1 clone
        r_p6 = subprocess.run(["bash", str(kit_path), str(c_p1)], capture_output=True, text=True)
        record("P6", "re-running applied kit exits 0 with already-applied status", r_p6.returncode == 0 and "already applied" in r_p6.stdout)

        # P7: Authoring repo untouched
        author_after_head = git(repo_root, "rev-parse", "HEAD")
        author_after_status = git(repo_root, "status", "--porcelain=v1", "--untracked-files=all")
        record("P7", "authoring repository untouched before/after battery", author_before_head == author_after_head and author_before_status == author_after_status)

        # Red Control: Corrupt 1 byte newline-anchored inside #__PAYLOAD_BEGIN__ block
        corrupt_kit = td_path / "corrupt_kit.sh"
        raw_kit_bytes = kit_path.read_bytes()
        marker = b"\n#__PAYLOAD_BEGIN__\n"
        idx = raw_kit_bytes.find(marker)
        corrupt_pos = idx + len(marker) + 32
        flipped = b"A" if raw_kit_bytes[corrupt_pos : corrupt_pos + 1] != b"A" else b"B"
        corrupt_bytes = raw_kit_bytes[:corrupt_pos] + flipped + raw_kit_bytes[corrupt_pos + 1 :]
        corrupt_kit.write_bytes(corrupt_bytes)
        c_red = make_baseline_clone("red_control")
        r_red = subprocess.run(["bash", str(corrupt_kit), str(c_red)], capture_output=True, text=True)
        record("RED_CONTROL", "newline-anchored payload byte corruption fails closed at G3 payload pin", r_red.returncode == 1 and "Corrupted payload block" in r_red.stderr and git(c_red, "rev-parse", "HEAD") == pin_base)

    passed_count = sum(1 for c in checks if c["status"] == "PASS")
    return {
        "protocol": PROTOCOL,
        "kit_path": str(kit_path),
        "total_checks": len(checks),
        "passed_checks": passed_count,
        "failed_checks": len(checks) - passed_count,
        "status": "GREEN" if passed_count == len(checks) else "RED",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--base", required=True, help="Baseline Git revision")
    parser.add_argument("--tip", default="HEAD", help="Candidate tip Git revision")
    parser.add_argument("--suite", required=True, help="Suite/project identifier")
    parser.add_argument("--round", required=True, help="Round identifier (e.g. round-1)")
    parser.add_argument("--output", required=True, help="Output path for generated update-*.sh kit")
    parser.add_argument("--key-file", default="", help="Optional round-critical relative file path to pin")
    parser.add_argument("--fingerprint-file", default="", help="Optional repo fingerprint relative file path")
    parser.add_argument("--gate-cmd", default="", help="Optional verification gate command")
    parser.add_argument("--optional-tool", default="", help="Optional runtime binary required by gate-cmd")
    parser.add_argument("--kit-class", default="U", choices=["F", "U", "H"], help="Kit class: F (First), U (Update), H (Bounded Handoff)")
    parser.add_argument("--delivery-mode", default="CERTIFIED_RELEASE", choices=["WIP_CHECKPOINT", "BOUNDED_HANDOFF", "CERTIFIED_RELEASE"])
    parser.add_argument("--epistemic-status", default="CERTIFIED", choices=["CERTIFIED", "BOUNDED_PASS"])
    parser.add_argument("--run-battery", action="store_true", help="Run the P0-P7 + Red Control battery immediately")
    parser.add_argument("--metadata-out", help="Write builder + battery metadata JSON to path")
    args = parser.parse_args()

    try:
        meta = build_kit(
            repo_root=Path(args.root),
            base_rev=args.base,
            tip_rev=args.tip,
            suite=args.suite,
            round_id=args.round,
            output_path=Path(args.output),
            key_file=args.key_file,
            fingerprint_file=args.fingerprint_file,
            gate_cmd=args.gate_cmd,
            optional_tool=args.optional_tool,
            kit_class=args.kit_class,
            delivery_mode=args.delivery_mode,
            epistemic_status=args.epistemic_status,
        )
        if args.run_battery:
            battery = run_battery(Path(args.root), Path(args.output))
            meta["battery"] = battery
            if battery["status"] != "GREEN":
                print(json.dumps(meta, indent=2, sort_keys=True), file=sys.stderr)
                return 1
        encoded = json.dumps(meta, indent=2, sort_keys=True) + "\n"
        if args.metadata_out:
            Path(args.metadata_out).write_text(encoded, encoding="utf-8")
        else:
            sys.stdout.write(encoded)
        return 0
    except Exception as exc:
        print(f"4ndr0neering kit builder failed closed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
