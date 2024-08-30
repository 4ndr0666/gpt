import json
import os
import shutil
from threading import Timer
import hashlib
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

def save_file_to_sandbox(file_path, content):
    """
    Save content to a file in the sandbox, ensuring it is secure and logging any issues.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path):
        logging.error(f"Attempted to save a file outside the sandbox: {full_path}")
        return False
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as file:
            file.write(content)
        logging.info(f"File successfully saved to {full_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to save file: {e}")
        return False

def schedule_file_cleanup(file_path, delay):
    """
    Schedule a file for cleanup (deletion) after a certain delay.
    """
    def cleanup():
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logging.info(f"File {file_path} successfully deleted.")
            except Exception as e:
                logging.error(f"Failed to delete file {file_path}: {e}")
        else:
            logging.error(f"File {file_path} does not exist.")
    
    Timer(delay, cleanup).start()
    logging.info(f"File cleanup for {file_path} scheduled in {delay} seconds.")

def compute_file_hash(file_path):
    """
    Compute the SHA-256 hash of a file's content for integrity checks.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path):
        logging.error(f"Attempted to access a file outside the sandbox: {full_path}")
        return None
    try:
        with open(full_path, 'rb') as file:
            file_content = file.read()
        return hashlib.sha256(file_content).hexdigest()
    except Exception as e:
        logging.error(f"Failed to compute hash for file {file_path}: {e}")
        return None
