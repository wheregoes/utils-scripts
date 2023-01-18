import os
import hashlib
from pathlib import Path
from tqdm import tqdm

file_path = os.getcwd()
files_count = sum(len(files) for _, _, files in os.walk(file_path))

unique_files = dict()

with tqdm(total=files_count, desc='Processing files') as pbar:
    for root, folders, files in os.walk(file_path):
        for file in files:
            file_path = Path(os.path.join(root, file))
            try:
                sha256_hash = hashlib.sha256()
                with open(file_path, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                Hash_file = sha256_hash.hexdigest()

                if Hash_file not in unique_files:
                    unique_files[Hash_file] = file_path
                else:
                    os.remove(file_path)
                    print(f"Duplicate file deleted: {file_path} \n Hash:{Hash_file} \n")
                pbar.update(1)
            except PermissionError:
                print(f"PermissionError: {file_path}")
            continue
