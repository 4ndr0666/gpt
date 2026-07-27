import json
import os
import shutil
from threading import Timer
import hashlib

# Function to compress a directory into a zip archive
def process_and_compress(directory_path, target_dir='/mnt/data/result', archive_format='zip'):
    if not os.path.isdir(directory_path):
        print(f"The specified directory does not exist: {directory_path}")
        return None

    os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists

    try:
        archive_name = os.path.join(target_dir, os.path.basename(directory_path))
        archive_path = shutil.make_archive(base_name=archive_name, format=archive_format, root_dir=directory_path)
        print(f"Directory successfully compressed into: {archive_path}")
        return archive_path
    except Exception as e:
        print(f"Failed to compress directory {directory_path}: {e}")
        return None

# Class to save data persistently with change detection
class PersistentDataSaver:
    def __init__(self, file_path='/mnt/data/persistent_data.json', interval=600):
        self.file_path = file_path
        self.interval = interval
        self.timer = None
        self.data_hash = None
        self.data = None

    def save_data(self, data):
        current_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()
        if current_hash != self.data_hash:
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(data, f)
                self.data_hash = current_hash
                print(f"Data saved successfully to {self.file_path}")
            except Exception as e:
                print(f"Failed to save data persistently: {e}")
        else:
            print("Data unchanged; no need to save.")
        self.schedule_next_save(data)

    def schedule_next_save(self, data):
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.interval, self.save_data, [data])
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()

if __name__ == "__main__":
    # Specify the directory you wish to compress
    directory_to_compress = "/mnt/data/"  # Source directory
    target_directory = "/mnt/data/result"  # Destination directory for the compressed archive
    archive_format = "zip"  # Compression format

    # Attempt to compress the specified directory
    compressed_archive_path = process_and_compress(directory_to_compress, target_directory, archive_format)
    if compressed_archive_path:
        print(f"Archive created at: {compressed_archive_path}")
    else:
        print("Compression failed.")









