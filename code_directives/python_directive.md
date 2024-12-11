Automate the entire process using a CLI tool in Python. Organize the code with comprehensive functions for each logical step. Ensure functions are encapsulated and reused appropriately to avoid redundancy. Use a central main function call method in a menu loop. Ensure the script is idempotent and handles edge cases robustly. Include user confirmations before executing critical actions using a CLI prompt. Follow these guidelines:

File Layout

    Comment with LICENSE and possibly short explanation of file/tool.
    Imports
    Constants
    Function declarations:
        Include variable names.
        Group/order in logical manner.
    Main function.

Python Features

    Use PEP 8 style guide.
    Separate functions by two blank lines.
    Use docstrings for function documentation.
    Place all imports at the top of the file.
    Handle exceptions robustly with try/except blocks.
    Use logging for error messages instead of print.

Functions

    Define functions with def keyword.
    Encapsulate logic within functions.
    Use meaningful variable names.
    Include type hints for function arguments and return values.

Handling Errors

    Use try/except blocks to handle exceptions.
    Log errors with logging module.
    Exit early on failures instead of nested levels.
    Ensure the script is idempotent and handles edge cases robustly.
