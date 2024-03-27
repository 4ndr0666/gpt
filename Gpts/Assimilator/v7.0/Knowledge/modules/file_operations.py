import os

# Define the SANDBOX_PATH at the top of your module for easy configuration
SANDBOX_PATH = "/mnt/data/sandbox"

def save_file_sandbox(file_path, content):
    """
    Saves a file with the specified content in the sandbox environment.
    
    :param file_path: Path of the file to save, relative to SANDBOX_PATH.
    :param content: Content to be saved in the file.
    :return: Boolean indicating success of the operation.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)  # Ensure the directory exists
    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Failed to save file {file_path}: {e}")
        return False

def read_file_sandbox(file_path):
    """
    Reads a file's content from the sandbox environment.
    
    :param file_path: Path of the file to read, relative to SANDBOX_PATH.
    :return: Content of the file or None if an error occurs.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")
        return None





