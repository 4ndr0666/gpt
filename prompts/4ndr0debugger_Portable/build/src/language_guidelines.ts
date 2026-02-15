// language_guidelines.ts
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
- **DOM Manipulation (if applicable):** Uses efficient, secure, and framework-idiomatic DOM manipulation, sanitizing user inputs to prevent XSS when directly manipulating DOM.
- **Memory Management:** Avoids memory leaks by properly managing event listeners, timeouts, intervals, and references.
- **Functional Programming:** Utilizes functional programming patterns where appropriate (e.g., immutability, pure functions, higher-order functions like \`map\`, \`filter\`, \`reduce\`).
- **Modularity:** Structures code into modules using ES6 import/export, avoiding global variables.
- **Performance Optimizations:** Minimizes unnecessary re-renders or computations; uses efficient algorithms and data structures.
- **Security Practices:** Implements measures against common vulnerabilities like XSS, CSRF (if applicable), and prototype pollution.
- **Code Style:** Follows consistent naming conventions (e.g., camelCase for variables/functions), indentation, and formatting.
- **Comments & Documentation:** Includes comments where logic is non-obvious.
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
  [SupportedLanguage.TYPESCRIPT]: `## Summary for TypeScript

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Annotations:** Uses appropriate type annotations for variables, parameters, return types, and properties to enhance type safety.
- **Interface & Type Definitions:** Defines interfaces or types for complex objects, function signatures, and generics where applicable.
- **Type Inference:** Leverages TypeScript's type inference capabilities effectively, avoiding unnecessary explicit types.
- **Union & Intersection Types:** Utilizes union and intersection types to model complex data structures accurately.
- **Generics:** Employs generics for reusable components and functions.
- **Type Guards & Narrowing:** Implements type guards to narrow types within conditional blocks.
- **Enums & Literal Types:** Uses enums or literal types for fixed sets of values.
- **Asynchronous Operations:** Properly types asynchronous code, including Promises and async/await.
- **Error Handling:** Types error objects and handles them appropriately in catch blocks.
- **Module System:** Uses ES modules with import/export statements.
- **Code Style:** Follows consistent naming conventions, indentation, and formatting.
- **Comments & Documentation:** Includes JSDoc comments for functions, classes, and types.
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
  [SupportedLanguage.PYTHON]: `## Summary for Python

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Hints:** Uses type hints for function parameters and return types to improve readability and enable static type checking.
- **Exception Handling:** Implements comprehensive exception handling using try/except/else/finally blocks, catching specific exceptions where appropriate.
- **Context Managers:** Utilizes context managers (with statements) for resource management (e.g., file handling, locks).
- **List Comprehensions & Generators:** Employs list/dict/set comprehensions and generator expressions for concise, efficient data transformations.
- **Decorators:** Uses decorators for adding functionality to functions/methods (e.g., @staticmethod, @property, custom decorators).
- **Classes & Inheritance:** Properly structures classes with init methods, instance/class methods, and appropriate inheritance.
- **Modules & Imports:** Organizes code into modules with relative/absolute imports, avoiding wildcard imports.
- **String Formatting:** Uses f-strings or str.format() for string interpolation.
- **Itertools & Collections:** Leverages standard library modules like itertools and collections for efficient operations.
- **Logging:** Implements logging instead of print statements for production code.
- **Code Style:** Follows PEP 8 conventions: 4-space indentation, 79-char line limit, snake_case naming.
- **Comments & Docstrings:** Includes docstrings for modules, classes, functions, and inline comments where necessary.
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
  [SupportedLanguage.JAVA]: `## Summary for Java

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Safety:** Uses generics, enums, and sealed classes/interfaces where appropriate to enhance type safety.
- **Exception Handling:** Implements checked/unchecked exceptions with try-catch-finally or try-with-resources for resource management.
- **Streams & Lambdas:** Utilizes Java Streams API and lambda expressions for functional-style operations on collections.
- **Optionals:** Uses Optional to handle null values and avoid NullPointerExceptions.
- **Interfaces & Abstract Classes:** Properly uses interfaces for contracts and abstract classes for partial implementations.
- **Annotations:** Employs built-in and custom annotations (e.g., @Override, @Deprecated).
- **Concurrency:** Uses java.util.concurrent package for thread-safe operations if applicable.
- **Collections Framework:** Chooses appropriate data structures from java.util (e.g., ArrayList, HashMap).
- **Logging:** Implements logging using SLF4J or java.util.logging.
- **Code Style:** Follows consistent naming (camelCase for methods/variables, PascalCase for classes), indentation, and formatting.
- **Comments & Javadoc:** Includes Javadoc comments for public APIs and inline comments where necessary.
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
  [SupportedLanguage.CSHARP]: `## Summary for C#

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Safety:** Uses strong typing, generics, and nullable reference types to prevent runtime errors.
- **Exception Handling:** Implements try-catch-finally blocks, catching specific exceptions and using 'using' statements for disposables.
- **LINQ:** Utilizes LINQ for querying collections and data transformations.
- **Async/Await:** Properly uses async/await for asynchronous operations with Task-based async patterns.
- **Properties & Auto-Properties:** Uses properties with getters/setters instead of public fields.
- **Interfaces & Abstract Classes:** Defines interfaces for contracts and abstract classes for base implementations.
- **Delegates & Events:** Uses delegates and events for callback mechanisms.
- **Attributes:** Employs attributes for metadata (e.g., [Obsolete], [Serializable]).
- **Namespaces & Using Directives:** Organizes code into namespaces with using directives at the top.
- **Logging:** Implements logging using Microsoft.Extensions.Logging or similar.
- **Code Style:** Follows consistent naming (PascalCase for methods/classes, camelCase for variables), indentation, and formatting.
- **Comments & XML Documentation:** Includes XML documentation comments for public members.
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
  [SupportedLanguage.CPP]: `## Summary for C++

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Smart Pointers:** Uses std::unique_ptr, std::shared_ptr, std::weak_ptr for memory management to prevent leaks.
- **RAII:** Implements Resource Acquisition Is Initialization for automatic resource cleanup.
- **Templates & Generics:** Utilizes templates for generic programming.
- **STL Containers:** Chooses appropriate containers from Standard Template Library (e.g., std::vector, std::map).
- **Algorithms:** Uses std::algorithm functions for common operations.
- **Exception Handling:** Implements try-catch blocks and defines custom exceptions if needed.
- **Const Correctness:** Applies const qualifiers to variables, parameters, and methods where appropriate.
- **Move Semantics:** Uses rvalue references and std::move for efficient resource transfer.
- **Namespaces:** Organizes code into namespaces to avoid name collisions.
- **Header Guards/Includes:** Uses #pragma once or include guards in headers.
- **Code Style:** Follows consistent naming, indentation, and formatting (e.g., snake_case or camelCase).
- **Comments:** Includes comments for complex logic and Doxygen-style for documentation.
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
  [SupportedLanguage.GO]: `## Summary for Go

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Error Handling:** Returns errors from functions and handles them properly (e.g., if err != nil { ... }).
- **Defer Statements:** Uses defer for cleanup operations (e.g., closing files, unlocking mutexes).
- **Goroutines & Channels:** Implements concurrency using goroutines and channels with proper synchronization.
- **Interfaces:** Defines interfaces for abstraction and polymorphism.
- **Structs & Methods:** Uses structs with embedded types and methods for OOP-like behavior.
- **Slices & Maps:** Utilizes slices and maps for dynamic arrays and dictionaries.
- **Packages & Imports:** Organizes code into packages with aliasable imports.
- **Constants & Enums:** Uses const and iota for constants and enum-like values.
- **Testing:** Includes unit tests using testing package.
- **Logging:** Uses log package or structured logging libraries.
- **Code Style:** Follows gofmt conventions: tab indentation, short variable names, PascalCase for exported identifiers.
- **Comments:** Includes comments and godoc-style documentation.
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
  [SupportedLanguage.RUBY]: `## Summary for Ruby

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Blocks & Procs:** Uses blocks, procs, and lambdas for flexible, reusable code.
- **Exception Handling:** Implements begin/rescue/else/ensure blocks, rescuing specific exceptions.
- **Modules & Mixins:** Uses modules for namespacing and mixins for shared behavior.
- **Classes & Inheritance:** Defines classes with proper inheritance and accessors (attr_reader, attr_writer).
- **Symbols & Hashes:** Utilizes symbols as hash keys and for method names.
- **Enumerables:** Leverages Enumerable methods (e.g., map, select, reduce) on arrays/hashes.
- **Metaprogramming:** Employs metaprogramming techniques judiciously (e.g., define_method).
- **Gems & Requires:** Manages dependencies with require or Bundler.
- **Testing:** Includes unit tests using Minitest or RSpec.
- **Logging:** Uses Logger class for logging.
- **Code Style:** Follows Ruby style guide: 2-space indentation, snake_case naming, no trailing whitespace.
- **Comments:** Includes comments where logic is non-obvious.
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
  [SupportedLanguage.PHP]: `## Summary for PHP

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Type Declarations:** Uses scalar type hints, return types, and strict_types declaration.
- **Exception Handling:** Implements try-catch-finally blocks and custom exceptions.
- **Namespaces & Use Statements:** Organizes code into namespaces with use statements for imports.
- **Classes & Traits:** Defines classes with properties, methods, and traits for code reuse.
- **Arrays & Arrow Functions:** Uses short array syntax and arrow functions for conciseness.
- **PDO or MySQLi:** Uses prepared statements for database interactions to prevent SQL injection.
- **Composer & Autoloading:** Assumes Composer for dependency management and autoloading.
- **Error Reporting:** Sets appropriate error reporting levels.
- **Security Practices:** Implements input sanitization, output escaping, and security headers.
- **Code Style:** Follows PSR-12: 4-space indentation, camelCase for methods, PascalCase for classes.
- **Comments & PHPDoc:** Includes PHPDoc blocks for documentation.
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
  [SupportedLanguage.HTML]: `## Summary for HTML

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Semantic Markup:** Uses appropriate semantic elements (e.g., <header>, <nav>, <main>, <footer>, <article>).
- **Accessibility:** Includes ARIA attributes, alt text for images, proper heading structure, and keyboard navigation support.
- **Meta Tags:** Includes necessary meta tags for charset, viewport, and SEO.
- **Doctype & Structure:** Starts with correct <!DOCTYPE html> and well-structured <html>, <head>, <body>.
- **Links & Resources:** Uses proper <link> for CSS, <script> for JS, with integrity attributes if applicable.
- **Forms:** Implements forms with labels, placeholders, and validation attributes.
- **Media Elements:** Uses <img>, <audio>, <video> with responsive attributes (e.g., srcset, sizes).
- **SVG & Canvas:** Properly embeds SVG or uses canvas for graphics.
- **Code Style:** Consistent indentation, lowercase tags/attributes, quoted attributes.
- **Comments:** Includes HTML comments for sectioning.
- **Correctness:** The code appears to achieve its stated purpose without obvious logical flaws.
- **Simplicity:** Avoids unnecessary complexity; solutions are as simple as possible but no simpler.
- **Modularity & Reusability:** Code is broken down into manageable sections that are potentially reusable.
- **Error Handling:** N/A for static HTML, but ensure valid syntax.
- **Resource Management:** N/A.
- **Input Validation:** Uses HTML5 validation attributes.
- **Maintainability:** Structure and comments make it easy to understand.
- **Efficiency:** Minimizes redundant tags/attributes.
- **Consistency:** Follows consistent formatting.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.CSS]: `## Summary for CSS

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Selectors:** Uses efficient selectors (e.g., class, ID, attribute) avoiding over-qualification.
- **Box Model:** Properly handles box-sizing, margins, padding, borders.
- **Flexbox/Grid:** Utilizes flexbox or grid for layout.
- **Responsive Design:** Includes media queries for different screen sizes.
- **Transitions & Animations:** Uses transitions and keyframes for smooth effects.
- **Variables:** Employs CSS custom properties (--var) for theming.
- **Pseudo-classes/elements:** Uses :hover, :focus, ::before, etc. appropriately.
- **Specificity:** Manages specificity to avoid !important overuse.
- **Code Style:** Consistent indentation, alphabetical property order.
- **Comments:** Includes comments for sections.
- **Correctness:** The styles appear to achieve their purpose without obvious flaws.
- **Simplicity:** Avoids unnecessary rules.
- **Modularity:** Groups related styles.
- **Efficiency:** Minimizes redundancy, uses shorthand properties.
- **Consistency:** Follows consistent naming/formatting.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.MARKDOWN]: `## Summary for Markdown

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Headings:** Uses # to ###### for hierarchy.
- **Lists:** Proper unordered/ordered lists with consistent indentation.
- **Code Blocks:** Fenced code blocks with language specifiers.
- **Links & Images:** Correct [text](url) and ![alt](url) syntax.
- **Tables:** Aligned columns with headers.
- **Emphasis:** Bold, italic, strikethrough.
- **Blockquotes:** > for quotes.
- **Horizontal Rules:** --- or ***.
- **Task Lists:** - [ ] for tasks.
- **Consistency:** Uniform formatting.
- **Readability:** Logical structure.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.SQL]: `## Summary for SQL

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Queries:** Uses SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY appropriately.
- **Joins:** Proper INNER/LEFT/RIGHT/FULL joins with ON clauses.
- **Subqueries & CTEs:** Utilizes subqueries or Common Table Expressions for complex logic.
- **Indexes:** Suggests indexes if performance is considered.
- **Transactions:** Uses BEGIN/COMMIT/ROLLBACK for atomicity.
- **Stored Procedures:** Defines procedures for reusable logic.
- **Functions:** Uses built-in and user-defined functions.
- **Error Handling:** Implements TRY-CATCH in supported dialects.
- **Security:** Uses parameterized queries to prevent SQL injection.
- **Comments:** Includes -- or /* */ comments.
- **Correctness:** Query achieves purpose without flaws.
- **Efficiency:** Optimizes with indexes, avoids SELECT *, uses appropriate joins.
- **Consistency:** Follows consistent casing/formatting.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.SHELL]: `## Summary for Shell Script

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Shebang:** Starts with #!/bin/bash or appropriate interpreter.
- **Error Handling:** Uses set -euo pipefail for strict error checking.
- **Variables:** Uses ${var} for expansion, avoids uppercase for locals.
- **Functions:** Defines functions for modularity.
- **Conditionals:** Uses if/else, case statements.
- **Loops:** For/while/until loops with break/continue.
- **Command Substitution:** Uses $(command) over backticks.
- **Parameter Expansion:** Utilizes ${param/default}, etc.
- **Traps:** Sets traps for cleanup on exit.
- **Comments:** Includes # comments.
- **Correctness:** Script achieves purpose without flaws.
- **Simplicity:** Avoids unnecessary commands.
- **Modularity:** Uses functions/subscripts.
- **Security:** Avoids eval, sanitizes inputs.
- **Efficiency:** Minimizes subshells.
- **Consistency:** Consistent formatting.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.KOTLIN]: `## Summary for Kotlin

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Null Safety:** Uses nullable types (? ), safe calls (?.), Elvis operator (?:), and non-null assertions (!! ).
- **Extension Functions:** Defines extension functions for added functionality.
- **Data Classes:** Uses data classes for simple POJOs with auto-generated methods.
- **Coroutines:** Implements asynchronous programming with coroutines.
- **Lambdas & Higher-Order Functions:** Utilizes lambdas and higher-order functions.
- **Delegates:** Uses property delegates (e.g., lazy, observable).
- **Sealed Classes:** For restricted class hierarchies.
- **Companion Objects:** For static-like members.
- **Code Style:** Consistent naming, indentation.
- **Comments:** Includes comments.
- **Correctness:** Code achieves purpose.
- **Simplicity:** Avoids complexity.
- **Modularity:** Broken down into functions/classes.
- **Error Handling:** Proper handling.
- **Resource Management:** Proper management.
- **Input Validation:** Validation present.
- **Maintainability:** Easy to maintain.
- **Efficiency:** Efficient.
- **Consistency:** Consistent style.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.SWIFT]: `## Summary for Swift

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Optionals:** Uses optionals (?) and forced/optional unwrapping (!, ?).
- **Error Handling:** Implements do-try-catch and throws.
- **Protocols & Extensions:** Defines protocols and extensions for code reuse.
- **Structs & Classes:** Uses structs for value types, classes for reference types.
- **Closures:** Utilizes closures with capture lists.
- **Generics:** Employs generics for type-safe code.
- **Enums:** Uses enums with associated values and raw values.
- **Guard Statements:** Uses guard for early exits.
- **Code Style:** Consistent indentation, naming.
- **Comments:** Includes // or /* */ comments.
- **Correctness:** Code achieves purpose.
- **Simplicity:** Avoids complexity.
- **Modularity:** Broken down.
- **Error Handling:** Present.
- **Resource Management:** Proper.
- **Input Validation:** Present.
- **Maintainability:** Easy.
- **Efficiency:** Efficient.
- **Consistency:** Consistent.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.RUST]: `## Summary for Rust

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Ownership & Borrowing:** Properly manages ownership, borrowing, and lifetimes to prevent data races.
- **Error Handling:** Uses Result and Option types with ? operator or match statements.
- **Traits & Impl:** Defines traits for interfaces and impl for implementations.
- **Enums & Match:** Uses enums with variants and match for pattern matching.
- **Generics & Bounds:** Employs generics with trait bounds.
- **Modules & Visibility:** Organizes code into modules with pub/private visibility.
- **Macros:** Uses macros for metaprogramming if appropriate.
- **Concurrency:** Implements threads or async with proper synchronization.
- **Code Style:** Follows rustfmt: 4-space indentation, snake_case naming.
- **Comments:** Includes // or /* */ comments, doc comments (///).
- **Correctness:** Code achieves purpose without flaws.
- **Simplicity:** Avoids complexity.
- **Modularity:** Broken down into functions/modules.
- **Error Handling:** Present.
- **Resource Management:** Proper (RAII-like).
- **Input Validation:** Present.
- **Maintainability:** Easy.
- **Efficiency:** Efficient.
- **Consistency:** Consistent.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
  [SupportedLanguage.OTHER]: `## Summary for Generic Code

Before presenting any adjusted code, you **must** perform a silent, internal "superset check." Your proposed revision must be a strict superset of the previous stable version's features. 
You will analyze the state (version number, history) to ensure that your new code does not accidentally omit or regress on previously solved problems (e.g., re-introducing a bug, removing a feature like crash-resilience). 
You are responsible for maintaining forward progress. A feature, once validated, must not be lost. To minimally guide your thought processes, ensure your review and subsequent revision address the following points:

- **Syntax & Structure:** Adheres to language syntax and best practices.
- **Error Handling:** Implements appropriate error checking and handling.
- **Modularity:** Breaks code into functions/modules.
- **Efficiency:** Uses efficient algorithms.
- **Security:** Addresses potential vulnerabilities.
- **Code Style:** Consistent formatting.
- **Comments:** Explains complex parts.
- **Correctness:** Achieves purpose.
- **Simplicity:** Simple as possible.
- **Reusability:** Reusable components.
- **Resource Management:** Proper handling.
- **Input Validation:** Validates inputs.
- **Maintainability:** Easy to maintain.
- **Consistency:** Consistent style.

After your detailed review, provide a complete, fully-functional, and production-ready revision of the code. This revision must incorporate all your feedback. The code you provide must be whole and complete; do not use placeholders, ellipses, or comments indicating omitted code. Present the revised code in a single, final markdown code block. **Crucially, any inline comments you add within this code block to explain changes MUST be correctly formatted using the appropriate comment syntax for the language.**`,
};
