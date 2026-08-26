#!/usr/bin/env python3
"""
golden_unit_hash.py — Named-unit hashing and three-way classification
for the Golden-Unit Protocol (v2).

This script implements §1 (atomization) and the hashing half of §2/§3
ONLY. It deliberately does NOT attempt the digest comparison in §3
("does the new digest semantically contain everything the old one
guaranteed?") or the architectural gate in §4 — those require reading
and judgment, not string comparison, and the protocol is explicit that
collapsing them into the hash check is itself a violation (§3, final
paragraph). Claude performs those steps; this script only produces the
MISSING / UNCHANGED / CHANGED skeleton for it to reason over.

Units are identified by NAME, never by position. A line-range window
(e.g. "lines 501-1000") is exactly the anti-pattern §1 rules out, so
this script refuses to fall back to fixed-size segmentation. If a
language has no parser support here, units must be supplied manually
as named blocks (see --manual-units below).

Supported automatic extraction: Python (functions, classes, methods)
and JavaScript/TypeScript (function declarations, class declarations,
arrow functions assigned to a const/let/var, methods) via simple
brace/indent-aware parsing — not a full AST, but enough to get stable
names and literal spans for hashing.

For any other domain (prose claims, math lemmas, contract clauses),
supply units manually as a JSON list:
  [{"name": "Lemma 3.2", "content": "..."}]
via --manual-units <file.json>, and this script will hash and diff
them the same way.

Usage:
  # Auto-extract units from a baseline and a candidate file, compare:
  python3 golden_unit_hash.py --baseline old.py --candidate new.py

  # Just produce a manifest for one file (no comparison):
  python3 golden_unit_hash.py --baseline old.py --manifest-only

  # Manual units (any domain):
  python3 golden_unit_hash.py --manual-units baseline_units.json \\
                               --manual-units-candidate candidate_units.json

Output: JSON to stdout with the manifest(s) and, if both sides are
given, a per-unit verdict list. Claude reads this and fills in digest,
class, and the §4 gate — this script never invents those fields.
"""

import argparse
import ast
import hashlib
import json
import re
import sys
from typing import Dict, List, Optional, Tuple


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Python extraction — uses the real ast module, so names are exact and spans
# are taken from the original source via line numbers (no re-serialization,
# which would normalize whitespace/comments and silently change the hash
# basis).
# ---------------------------------------------------------------------------

def extract_python_units(source: str) -> Dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}

    def span_text(node) -> str:
        start = node.lineno - 1
        end = getattr(node, "end_lineno", node.lineno)
        return "".join(lines[start:end])

    def qualified_name(node, prefix: str) -> str:
        return f"{prefix}{node.name}" if prefix else node.name

    def walk(node, prefix=""):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = qualified_name(child, prefix)
                units[name] = span_text(child)
                # Methods inside this function (nested defs) get a dotted
                # name too, but don't double-walk into unrelated scopes.
                walk(child, prefix=f"{name}.")
            elif isinstance(child, ast.ClassDef):
                name = qualified_name(child, prefix)
                units[name] = span_text(child)
                walk(child, prefix=f"{name}.")
            else:
                walk(child, prefix=prefix)

    walk(tree)
    return units


# ---------------------------------------------------------------------------
# JS/TS extraction — no AST available without extra deps, so this uses a
# brace-matching scan anchored on common declaration patterns. It is
# intentionally conservative: it only claims a unit when it finds one of a
# small set of unambiguous patterns, and always recovers the literal source
# span via brace counting rather than guessing line counts.
# ---------------------------------------------------------------------------

_JS_PATTERNS = [
    re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\("),
    re.compile(r"^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)\b"),
    re.compile(
        r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*"
        r"(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*\{"
    ),
    re.compile(
        r"^\s*(?:async\s+)?([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{"
    ),  # method shorthand inside a class
]


def _find_matching_brace(text: str, open_idx: int) -> int:
    depth = 0
    i = open_idx
    in_str: Optional[str] = None
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        elif ch in ("'", '"', "`"):
            in_str = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


_JS_FUNCTION_PATTERN = _JS_PATTERNS[0]
_JS_CLASS_PATTERN = _JS_PATTERNS[1]
_JS_ARROW_CONST_PATTERN = _JS_PATTERNS[2]
_JS_METHOD_PATTERN = _JS_PATTERNS[3]


def extract_js_units(source: str) -> Dict[str, str]:
    """Scan top-down, tracking which class (if any) the current line falls
    inside via brace depth, so methods are recorded as 'ClassName.method'
    instead of a bare name that could collide across unrelated classes —
    the same qualification convention extract_python_units uses.
    """
    units: Dict[str, str] = {}
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    # Stack of (class_name, brace_depth_at_entry) so nested classes work too.
    class_stack: List[Tuple[str, int]] = []
    depth = 0

    for line_no, line in enumerate(lines):
        current_class = class_stack[-1][0] if class_stack else ""

        class_m = _JS_CLASS_PATTERN.match(line)
        if class_m:
            name = class_m.group(1)
            brace_col = line.find("{")
            if brace_col != -1:
                abs_open = offsets[line_no] + brace_col
                abs_close = _find_matching_brace(source, abs_open)
                if abs_close != -1:
                    qualified = f"{current_class}.{name}" if current_class else name
                    units.setdefault(qualified, source[offsets[line_no]:abs_close + 1])
                    class_stack.append((qualified, depth))
            depth += line.count("{") - line.count("}")
            continue

        # Only attempt function/arrow/method matches while not re-matching
        # the class line itself (handled above).
        matched = False
        for pattern, is_method_shorthand in (
            (_JS_FUNCTION_PATTERN, False),
            (_JS_ARROW_CONST_PATTERN, False),
            (_JS_METHOD_PATTERN, True),
        ):
            m = pattern.match(line)
            if not m:
                continue
            # Method shorthand only counts inside a class body; otherwise
            # it's ambiguous with object-literal methods and other syntax
            # this script doesn't attempt to disambiguate, so skip it.
            if is_method_shorthand and not current_class:
                continue
            name = m.group(1)
            brace_col = line.find("{", m.end() - 1)
            if brace_col == -1:
                continue
            abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close == -1:
                continue
            unit_text = source[offsets[line_no]:abs_close + 1]
            qualified = f"{current_class}.{name}" if (is_method_shorthand and current_class) else name
            units.setdefault(qualified, unit_text)
            matched = True
            break

        depth_before = depth
        depth += line.count("{") - line.count("}")
        if matched:
            continue

        # Pop class scope once we've closed back past the class's own depth.
        while class_stack and depth <= class_stack[-1][1]:
            class_stack.pop()

    return units


# ---------------------------------------------------------------------------
# Manifest + diff
# ---------------------------------------------------------------------------

def build_manifest(units: Dict[str, str]) -> List[dict]:
    return [
        {"unit": name, "hash": sha256_text(content)}
        for name, content in sorted(units.items())
    ]


def extract_units(path: str, language: Optional[str]) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    lang = language
    if lang is None:
        if path.endswith(".py"):
            lang = "python"
        elif path.endswith((".js", ".jsx", ".ts", ".tsx")):
            lang = "js"
        else:
            raise ValueError(
                f"Cannot auto-detect language for {path}. Pass --language "
                f"explicitly, or use --manual-units for non-code domains "
                f"(prose, math, contracts, etc.) since this script only "
                f"parses Python and JS/TS automatically."
            )

    if lang == "python":
        return extract_python_units(source)
    elif lang == "js":
        return extract_js_units(source)
    else:
        raise ValueError(f"Unsupported language: {lang}")


def load_manual_units(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    units = {}
    for entry in data:
        units[entry["name"]] = entry["content"]
    return units


def diff_manifests(
    baseline: Dict[str, str], candidate: Dict[str, str]
) -> List[dict]:
    all_names = sorted(set(baseline) | set(candidate))
    report = []
    for name in all_names:
        b = baseline.get(name)
        c = candidate.get(name)
        if b is not None and c is None:
            report.append({"unit": name, "verdict": "MISSING", "hash": sha256_text(b)})
        elif b is None and c is not None:
            report.append({"unit": name, "verdict": "NEW", "hash": sha256_text(c)})
        elif sha256_text(b) == sha256_text(c):
            report.append({"unit": name, "verdict": "UNCHANGED", "hash": sha256_text(b)})
        else:
            report.append(
                {
                    "unit": name,
                    "verdict": "CHANGED",
                    "baseline_hash": sha256_text(b),
                    "candidate_hash": sha256_text(c),
                }
            )
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Named-unit hashing for the Golden-Unit Protocol. "
        "Produces MISSING/UNCHANGED/CHANGED/NEW by unit name, never by "
        "line position. Digest comparison and the §4 architectural gate "
        "are NOT performed here — Claude does those by reading the "
        "flagged CHANGED/NEW units."
    )
    parser.add_argument("--baseline", help="Path to baseline source file")
    parser.add_argument("--candidate", help="Path to candidate source file")
    parser.add_argument(
        "--language",
        choices=["python", "js"],
        help="Override auto-detection by file extension",
    )
    parser.add_argument(
        "--manual-units",
        help="JSON file of baseline units for non-code domains: "
        '[{"name": "...", "content": "..."}]',
    )
    parser.add_argument(
        "--manual-units-candidate",
        help="JSON file of candidate units, paired with --manual-units",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only emit the manifest for --baseline, skip comparison",
    )
    args = parser.parse_args()

    if args.manual_units:
        baseline_units = load_manual_units(args.manual_units)
    elif args.baseline:
        baseline_units = extract_units(args.baseline, args.language)
    else:
        parser.error("Provide --baseline or --manual-units")
        return

    if args.manifest_only:
        print(json.dumps({"manifest": build_manifest(baseline_units)}, indent=2))
        return

    if args.manual_units_candidate:
        candidate_units = load_manual_units(args.manual_units_candidate)
    elif args.candidate:
        candidate_units = extract_units(args.candidate, args.language)
    else:
        parser.error(
            "Provide --candidate or --manual-units-candidate, or pass "
            "--manifest-only for a single-file manifest"
        )
        return

    result = {
        "baseline_manifest": build_manifest(baseline_units),
        "candidate_manifest": build_manifest(candidate_units),
        "diff": diff_manifests(baseline_units, candidate_units),
        "note": (
            "verdict is hash-based only. CHANGED/NEW units still require "
            "the §3 digest comparison and, if class is orchestrator or "
            "volatile-logic, the §4 architectural gate -- both are "
            "judgment calls this script does not make."
        ),
    }
    print(json.dumps(result, indent=2))

    missing = [u for u in result["diff"] if u["verdict"] == "MISSING"]
    if missing:
        names = ", ".join(u["unit"] for u in missing)
        print(f"\n[HARD FAIL] MISSING units (present in baseline, absent in candidate): {names}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
