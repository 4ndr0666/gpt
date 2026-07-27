Automate the entire process using Rust. Create comprehensive functions from the logic within each step. Ensure functions are encapsulated and reused appropriately to avoid redundancy. Use a central main function call method in a menu loop. Ensure the script is idempotent and handles edge cases robustly. Include user confirmations before executing critical actions using CLI prompts. Follow these guidelines:

File Layout

    Comment with LICENSE and possibly short explanation of file/tool.
    Crate attributes
    Modules
    Imports
    Constants
    Variables
    Function declarations:
        Include variable names.
        Group/order in logical manner.
    main

Rust Features

    Follow Rust guidelines (rustfmt).
    Use Result and Option for error handling.
    Group related functions together.
    Use proper error messages.

Functions

    Define functions with fn keyword.
    Encapsulate logic within functions.
    Use meaningful variable names.
    Document functions with comments.

Handling Errors

    Return Result from functions and check them.
    Use panic! for unrecoverable errors.
    Ensure the script is idempotent and handles edge cases robustly.
