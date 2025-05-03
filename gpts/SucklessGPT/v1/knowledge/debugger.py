#!/usr/bin/env python3
# debugger.py (v2.2.0)
# Automates phase transitions, static and dynamic analysis, and debugging routines
# per the SucklessCodeGPT minimalistic philosophy. Supports Python, Shell, C, and
# additional languages. Provides extensible hooks, detailed reports, and integration
# with external linters/formatters.

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
    'Python': ['pylint', '--disable=C0114,C0115,C0116'],  # disable missing docstring warnings
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
# Utility Functions
# ------------------------
def log_event(event: str) -> None:
    """Append a timestamped event to the debug log."""
    ts = datetime.datetime.utcnow().isoformat() + 'Z'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{ts} {event}\n")

def read_file(path: str) -> str:
    """Read a file and return its contents."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    """Write content to a file, creating directories as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# ------------------------
# Language Detection
# ------------------------
def detect_language(code: str, filename: str = "") -> str:
    """
    Detect the programming language based on shebang, file extension, or code patterns.
    Returns one of: Python, Shell, C, Markdown, Unknown.
    """
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
    """
    Estimate token budget for analysis based on code complexity:
    length + counts of keywords and punctuation.
    """
    base = len(code)
    keyword_count = sum(code.count(k) for k in ('def ', 'if ', 'for ', 'while ', ';', '{', '}'))
    complexity = base + keyword_count * 20
    return max(10, complexity // MAX_TOKEN_DIVISOR)

# ------------------------
# Static Analysis Checks
# ------------------------
def python_checks(code: str) -> Dict[str, Any]:
    """Run static analysis and style checks for Python code."""
    errors: List[str] = []
    insights: List[str] = []

    # Basic pattern checks
    if 'print(' not in code:
        insights.append('Consider using print() for user feedback.')
    if not re.search(r'\bdef\s+\w+\(', code):
        errors.append('No function definitions detected.')
    if len(code) > 10000:
        insights.append('File is large; consider splitting into modules.')

    # External linter
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
    """Run checks for shell scripts."""
    errors: List[str] = []
    insights: List[str] = []

    # Shebang
    if not code.startswith('#!'):
        errors.append('Missing shebang line.')
    # UX echo
    if 'echo ' not in code:
        insights.append('Consider using echo for user messages.')

    # External linter
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
    """Run checks for C code."""
    errors: List[str] = []
    insights: List[str] = []

    # Basic structural checks
    if 'main(' not in code:
        errors.append('Missing main() function.')
    if '#include' not in code:
        errors.append('No #include directives found.')

    # External compiler syntax check
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
    """Perform basic checks on Markdown documents."""
    errors: List[str] = []
    insights: List[str] = []

    # Ensure front-matter or title
    if not re.search(r'^# ', code, flags=re.MULTILINE):
        insights.append('Add a top-level title using "# Title".')
    # Check for trailing whitespace
    if re.search(r'[ \t]+$', code, flags=re.MULTILINE):
        insights.append('Remove trailing whitespace.')

    # Optional: pandoc or markdownlint could be integrated here

    return {'errors': ['OK'], 'insights': insights}

# ------------------------
# Command Extraction
# ------------------------
def extract_command(msg: str) -> str:
    """
    Extract a slash-command from a chat message.
    Supported: /store, /view, /write, /parse, /lint, /debug, /grade, /feedback, /status
    """
    m = re.match(r'^/(store|view|write|parse|lint|debug|grade|feedback|status)\b', msg)
    return m.group(1) if m else ''

# ------------------------
# Main Debug Function
# ------------------------
def debug_code(code: str, filename: str = "") -> Dict[str, Any]:
    """
    Perform full debug analysis:
    - Detect language
    - Run static checks
    - Run optional formatters
    - Return a comprehensive report dict
    """
    lang = detect_language(code, filename)
    token_budget = adjust_tokens(code)
    report: Dict[str, Any] = {
        'language': lang,
        'token_budget': token_budget,
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    }

    # Route to appropriate check
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
