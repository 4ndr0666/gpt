import os
import shutil
import logging

# Define the SANDBOX_PATH at the top of your module for easy configuration
SANDBOX_PATH = "/mnt/data/sandbox"

def is_safe_path(basedir, path, follow_symlinks=True):
    """
    Check if the path is secure and confined within the specified basedir, following the compliance rules set in code_directive.json.
    """
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def move_file_to_sandbox(source_dir, target_dir):
    """
    Moves a file from the source directory to the target directory within the sandbox,
    adhering to security protocols and logging errors for non-compliance.
    """
    if not os.path.exists(source_dir):
        logging.error(f"Source file does not exist: {source_dir}")
        return False

    if not is_safe_path(SANDBOX_PATH, target_dir):
        logging.error(f"Attempted to move a file outside the sandbox: {target_dir}")
        return False

    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    try:
        shutil.move(source_dir, target_dir)
        logging.info(f"File successfully moved from {source_dir} to {target_dir}")
        return True
    except Exception as e:
        logging.error(f"Failed to move file: {e}")
        return False

def read_file_sandbox(file_path):
    """
    Reads a file's content securely from the sandbox, ensuring compliance and logging specific errors.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path):
        logging.error(f"Unauthorized file access attempt: {full_path}")
        return None
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Failed to read file {file_path}: {e}")
        return None
