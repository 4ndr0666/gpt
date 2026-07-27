import os
import shutil
import logging

# Define the SANDBOX_PATH at the top of your module for easy configuration
SANDBOX_PATH = "/mnt/data/sandbox"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_safe_path(basedir, path, follow_symlinks=True):
    """
    Check if the path is secure and confined within the specified basedir.
    
    Args:
        basedir (str): The base directory to compare against.
        path (str): The path to validate.
        follow_symlinks (bool): Whether to resolve symlinks.

    Returns:
        bool: True if the path is within the basedir, False otherwise.
    """
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def move_file_to_sandbox(source_path, target_path):
    """
    Move a file from the source path to the target path within the sandbox.
    
    Args:
        source_path (str): The file path to move.
        target_path (str): The destination path within the sandbox.

    Returns:
        bool: True if the file is successfully moved, False otherwise.
    """
    if not os.path.exists(source_path):
        logging.error(f"Source file does not exist: {source_path}")
        return False

    if not is_safe_path(SANDBOX_PATH, target_path):
        logging.error(f"Attempted to move a file outside the sandbox: {target_path}")
        return False

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    try:
        shutil.move(source_path, target_path)
        logging.info(f"File successfully moved from {source_path} to {target_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to move file: {e}")
        return False

def read_file_sandbox(file_path):
    """
    Read a file's content securely from the sandbox.
    
    Args:
        file_path (str): The path to the file within the sandbox.

    Returns:
        str: The content of the file, or None if an error occurs.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path):
        logging.error(f"Unauthorized file access attempt: {full_path}")
        return None
    try:
        with open(full_path, 'r') as file:
            content = file.read()
            logging.info(f"File read successfully: {file_path}")
            return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except IOError as e:
        logging.error(f"IOError reading file {file_path}: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error reading file {file_path}: {str(e)}")
    return None

if __name__ == "__main__":
    # Example usage of the module
    source_file = os.path.join(SANDBOX_PATH, "example.txt")
    target_file = os.path.join(SANDBOX_PATH, "destination", "example.txt")

    # Attempt to move a file
    if move_file_to_sandbox(source_file, target_file):
        logging.info("File move operation completed successfully.")
    else:
        logging.error("File move operation failed.")

    # Attempt to read a file
    content = read_file_sandbox("destination/example.txt")
    if content:
        logging.info("File content retrieved successfully.")
    else:
        logging.error("Failed to retrieve file content.")
