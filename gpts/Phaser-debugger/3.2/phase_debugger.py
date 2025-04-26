# phase_debugger.py (v2.0.0)

import re
import subprocess

def adjust_tokens(code):
    complexity = len(code) + code.count('def') + code.count('if') + code.count('for') + code.count('while')
    return max(1, complexity // 10)

def detect_language(code):
    if "def" in code: return "Python"
    if re.search(r'#!/bin/(sh|bash)', code): return "Shell"
    return None

def debug_code(code):
    language = detect_language(code)
    tokens = adjust_tokens(code)
    if language == "Python":
        errors, insights = python_debug_checks(code)
    elif language == "Shell":
        errors, insights = shell_debug_checks(code)
    else:
        return handle_error("003"), tokens
    return errors, insights, tokens

def python_debug_checks(code):
    errors = []
    insights = []
    if "print(" not in code:
        errors.append("Warning: Missing print statement.")
    if not re.match(r'^[ \t]*(def|class)[ \t]+\w+\(', code):
        errors.append("Error: Missing proper function/class definition.")
    if re.search(r'random\.', code):
        insights.append("Random operations found, may cause non-deterministic behavior.")
    return errors, insights if errors or insights else ["No errors found"]

def shell_debug_checks(code):
    errors = []
    insights = []
    if not re.match(r'#!/bin/(sh|bash)', code):
        errors.append("Error: Missing shebang.")
    if not re.search(r'echo', code):
        insights.append("Consider adding echo statements for better UX.")
    return errors, insights if errors or insights else ["No errors found"]

def handle_error(code):
    errors = {
        "003": "Unsupported language error."
    }
    return errors.get(code, "Unknown error.")