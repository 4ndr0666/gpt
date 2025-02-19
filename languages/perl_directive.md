Automate the entire process using Perl. Create comprehensive subroutines from the logic within each step. Ensure subroutines are encapsulated and reused appropriately to avoid redundancy. Use a central main subroutine call method in a menu loop. Ensure the script is idempotent and handles edge cases robustly. Include user confirmations before executing critical actions using CLI prompts. Follow these guidelines:

File Layout

    Comment with LICENSE and possibly short explanation of file/tool.
    Pragmas
    Constants
    Subroutine declarations:
        Include variable names.
        Group/order in logical manner.
    Global variables.
    Subroutine definitions in same order as declarations.
    main

Perl Features

    Use strict and warnings pragmas.
    Use named subroutines for better readability.
    Use Getopt::Long for command-line options.
    Use Pod::Usage for usage information.
    Use meaningful variable names.

Subroutines

    Define subroutines with sub keyword.
    Encapsulate logic within subroutines.
    Use meaningful variable names.
    Document subroutines with comments.

Handling Errors

    Use eval to catch exceptions.
    Use die for fatal errors with meaningful messages.
    Ensure the script is idempotent and handles edge cases robustly.
