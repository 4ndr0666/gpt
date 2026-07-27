import json
import os
import shutil
from threading import Timer
import hashlib
import logging

# Define the SANDBOX_PATH for secure file operations
SANDBOX_PATH = "/mnt/data/sandbox"

# Initialize logging for detailed output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_safe_path(basedir, path, follow_symlinks=True):
    """
    Check if the path is secure and confined within the specified basedir.

    Args:
        basedir (str): The base directory to validate against.
        path (str): The file path to validate.
        follow_symlinks (bool): Whether to follow symlinks for path validation.

    Returns:
        bool: True if the path is within the basedir, False otherwise.
    """
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def save_file_to_sandbox(file_path, content):
    """
    Save content to a file within the sandbox environment securely.

    Args:
        file_path (str): The relative file path within the sandbox.
        content (str): The content to save in the file.

    Returns:
        bool: True if the file is saved successfully, False otherwise.
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
    except IOError as e:
        logging.error(f"IOError while saving file {file_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error saving file {file_path}: {e}")
    return False

def schedule_file_cleanup(file_path, delay):
    """
    Schedule a file for deletion after a specified delay.

    Args:
        file_path (str): The path to the file within the sandbox.
        delay (int): The delay in seconds before the file is deleted.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)

    def cleanup():
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
                logging.info(f"File {full_path} successfully deleted.")
            except OSError as e:
                logging.error(f"OSError while deleting file {full_path}: {e}")
            except Exception as e:
                logging.error(f"Unexpected error deleting file {full_path}: {e}")
        else:
            logging.warning(f"File {full_path} does not exist for cleanup.")

    Timer(delay, cleanup).start()
    logging.info(f"File cleanup for {full_path} scheduled in {delay} seconds.")

def compute_file_hash(file_path):
    """
    Compute the SHA-256 hash of a file's contents for integrity verification.

    Args:
        file_path (str): The path to the file within the sandbox.

    Returns:
        str: The SHA-256 hash of the file contents, or None if an error occurs.
    """
    full_path = os.path.join(SANDBOX_PATH, file_path)
    if not is_safe_path(SANDBOX_PATH, full_path):
        logging.error(f"Attempted to access a file outside the sandbox: {full_path}")
        return None
    try:
        with open(full_path, 'rb') as file:
            file_content = file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        logging.info(f"Computed hash for file {file_path}: {file_hash}")
        return file_hash
    except FileNotFoundError:
        logging.error(f"File not found for hashing: {file_path}")
    except IOError as e:
        logging.error(f"IOError while reading file {file_path} for hashing: {e}")
    except Exception as e:
        logging.error(f"Unexpected error computing hash for file {file_path}: {e}")
    return None

if __name__ == "__main__":
    # Example usage of the module
    test_file_path = "test_file.txt"
    test_content = "This is a test content for file saving operations."

    # Attempt to save a file
    if save_file_to_sandbox(test_file_path, test_content):
        logging.info("File save operation completed successfully.")
    else:
        logging.error("File save operation failed.")

    # Schedule file cleanup
    schedule_file_cleanup(test_file_path, 10)  # Cleanup after 10 seconds

    # Compute file hash
    file_hash = compute_file_hash(test_file_path)
    if file_hash:
        logging.info(f"File hash: {file_hash}")
    else:
        logging.error("Failed to compute file hash.")
