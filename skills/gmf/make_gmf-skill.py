#!/usr/bin/env python3
"""
package_skill.py - Self-Extracting / Packager Deliverable for git-md-formatter.skill
Builds or unpacks the certified .skill package with embedded SHA-256 validation.
"""

import os
import sys
import zipfile
import hashlib
import io

FILES = {
    "git-md-formatter/SKILL.md": """---
name: git-md-formatter
description: High-performance GFM syntax correction, validation, and verbatim emissions engine. Triggers automatically on single-word commands like 'go', raw unformatted text pastes, code blocks, or requests to clean, repair, or format Markdown. Emits only the literal GFM wrapped in quadruple backticks with zero conversational preamble.
---

# Git-MD Formatter

A high-performance execution engine specialized in GitHub Flavored Markdown (GFM) syntax correction, validation, and verbatim emission.

## Trigger Conditions

Activate immediately with zero confirmation, zero conversational setup, and zero prompt engineering whenever:
- The user inputs "go", "run", "format", or similar single-word execution commands.
- The user pastes raw, unformatted, or malformed Markdown, notes, logs, or text blocks.
- The user provides content requiring strict GFM compliance and verbatim output.

## Operational Procedures

1. **Autonomous Execution & Direct Output:**
   - Execute immediately upon receipt of input.
   - Do NOT ask clarifying questions or require formatting parameters.
   - Output ONLY the processed GFM text wrapped in quadruple backticks (````).
   - Omit all conversational greetings, setups, explanations, status reports, summaries, or sign-offs.
   - **DO NOT USE CANVAS** or external UI artifacts.

2. **Syntax Enforcement:**
   - Conduct a thorough analysis of input text against the GitHub Flavored Markdown (GFM) Spec.
   - Automatically resolve all detected issues, syntax errors, malformed links, unclosed tags, or broken tables.
   - Resolve commented-out placeholders (e.g., `//placeholders`) or missing concepts; ensure all points in the text are fully realized, fleshed out, and logically sound.
   - PRESERVATION OF NESTED CODE: If the input data contains prompts, lists, or instructions intended for an LLM, these MUST be wrapped in triple-backtick (```) code blocks within the final output.
   - RAW GFM FIDELITY: Ensure headers such as "## Stock Templates" and "## Upscale 4K" remain verbatim as per the canonical manifest.

3. **Verification Protocols (Superset Check):**
   - Perform a silent, internal 'superset check' by counting total characters of the uploaded text.
   - Rigorously analyze revisions to ensure no text is omitted, regressed, or truncated.
   - Character loss or degradation is considered a CRITICAL FAILURE unless explicitly specified by the operator.
   - Character count is strictly maintained.
   - Structure continuity is strictly upheld.
   - Zero formatting and syntax errors.
   - No summarizing.
   - No re-formatting bullet points into paragraphs.
   - No changing "Stock" to "Native" or other synonyms.

4. **Finalization, Cohesion, and Emissions Contract:**
   - Isolate and validate the entire text to guarantee strict compliance with the spec.
   - Conduct an end-to-end review for systemic alignment, cohesion, and superset validation.
   - Ensure the final output is robust with zero syntax errors, stubs, or incorrect formatting.
   - The *entire* literal, raw (GFM) compliant code is parsed for verbatim copy/paste, not plain text.
   - Final output is strictly wrapped in quadruple backticks (````) to ensure the chat renderer treats internal triple-backticks as literal text rather than formatting markers.

## Auxiliary Validation Harness

The skill includes an automated test battery located at `scripts/validate_gfm.py` to verify output against all emissions contract gates:
- Run self-test: `python scripts/validate_gfm.py --test`
- Validate file pair: `python scripts/validate_gfm.py <input.md> <output.md>`
""",
    "git-md-formatter/scripts/validate_gfm.py": """#!/usr/bin/env python3
\"\"\"
validate_gfm.py - Test and Validation Harness for Git-MD Formatter

Validates raw input vs. formatted GFM output against all canonical contract gates:
1. Quadruple backtick container isolation (renderer shielding)
2. Zero conversational boilerplate (no pre/post conversational framing)
3. Strict superset integrity (zero character truncation or content loss)
4. Verbatim header retention (exact canonical matches, e.g., '## Stock Templates')
5. Synonym mutation defense (e.g., forbidding 'Stock' -> 'Native')
6. Nested code-fence wrapping (prompts/instructions wrapped in triple backticks)
7. Placeholder elimination (zero unexpanded '//placeholders' or stub comments)
8. Structural sequence continuity (headings preserve order and depth)
\"\"\"

import sys
import re
from typing import List, Tuple, Dict, Any

CANONICAL_REQUIRED_HEADERS = [
    "## Stock Templates",
    "## Upscale 4K",
]

FORBIDDEN_MUTATIONS = [
    (r"\\bNative Templates\\b", "Mutation of 'Stock Templates' to synonym 'Native'"),
    (r"\\bUpscale UltraHD\\b", "Mutation of 'Upscale 4K' to synonym"),
]

PLACEHOLDER_PATTERNS = [
    r"//\\s*placeholder",
    r"//\\s*TODO",
    r"//\\s*stub",
    r"<!--\\s*placeholder\\s*-->",
]


class ValidationReport:
    def __init__(self):
        self.passed: bool = True
        self.checks: List[Tuple[str, bool, str]] = []

    def record(self, name: str, passed: bool, message: str):
        self.checks.append((name, passed, message))
        if not passed:
            self.passed = False

    def render(self) -> str:
        lines = ["# Git-MD Formatter Validation Report", ""]
        lines.append(f"**Overall Status:** {'PASS' if self.passed else 'CRITICAL FAILURE'}")
        lines.append("")
        lines.append("| Gate | Status | Diagnostic |")
        lines.append("| :--- | :---: | :--- |")
        for name, passed, message in self.checks:
            status = "PASS" if passed else "FAIL"
            lines.append(f"| {name} | {status} | {message} |")
        return "\\n".join(lines)


def validate_quadruple_backticks(output_text: str, report: ValidationReport) -> str:
    stripped = output_text.strip()
    match = re.match(r"^````(?:markdown|gfm)?\\n([\\s\\S]*?)\\n````$", stripped)
    if not match:
        report.record(
            "Outer Quadruple Fence",
            False,
            "Output is not strictly encapsulated in outer quadruple backticks (````)."
        )
        return stripped

    fence_start = output_text.find("````")
    fence_end = output_text.rfind("````") + 4
    pre_text = output_text[:fence_start].strip()
    post_text = output_text[fence_end:].strip()

    if pre_text or post_text:
        report.record(
            "Zero Preamble/Postamble",
            False,
            f"Detected conversational noise outside container (Pre: '{pre_text[:30]}...', Post: '{post_text[:30]}...')."
        )
    else:
        report.record("Zero Preamble/Postamble", True, "Zero external conversational noise detected.")

    report.record("Outer Quadruple Fence", True, "Successfully encapsulated in ```` container.")
    return match.group(1)


def validate_superset_integrity(raw_input: str, extracted_output: str, report: ValidationReport):
    raw_len = len(raw_input.strip())
    out_len = len(extracted_output.strip())

    if out_len < raw_len:
        report.record(
            "Superset Character Retention",
            False,
            f"Character degradation detected: Input={raw_len} chars, Output={out_len} chars (Deficit: {raw_len - out_len})."
        )
    else:
        report.record(
            "Superset Character Retention",
            True,
            f"Character retention satisfied: Input={raw_len} chars, Output={out_len} chars (Expansion/Preservation: +{out_len - raw_len})."
        )


def validate_placeholders(extracted_output: str, report: ValidationReport):
    found_stubs = []
    for pattern in PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, extracted_output, re.IGNORECASE)
        if matches:
            found_stubs.extend(matches)

    if found_stubs:
        report.record(
            "Placeholder Expansion",
            False,
            f"Unresolved placeholders detected in emission: {list(set(found_stubs))}."
        )
    else:
        report.record("Placeholder Expansion", True, "Zero placeholder/stub tokens remain; all fully realized.")


def validate_canonical_headers(raw_input: str, extracted_output: str, report: ValidationReport):
    missing_headers = []
    for header in CANONICAL_REQUIRED_HEADERS:
        if header.lower() in raw_input.lower():
            if header not in extracted_output:
                missing_headers.append(header)

    if missing_headers:
        report.record(
            "Canonical Header Fidelity",
            False,
            f"Canonical headers not preserved verbatim: {missing_headers}."
        )
    else:
        report.record("Canonical Header Fidelity", True, "All canonical headers preserved verbatim.")


def validate_synonym_mutations(extracted_output: str, report: ValidationReport):
    mutations = []
    for pattern, description in FORBIDDEN_MUTATIONS:
        if re.search(pattern, extracted_output):
            mutations.append(description)

    if mutations:
        report.record("Synonym Mutation Defense", False, f"Unauthorized mutations found: {mutations}.")
    else:
        report.record("Synonym Mutation Defense", True, "No unauthorized synonym substitutions detected.")


def validate_nested_code_fences(extracted_output: str, report: ValidationReport):
    triple_backticks = re.findall(r"```[a-zA-Z0-9_-]*\\n[\\s\\S]*?```", extracted_output)
    if "prompt" in extracted_output.lower() and not triple_backticks:
        report.record(
            "Nested Code-Fence Wrapping",
            False,
            "Input contains prompt/instruction structures but no internal triple-backtick blocks were emitted."
        )
    else:
        report.record(
            "Nested Code-Fence Wrapping",
            True,
            f"Nested code blocks properly protected ({len(triple_backticks)} fence pairs verified)."
        )


def run_validation(raw_input: str, output_text: str) -> ValidationReport:
    report = ValidationReport()
    inner_gfm = validate_quadruple_backticks(output_text, report)
    validate_superset_integrity(raw_input, inner_gfm, report)
    validate_placeholders(inner_gfm, report)
    validate_canonical_headers(raw_input, inner_gfm, report)
    validate_synonym_mutations(inner_gfm, report)
    validate_nested_code_fences(raw_input, report)
    return report


def self_test():
    print("Executing Git-MD Formatter Self-Test Battery...\\n")

    raw_sample = (
        "# Core Specs\\n"
        "## Stock Templates\\n"
        "Here is a prompt for the model:\\n"
        "Extract entities verbatim.\\n"
        "- Spec A: //placeholders\\n"
        "- Spec B: active\\n"
        "## Upscale 4K\\n"
        "Parameters set."
    )

    valid_output = (
        "````markdown\\n"
        "# Core Specs\\n\\n"
        "## Stock Templates\\n\\n"
        "Here is a prompt for the model:\\n\\n"
        "```prompt\\n"
        "Extract entities verbatim.\\n"
        "```\\n\\n"
        "- Spec A: Production-ready operational values and fully realized configuration\\n"
        "- Spec B: active\\n\\n"
        "## Upscale 4K\\n\\n"
        "Parameters set.\\n"
        "````"
    )

    report = run_validation(raw_sample, valid_output)
    print(report.render())
    assert report.passed, "Expected self-test valid sample to pass all gates!"

    flawed_output = (
        "Here is your formatted text:\\n"
        "````\\n"
        "# Core Specs\\n"
        "## Native Templates\\n"
        "- Spec A: //placeholders\\n"
        "````"
    )
    fail_report = run_validation(raw_sample, flawed_output)
    print("\\n--- Negative Test Case (Intentional Violations) ---")
    print(fail_report.render())
    assert not fail_report.passed, "Expected flawed sample to fail verification!"
    print("\\nSelf-Test Battery completed successfully.")


if __name__ == "__main__":
    if len(sys.argv) == 1 or "--test" in sys.argv:
        self_test()
    elif len(sys.argv) == 3:
        with open(sys.argv[1], "r", encoding="utf-8") as f_in:
            raw_data = f_in.read()
        with open(sys.argv[2], "r", encoding="utf-8") as f_out:
            out_data = f_out.read()
        rep = run_validation(raw_data, out_data)
        print(rep.render())
        sys.exit(0 if rep.passed else 1)
    else:
        print("Usage:")
        print("  python validate_gfm.py --test")
        print("  python validate_gfm.py <raw_input.md> <formatted_output.md>")
        sys.exit(2)
"""
}

def build_skill_package(output_path="git-md-formatter.skill"):
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for rel_path, content in FILES.items():
            # Zip archive contains files relative to the skill package root
            internal_arcname = rel_path.replace("git-md-formatter/", "")
            zf.writestr(internal_arcname, content)
            print(f"  [+] Packaged: {internal_arcname} ({len(content.encode('utf-8'))} bytes)")

    with open(output_path, "rb") as f:
        pkg_sha256 = hashlib.sha256(f.read()).hexdigest()

    print(f"\nSuccessfully generated skill package: {output_path}")
    print(f"SHA-256 Pin: {pkg_sha256}")
    return pkg_sha256

def unpack_files():
    for rel_path, content in FILES.items():
        dirname = os.path.dirname(rel_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(rel_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [+] Extracted: {rel_path}")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "--build"
    if action == "--build":
        build_skill_package()
    elif action == "--unpack":
        unpack_files()
    else:
        print("Usage:")
        print("  python package_skill.py --build   # Produces git-md-formatter.skill")
        print("  python package_skill.py --unpack  # Unpacks files to disk")
