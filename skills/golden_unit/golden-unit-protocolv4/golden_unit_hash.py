#!/usr/bin/env python3
"""
golden_unit_hash.py v3.0.0 — Named-unit hashing for the Golden-Unit Protocol v4.

WHAT THIS SCRIPT DOES
---------------------
Implements GUP §1 (atomization) and the hashing half of §2/§3 ONLY.

It deliberately does NOT perform:
  - The §3 digest comparison ("does the candidate semantically contain
    everything the baseline guaranteed?")
  - The §4 architectural soundness gate

Both require reading and judgment, not string comparison. Collapsing
them into the hash check is itself a protocol violation (§3, final
paragraph). The model performs those steps; this script only produces
the MISSING / UNCHANGED / CHANGED / NEW skeleton for it to reason over.

UNIT IDENTITY
-------------
Units are identified by NAME, never by position. "lines 501-1000" is
the anti-pattern §1 explicitly rules out; this script refuses to fall
back to fixed-size segmentation under any circumstances.

SUPPORTED LANGUAGES (automatic extraction)
------------------------------------------
Brace-delimited (function bodies bounded by { }):
  Python     — stdlib ast module; exact AST spans, qualified names
  JavaScript — brace-match scan; function/class/arrow/method
  TypeScript — same extractor as JavaScript
  Go         — func Name( and func (recv) Name(
  Rust       — fn name( and impl Type { fn name( }
  Java       — class/interface/enum + method (Name.Function tokens)
  C          — Name.Function tokens + brace matching
  C++        — same as C, plus class/struct scope qualification
  C#         — class + Name.Function tokens
  Kotlin     — fun name( and class Name
  Swift      — func name( and class/struct/enum Name
  PHP        — function name( and class Name
  Scala      — def name( and class/object/trait Name
  Dart       — Name tokens before ( inside class + brace matching
  PowerShell — function Name {

End-keyword-delimited (bodies end with 'end'):
  Ruby       — def name / class Name / module Name ... end
  Lua        — function name( / local function name( ... end
  Elixir     — def/defp name( / defmodule Name ... end

Type-signature-anchored (indentation-agnostic):
  Haskell    — name :: Type sig + following binding equations

Data-structure (section/key-based):
  TOML       — top-level sections and nested tables as dotted keys
  YAML       — top-level keys (stdlib yaml-less; uses key:value scan)
  JSON       — top-level keys via stdlib json
  SQL        — CREATE TABLE/VIEW/PROCEDURE/FUNCTION/TRIGGER name

Shell:
  Bash/Shell — name() { and function name {

For any other domain (prose claims, math lemmas, contract clauses,
protobuf schemas, Dockerfile stages, etc.), supply units manually:
  [{"name": "Lemma 3.2", "content": "..."}]
via --manual-units <file.json>.

EXIT CODES
----------
  0 — no MISSING units (NEW units present but not a script-level fail)
  1 — one or more MISSING units (hard fail)

NEW units exit 0 because acceptability depends on the §4 architectural
gate, which requires model judgment. They are surfaced to stderr.

USAGE
-----
  python3 golden_unit_hash.py --baseline old.py --candidate new.py
  python3 golden_unit_hash.py --baseline old.py --manifest-only
  python3 golden_unit_hash.py --manual-units base.json --manual-units-candidate cand.json
  python3 golden_unit_hash.py --version
"""

import argparse
import ast
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

__version__ = "3.0.0"
_GUP_VERSION = "v4"


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Shared utilities
# ---------------------------------------------------------------------------

def _find_matching_brace(text: str, open_idx: int) -> int:
    """Return the index of the } matching the { at open_idx.
    Respects single/double/backtick string literals and escape sequences.
    Returns -1 if unmatched.
    """
    depth = 0
    i = open_idx
    in_str: Optional[str] = None
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\" and in_str != "`":
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


def _build_line_offsets(source: str) -> List[int]:
    """Return byte offset of the start of each line (0-indexed)."""
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    return offsets


# ---------------------------------------------------------------------------
# PYTHON — stdlib ast (exact, whitespace-preserving)
# ---------------------------------------------------------------------------

def extract_python_units(source: str) -> Dict[str, str]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}

    def span_text(node: ast.AST) -> str:
        start = node.lineno - 1  # type: ignore[attr-defined]
        end = getattr(node, "end_lineno", node.lineno)  # type: ignore[attr-defined]
        return "".join(lines[start:end])

    def qualified(node: ast.AST, prefix: str) -> str:
        name = node.name  # type: ignore[attr-defined]
        return f"{prefix}{name}" if prefix else name

    def walk(node: ast.AST, prefix: str = "") -> None:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                q = qualified(child, prefix)
                units[q] = span_text(child)
                walk(child, f"{q}.")
            elif isinstance(child, ast.ClassDef):
                q = qualified(child, prefix)
                units[q] = span_text(child)
                walk(child, f"{q}.")
            else:
                walk(child, prefix)

    walk(tree)
    return units


# ---------------------------------------------------------------------------
# BRACE-FAMILY — shared engine used by JS/TS, Go, Rust, Java, C, C++,
#                C#, Kotlin, Swift, PHP, Scala, Dart, PowerShell
#
# Each language supplies a list of (pattern, name_group, is_method,
# needs_class_scope) tuples plus an optional class-opening pattern.
# The engine handles class-stack tracking and brace matching uniformly.
# ---------------------------------------------------------------------------

def _brace_extract(
    source: str,
    func_patterns: List[Tuple],
    class_pattern: Optional[re.Pattern],
    class_name_group: int = 1,
) -> Dict[str, str]:
    """Generic brace-delimited unit extractor.

    func_patterns: list of (compiled_re, name_group, is_method_shorthand)
      - is_method_shorthand=True  → only match inside a class scope
      - is_method_shorthand=False → match anywhere
    class_pattern: re that identifies a class/struct/impl/interface opener.
    class_name_group: group index for the class name in class_pattern.
    """
    units: Dict[str, str] = {}
    lines = source.splitlines(keepends=True)
    offsets = _build_line_offsets(source)

    class_stack: List[Tuple[str, int]] = []  # (qualified_name, brace_depth)
    depth = 0

    for line_no, line in enumerate(lines):
        current_class = class_stack[-1][0] if class_stack else ""

        # --- Class / struct / impl opener ---
        if class_pattern:
            cm = class_pattern.match(line)
            if cm:
                name = cm.group(class_name_group)
                qualified = f"{current_class}.{name}" if current_class else name
                brace_col = line.find("{")
                if brace_col != -1:
                    abs_open = offsets[line_no] + brace_col
                    abs_close = _find_matching_brace(source, abs_open)
                    if abs_close != -1:
                        units.setdefault(qualified, source[offsets[line_no]:abs_close + 1])
                        class_stack.append((qualified, depth))
                depth += line.count("{") - line.count("}")
                continue

        # --- Function / method patterns ---
        matched = False
        for pattern, name_group, is_method_shorthand in func_patterns:
            m = pattern.match(line)
            if not m:
                continue
            if is_method_shorthand and not current_class:
                continue
            name = m.group(name_group)
            qualified = f"{current_class}.{name}" if (current_class and is_method_shorthand) else name
            brace_col = line.find("{", m.end() - 1)
            if brace_col == -1:
                # Signature may span multiple lines; search forward
                search_start = offsets[line_no] + len(line)
                next_brace = source.find("{", offsets[line_no])
                next_newline = source.find("\n", offsets[line_no])
                # Only accept a { that precedes the next top-level statement
                if next_brace == -1 or (next_newline != -1 and next_brace > next_newline + 120):
                    continue
                brace_col = next_brace - offsets[line_no]
            abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close == -1:
                continue
            units.setdefault(qualified, source[offsets[line_no]:abs_close + 1])
            matched = True
            break

        depth += line.count("{") - line.count("}")
        if matched:
            continue

        while class_stack and depth <= class_stack[-1][1]:
            class_stack.pop()

    return units


# --- JS / TS ---

_JS_CLASS_PAT = re.compile(
    r"^\s*(?:export\s+)?(?:abstract\s+)?class\s+([A-Za-z_$][\w$]*)\b"
)
_JS_FUNC_PATTERNS = [
    (re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s*\*?\s*([A-Za-z_$][\w$]*)\s*\("), 1, False),
    (re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*\{"), 1, False),
    (re.compile(r"^\s*(?:static\s+)?(?:async\s+)?(?:get\s+|set\s+)?([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*(?::\s*\S+\s*)?\{"), 1, True),
]

def extract_js_units(source: str) -> Dict[str, str]:
    return _brace_extract(source, _JS_FUNC_PATTERNS, _JS_CLASS_PAT)


# --- Go ---

_GO_CLASS_PAT = re.compile(
    r"^\s*type\s+([A-Za-z_]\w*)\s+(?:struct|interface)\s*\{"
)
_GO_FUNC_PATTERNS = [
    # func (recv *Type) MethodName( — receiver method, qualify under Type
    (re.compile(r"^\s*func\s+\([^)]*\*?\s*([A-Za-z_]\w*)\)\s+([A-Za-z_]\w*)\s*\("), 2, False),
    # func Name(
    (re.compile(r"^\s*func\s+([A-Za-z_]\w*)\s*\("), 1, False),
]

def extract_go_units(source: str) -> Dict[str, str]:
    units: Dict[str, str] = {}
    lines = source.splitlines(keepends=True)
    offsets = _build_line_offsets(source)

    RECV_METHOD = re.compile(r"^\s*func\s+\(\s*\w+\s+\*?\s*([A-Za-z_]\w*)\s*\)\s+([A-Za-z_]\w*)\s*\(")
    PLAIN_FUNC  = re.compile(r"^\s*func\s+([A-Za-z_]\w*)\s*\(")
    TYPE_DECL   = re.compile(r"^\s*type\s+([A-Za-z_]\w*)\s+(?:struct|interface)\s*\{")

    for line_no, line in enumerate(lines):
        rm = RECV_METHOD.match(line)
        if rm:
            receiver_type, method_name = rm.group(1), rm.group(2)
            qualified = f"{receiver_type}.{method_name}"
            brace_col = line.find("{")
            if brace_col == -1:
                brace_col_abs = source.find("{", offsets[line_no])
                if brace_col_abs == -1:
                    continue
                abs_open = brace_col_abs
            else:
                abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close != -1:
                units.setdefault(qualified, source[offsets[line_no]:abs_close + 1])
            continue

        pm = PLAIN_FUNC.match(line)
        if pm:
            name = pm.group(1)
            brace_col = line.find("{")
            if brace_col == -1:
                brace_col_abs = source.find("{", offsets[line_no])
                if brace_col_abs == -1:
                    continue
                abs_open = brace_col_abs
            else:
                abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close != -1:
                units.setdefault(name, source[offsets[line_no]:abs_close + 1])
            continue

        tm = TYPE_DECL.match(line)
        if tm:
            name = tm.group(1)
            brace_col = line.find("{")
            if brace_col == -1:
                continue
            abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close != -1:
                units.setdefault(name, source[offsets[line_no]:abs_close + 1])

    return units


# --- Rust ---

def extract_rust_units(source: str) -> Dict[str, str]:
    units: Dict[str, str] = {}
    lines = source.splitlines(keepends=True)
    offsets = _build_line_offsets(source)

    IMPL_PAT = re.compile(r"^\s*impl(?:<[^>]*>)?\s+(?:\w+\s+for\s+)?([A-Za-z_]\w*)")
    FN_PAT   = re.compile(r"^\s*(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+([A-Za-z_]\w*)\s*[<(]")

    impl_stack: List[Tuple[str, int]] = []
    depth = 0

    for line_no, line in enumerate(lines):
        current_impl = impl_stack[-1][0] if impl_stack else ""

        im = IMPL_PAT.match(line)
        if im:
            type_name = im.group(1)
            brace_col = line.find("{")
            if brace_col != -1:
                impl_stack.append((type_name, depth))
            depth += line.count("{") - line.count("}")
            continue

        fm = FN_PAT.match(line)
        if fm:
            name = fm.group(1)
            qualified = f"{current_impl}.{name}" if current_impl else name
            brace_col = line.find("{")
            if brace_col == -1:
                # Multi-line signature: find first { not inside < >
                search = source.find("{", offsets[line_no])
                if search == -1:
                    depth += line.count("{") - line.count("}")
                    continue
                abs_open = search
            else:
                abs_open = offsets[line_no] + brace_col
            abs_close = _find_matching_brace(source, abs_open)
            if abs_close != -1:
                units.setdefault(qualified, source[offsets[line_no]:abs_close + 1])
            depth += line.count("{") - line.count("}")
            continue

        depth += line.count("{") - line.count("}")
        while impl_stack and depth <= impl_stack[-1][1]:
            impl_stack.pop()

    return units


# --- Java / C# / Kotlin / Swift / Dart (Pygments-assisted) ---

def _pygments_brace_extract(source: str, lang_alias: str) -> Dict[str, str]:
    """Use Pygments token stream to identify Name.Function and Name.Class
    tokens, then use brace matching to extract spans. Works for Java, C#,
    Kotlin, Swift, Dart.
    """
    try:
        from pygments.lexers import get_lexer_by_name
        from pygments.token import Token
    except ImportError:
        return {}

    lexer = get_lexer_by_name(lang_alias)
    tokens = list(lexer.get_tokens(source))
    lines = source.splitlines(keepends=True)
    offsets = _build_line_offsets(source)

    units: Dict[str, str] = {}
    class_stack: List[str] = []
    depth = 0
    i = 0

    # Reconstruct a position-indexed list for span recovery
    pos = 0
    tok_pos = []  # (start_pos, end_pos, ttype, value)
    for ttype, val in tokens:
        tok_pos.append((pos, pos + len(val), ttype, val))
        pos += len(val)

    for idx, (start, end, ttype, val) in enumerate(tok_pos):
        stripped = val.strip()
        if not stripped:
            continue

        if ttype in (Token.Keyword.Declaration, Token.Keyword) and stripped in (
            "class", "interface", "enum", "object", "struct", "trait",
        ):
            # Next Name.Class token is the type name
            for j in range(idx + 1, min(idx + 6, len(tok_pos))):
                _, _, ntt, nval = tok_pos[j]
                if nval.strip() and ntt in (Token.Name.Class, Token.Name):
                    cname = nval.strip()
                    qualified = f"{class_stack[-1]}.{cname}" if class_stack else cname
                    # Find { in source after this position
                    brace_abs = source.find("{", tok_pos[j][1])
                    if brace_abs != -1:
                        close = _find_matching_brace(source, brace_abs)
                        if close != -1:
                            # Find line start
                            line_start = source.rfind("\n", 0, start) + 1
                            units.setdefault(qualified, source[line_start:close + 1])
                            class_stack.append(qualified)
                    break

        if ttype == Token.Name.Function and stripped:
            current_class = class_stack[-1] if class_stack else ""
            qualified = f"{current_class}.{stripped}" if current_class else stripped
            brace_abs = source.find("{", end)
            # Make sure the { is on the same or next line (not in a far-off body)
            newline_after = source.find("\n", end)
            if brace_abs != -1 and (newline_after == -1 or brace_abs <= newline_after + 200):
                close = _find_matching_brace(source, brace_abs)
                if close != -1:
                    line_start = source.rfind("\n", 0, start) + 1
                    units.setdefault(qualified, source[line_start:close + 1])

        # Track depth for class stack popping
        for ch in val:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if class_stack and depth < len(class_stack):
                    class_stack.pop()

    return units


def extract_java_units(source: str) -> Dict[str, str]:
    return _pygments_brace_extract(source, "java")

def extract_csharp_units(source: str) -> Dict[str, str]:
    return _pygments_brace_extract(source, "csharp")

def extract_kotlin_units(source: str) -> Dict[str, str]:
    return _pygments_brace_extract(source, "kotlin")

def extract_swift_units(source: str) -> Dict[str, str]:
    return _pygments_brace_extract(source, "swift")

def extract_dart_units(source: str) -> Dict[str, str]:
    """Dart lexer emits Token.Name (not Token.Name.Function) for method names.
    Pattern: Token.Keyword.Type → Token.Name → Token.Punctuation '(' → '{' body.
    """
    try:
        from pygments.lexers import get_lexer_by_name
        from pygments.token import Token
    except ImportError:
        return {}

    lexer = get_lexer_by_name("dart")
    raw_tokens = list(lexer.get_tokens(source))

    units: Dict[str, str] = {}
    class_stack: List[str] = []
    depth = 0

    pos = 0
    tok_pos: List[Tuple[int, int, object, str]] = []
    for ttype, val in raw_tokens:
        tok_pos.append((pos, pos + len(val), ttype, val))
        pos += len(val)

    _SKIP_KEYWORDS = frozenset({"return", "var", "final", "const", "late", "new"})

    for idx, (start, end, ttype, val) in enumerate(tok_pos):
        stripped = val.strip()
        if not stripped:
            continue

        # Class opener
        if ttype == Token.Keyword.Declaration and stripped == "class":
            for j in range(idx + 1, min(idx + 5, len(tok_pos))):
                _, je, ntt, nval = tok_pos[j]
                if not nval.strip():
                    continue
                if ntt == Token.Name.Class:
                    cname = nval.strip()
                    qualified = f"{class_stack[-1]}.{cname}" if class_stack else cname
                    brace = source.find("{", je)
                    if brace != -1:
                        close = _find_matching_brace(source, brace)
                        if close != -1:
                            lstart = source.rfind("\n", 0, start) + 1
                            units.setdefault(qualified, source[lstart:close + 1])
                            class_stack.append(qualified)
                break

        # Method/function: Keyword.Type → Name → '('
        if ttype == Token.Keyword.Type and stripped not in _SKIP_KEYWORDS:
            name_idx = None
            for j in range(idx + 1, min(idx + 6, len(tok_pos))):
                _, _, ntt, nval = tok_pos[j]
                if not nval.strip():
                    continue
                if ntt == Token.Name and nval.strip().isidentifier():
                    name_idx = j
                else:
                    break
                break
            if name_idx is not None:
                for k in range(name_idx + 1, min(name_idx + 5, len(tok_pos))):
                    _, ke, ktt, kval = tok_pos[k]
                    if not kval.strip():
                        continue
                    if kval.strip() == "(":
                        fn_name = tok_pos[name_idx][3].strip()
                        current_class = class_stack[-1] if class_stack else ""
                        qualified = f"{current_class}.{fn_name}" if current_class else fn_name
                        brace = source.find("{", ke)
                        if brace != -1:
                            close = _find_matching_brace(source, brace)
                            if close != -1:
                                lstart = source.rfind("\n", 0, start) + 1
                                units.setdefault(qualified, source[lstart:close + 1])
                    break

        for ch in val:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if class_stack and depth < len(class_stack):
                    class_stack.pop()

    return units


# --- C / C++ (Pygments-assisted) ---

def _c_family_extract(source: str, lang_alias: str) -> Dict[str, str]:
    """C and C++ share the same strategy: Name.Function tokens are function
    names; struct/class tokens open a scope for qualification.
    """
    try:
        from pygments.lexers import get_lexer_by_name
        from pygments.token import Token
    except ImportError:
        return {}

    return _pygments_brace_extract(source, lang_alias)

def extract_c_units(source: str) -> Dict[str, str]:
    return _c_family_extract(source, "c")

def extract_cpp_units(source: str) -> Dict[str, str]:
    return _c_family_extract(source, "cpp")


# --- PHP ---

_PHP_CLASS_PAT = re.compile(
    r"^\s*(?:abstract\s+|final\s+)?class\s+([A-Za-z_]\w*)"
)
_PHP_FUNC_PATTERNS = [
    (re.compile(r"^\s*(?:public|protected|private|static|abstract|\s)*function\s+([A-Za-z_]\w*)\s*\("), 1, False),
]

def extract_php_units(source: str) -> Dict[str, str]:
    return _brace_extract(source, _PHP_FUNC_PATTERNS, _PHP_CLASS_PAT)


# --- Scala ---

_SCALA_CLASS_PAT = re.compile(
    r"^\s*(?:abstract\s+|sealed\s+|final\s+|case\s+)?(?:class|object|trait)\s+([A-Za-z_]\w*)"
)
_SCALA_FUNC_PATTERNS = [
    (re.compile(r"^\s*(?:override\s+)?(?:private\s+|protected\s+)?(?:final\s+)?def\s+([A-Za-z_`]\w*)\s*[(\[]"), 1, True),
    (re.compile(r"^\s*def\s+([A-Za-z_`]\w*)\s*[(\[]"), 1, False),
]

def extract_scala_units(source: str) -> Dict[str, str]:
    return _brace_extract(source, _SCALA_FUNC_PATTERNS, _SCALA_CLASS_PAT)


# --- PowerShell ---

_PS_FUNC_PATTERNS = [
    (re.compile(r"^\s*function\s+([\w-]+)\s*(?:\([^)]*\))?\s*\{"), 1, False),
]

def extract_powershell_units(source: str) -> Dict[str, str]:
    return _brace_extract(source, _PS_FUNC_PATTERNS, None)


# ---------------------------------------------------------------------------
# END-KEYWORD FAMILY — Ruby, Lua, Elixir
# ---------------------------------------------------------------------------

def _end_keyword_extract(
    source: str,
    open_patterns: List[Tuple[re.Pattern, str, str]],
    close_pattern: re.Pattern,
    parent_kinds: List[str],
) -> Dict[str, str]:
    """Extract units delimited by an opening keyword and a matching 'end'.

    open_patterns: list of (compiled_re, kind_label, name_group_spec)
      name_group_spec: 'g1' or 'g1+g2' to concatenate groups
    close_pattern: matches the 'end' (or equivalent) line
    parent_kinds: which kinds contribute to qualified name prefix
    """
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}
    stack: List[Tuple[str, str, int]] = []  # (kind, qualified_name, lineno)

    for lineno, line in enumerate(lines):
        if close_pattern.match(line):
            if stack:
                kind, name, start = stack.pop()
                units[name] = "".join(lines[start:lineno + 1])
            continue

        for pat, kind, group_spec in open_patterns:
            m = pat.match(line)
            if not m:
                continue
            if group_spec == "g1":
                raw_name = m.group(1)
            elif group_spec == "g1g2":
                raw_name = (m.group(1) or "") + m.group(2)
            else:
                raw_name = m.group(1)
            parent = next(
                (s[1] for s in reversed(stack) if s[0] in parent_kinds), None
            )
            qualified = f"{parent}.{raw_name}" if parent else raw_name
            stack.append((kind, qualified, lineno))
            break

    return units


# --- Ruby ---

def extract_ruby_units(source: str) -> Dict[str, str]:
    open_pats = [
        (re.compile(r"^\s*(class|module)\s+([A-Za-z_]\w*)"), "class", "g1g2_ruby_class"),
        (re.compile(r"^\s*def\s+(self\.)?([A-Za-z_]\w*[\?!]?)"), "def", "g1g2"),
    ]
    close_pat = re.compile(r"^\s*end\b")
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}
    stack: List[Tuple[str, str, int]] = []

    CLASS_MOD = re.compile(r"^\s*(class|module)\s+([A-Za-z_:]\w*)")
    DEF = re.compile(r"^\s*def\s+(self\.)?([A-Za-z_]\w*[\?!]?)")
    END = re.compile(r"^\s*end\b")
    DO_BLOCK = re.compile(r"\bdo\b|\{")

    for lineno, line in enumerate(lines):
        if END.match(line):
            if stack:
                kind, name, start = stack.pop()
                units[name] = "".join(lines[start:lineno + 1])
            continue
        cm = CLASS_MOD.match(line)
        if cm:
            raw = cm.group(2).replace("::", ".")
            parent = next((s[1] for s in reversed(stack) if s[0] in ("class", "module")), None)
            qualified = f"{parent}.{raw}" if parent else raw
            stack.append((cm.group(1), qualified, lineno))
            continue
        dm = DEF.match(line)
        if dm:
            raw = (dm.group(1) or "") + dm.group(2)
            parent = next((s[1] for s in reversed(stack) if s[0] in ("class", "module")), None)
            qualified = f"{parent}.{raw}" if parent else raw
            stack.append(("def", qualified, lineno))
            continue

    return units


# --- Lua ---

def extract_lua_units(source: str) -> Dict[str, str]:
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}
    stack: List[Tuple[str, int]] = []

    FUNC = re.compile(
        r"^\s*(?:local\s+)?function\s+([A-Za-z_]\w*(?:[.:][A-Za-z_]\w*)*)\s*\("
    )
    END = re.compile(r"^\s*end\b")
    # Track if/for/while/do blocks to avoid mismatched end counting
    BLOCK_OPEN = re.compile(r"\b(?:if|for|while|do|repeat)\b")
    BLOCK_CLOSE = re.compile(r"\b(?:end|until)\b")

    depth = 0  # non-function block depth

    for lineno, line in enumerate(lines):
        fm = FUNC.match(line)
        if fm:
            name = fm.group(1)
            stack.append((name, lineno))
            continue

        if END.match(line):
            if stack and depth == 0:
                name, start = stack.pop()
                units[name] = "".join(lines[start:lineno + 1])
            else:
                depth = max(0, depth - 1)
            continue

        # Count non-function block opens to properly match ends
        opens = len(BLOCK_OPEN.findall(line))
        depth += opens

    return units


# --- Elixir ---

def extract_elixir_units(source: str) -> Dict[str, str]:
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}
    stack: List[Tuple[str, str, int]] = []

    MODULE = re.compile(r"^\s*defmodule\s+([\w.]+)\s+do")
    DEF    = re.compile(r"^\s*(defp?)\s+([A-Za-z_]\w*)\s*[(\s]")
    END    = re.compile(r"^\s*end\b")

    for lineno, line in enumerate(lines):
        mm = MODULE.match(line)
        if mm:
            name = mm.group(1)
            stack.append(("module", name, lineno))
            continue

        dm = DEF.match(line)
        if dm:
            fn_name = dm.group(2)
            parent = next((s[1] for s in reversed(stack) if s[0] == "module"), None)
            qualified = f"{parent}.{fn_name}" if parent else fn_name
            stack.append(("def", qualified, lineno))
            continue

        if END.match(line):
            if stack:
                kind, name, start = stack.pop()
                units[name] = "".join(lines[start:lineno + 1])

    return units


# ---------------------------------------------------------------------------
# HASKELL — type-signature-anchored
# ---------------------------------------------------------------------------

def extract_haskell_units(source: str) -> Dict[str, str]:
    lines = source.splitlines(keepends=True)
    units: Dict[str, str] = {}

    TYPE_SIG  = re.compile(r"^([a-z_][A-Za-z0-9_']*)\s*::")
    BINDING   = re.compile(r"^([a-z_][A-Za-z0-9_']*)\b")
    DATA_DECL = re.compile(r"^(data|newtype|type)\s+([A-Za-z]\w*)")

    i = 0
    while i < len(lines):
        line = lines[i]

        dm = DATA_DECL.match(line)
        if dm:
            name = dm.group(2)
            start = i
            i += 1
            while i < len(lines) and (
                lines[i].startswith(" ")
                or lines[i].strip().startswith("deriving")
                or not lines[i].strip()
            ):
                i += 1
            units[name] = "".join(lines[start:i])
            continue

        tm = TYPE_SIG.match(line)
        if tm:
            name = tm.group(1)
            start = i
            i += 1
            while i < len(lines):
                l = lines[i]
                if not l.strip() or l.startswith("--"):
                    i += 1
                    continue
                bm = BINDING.match(l)
                if bm and bm.group(1) == name:
                    i += 1
                    continue
                break
            units[name] = "".join(lines[start:i]).rstrip()
            continue

        i += 1

    return units


# ---------------------------------------------------------------------------
# BASH / SHELL
# ---------------------------------------------------------------------------

def extract_bash_units(source: str) -> Dict[str, str]:
    lines = source.splitlines(keepends=True)
    offsets = _build_line_offsets(source)
    units: Dict[str, str] = {}

    # POSIX: name() { and bash: function name {
    FUNC1 = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*\(\s*\)\s*\{")
    FUNC2 = re.compile(r"^\s*function\s+([A-Za-z_][\w-]*)\s*(?:\(\s*\))?\s*\{")

    for line_no, line in enumerate(lines):
        m = FUNC1.match(line) or FUNC2.match(line)
        if not m:
            continue
        name = m.group(1)
        brace_col = line.rfind("{")
        abs_open = offsets[line_no] + brace_col
        abs_close = _find_matching_brace(source, abs_open)
        if abs_close != -1:
            units.setdefault(name, source[offsets[line_no]:abs_close + 1])

    return units


# ---------------------------------------------------------------------------
# SQL — CREATE DDL statement extraction
# ---------------------------------------------------------------------------

def extract_sql_units(source: str) -> Dict[str, str]:
    units: Dict[str, str] = {}
    # Match CREATE [OR REPLACE] TABLE/VIEW/PROCEDURE/FUNCTION/TRIGGER name
    # Spans from CREATE to the first semicolon at statement level
    DDL = re.compile(
        r"CREATE\s+(?:OR\s+REPLACE\s+)?(?:TEMP(?:ORARY)?\s+)?"
        r"(TABLE|VIEW|PROCEDURE|FUNCTION|TRIGGER|INDEX)\s+"
        r"(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][\w.]*)",
        re.IGNORECASE,
    )
    # Split on statement-ending semicolons (simplistic but robust for DDL)
    # We scan the original source preserving positions
    pos = 0
    src_upper = source.upper()
    while pos < len(source):
        m = DDL.search(source, pos)
        if not m:
            break
        obj_type = m.group(1).upper()
        obj_name = m.group(2)
        start = m.start()
        # Find statement end: next ; at depth 0 of BEGIN/END blocks
        end = _find_sql_statement_end(source, m.end())
        span = source[start:end].strip()
        units[f"{obj_type}.{obj_name}"] = span
        pos = end

    return units


def _find_sql_statement_end(source: str, from_pos: int) -> int:
    """Find the end of a SQL statement, respecting BEGIN...END blocks."""
    depth = 0
    i = from_pos
    src_upper = source.upper()
    while i < len(source):
        if src_upper[i:i+5] == "BEGIN":
            depth += 1
            i += 5
            continue
        if src_upper[i:i+3] == "END":
            if depth > 0:
                depth -= 1
            i += 3
            continue
        if source[i] == ";" and depth == 0:
            return i + 1
        i += 1
    return len(source)


# ---------------------------------------------------------------------------
# TOML — stdlib tomllib (Python 3.11+)
# ---------------------------------------------------------------------------

def extract_toml_units(source: str) -> Dict[str, str]:
    try:
        data = tomllib.loads(source)
    except Exception as e:
        raise ValueError(f"TOML parse error: {e}") from e

    units: Dict[str, str] = {}

    def flatten(obj: object, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                key = f"{prefix}.{k}" if prefix else k
                units[key] = json.dumps(v, indent=2) if isinstance(v, (dict, list)) else json.dumps(v)
                if isinstance(v, (dict, list)):
                    flatten(v, key)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                key = f"{prefix}[{idx}]"
                units[key] = json.dumps(item, indent=2)
                if isinstance(item, dict):
                    flatten(item, key)

    flatten(data)
    return units


# ---------------------------------------------------------------------------
# YAML — lightweight key-scanner (no PyYAML dependency)
# ---------------------------------------------------------------------------

def extract_yaml_units(source: str) -> Dict[str, str]:
    """Extract top-level and nested YAML keys as dotted-path units.
    Handles indentation-based nesting. Does not parse anchors/aliases.
    Sufficient for config files and schema-like YAML; not a full parser.
    """
    units: Dict[str, str] = {}
    lines = source.splitlines(keepends=True)

    KEY = re.compile(r"^(\s*)([A-Za-z_][\w-]*)(\s*):(?!\s*:)")
    stack: List[Tuple[int, str]] = []  # (indent, qualified_key)

    for line in lines:
        m = KEY.match(line)
        if not m:
            continue
        indent = len(m.group(1))
        key = m.group(2)

        # Pop stack until we find the parent indent level
        while stack and stack[-1][0] >= indent:
            stack.pop()

        parent = stack[-1][1] if stack else ""
        qualified = f"{parent}.{key}" if parent else key
        units[qualified] = line.rstrip()
        stack.append((indent, qualified))

    return units


# ---------------------------------------------------------------------------
# JSON — top-level keys via stdlib
# ---------------------------------------------------------------------------

def extract_json_units(source: str) -> Dict[str, str]:
    try:
        data = json.loads(source)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}") from e

    units: Dict[str, str] = {}
    if isinstance(data, dict):
        for k, v in data.items():
            units[k] = json.dumps(v, indent=2)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            units[f"[{i}]"] = json.dumps(item, indent=2)
    return units


# ---------------------------------------------------------------------------
# Language dispatch table
# ---------------------------------------------------------------------------

# Maps: file extension OR explicit --language value → extractor function
_EXTRACTORS: Dict[str, object] = {
    # Python
    "py": extract_python_units,
    "pyi": extract_python_units,
    "pyw": extract_python_units,
    "python": extract_python_units,
    # JavaScript / TypeScript
    "js": extract_js_units,
    "mjs": extract_js_units,
    "cjs": extract_js_units,
    "jsx": extract_js_units,
    "ts": extract_js_units,
    "tsx": extract_js_units,
    "javascript": extract_js_units,
    "typescript": extract_js_units,
    # Go
    "go": extract_go_units,
    # Rust
    "rs": extract_rust_units,
    "rust": extract_rust_units,
    # Java
    "java": extract_java_units,
    # C# 
    "cs": extract_csharp_units,
    "csharp": extract_csharp_units,
    # Kotlin
    "kt": extract_kotlin_units,
    "kts": extract_kotlin_units,
    "kotlin": extract_kotlin_units,
    # Swift
    "swift": extract_swift_units,
    # PHP
    "php": extract_php_units,
    # Scala
    "scala": extract_scala_units,
    # Dart
    "dart": extract_dart_units,
    # C / C++
    "c": extract_c_units,
    "h": extract_c_units,
    "cpp": extract_cpp_units,
    "cc": extract_cpp_units,
    "cxx": extract_cpp_units,
    "hpp": extract_cpp_units,
    "hxx": extract_cpp_units,
    # PowerShell
    "ps1": extract_powershell_units,
    "psm1": extract_powershell_units,
    "powershell": extract_powershell_units,
    # Ruby
    "rb": extract_ruby_units,
    "ruby": extract_ruby_units,
    # Lua
    "lua": extract_lua_units,
    # Elixir
    "ex": extract_elixir_units,
    "exs": extract_elixir_units,
    "elixir": extract_elixir_units,
    # Haskell
    "hs": extract_haskell_units,
    "lhs": extract_haskell_units,
    "haskell": extract_haskell_units,
    # Shell / Bash
    "sh": extract_bash_units,
    "bash": extract_bash_units,
    "ksh": extract_bash_units,
    "zsh": extract_bash_units,
    "shell": extract_bash_units,
    # SQL
    "sql": extract_sql_units,
    # Data / Config
    "toml": extract_toml_units,
    "yaml": extract_yaml_units,
    "yml": extract_yaml_units,
    "json": extract_json_units,
}

_PYGMENTS_REQUIRED = {
    "java", "cs", "csharp", "kotlin", "kt", "kts",
    "swift", "dart", "c", "h", "cpp", "cc", "cxx", "hpp", "hxx",
}


def _check_pygments(lang_key: str) -> None:
    if lang_key in _PYGMENTS_REQUIRED:
        try:
            import pygments  # noqa: F401
        except ImportError:
            raise ImportError(
                f"Language '{lang_key}' requires Pygments. "
                "Install it with: pip install pygments"
            )


def extract_units(path: str, language: Optional[str]) -> Dict[str, str]:
    p = Path(path)
    source = p.read_text(encoding="utf-8")

    lang_key: Optional[str] = None
    if language:
        lang_key = language.lower()
    else:
        suffix = p.suffix.lstrip(".").lower()
        if suffix:
            lang_key = suffix

    if lang_key is None or lang_key not in _EXTRACTORS:
        supported = sorted(set(_EXTRACTORS.keys()))
        raise ValueError(
            f"Cannot auto-detect language for '{path}' "
            f"(extension: '{p.suffix or 'none'}').\n"
            f"Pass --language explicitly with one of:\n  {', '.join(supported)}\n"
            f"Or use --manual-units for unsupported domains."
        )

    _check_pygments(lang_key)
    extractor = _EXTRACTORS[lang_key]
    return extractor(source)  # type: ignore[operator]


# ---------------------------------------------------------------------------
# Manual units (any domain)
# ---------------------------------------------------------------------------

def load_manual_units(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    units: Dict[str, str] = {}
    for entry in data:
        units[entry["name"]] = entry["content"]
    return units


# ---------------------------------------------------------------------------
# Manifest + diff
# ---------------------------------------------------------------------------

def build_manifest(units: Dict[str, str]) -> List[dict]:
    return [
        {"unit": name, "hash": sha256_text(content)}
        for name, content in sorted(units.items())
    ]


def diff_manifests(
    baseline: Dict[str, str], candidate: Dict[str, str]
) -> List[dict]:
    report = []
    for name in sorted(set(baseline) | set(candidate)):
        b = baseline.get(name)
        c = candidate.get(name)
        if b is not None and c is None:
            report.append({"unit": name, "verdict": "MISSING", "hash": sha256_text(b)})
        elif b is None and c is not None:
            report.append({"unit": name, "verdict": "NEW", "hash": sha256_text(c)})
        elif sha256_text(b) == sha256_text(c):
            report.append({"unit": name, "verdict": "UNCHANGED", "hash": sha256_text(b)})
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
        prog="golden_unit_hash",
        description=(
            f"Named-unit hashing for the Golden-Unit Protocol {_GUP_VERSION} "
            f"(script v{__version__}). Produces MISSING/UNCHANGED/CHANGED/NEW "
            "by unit name — never by line position. Digest comparison (§3) and "
            "the §4 architectural gate require model judgment and are NOT "
            "performed here."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Supported --language values:\n  {', '.join(sorted(set(_EXTRACTORS.keys())))}",
    )
    parser.add_argument("--baseline", metavar="FILE",
                        help="Path to baseline source file.")
    parser.add_argument("--candidate", metavar="FILE",
                        help="Path to candidate source file.")
    parser.add_argument("--language", metavar="LANG",
                        help="Override auto-detection (see supported values below).")
    parser.add_argument("--manual-units", metavar="FILE",
                        help='JSON file: [{"name": "...", "content": "..."}]')
    parser.add_argument("--manual-units-candidate", metavar="FILE",
                        help="Candidate JSON, paired with --manual-units.")
    parser.add_argument("--manifest-only", action="store_true",
                        help="Emit manifest for --baseline only; skip comparison.")
    parser.add_argument("--version", action="version",
                        version=f"golden_unit_hash {__version__} (GUP {_GUP_VERSION})")
    args = parser.parse_args()

    # ---- Load baseline ----
    if args.manual_units:
        baseline_units = load_manual_units(args.manual_units)
    elif args.baseline:
        baseline_units = extract_units(args.baseline, args.language)
    else:
        parser.error("Provide --baseline or --manual-units.")
        return

    # ---- Manifest-only mode ----
    if args.manifest_only:
        print(json.dumps({
            "gup_version": _GUP_VERSION,
            "script_version": __version__,
            "manifest": build_manifest(baseline_units),
        }, indent=2))
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

    print(json.dumps({
        "gup_version": _GUP_VERSION,
        "script_version": __version__,
        "baseline_manifest": build_manifest(baseline_units),
        "candidate_manifest": build_manifest(candidate_units),
        "diff": diff,
        "note": (
            "Verdicts are hash-based only. CHANGED and NEW units require "
            "the §3 semantic digest comparison and, if class is "
            "'orchestrator' or 'volatile-logic', the §4 architectural gate "
            "— both are judgment calls this script does not make."
        ),
    }, indent=2))

    # ---- Stderr signals ----
    missing  = [u for u in diff if u["verdict"] == "MISSING"]
    new_     = [u for u in diff if u["verdict"] == "NEW"]
    changed  = [u for u in diff if u["verdict"] == "CHANGED"]
    unchanged = [u for u in diff if u["verdict"] == "UNCHANGED"]

    print(
        f"\n[GUP {_GUP_VERSION} | script v{__version__}] "
        f"UNCHANGED={len(unchanged)}  CHANGED={len(changed)}  "
        f"NEW={len(new_)}  MISSING={len(missing)}",
        file=sys.stderr,
    )

    if new_:
        names = ", ".join(u["unit"] for u in new_)
        print(
            f"[REVIEW REQUIRED] NEW units — require §3 digest "
            f"and §4 Gate 2 review: {names}",
            file=sys.stderr,
        )

    if missing:
        names = ", ".join(u["unit"] for u in missing)
        print(
            f"[HARD FAIL] MISSING units (present in baseline, "
            f"absent in candidate): {names}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
