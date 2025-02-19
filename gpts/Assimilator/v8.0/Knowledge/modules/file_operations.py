import os
import shutil
import logging

# Define the SANDBOX_PATH at the top of your module for easy configuration
SANDBOX_PATH = "/mnt/data/sandbox"

def is_safe_path(basedir, path, follow_symlinks=True):
    """
    Resolve the absolute path and optionally follow symlinks to ensure the path is safe.
    """
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def move_file_to_sandbox(source_dir, target_dir):
    """
    Moves a file from the source directory to the target directory within the sandbox.
    """
    # Check if the source file exists
    if not os.path.exists(source_dir):
        print(f"Source file does not exist: {source_dir}")
        return False

    # Ensure the target directory exists
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)

    # Attempt to move the file
    try:
        shutil.move(source_dir, target_dir)
        print(f"File successfully moved from {source_dir} to {target_dir}")
        return True
    except Exception as e:
        print(f"Failed to move file: {e}")
        return False

def save_file_sandbox(file_path, content):
    """
    Saves a file with the specified content in the sandbox environment.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path, follow_symlinks=False):
        logging.error(f"Attempted access outside sandbox: {file_path}")
        return False
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
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
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read file {file_path}: {e}")
        return None



