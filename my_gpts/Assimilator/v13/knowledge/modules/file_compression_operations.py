import json
import os
import shutil
from threading import Timer
import hashlib
import logging

# Define the SANDBOX_PATH
SANDBOX_PATH = "/mnt/data/sandbox"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_safe_path(basedir, path, follow_symlinks=True):
    """Ensure the path is within the allowed directory."""
    if follow_symlinks:
        return os.path.realpath(path).startswith(basedir)
    else:
        return os.path.abspath(path).startswith(basedir)

def process_and_compress(directory_path, target_dir=os.path.join(SANDBOX_PATH, 'result'), archive_format='zip'):
    """
    Compress a directory into an archive.
    
    Args:
        directory_path (str): The directory to compress.
        target_dir (str): The directory where the archive will be saved.
        archive_format (str): The format of the archive, default is 'zip'.

    Returns:
        str: The path to the compressed archive if successful, None otherwise.
    """
    # Check for path safety
    if not is_safe_path(SANDBOX_PATH, directory_path) or not is_safe_path(SANDBOX_PATH, target_dir):
        logging.error("Attempted to access outside of sandbox.")
        return None

    # Validate directory existence
    if not os.path.isdir(directory_path):
        logging.error(f"The specified directory does not exist: {directory_path}")
        return None

    os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists

    try:
        archive_name = os.path.join(target_dir, os.path.basename(directory_path))
        archive_path = shutil.make_archive(base_name=archive_name, format=archive_format, root_dir=directory_path)
        logging.info(f"Directory successfully compressed into: {archive_path}")
        return archive_path
    except Exception as e:
        logging.error(f"Failed to compress directory {directory_path}: {e}")
        return None

class PersistentDataSaver:
    """
    Class to handle persistent data saving with change detection.
    
    Args:
        file_path (str): Path to the persistent data file.
        interval (int): Time interval in seconds for saving data persistently.
    """
    def __init__(self, file_path=os.path.join(SANDBOX_PATH, 'persistent_data.json'), interval=600):
        self.file_path = file_path
        self.interval = interval
        self.timer = None
        self.data_hash = None
        self.data = None

    def save_data(self, data):
        """
        Save data if changes are detected.
        
        Args:
            data (dict): The data to be saved.
        """
        current_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        if current_hash != self.data_hash:
            if not is_safe_path(SANDBOX_PATH, self.file_path):
                logging.error("Attempted to write outside of sandbox.")
                return

            try:
                with open(self.file_path, 'w') as f:
                    json.dump(data, f, indent=4)  # Save JSON with indentation for readability
                self.data_hash = current_hash
                logging.info(f"Data saved successfully to {self.file_path}")
            except Exception as e:
                logging.error(f"Failed to save data persistently: {e}")
        else:
            logging.info("Data unchanged; no need to save.")
        self.schedule_next_save(data)

    def schedule_next_save(self, data):
        """
        Schedule the next save operation.
        
        Args:
            data (dict): The data to be saved.
        """
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.interval, self.save_data, [data])
        self.timer.start()

    def stop(self):
        """Stop the scheduled saving process."""
        if self.timer:
            self.timer.cancel()

if __name__ == "__main__":
    # Use a specific directory within the sandbox to compress
    directory_to_compress = os.path.join(SANDBOX_PATH, "source")  # Source directory
    target_directory = os.path.join(SANDBOX_PATH, "result")  # Destination directory for the compressed archive
    archive_format = "zip"  # Compression format

    # Attempt to compress the specified directory
    compressed_archive_path = process_and_compress(directory_to_compress, target_directory, archive_format)
    if compressed_archive_path:
        logging.info(f"Archive created at: {compressed_archive_path}")
    else:
        logging.error("Compression failed.")
