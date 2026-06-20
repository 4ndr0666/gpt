Automate the entire process using standard C. Create comprehensive functions from the logic within each step. Ensure functions are encapsulated and reused appropriately to avoid redundancy. Use a central main function call method in a menu loop. Ensure the script is idempotent and handles edge cases robustly. Include user confirmations before executing critical actions using command-line prompts. Follow these guidelines:

File Layout

    Comment with LICENSE and possibly short explanation of file/tool.
    Headers
    Macros
    Types
    Function declarations:
        Include variable names.
        Group/order in logical manner.
    Global variables.
    Function definitions in same order as declarations.
    main

C Features

    Use C99 without extensions (ISO/IEC 9899:1999).
    Use POSIX.1-2008:
        When using gcc define _POSIX_C_SOURCE 200809L.
        Alternatively define _XOPEN_SOURCE 700.
    Do not mix declarations and code.
    Do not use for loop initial declarations.
    Use /* */ for comments, not //.
    Variadic macros are acceptable, but remember:
        __VA_ARGS__ not a named parameter.
        Arg list cannot be empty.

Blocks

    All variable declarations at top of block.
    { on same line preceded by single space (except functions).
    } on own line unless continuing statement (if else, do while, ...).

Use block for single statement if inner statement needs a block.

for (;;) {
	if (foo) {
		bar;
		baz;
	}
}

Use block if another branch of the same statement needs a block:

if (foo) {
	bar;
} else {
	baz;
	qux;
}

Leading Whitespace

Use tabs for indentation and spaces for alignment. This ensures everything will line up independent of tab size. This means:

    No tabs except beginning of line.
    Use spaces - not tabs - for multiline macros as the indentation level is 0, where the #define began.

Functions

    Return type and modifiers on own line.
    Function name and argument list on next line. This allows to grep for function names simply using grep ^functionname(.
    Opening { on own line (function definitions are a special case of blocks as they cannot be nested).
    Functions not used outside translation unit should be declared and defined static.

Example:

static void
usage(void)
{
	eprintf("usage: %s [file ...]\n", argv0);
}

Variables

    Global variables not used outside translation unit should be declared static.
    In declaration of pointers the * is adjacent to variable name, not type.

Keywords

    Use a space after if, for, while, switch (they are not function calls).
    Do not use a space after the opening ( and before the closing ).
    Preferably use () with sizeof.
    Do not use a space with sizeof().

Switch

    Do not indent cases another level.
    Comment cases that FALLTHROUGH.

Example:

switch (value) {
case 0: /* FALLTHROUGH */
case 1:
case 2:
	break;
default:
	break;
}

Headers

    Place system/libc headers first in alphabetical order.
        If headers must be included in a specific order add a comment to explain.
    Place local headers after an empty line.
    When writing and using local headers.
        Try to avoid cyclic header inclusion dependencies.
        Instead ensure they are included where and when they are needed.
        Read https://talks.golang.org/2012/splash.article#TOC_5.
        Read http://plan9.io/sys/doc/comp.html

User Defined Types

    Do not use type_t naming (it is reserved for POSIX and less readable).
    Typedef opaque structs.
    Do not typedef builtin types.
    Use CamelCase for typedef'd types.

Line Length

    Keep lines to reasonable length (max 79 characters).

Tests and Boolean Values

    Do not use C99 bool types (stick to integer types).
    Otherwise use compound assignment and tests unless the line grows too long:

if (!(p = malloc(sizeof(*p))))
	hcf();

Handling Errors

    When functions return -1 for error test against 0 not -1:

if (func() < 0)
	hcf();

    Use goto to unwind and cleanup when necessary instead of multiple nested levels.
    return or exit early on failures instead of multiple nested levels.
    Unreachable code should have a NOTREACHED comment.
    Think long and hard on whether or not you should cleanup on fatal errors. For simple "one-shot" programs (not daemons) it can be OK to not free memory. It is advised to cleanup temporary files however.

Enums and #define

Use enums for values that are grouped semantically and #define otherwise:

#define MAXSZ  4096
#define MAGIC1 0xdeadbeef

enum {
	DIRECTION_X,
	DIRECTION_Y,
	DIRECTION_Z
};
