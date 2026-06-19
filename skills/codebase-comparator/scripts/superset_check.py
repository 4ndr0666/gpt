#!/usr/bin/env python3
"""
Superset Verification Protocol: Full Implementation
Strict segment/function hashing and manifest-based regression detection.
Author: 4ndr0666
License: MIT/WTFPL/Forcible Assimilation
"""

import hashlib, json, sys, os, argparse
import difflib
from collections import OrderedDict

SEGMENT_SIZE = 500  # lines per segment (customize as needed)

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha256_text(text):
    return sha256_bytes(text.encode('utf-8'))

def segment_file(file_path, segment_size=SEGMENT_SIZE):
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()
    segments = []
    for i in range(0, len(lines), segment_size):
        segment = ''.join(lines[i:i+segment_size])
        segments.append({
            'start': i+1,
            'end': min(i+segment_size, len(lines)),
            'content': segment,
            'sha256': sha256_text(segment)
        })
    return segments, lines

def compute_manifest(file_path, version_tag=None):
    segments, lines = segment_file(file_path)
    manifest = {
        "version": version_tag or os.path.basename(file_path),
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()+'Z',
        "overall_sha256": sha256_text(''.join(lines)),
        "segments": OrderedDict(),
        "file": os.path.abspath(file_path),
        "line_count": len(lines)
    }
    for seg in segments:
        key = f"{seg['start']}-{seg['end']}"
        manifest["segments"][key] = seg["sha256"]
    return manifest

def load_manifest(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OrderedDict)

def save_manifest(manifest, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

def compare_manifests(baseline, candidate):
    report = []
    baseline_segs = baseline["segments"]
    candidate_segs = candidate["segments"]
    all_keys = set(baseline_segs.keys()) | set(candidate_segs.keys())
    for key in sorted(all_keys, key=lambda x: int(x.split('-')[0])):
        b_hash = baseline_segs.get(key)
        c_hash = candidate_segs.get(key)
        if not b_hash and c_hash:
            report.append((key, "NEW", c_hash))
        elif b_hash and not c_hash:
            report.append((key, "MISSING", b_hash))
        elif b_hash == c_hash:
            report.append((key, "UNCHANGED", b_hash))
        else:
            report.append((key, "CHANGED", f"{b_hash[:8]} -> {c_hash[:8]}"))
    return report

def superset_check(baseline_path, candidate_path, baseline_manifest=None, manifest_out=None, verbose=True):
    if not baseline_manifest:
        baseline_manifest = compute_manifest(baseline_path, version_tag="baseline")
        save_manifest(baseline_manifest, "baseline_manifest.json")
    else:
        baseline_manifest = load_manifest(baseline_manifest)
    candidate_manifest = compute_manifest(candidate_path, version_tag="candidate")
    if manifest_out:
        save_manifest(candidate_manifest, manifest_out)

    report = compare_manifests(baseline_manifest, candidate_manifest)
    fail = False
    for key, status, hash_val in report:
        if status == "MISSING":
            print(f"[!] Segment {key} is MISSING in candidate. (hash: {hash_val})")
            fail = True
        elif status == "CHANGED":
            print(f"[!] Segment {key} CHANGED. ({hash_val})")
            b_start, b_end = map(int, key.split('-'))
            with open(baseline_path, 'r', encoding='utf-8', errors='replace') as f:
                b_lines = f.readlines()[b_start-1:b_end]
            with open(candidate_path, 'r', encoding='utf-8', errors='replace') as f:
                c_lines = f.readlines()[b_start-1:b_end]
            diff = list(difflib.unified_diff(b_lines, c_lines, fromfile='baseline', tofile='candidate', lineterm=''))
            if verbose and diff:
                print('\n'.join(diff))
        elif status == "NEW":
            print(f"[+] Segment {key} is NEW in candidate.")
        elif status == "UNCHANGED":
            if verbose:
                print(f"[=] Segment {key} is unchanged.")
    if fail:
        print("\n[FAIL] SUPRSET CHECK FAILED: Regression or segment missing detected.")
        sys.exit(1)
    print("\n[PASS] Superset protocol check complete. No regression found.")

def create_snapshot_checkpoint(file_path, out_manifest):
    manifest = compute_manifest(file_path)
    save_manifest(manifest, out_manifest)
    print(f"Snapshot checkpoint saved to {out_manifest}")

def main():
    parser = argparse.ArgumentParser(description="Superset Verification Protocol: Strict Code Regression Detector")
    parser.add_argument('--baseline', help='Path to baseline (golden) code file')
    parser.add_argument('--candidate', help='Path to candidate (new) code file')
    parser.add_argument('--baseline-manifest', help='Path to existing baseline manifest (optional)', default=None)
    parser.add_argument('--manifest', help='Output manifest for candidate/snapshot')
    parser.add_argument('--snapshot', help='Snapshot mode: just create manifest for file', action='store_true')
    parser.add_argument('--quiet', help='Quiet mode (minimal output)', action='store_true')
    args = parser.parse_args()

    if args.snapshot:
        if not args.candidate or not args.manifest:
            print("Snapshot mode requires --candidate <file> and --manifest <manifest.json>")
            sys.exit(2)
        create_snapshot_checkpoint(args.candidate, args.manifest)
        return

    if not args.baseline or not args.candidate:
        print("Both --baseline and --candidate are required unless in snapshot mode.")
        sys.exit(2)

    superset_check(args.baseline, args.candidate, baseline_manifest=args.baseline_manifest, manifest_out=args.manifest, verbose=not args.quiet)

if __name__ == '__main__':
    main()
