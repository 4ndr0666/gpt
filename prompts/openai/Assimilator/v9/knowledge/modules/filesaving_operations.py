import json
import os
import shutil
from threading import Timer
import hashlib
import logging

# Define the SANDBOX_PATH
SANDBOX_PATH = "/mnt/data/sandbox"

def process_and_compress(directory_path, target_dir=os.path.join(SANDBOX_PATH, 'result'), archive_format='zip'):
    """
    Compresses a directory within the sandbox to a zip file, ensuring operations are compliant with set security protocols.
    """
    if not os.path.isdir(directory_path) or not is_safe_path(SANDBOX_PATH, directory_path):
        logging.error("Directory compression attempted outside of sandbox or directory does not exist.")
        return None

    os.makedirs(target_dir, exist_ok=True)
    try {
        archive_name = os.path.join(target_dir, os.path.basename(directory_path))
        archive_path = shutil.make_archive(base_name=archive_name, format=archive_format, root_dir=directory_path)
        logging.info(f"Directory successfully compressed into: {archive_path}")
        return archive_path
    except Exception as e:
        logging.error(f"Failed to compress directory: {e}")
        return None

class PersistentDataSaver:
    """
    Manages persistent data saving within the sandbox, ensuring changes are compliant and monitored for integrity.
    """
    def __init__(self, file_path=os.path.join(SANDBOX_PATH, 'persistent_data.json'), interval=600):
        self.file_path = file_path
        self.interval = interval
        self.timer = None
        self.data_hash = None
        self.data = None

    def save_data(self, data):
        current_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        if current_hash != self.data_hash:
            if not is_safe_path(SANDBOX_PATH, self.file_path):
                logging.error("Data saving attempt outside of sandbox.")
                return
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(data, f)
                self.data_hash = current_hash
                logging.info(f"Data saved successfully to {self.file_path}")
            except Exception as e:
                logging.error(f"Failed to save data: {e}")
        else:
            logging.info("No data change detected; skip saving.")
        self.schedule_next_save(data)
