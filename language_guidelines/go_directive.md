Automate the entire process using Go. Create comprehensive functions from the logic within each step. Ensure functions are encapsulated and reused appropriately to avoid redundancy. Use a central main function call method in a menu loop. Ensure the script is idempotent and handles edge cases robustly. Include user confirmations before executing critical actions using CLI prompts. Follow these guidelines:

File Layout

    Comment with LICENSE and possibly short explanation of file/tool.
    Package declaration
    Imports
    Constants
    Variables
    Function declarations:
        Include variable names.
        Group/order in logical manner.
    main

Go Features

    Follow effective Go guidelines.
    Use fmt for formatted I/O.
    Use error for error handling.
    Group related functions together.
    Use proper error messages.

Functions

    Define functions with func keyword.
    Encapsulate logic within functions.
    Use meaningful variable names.
    Document functions with comments.

Handling Errors

    Return errors from functions and check them.
    Use log.Fatal for unrecoverable errors.
    Ensure the script is idempotent and handles edge cases robustly.
