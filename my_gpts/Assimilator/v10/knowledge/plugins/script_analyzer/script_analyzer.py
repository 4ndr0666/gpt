import ast
import os

def analyze_script(script_path):
    """
    Analyze a Python script to extract function definitions and their details using AST.
    Extracts the name, docstring, parameters, and a placeholder for return values.
    """
    with open(script_path, 'r') as file:
        node = ast.parse(file.read(), filename=script_path)

    functions = []
    for func in node.body:
        if isinstance(func, ast.FunctionDef):
            docstring = ast.get_docstring(func) or "No description provided."
            parameters = [arg.arg for arg in func.args.args]
            return_annotation = ast.unparse(func.returns) if func.returns else "None"
            functions.append({
                "Function Name": func.name,
                "Description": docstring,
                "Parameters": parameters,
                "Return Values": return_annotation
            })
    return functions

def generate_markdown_table(functions):
    """
    Generate a markdown table from the list of functions.
    Includes columns for function name, description, parameters, and return values.
    """
    headers = "| Function Name | Description | Parameters | Return Values |\n"
    separator = "|---------------|-------------|------------|---------------|\n"
    table = headers + separator
    for func in functions:
        params = ', '.join(func['Parameters'])
        table += f"| {func['Function Name']} | {func['Description']} | {params} | {func['Return Values']} |\n"
    return table

def analyze_and_display_script(script_path):
    """
    Function to analyze a script and display the results in markdown format.
    This function fits the specifications for use as a plugin.
    """
    if not os.path.exists(script_path):
        print("Script file does not exist. Please check the path and try again.")
        return

    functions = analyze_script(script_path)
    table = generate_markdown_table(functions)
    print(table)

# Additional module code can go here if necessary.

