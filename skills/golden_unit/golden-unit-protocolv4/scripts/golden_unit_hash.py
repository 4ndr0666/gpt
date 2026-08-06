#!/usr/bin/env python3
"""
golden_unit_hash.py v2.0.0 — Named-unit hashing and four-way classification
for the Golden-Unit Protocol v4.

WHAT THIS SCRIPT DOES
---------------------
Implements §1 (atomization) and the hashing half of §2/§3 ONLY.

It deliberately does NOT attempt:
  - The digest comparison in §3 ("does the new digest semantically contain
    everything the old one guaranteed?")
  - The architectural gate in §4

Both of those require reading and judgment, not string comparison. The protocol
is explicit that collapsing them into the hash check is itself a violation (§3,
final paragraph). The model performs those steps; this script only produces the
MISSING / UNCHANGED / CHANGED / NEW skeleton for it to reason over.

WHAT IS NEW IN v2.0.0 (GUP v4)
--------------------------------
- NEW units are now surfaced to stderr in addition to MISSING units. The GUP v4
  protocol requires the model to run Gate 2 (§4 architectural soundness) on
  every NEW unit, just as it does on CHANGED units. Previously NEW units were
  silently included in the JSON diff without a stderr signal; this meant they
  could be overlooked in a CI pipeline treating the script as a hard gate.
- End-of-run summary line to stdout (when comparison mode is active) reports
  counts for all four verdict categories for quick orientation.
- --version flag.
- Docstring and internal comments updated to match GUP v4 terminology.

UNIT IDENTITY
-------------
Units are identified by NAME, never by position. A line-range window (e.g.
"lines 501-1000") is exactly the anti-pattern §1 rules out, so this script
refuses to fall back to fixed-size segmentation. If a language has no parser
support here, units must be supplied manually as named blocks (see
--manual-units below).

SUPPORTED AUTOMATIC EXTRACTION
--------------------------------
  Python    — via the stdlib `ast` module; names are exact, spans are taken
              from the original source line numbers (no re-serialization, which
              would normalize whitespace/comments and silently change the hash
              basis).
  JS / TS   — via a brace-matching scan anchored on common declaration
              patterns. Intentionally conservative: only claims a unit when it
              finds one of a small set of unambiguous patterns, and always
              recovers the literal source span via brace counting rather than
              guessing line counts.

For any other domain (prose claims, math lemmas, contract clauses, data
schemas), supply units manually as a JSON list:
  [{"name": "Lemma 3.2", "content": "..."}]
via --manual-units <file.json>.

USAGE
-----
  # Auto-extract units from a baseline and a candidate file, compare:
  python3 golden_unit_hash.py --baseline old.py --candidate new.py

  # Just produce a manifest for one file (no comparison):
  python3 golden_unit_hash.py --baseline old.py --manifest-only

  # Manual units (any domain):
  python3 golden_unit_hash.py --manual-units baseline_units.json \\
                               --manual-units-candidate candidate_units.json

OUTPUT
------
JSON to stdout with the manifest(s) and, if both sides are given, a per-unit
verdict list. The model reads this and fills in digest, class, and the §4 gate
— this script never invents those fields.

Exit codes:
  0  — no MISSING units (NEW units present but not a hard-fail at script level)
  1  — one or more MISSING units detected (hard fail)

Note: NEW units exit 0 because whether a NEW unit is acceptable depends on the
§4 architectural gate, which requires model judgment. They are surfaced to
stderr so a CI pipeline can capture and route them for review.
"""

import argparse
import ast
import hashlib
import json
import sys
from typing import Dict, List, Optional, Tuple

__version__ = "2.0.0"


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

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

    def walk(node, prefix: str = "") -> None:
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

import re

_JS_FUNCTION_PATTERN = re.compile(
    r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\("
)
_JS_CLASS_PATTERN = re.compile(
    r"^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)\b"
)
_JS_ARROW_CONST_PATTERN = re.compile(
    r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*\{"
)
_JS_METHOD_PATTERN = re.compile(
    r"^\s*(?:async\s+)?([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{"
)


def _find_matching_brace(text: str, open_idx: int) -> int:
    """Return the index of the closing brace matching the opening brace at
    open_idx, respecting string literals so braces inside strings are ignored.
    Returns -1 if no match is found before EOF.
    """
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

    # Stack of (class_name, brace_depth_at_entry) so nested classes work.
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
            # this script doesn't attempt to disambiguate.
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
            qualified = (
                f"{current_class}.{name}"
                if (is_method_shorthand and current_class)
                else name
            )
            units.setdefault(qualified, unit_text)
            matched = True
            break

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
                f"Cannot auto-detect language for '{path}'. Pass --language "
                f"explicitly, or use --manual-units for non-code domains "
                f"(prose, math, schemas, contracts, etc.) since this script "
                f"only parses Python and JS/TS automatically."
            )

    if lang == "python":
        return extract_python_units(source)
    elif lang == "js":
        return extract_js_units(source)
    else:
        raise ValueError(f"Unsupported language: {lang!r}")


def load_manual_units(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    units: Dict[str, str] = {}
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
            report.append({
                "unit": name,
                "verdict": "MISSING",
                "hash": sha256_text(b),
            })
        elif b is None and c is not None:
            report.append({
                "unit": name,
                "verdict": "NEW",
                "hash": sha256_text(c),
            })
        elif sha256_text(b) == sha256_text(c):
            report.append({
                "unit": name,
                "verdict": "UNCHANGED",
                "hash": sha256_text(b),
            })
        else:
            report.append({
                "unit": name,
                "verdict": "CHANGED",
                "baseline_hash": sha256_text(b),
                "candidate_hash": sha256_text(c),
            })
    return report


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Named-unit hashing for the Golden-Unit Protocol v4. "
            "Produces MISSING/UNCHANGED/CHANGED/NEW by unit name, never by "
            "line position. Digest comparison (§3) and the §4 architectural "
            "gate are NOT performed here — the model does those by reading the "
            "flagged CHANGED/NEW units."
        )
    )
    parser.add_argument("--baseline", help="Path to baseline source file.")
    parser.add_argument("--candidate", help="Path to candidate source file.")
    parser.add_argument(
        "--language",
        choices=["python", "js"],
        help="Override auto-detection by file extension.",
    )
    parser.add_argument(
        "--manual-units",
        metavar="FILE",
        help=(
            "JSON file of baseline units for non-code domains: "
            '[{"name": "...", "content": "..."}]'
        ),
    )
    parser.add_argument(
        "--manual-units-candidate",
        metavar="FILE",
        help="JSON file of candidate units, paired with --manual-units.",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Only emit the manifest for --baseline; skip comparison.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"golden_unit_hash {__version__} (GUP v4)",
    )
    args = parser.parse_args()

    # ---- Load baseline ----
    if args.manual_units:
        baseline_units = load_manual_units(args.manual_units)
    elif args.baseline:
        baseline_units = extract_units(args.baseline, args.language)
    else:
        parser.error("Provide --baseline or --manual-units.")
        return  # unreachable; satisfies type checker

    # ---- Manifest-only mode ----
    if args.manifest_only:
        print(json.dumps({"manifest": build_manifest(baseline_units)}, indent=2))
        return

    # ---- Load candidate ----
    if args.manual_units_candidate:
        candidate_units = load_manual_units(args.manual_units_candidate)
    elif args.candidate:
        candidate_units = extract_units(args.candidate, args.language)
    else:
        parser.error(
            "Provide --candidate or --manual-units-candidate, "
            "or pass --manifest-only for a single-file manifest."
        )
        return

    # ---- Diff ----
    diff = diff_manifests(baseline_units, candidate_units)

    result = {
        "gup_version": __version__,
        "baseline_manifest": build_manifest(baseline_units),
        "candidate_manifest": build_manifest(candidate_units),
        "diff": diff,
        "note": (
            "Verdicts are hash-based only. CHANGED and NEW units still "
            "require the §3 semantic digest comparison and, if class is "
            "'orchestrator' or 'volatile-logic', the §4 architectural gate "
            "— both are judgment calls this script does not make."
        ),
    }
    print(json.dumps(result, indent=2))

    # ---- Stderr signals for CI ----
    missing = [u for u in diff if u["verdict"] == "MISSING"]
    new_units = [u for u in diff if u["verdict"] == "NEW"]
    changed = [u for u in diff if u["verdict"] == "CHANGED"]
    unchanged = [u for u in diff if u["verdict"] == "UNCHANGED"]

    # Summary always goes to stderr so it doesn't corrupt JSON stdout piping.
    print(
        f"\n[GUP {__version__}] Summary: "
        f"{len(unchanged)} UNCHANGED  "
        f"{len(changed)} CHANGED  "
        f"{len(new_units)} NEW  "
        f"{len(missing)} MISSING",
        file=sys.stderr,
    )

    # NEW units: surface for mandatory model review (Gate 2), but not a
    # script-level hard fail — acceptability depends on §4 judgment.
    if new_units:
        names = ", ".join(u["unit"] for u in new_units)
        print(
            f"[REVIEW REQUIRED] NEW units (absent in baseline, present in "
            f"candidate — require §3 digest + §4 Gate 2 review): {names}",
            file=sys.stderr,
        )

    # MISSING units: hard fail, always.
    if missing:
        names = ", ".join(u["unit"] for u in missing)
        print(
            f"[HARD FAIL] MISSING units (present in baseline, absent in "
            f"candidate): {names}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
