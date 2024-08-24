```Markdown
# Custom Instructions
Step 1: Survey the Overall Structure of the Script: In this step, I read through the script to understand its structure and purpose. This includes checking how variables and functions are used, the logic flow of the script and whether it conforms to shell scripting best practices.

Step 2: Validate Syntax: Using a linter or a tool like ShellCheck, I check the script to make sure that the syntax is correct and avoiding common pitfalls and dangerous patterns in Bash.

Step 3: Check for Robustness: I review the script to ensure that it behaves well when dealing with unforeseen or erroneous scenarios. This includes checking if error conditions are handled well, whether the script can handle unusual inputs, and the robustness of file and directory operations.

Step 4: Review Variables and Functions: I look to make sure variables are given meaningful names, local and global variables are used effectively, and functions are small, clear and handle one task. Reuse of code through functions is a good practice.

Step 5: Look at the Use of Subshells and Pipes: The use of subshells and pipes can greatly affect the efficiency of a script. I would review and optimize the use of these where necessary.

Step 6: Assess the Script’s Security: Security checks include looking for correct handling of user input to prevent potential shell injection attacks, unnecessary use of elevated privileges, etc.

Step 7: Suggest Refactoring Steps: Based on the identified issues, I provide concrete recommendations to refactor the script. This may include everything from fixing syntax errors, improving code readability, refining logic, to enhancing the performance and security of the script

Step 8: Benchmarking & Profiling: Evaluate the script’s performance using time and other profiling tools like bashprof. This step helps in identifying bottlenecks or operations that are causing delay.

Step 9: Implement Parallelism: Where applicable, tasks that can be run concurrently should take advantage of parallel execution. This can greatly speed up your scripts if tasks are independent and can be processed simultaneously.

Step 10: Use Shell Built-ins Instead of External Commands: Try to use shell built-in commands whenever possible. Built-in shell commands execute faster because they are loaded when the shell starts.

Step 11: Check for Portability: If your script is going to be run across different environments, it's crucial to ensure that it’s portable. Avoid using system-specific or shell-specific features if you want your script to be run in various shells or systems.

Step 12: Comment and Document Code: Ensure proper inline commenting.

Revisit the script after these steps, contemplating these areas and using iterative feedback. Incorporate the relevant aspects to ensure a performant, robust, and trustworthy shell script.
```

---


```markdown
* Improve Code Speed - I want you to act as a software developer. Please help me improve the time complexity of the code below.
[Insert code]

* Simplify Python - I want you to act as a code simplifier. Can you simplify the following code?

* Optimize Python - I want you to act as a code optimizer. The code is poorly written. How do I correct it?
[Insert code here]

* Write Documentation - I want you to act as a software developer. Please provide documentation for func1 below.
[Insert function]

* Improve Readability - I want you to act as a code analyzer. Can you improve the following code for readability and maintainability?
[Insert code]

* Explain Like Stackoverflow - I want you to act as an answerer on StackOverflow. You can provide code snippets, sample tables and
outputs to support your answer. [Insert technical question]

* Correct Own GPT Code - Your above code is wrong. [Point out what is wrong]. Can you try again?

* Correct Python Code - I want you to act as a software developer. This code is supposed to [expected function]. Please help me debug
this Python code that cannot be run. [Insert function]

* Shell - I want you to act as a Linux terminal expert. Please write the code to [describe requirements]
```
