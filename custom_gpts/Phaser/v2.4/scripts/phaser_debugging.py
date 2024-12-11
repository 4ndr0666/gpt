import re
import subprocess

# Adjust token allocation based on code complexity
def adjust_tokens(code):
    """
    Adjust tokens based on the complexity of the provided code. 
    This function counts lines, functions, control structures, and loops to determine complexity.
    """
    complexity = len(code) + code.count('def') + code.count('if') + code.count('for') + code.count('while')
    # Token adjustment logic based on complexity
    return max(1, complexity // 10)

# Detect the programming language based on the code content
def detect_language(code):
    """
    Detect the programming language of the provided code by analyzing keywords or constructs.
    Currently supports Python and Shell (bash) detection.
    """
    if "def" in code:
        return "Python"
    elif re.search(r'#!/bin/(sh|bash)', code):
        return "Shell"
    return None

# Main function that handles debugging and returns errors, insights, and token adjustments
def debug_code(code):
    """
    Main function to debug the code based on detected language. 
    It adjusts tokens based on complexity, applies language-specific checks, and provides insights.
    """
    language = detect_language(code)
    tokens = adjust_tokens(code)

    if language == "Python":
        errors, insights = python_debug_checks(code)
    elif language == "Shell":
        errors, insights = shell_debug_checks(code)
    else:
        return handle_error("003"), tokens  # Unsupported Language Error

    return errors, insights, tokens

# Python-specific debugging checks
def python_debug_checks(code):
    """
    Perform Python-specific checks on the provided code. 
    This includes checking for syntax issues, missing key statements, and providing performance optimization insights.
    """
    errors = []
    insights = []

    # Check for missing print statements in functions
    if "print(" not in code:
        errors.append("Warning: Missing print statement in Python code. Ensure output is handled properly.")
    
    # Ensure all functions and classes are properly defined
    if not re.match(r'^[ \t]*(def|class)[ \t]+\w+\(', code):
        errors.append("Error: Functions or classes are not properly defined.")

    # Check for idempotency issues (random operations)
    if re.search(r'random\.\w+\(', code):
        insights.append("Code might not be idempotent due to random operations. Ensure deterministic behavior.")

    # Check for loop count and provide optimization advice if necessary
    loop_count = code.count("for") + code.count("while")
    if loop_count > 10:
        insights.append("Consider optimizing loops. More than 10 loops detected, which may affect performance.")

    # Check for global variable usage (can affect modularity and maintainability)
    if "global" in code:
        insights.append("Global variables detected. Consider refactoring to avoid global state and improve modularity.")

    return errors, insights if errors or insights else ["No errors found"]

# Shell script-specific debugging checks
def shell_debug_checks(code):
    """
    Perform shell script-specific checks on the provided code. 
    This includes checking for proper shebang, missing echo statements, and linting via shellcheck.
    """
    errors = []
    insights = []

    # Check if shell script has the proper shebang
    if not re.match(r'#!/bin/(sh|bash)', code):
        errors.append("Error: Shell script is missing a proper shebang (#!) at the top of the file.")
    
    # Check for missing echo statements (to provide feedback in shell scripts)
    if not re.search(r'echo', code):
        insights.append("Consider adding echo statements for better feedback during shell script execution.")

    # Perform shell script linting using external shellcheck (if available)
    shell_lint_results = shell_lint_check(code)
    if shell_lint_results != "No issues found.":
        errors.append(shell_lint_results)

    return errors, insights if errors or insights else ["No errors found"]

# External shell linting using subprocess and shellcheck
def shell_lint_check(shell_code):
    """
    Perform shell script linting using shellcheck if available. 
    This function captures and returns any issues found or indicates if no issues are detected.
    """
    try:
        result = subprocess.run(['shellcheck', '--format=gcc'], input=shell_code, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            return result.stdout  # Return any linting errors
        return "No issues found."
    except FileNotFoundError:
        return "Warning: shellcheck tool is not available. Skipping shell linting."
    except Exception as e:
        return f"Error while running shellcheck: {str(e)}"

# Handle error codes for unsupported or unknown languages
def handle_error(error_code):
    """
    Handle different error codes based on the detected language or internal processing.
    This function maps error codes to descriptive error messages.
    """
    error_messages = {
        "003": "Unsupported language error. The provided code language is not supported.",
        "004": "Unknown language error. Unable to detect the programming language."
    }
    return error_messages.get(error_code, "Unrecognized error code.")

# Main entry point for testing/debugging purposes (this will not execute in GPT environment)
if __name__ == "__main__":
    # Sample Python code for debugging
    sample_code_python = '''
    def my_func():
        x = 5
        print(x)
    '''

    # Sample Shell script for debugging
    sample_code_shell = '''
    #!/bin/bash
    echo "Hello, World!"
    '''

    # Debug Python code
    python_errors, python_insights, python_tokens = debug_code(sample_code_python)
    print("Python Errors:", python_errors)
    print("Python Insights:", python_insights)
    print("Python Tokens:", python_tokens)

    # Debug Shell script
    shell_errors, shell_insights, shell_tokens = debug_code(sample_code_shell)
    print("Shell Errors:", shell_errors)
    print("Shell Insights:", shell_insights)
    print("Shell Tokens:", shell_tokens)
