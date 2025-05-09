#!/usr/bin/env python3
# SucklessGPT Debug Controller — Fully Compliant Version

import re
import subprocess
import tempfile
import shutil
import os
import sys
import json
import datetime
from typing import Tuple, List, Dict, Any

# ------------------------
# Configuration Defaults
# ------------------------
LINTERS = {
    'Python': ['pylint', '--disable=C0114,C0115,C0116'],
    'Shell': ['shellcheck', '--severity=warning'],
    'C': ['gcc', '-Wall', '-Wextra', '-std=c11', '-fsyntax-only']
}
FORMATTERS = {
    'Python': ['black', '--quiet'],
    'Shell': ['shfmt', '-w'],
    'C': ['clang-format', '-style=Google']
}
MAX_TOKEN_DIVISOR = 10
PROJECT_ROOT = os.getcwd()
LOG_FILE = os.path.expanduser('~/.debugger.log')

# ------------------------
# Abstract Reference Substitution
# ------------------------
def redact_internal_refs(text: str) -> str:
    return re.sub(
        r"`?(phase_debugger\.py|optimize\.md|notes\.md)`?",
        lambda m: {
            "phase_debugger.py": "**debug controller**",
            "optimize.md": "**optimization routines**",
            "notes.md": "**behavior map**"
        }.get(m.group(1), "**internal module**"),
        text
    )

# ------------------------
# Utility Functions
# ------------------------
def log_event(event: str) -> None:
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{ts} {event}\n")

def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ------------------------
# Language Detection
# ------------------------
def detect_language(code: str, filename: str = "") -> str:
    if filename.endswith('.py') or re.search(r'\bimport\b', code):
        return 'Python'
    if filename.endswith(('.sh', '.bash')) or code.startswith('#!') and ('/sh' in code or '/bash' in code):
        return 'Shell'
    if filename.endswith(('.c', '.h')) or re.search(r'#include <', code):
        return 'C'
    if filename.endswith(('.md', '.markdown')) or re.search(r'^# ', code, flags=re.MULTILINE):
        return 'Markdown'
    return 'Unknown'

# ------------------------
# Token / Complexity Analysis
# ------------------------
def adjust_tokens(code: str) -> int:
    base = len(code)
    keyword_count = sum(code.count(k) for k in ('def ', 'if ', 'for ', 'while ', ';', '{', '}'))
    complexity = base + keyword_count * 20
    return max(10, complexity // MAX_TOKEN_DIVISOR)

# ------------------------
# Static Analysis Checks
# ------------------------
def python_checks(code: str) -> Dict[str, Any]:
    errors: List[str] = []
    insights: List[str] = []

    if 'print(' not in code:
        insights.append('Consider using print() for user feedback.')
    if not re.search(r'\bdef\s+\w+\(', code) and 'class ' not in code:
        errors.append('No function or class definitions detected.')
    if len(code) > 10000:
        insights.append('File is large; consider splitting into modules.')

    try:
        proc = subprocess.run(LINTERS['Python'] + ['-'], input=code.encode('utf-8'),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        lint_out = proc.stdout.decode() + proc.stderr.decode()
        if proc.returncode != 0:
            errors.append('Pylint issues:\n' + lint_out.strip())
    except Exception as e:
        errors.append(f'Pylint failed: {e}')

    return {'errors': errors or ['OK'], 'insights': insights}

def shell_checks(code: str) -> Dict[str, Any]:
    errors: List[str] = []
    insights: List[str] = []

    if not code.startswith('#!'):
        errors.append('Missing shebang line.')
    if 'echo ' not in code:
        insights.append('Consider using echo for user messages.')

    try:
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write(code)
            tf.flush()
            proc = subprocess.run(LINTERS['Shell'] + [tf.name],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        os.unlink(tf.name)
        out = proc.stdout.decode() + proc.stderr.decode()
        if proc.returncode != 0:
            errors.append('ShellCheck issues:\n' + out.strip())
    except Exception as e:
        errors.append(f'ShellCheck failed: {e}')

    return {'errors': errors or ['OK'], 'insights': insights}

def c_checks(code: str) -> Dict[str, Any]:
    errors: List[str] = []
    insights: List[str] = []

    if 'main(' not in code:
        errors.append('Missing main() function.')
    if '#include' not in code:
        errors.append('No #include directives found.')

    try:
        with tempfile.NamedTemporaryFile('w', suffix='.c', delete=False) as tf:
            tf.write(code)
            tf.flush()
            proc = subprocess.run(LINTERS['C'] + [tf.name],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        os.unlink(tf.name)
        out = proc.stdout.decode() + proc.stderr.decode()
        if proc.returncode != 0:
            errors.append('C compilation issues:\n' + out.strip())
    except Exception as e:
        errors.append(f'GCC check failed: {e}')

    return {'errors': errors or ['OK'], 'insights': insights}

# ------------------------
# Markdown Checks
# ------------------------
def markdown_checks(code: str) -> Dict[str, Any]:
    errors: List[str] = []
    insights: List[str] = []

    if not re.search(r'^# ', code, flags=re.MULTILINE):
        insights.append('Add a top-level title using "# Title".')
    if re.search(r'[ \t]+$', code, flags=re.MULTILINE):
        insights.append('Remove trailing whitespace.')

    return {'errors': ['OK'], 'insights': insights}

# ------------------------
# Command Extraction
# ------------------------
def extract_command(msg: str) -> str:
    m = re.match(r'^/(store|view|write|parse|lint|debug|grade|feedback|status)\b', msg)
    return m.group(1) if m else ''

# ------------------------
# Main Debug Function
# ------------------------
def debug_code(code: str, filename: str = "") -> Dict[str, Any]:
    lang = detect_language(code, filename)
    token_budget = adjust_tokens(code)
    report: Dict[str, Any] = {
        'language': lang,
        'token_budget': token_budget,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }

    if lang == 'Python':
        result = python_checks(code)
    elif lang == 'Shell':
        result = shell_checks(code)
    elif lang == 'C':
        result = c_checks(code)
    elif lang == 'Markdown':
        result = markdown_checks(code)
    else:
        result = {'errors': ['Unsupported or unknown language'], 'insights': []}

    result['errors'] = [redact_internal_refs(e) for e in result['errors']]
    result['insights'] = [redact_internal_refs(i) for i in result['insights']]
    report.update(result)
    log_event(f"Debugged {lang} code; errors={result['errors']}")
    return report

# ------------------------
# CLI Interface
# ------------------------
def main_cli():
    import argparse
    parser = argparse.ArgumentParser(description='Debugger utility for code analysis')
    parser.add_argument('file', help='Path to source file to debug')
    parser.add_argument('--json', action='store_true', help='Output report as JSON')
    args = parser.parse_args()

    code = read_file(args.file)
    report = debug_code(code, args.file)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Language: {report['language']}")
        print(f"Token Budget: {report['token_budget']}")
        print("Errors:")
        for e in report['errors']:
            print(f"  - {e}")
        print("Insights:")
        for i in report.get('insights', []):
            print(f"  - {i}")

if __name__ == '__main__':
    main_cli()
