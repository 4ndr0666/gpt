
import { SupportedLanguage } from './types.ts';

export const LANGUAGE_SPECIFIC_INSTRUCTIONS: Record<SupportedLanguage, string> = {
  [SupportedLanguage.JAVASCRIPT]: `## Summary for JavaScript

 Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
 You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
 You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Coercion & Equality:** Consistently uses strict equality (\`===\` and \`!==\`) to prevent unexpected type coercion bugs.
- **Variable Scoping:** Correctly uses \`let\` and \`const\` for block-scoped variable declarations, avoiding \`var\`.
- **Asynchronous Operations:** Implements Promises or \`async/await\` for asynchronous tasks with robust error handling (e.g., \`try/catch\` with \`await\`, \`.catch()\` for Promises).
- **Error Handling:** Employs comprehensive error handling mechanisms (e.g., \`try...catch\`, custom \`Error\` objects) for both synchronous and asynchronous code.
- **DOM Manipulation (if applicable):** Uses efficient, secure, and framework-idiomatic DOM manipulation, sanitizing user inputs to prevent XSS when directly manipulating \`innerHTML\` or similar properties.
- **Modularity & Reusability:** Code is well-organized into modules (ESM syntax), functions, and classes that are reusable and follow the Single Responsibility Principle.
- **Truthy/Falsy Values:** Demonstrates a clear understanding of JavaScript's truthy and falsy values in conditional logic.
- **Array & Object Methods:** Utilizes modern array/object methods (\`map\`, \`filter\`, \`reduce\`, \`find\`, spread/rest syntax, optional chaining, nullish coalescing) appropriately for conciseness and readability.
- **\`this\` Keyword Context:** Shows correct understanding and binding of \`this\` in various contexts (functions, classes, arrow functions, event handlers).
- **Performance Considerations:** Avoids common performance bottlenecks such as excessive DOM manipulations in loops, blocking operations on the main thread, or inefficient algorithms.
- **Code Style & Readability:** Adheres to a consistent code style (e.g., consistent naming conventions like camelCase, indentation, comments where necessary).
- **Security:** Actively guards against common web vulnerabilities (e.g., XSS, CSRF if applicable) and validates/sanitizes all external data.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.TYPESCRIPT]: `## Summary for TypeScript

 Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
 You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
 You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Safety:** Leverages TypeScript's type system effectively; uses specific types over \`any\` where possible. Interfaces and custom types are well-defined.
- **Strict Null Checks:** Code is written with \`strictNullChecks\` in mind, handling \`null\` and \`undefined\` explicitly.
- **Type Inference:** Relies on type inference where appropriate for cleaner code but provides explicit types for function signatures and complex structures.
- **Enums & Union Types:** Uses enums and union/intersection types judiciously to model data accurately.
- **Generics:** Applies generics for creating reusable and type-safe components, functions, and classes.
- **Error Handling:** Implements typed error handling, potentially using custom error classes.
- **Module System:** Utilizes ES modules (\`import\`/\`export\`) for organizing code.
- **Decorators (if applicable):** Uses decorators with a clear understanding of their functionality and impact, following established patterns.
- **Readability & Maintainability:** Code is well-structured, with clear type annotations enhancing understanding.
- **Compatibility:** Considers JavaScript interoperability and declaration files (\`.d.ts\`) if creating libraries.
- **Build Process:** Assumes code will be compiled; avoids TypeScript-specific syntax that might cause issues in plain JavaScript environments if not properly handled by a build step.
- **Utility Types:** Effectively uses built-in utility types (e.g., \`Partial\`, \`Readonly\`, \`Pick\`, \`Omit\`) to transform and manage types.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.PYTHON]: `## Summary for Python

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:


- **PEP 8 Compliance:** Adheres to PEP 8 style guidelines for code layout, naming conventions (snake_case), and comments/docstrings.
- **Idiomatic Python:** Uses Pythonic constructs and built-in functions/libraries where appropriate (e.g., list comprehensions, generators, context managers \`with\` statement).
- **Data Structures:** Selects appropriate built-in data structures (lists, tuples, dictionaries, sets) for the task.
- **Error Handling:** Implements robust error handling using \`try-except-else-finally\` blocks, raising and catching specific exceptions.
- **Mutability:** Shows clear understanding of mutable vs. immutable types and their implications, especially with function arguments.
- **Virtual Environments & Dependencies:** Assumes best practice of using virtual environments; imports are clear and well-managed (e.g., organized imports at the top).
- **Object-Oriented Programming (if applicable):** Classes are well-designed, with clear use of inheritance, encapsulation, and polymorphism. Magic methods (dunder methods) are used correctly.
- **Functional Programming (if applicable):** Utilizes functions as first-class citizens, lambdas, \`map\`, \`filter\` where it enhances clarity.
- **Docstrings & Type Hinting:** Includes comprehensive docstrings for modules, classes, and functions. Uses type hints (PEP 484) for improved readability and static analysis.
- **Resource Management:** Ensures proper cleanup of resources (e.g., files, network connections) using \`with\` statements or \`finally\` blocks.
- **Performance:** Aware of potential performance bottlenecks, chooses efficient algorithms and data structures.
- **Security:** If dealing with web applications or external input, guards against common vulnerabilities (e.g., SQL injection, command injection, insecure deserialization).

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`# ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the \`#\` syntax.**`,
  [SupportedLanguage.JAVA]: `## Summary for Java

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Object-Oriented Principles:** Strongly adheres to OOP principles (Encapsulation, Inheritance, Polymorphism, Abstraction).
- **SOLID Principles:** Design reflects SOLID principles where applicable.
- **Exception Handling:** Uses Java's checked and unchecked exceptions appropriately with \`try-catch-finally\` blocks. Custom exceptions are meaningful.
- **Collections Framework:** Utilizes the Java Collections Framework effectively, choosing appropriate collection types (List, Set, Map) and their implementations.
- **Generics:** Employs generics for type safety and code reusability.
- **Concurrency (if applicable):** Handles multithreading safely using \`synchronized\`, \`java.util.concurrent\` utilities, or other concurrency control mechanisms. Understands thread safety issues.
- **Resource Management:** Uses try-with-resources statements for managing resources that implement \`AutoCloseable\`.
- **Immutability:** Prefers immutability for objects where possible to enhance simplicity and thread safety.
- **Java Streams API (Java 8+):** Leverages the Streams API for processing collections in a functional style where it improves readability and conciseness.
- **Naming Conventions:** Follows standard Java naming conventions (e.g., PascalCase for classes, camelCase for methods/variables).
- **Javadoc:** Includes comprehensive Javadoc comments for public APIs.
- **Memory Management:** While Java has garbage collection, avoids memory leaks (e.g., unclosed resources, loitering objects).
- **Design Patterns:** Applies appropriate design patterns to solve common problems.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.CSHARP]: `## Summary for C#

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Object-Oriented Principles:** Code demonstrates strong adherence to OOP principles.
- **Properties & Indexers:** Uses properties (auto-implemented or full) over public fields. Uses indexers where appropriate.
- **LINQ:** Leverages Language Integrated Query (LINQ) for data manipulation where it enhances readability and conciseness.
- **Async/Await:** Correctly uses \`async\` and \`await\` for asynchronous programming, avoiding deadlocks and ensuring proper context.
- **Exception Handling:** Implements robust exception handling using \`try-catch-finally\` blocks and filters. Uses specific exception types.
- **Delegates & Events:** Uses delegates and events appropriately for implementing callbacks and event-driven patterns.
- **Generics:** Applies generics for type-safe and reusable code.
- **Resource Management:** Uses \`using\` statements for \`IDisposable\` objects to ensure proper resource disposal.
- **Nullable Reference Types (C# 8+):** If enabled, handles nullable reference types correctly to prevent \`NullReferenceException\`.
- **Naming Conventions:** Follows Microsoft's C# naming conventions (PascalCase for types/methods/properties, camelCase for local variables/parameters).
- **XML Documentation Comments:** Includes XML documentation comments for public APIs.
- **Value Types vs. Reference Types:** Shows clear understanding of the distinction and their implications.
- **Pattern Matching (C# 7+):** Utilizes pattern matching features to simplify conditional logic.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.CPP]: `## Summary for C++

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:


- **RAII (Resource Acquisition Is Initialization):** Strictly adheres to RAII for resource management (memory, files, locks, etc.), using smart pointers (\`std::unique_ptr\`, \`std::shared_ptr\`) and custom RAII wrappers.
- **Memory Management:** Avoids manual \`new\`/\`delete\` where smart pointers or STL containers can be used. No memory leaks, dangling pointers, or double frees.
- **STL Usage:** Effectively uses the Standard Template Library (containers, algorithms, iterators) for robust and efficient code.
- **Const Correctness:** Applies \`const\` correctly to variables, member functions, and parameters to ensure immutability where intended and improve safety.
- **Object-Oriented Design:** If OOP is used, classes are well-designed with appropriate access specifiers, constructors, destructors, and operator overloading (if necessary and done carefully).
- **Error Handling:** Uses exceptions for error reporting in a way that ensures exception safety (e.g., strong exception guarantee where feasible).
- **Modern C++ Features (C++11 and newer):** Leverages modern C++ features like move semantics, lambdas, range-based for loops, \`auto\` type deduction, threading utilities, etc., where appropriate.
- **Header Files & Compilation:** Header files are well-structured with include guards. Minimizes compilation dependencies.
- **Undefined Behavior:** Code is free from constructs that lead to undefined behavior.
- **Performance:** Writes efficient code, considering algorithm complexity and C++ performance characteristics.
- **Templates & Metaprogramming (if applicable):** Uses templates effectively for generic programming.
- **Readability:** Code is well-formatted, commented, and follows consistent naming conventions.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.GO]: `## Summary for Go

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:


- **Error Handling:** Explicitly checks for errors returned from function calls and handles them appropriately (typically by returning them up the call stack). Avoids panic for ordinary errors.
- **Goroutines & Channels (Concurrency):** Uses goroutines and channels idiomatically for concurrent programming. Manages goroutine lifecycles and avoids deadlocks or race conditions.
- **Interfaces:** Defines and uses interfaces effectively to promote decoupling and polymorphism. "Accept interfaces, return structs."
- **Packages & Visibility:** Code is organized into logical packages. Exported (public) and unexported (private) identifiers are used correctly (capitalization).
- **Defer Statement:** Uses \`defer\` for cleanup actions (e.g., closing files, unlocking mutexes) to ensure they run before a function returns.
- **Simplicity & Readability:** Adheres to Go's philosophy of simplicity. Code is straightforward and easy to understand. Avoids overly complex abstractions.
- **Formatting (\`gofmt\`):** Code is formatted according to \`gofmt\` standards.
- **Testing:** Assumes code is testable and encourages writing unit tests using the \`testing\` package.
- **Resource Management:** Manages resources carefully, especially in concurrent contexts.
- **Zero Values:** Understands and utilizes zero values for types effectively.
- **Pointers:** Uses pointers judiciously, understanding when to pass by value versus by pointer.
- **Build & Dependencies:** Manages dependencies using Go Modules.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.RUBY]: `## Summary for Ruby

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Ruby Idioms:** Employs idiomatic Ruby constructs (e.g., iterators like \`each\`, \`map\`, \`select\`; symbols; truthiness; blocks, procs, and lambdas).
- **Readability & Expressiveness:** Code is expressive and reads like natural language where possible.
- **Convention Over Configuration:** Follows Ruby/Rails conventions where applicable.
- **Gems & Bundler:** Manages dependencies using Bundler and a Gemfile.
- **Object-Oriented Programming:** Classes and modules are well-designed. Understands mixins and inheritance.
- **Metaprogramming (if applicable):** Uses metaprogramming cautiously and where it genuinely simplifies or enhances the code, with clear documentation.
- **Error Handling:** Uses \`begin-rescue-else-ensure-end\` blocks for exception handling, rescuing specific standard errors.
- **Blocks & Iterators:** Leverages blocks, procs, and lambdas effectively for iteration and callbacks.
- **Testing (RSpec/Minitest):** Code is structured to be testable.
- **Performance:** Aware of common Ruby performance characteristics and avoids obvious bottlenecks.
- **Security (if Rails or web-related):** Guards against common web vulnerabilities (SQL injection, XSS, CSRF, mass assignment).
- **Monkey Patching:** Avoids monkey patching core classes unless absolutely necessary and well-justified with minimal scope.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`# ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the \`#\` syntax.**`,
  [SupportedLanguage.PHP]: `## Summary for PHP

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Modern PHP Practices (PHP 7+):** Uses modern PHP features (e.g., strict types, return type declarations, arrow functions, null coalescing operator). Avoids deprecated features.
- **Error Handling & Exceptions:** Uses exceptions for error handling over traditional PHP errors where appropriate. \`try-catch\` blocks are used effectively.
- **Dependency Management (Composer):** Manages dependencies using Composer and \`autoload.php\`.
- **Security:**
  - **Input Validation & Sanitization:** All external input (GET, POST, cookies, etc.) is validated and sanitized.
  - **SQL Injection Prevention:** Uses prepared statements (PDO or MySQLi) for database interactions.
  - **XSS Prevention:** Escapes output correctly to prevent Cross-Site Scripting.
  - **CSRF Protection:** Implements CSRF tokens for state-changing requests.
- **Object-Oriented PHP:** Code is well-structured using classes, interfaces, and traits. Adheres to OOP principles.
- **PSR Standards:** Follows relevant PSR (PHP Standards Recommendations) for coding style (PSR-12), autoloading (PSR-4), etc.
- **Framework Usage (if applicable):** If a framework (e.g., Laravel, Symfony) is used, code adheres to framework conventions and best practices.
- **Session Management:** Implements secure session management if applicable.
- **Readability & Maintainability:** Code is well-commented, organized, and easy to understand.
- **Database Interaction:** Uses an appropriate abstraction layer (e.g., PDO) for database operations.
- **API Design (if applicable):** If building an API, follows RESTful principles or other clear API design standards.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.HTML]: `## Summary for HTML

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Semantic Markup:** Uses HTML5 semantic elements correctly (\`<article>\`, \`<aside>\`, \`<nav>\`, \`<section>\`, \`<header>\`, \`<footer>\`, etc.) to convey meaning and structure.
- **Accessibility (A11y):**
  - Adheres to WCAG guidelines where possible.
  - Uses ARIA attributes appropriately to enhance accessibility for assistive technologies.
  - Provides \`alt\` text for images.
  - Ensures keyboard navigability and focus management.
  - Sufficient color contrast (though this often overlaps with CSS).
- **Validation:** HTML is well-formed and would pass W3C validation. Proper doctype (\`<!DOCTYPE html>\`).
- **Forms:** Uses correct form elements, labels are associated with inputs (\`<label for="...">\`), appropriate input types are used. Includes form validation attributes.
- **Links & Navigation:** Links are descriptive and used correctly. Navigation is clear and logical.
- **Headings:** Uses heading elements (\`<h1>\` - \`<h6>\`) hierarchically to structure content.
- **Lists:** Uses \`<ul>\`, \`<ol>\`, and \`<dl>\` appropriately for list-based content.
- **Readability & Maintainability:** Code is well-indented and comments are used for complex sections if necessary.
- **Performance:** Avoids excessive or deeply nested DOM elements where simpler structures suffice. Optimizes images if referenced.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the markup. This revision must incorporate all your feedback. The markup you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`<!-- ... rest of the code -->\`). Present the revised markup in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`<!-- -->\` syntax.**`,
  [SupportedLanguage.CSS]: `## Summary for CSS

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Readability & Maintainability:**
  - CSS is well-organized, possibly grouped by component or section.
  - Uses comments to explain complex selectors or non-obvious styles.
  - Follows consistent naming conventions (e.g., BEM, SMACSS, or a custom consistent scheme).
- **Specificity:** Manages selector specificity effectively to avoid conflicts and the overuse of \`!important\`.
- **Responsiveness:** Uses responsive design techniques (e.g., media queries, flexible grids/layouts like Flexbox or Grid) to ensure good display on various screen sizes.
- **Box Model:** Demonstrates correct understanding and usage of the CSS box model (\`content-box\` vs \`border-box\`).
- **Layout Techniques:** Uses modern layout techniques (Flexbox, CSS Grid) appropriately for structuring page content. Avoids outdated techniques like floats for layout where modern alternatives are better.
- **Units:** Uses appropriate units for different properties (e.g., \`rem\` or \`em\` for scalable typography, \`px\` for fixed sizes where needed, \`%\` or \`vw/vh\` for responsive layouts).
- **Performance:**
  - Avoids overly complex selectors that can degrade rendering performance.
  - Minimizes CSS that causes reflows and repaints unnecessarily.
  - Considers techniques like critical CSS if applicable for large sites.
- **Cross-Browser Compatibility:** Writes CSS that works consistently across modern browsers, possibly using vendor prefixes where necessary (though often handled by autoprefixers in build tools).
- **Accessibility:** Ensures sufficient color contrast. Focus states for interactive elements are clear.
- **Modularity:** CSS is modular and avoids global styles that are hard to override or lead to unintended side effects.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the stylesheet. This revision must incorporate all your feedback. The stylesheet you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`/* ... rest of the code */\`). Present the revised stylesheet in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`/* */\` syntax.**`,
  [SupportedLanguage.MARKDOWN]: `## Summary for Markdown

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Syntax Correctness:** Adheres to standard Markdown syntax (e.g., CommonMark or GFM if specified). All elements are correctly formatted.
- **Readability:** The raw Markdown is easy to read and understand. Formatting choices enhance the readability of the rendered output.
- **Consistency:** Uses consistent formatting for similar elements (e.g., consistent heading levels, list markers).
- **Appropriate Use of Elements:**
  - Uses headings (\`#\`, \`##\`, etc.) hierarchically.
  - Uses bold (\`**text**\` or \`__text__\`) and italics (\`*text*\` or \`_text_\`) for emphasis appropriately.
  - Formats lists (ordered and unordered) correctly.
  - Uses code blocks (\`\`\` \`\`\`) for multi-line code and inline code (\` \` \`) for short snippets.
  - Formats links (\`[text](url)\`) and images (\`![alt text](url)\`) correctly.
- **Blockquotes:** Uses blockquotes (\`>\`) for quotations.
- **Tables (if GFM):** If GitHub Flavored Markdown is implied, tables are formatted correctly.
- **Line Breaks:** Understands how Markdown handles line breaks (e.g., requiring two spaces at the end of a line for a \`<br>\` or a blank line for a new paragraph).
- **Minimalism:** Avoids overly complex or unnecessary Markdown where simpler formatting would suffice.

Your review should be in markdown format. Do not provide a separate "revision" block for markdown, but you can include corrected examples within your review.`,
  [SupportedLanguage.SQL]: `## Summary for SQL

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Clarity & Readability:** SQL queries are well-formatted (e.g., consistent indentation, capitalization of keywords) and easy to understand.
- **Correctness:** The query achieves the intended result accurately.
- **Performance & Optimization:**
  - Queries are written efficiently. Avoids \`SELECT *\` when only specific columns are needed.
  - Uses \`JOIN\`s effectively.
  - Indexes are likely to be used effectively by the query (though index creation is outside the query itself, query structure can leverage them).
  - Avoids unnecessary subqueries or complex operations that can be simplified.
  - \`WHERE\` clauses are sargable where possible.
- **Security (SQL Injection Prevention):** If the SQL is part of an application, it MUST be structured to prevent SQL injection (e.g., by indicating where parameterization/prepared statements should be used in application code). Avoids dynamic SQL concatenation with user input.
- **Data Integrity:** Queries consider data integrity constraints (e.g., when inserting or updating data).
- **Standard SQL:** Uses ANSI SQL standard syntax where possible for portability, unless specific database dialect features are intentionally and appropriately used.
- **Transaction Management (if DML):** For Data Manipulation Language (DML) statements (\`INSERT\`, \`UPDATE\`, \`DELETE\`), consider if they should be part of a transaction in the application logic.
- **Normalization:** Table structures implied by the query should ideally reflect good normalization principles (though this is about schema design, queries interact with it).
- **Clarity of Intent:** Query clearly expresses what data is being requested or manipulated. Complex logic is broken down or commented if necessary.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the query. This revision must incorporate all your feedback. The query you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`-- ... rest of the code\`). Present the revised query in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`--\` syntax.**`,
  [SupportedLanguage.SHELL]: `## Summary for Shell Script

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. First, provide a detailed review based on the following criteria. Pay close attention to Shellcheck guidelines and general best practices.

- **Linting:** Code should be free of common Shellcheck warnings.
- **Robustness:** Ensure exit statuses are checked, variables are quoted to prevent word splitting and globbing, and input is handled safely. Use \`set -euo pipefail\` where appropriate.
- **Clarity & Style:** Code should be readable, well-formatted, and use clear variable names. Use \`local\` for variables inside functions.
- **Correctness:** Logic should be sound and free from common pitfalls like incorrect redirection (\`&>\` should be \`>file 2>&1\`).
- **Idempotency & Scoping:** Scripts should be idempotent where possible. Variables should be properly scoped.
- **Complexity:** Avoid unnecessary cyclomatic complexity.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the script. This revision must incorporate all your feedback and adhere to the guidelines above. The script you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`# ... rest of the code\`). Present the revised script in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the \`#\` syntax.**`,
  [SupportedLanguage.KOTLIN]: `## Summary for Kotlin

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Null Safety:** Effectively utilizes Kotlin's null safety features (\`?\`, \`!!\`, \`?.\`, \`?:\`, \`let\`). Avoids unnecessary \`!!\` assertions.
- **Immutability:** Prefers immutable data structures (\`val\`, \`listOf\`, \`mapOf\`, \`setOf\`, data class \`copy\`) where possible.
- **Conciseness & Readability:** Leverages Kotlin's concise syntax (e.g., type inference, data classes, extension functions, lambdas) to write expressive and readable code.
- **Coroutines (if applicable):** Uses Kotlin Coroutines idiomatically for asynchronous programming, managing scopes and error handling correctly.
- **Standard Library Functions:** Makes good use of Kotlin's rich standard library functions (e.g., scope functions like \`let\`, \`run\`, \`with\`, \`apply\`, \`also\`; collection processing functions).
- **Interoperability with Java (if applicable):** Code is written with Java interoperability in mind, handling platform types and annotations correctly.
- **Object-Oriented & Functional Features:** Balances object-oriented and functional programming paradigms effectively.
- **Sealed Classes & When Expressions:** Uses sealed classes and exhaustive \`when\` expressions for modeling restricted hierarchies and state management.
- **Extension Functions/Properties:** Uses extension functions/properties to enhance existing classes judiciously.
- **Error Handling:** Uses Kotlin's exception handling mechanisms (\`try-catch-finally\`) or functional approaches (e.g., \`Result\` type) appropriately.
- **Coding Conventions:** Follows official Kotlin coding conventions.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.SWIFT]: `## Summary for Swift

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Safety & Optionals:** Effectively uses Swift's type system and handles optionals safely (\`?\`, \`!\`, optional binding \`if let\`/\`guard let\`, optional chaining, nil-coalescing operator \`??\`). Avoids forced unwrapping (\`!\`) unless safety is guaranteed.
- **Value vs. Reference Types:** Demonstrates clear understanding and appropriate use of value types (structs, enums) and reference types (classes). Prefers value types where appropriate.
- **Immutability:** Prefers \`let\` over \`var\` for constants to promote immutability.
- **Error Handling:** Uses Swift's error handling model (\`do-try-catch\`, \`throws\`, \`Result\` type) robustly.
- **Protocols & Protocol-Oriented Programming:** Leverages protocols for abstraction and polymorphism. Uses protocol extensions effectively.
- **Generics:** Applies generics to write flexible and reusable code.
- **Automatic Reference Counting (ARC):** Understands ARC and avoids strong reference cycles (e.g., using \`weak\` or \`unowned\` references).
- **Closures:** Uses closures idiomatically, understanding capture lists to manage memory.
- **Concurrency (Grand Central Dispatch, async/await):** Uses GCD or modern Swift concurrency (\`async/await\`, Actors) correctly and safely.
- **API Design Guidelines:** Follows Swift API Design Guidelines for naming and clarity.
- **Higher-Order Functions:** Utilizes higher-order functions like \`map\`, \`filter\`, \`reduce\` for collection processing.
- **Readability:** Code is clear, concise, and follows Swift's expressive style.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.RUST]: `## Summary for Rust

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Ownership & Borrowing:** Correctly applies Rust's ownership, borrowing (immutable \`&\` and mutable \`&mut\`), and lifetime rules. Code compiles without fighting the borrow checker excessively.
- **Memory Safety:** Code is memory safe, with no data races, or use-after-free errors (as enforced by the compiler).
- **Error Handling (\`Result\` & \`Option\`):** Uses \`Result<T, E>\` for recoverable errors and \`Option<T>\` for optional values idiomatically. Propagates errors using \`?\` operator. Avoids \`unwrap()\` or \`expect()\` in library code or where errors are expected.
- **Pattern Matching:** Leverages powerful pattern matching with \`match\` expressions effectively.
- **Traits & Generics:** Uses traits for defining shared behavior (similar to interfaces) and generics for writing abstract, reusable code.
- **Concurrency:** Implements safe concurrency using Rust's mechanisms like threads, channels, \`Arc\`, \`Mutex\`, or async programming with \`async/await\` and runtimes like Tokio/async-std.
- **Macros (if applicable):** Uses macros (declarative or procedural) appropriately and understands their implications.
- **Crates & Modules:** Organizes code into modules and manages dependencies using \`Cargo.toml\`.
- **Clippy Lints:** Code adheres to common Clippy lint suggestions for idiomatic and correct Rust.
- **Unsafe Code:** Avoids \`unsafe\` blocks unless absolutely necessary, well-justified, and correctly implemented to uphold safety invariants.
- **Documentation (\`rustdoc\`):** Includes documentation comments for public APIs.
- **Performance:** Writes performant code, taking advantage of Rust's low-level control when needed.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code (e.g., \`// ... rest of the code\`). Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using \`//\` syntax.**`,
  [SupportedLanguage.OTHER]: `## Summary for Other (Generic)

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Clarity & Readability:** Code is well-formatted, uses clear and consistent naming conventions, and includes comments where logic is non-obvious.
- **Correctness:** The code appears to achieve its stated purpose without obvious logical flaws.
- **Simplicity:** Avoids unnecessary complexity; solutions are as simple as possible but no simpler.
- **Modularity & Reusability:** Code is broken down into manageable functions, methods, or modules that are potentially reusable.
- **Error Handling:** Basic error handling mechanisms are present and seem appropriate for the context shown.
- **Resource Management:** If resources (files, connections, memory) are explicitly managed, there are indications of proper acquisition and release.
- **Input Validation:** If the code processes external input, there are signs of basic validation or sanitization.
- **Maintainability:** Code structure and comments suggest that it would be reasonably easy for another developer to understand and maintain.
- **Efficiency:** No glaringly inefficient algorithms or operations are apparent for the given task.
- **Consistency:** Follows a consistent style throughout the provided snippet.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
};
