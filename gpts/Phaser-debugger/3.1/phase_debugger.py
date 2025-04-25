import re
import subprocess

# Adjust tokens based on complexity
def adjust_tokens(code):
    complexity = len(code) + code.count('def') + code.count('if') + code.count('for') + code.count('while')
    return max(1, complexity // 10)

# Detect language
def detect_language(code):
    if "def " in code or "class " in code:
        return "Python"
    if re.search(r'#!/bin/(sh|bash)', code):
        return "Shell"
    return None

# Main debug handler
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

# Python checks
def python_debug_checks(code):
    errors = []
    insights = []

    if "print(" not in code:
        errors.append("Warning: Missing print statement for output visibility.")
    if not re.search(r'(def|class)\s+\w+', code):
        errors.append("Error: Functions or classes may be improperly defined.")
    if "random." in code:
        insights.append("Randomness detected. Consider ensuring deterministic behavior.")
    if code.count("for") + code.count("while") > 10:
        insights.append("Optimization Tip: >10 loops detected, review performance impact.")
    if "global" in code:
        insights.append("Global variables found; recommend modularization.")

    return errors, insights if (errors or insights) else ["No errors found"]

# Shell checks
def shell_debug_checks(code):
    errors = []
    insights = []

    if not re.match(r'#!/bin/(sh|bash)', code):
        errors.append("Error: Missing or incorrect shebang.")
    if "echo" not in code:
        insights.append("Consider adding echo statements for user feedback.")

    lint = shell_lint_check(code)
    if lint != "No issues found.":
        errors.append(lint)

    return errors, insights if (errors or insights) else ["No errors found"]

# Shell lint
def shell_lint_check(shell_code):
    try:
        result = subprocess.run(['shellcheck', '--format=gcc'], input=shell_code, capture_output=True, text=True, shell=True)
        return result.stdout if result.returncode != 0 else "No issues found."
    except FileNotFoundError:
        return "Warning: shellcheck not found."
    except Exception as e:
        return f"Error during shellcheck: {str(e)}"

# Error Handling
def handle_error(error_code):
    return {
        "003": "Unsupported language error. Only Python and Shell supported.",
        "004": "Unknown language error. Cannot detect the programming language."
    }.get(error_code, "Unrecognized error.")
