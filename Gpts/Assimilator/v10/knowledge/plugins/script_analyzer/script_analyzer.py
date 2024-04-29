import ast
import os
import logging

def analyze_and_display_script(script_path):
    """
    Analyze a Python script and display its API in a markdown table format.
    Uses paths and parameters dynamically received from the main system configuration.
    """
    if not os.path.isfile(script_path):
        logging.error("Provided script path does not exist or is not a file.")
        return

    try:
        functions = analyze_script(script_path)
        table = generate_markdown_table(functions)
        print("\nGenerated API Table:")
        print(table)
    except Exception as e:
        logging.error(f"Error analyzing script: {str(e)}")

def analyze_script(script_path):
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
    headers = "| Function Name | Description | Parameters | Return Values |\n"
    separator = "|---------------|-------------|------------|---------------|\n"
    table = headers + separator
    for func in functions:
        params = ', '.join(func['Parameters'])
        table += f"| {func['Function Name']} | {func['Description']} | {params} | {func['Return Values']} |\n"
    return table
