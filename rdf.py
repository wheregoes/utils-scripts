import os
import hashlib
import logging
import sqlite3
import argparse
from pathlib import Path
from tqdm import tqdm

def create_database():
    if os.path.exists('hashes.sqlite'):
        print("Error: The database file 'hashes.sqlite' already exists. Please rename or delete the file and try again. This is to prevent previously calculated hashes of unique files to be deleted accidentally")
        exit(1)

    connection = sqlite3.connect('hashes.sqlite')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS files (hash TEXT PRIMARY KEY, file_path TEXT)')
    connection.commit()
    connection.close()

def process_files(start_path):
    files_count = sum(len(files) for _, _, files in os.walk(start_path))

    logging.basicConfig(filename='rdf-PermissionError.log', level=logging.ERROR)

    with tqdm(total=files_count, desc='Processing files') as pbar:
        for root, folders, files in os.walk(start_path):
            for file in files:
                file_path = Path(os.path.join(root, file))
                try:
                    sha256_hash = hashlib.sha256()
                    with open(file_path, "rb") as f:
                        for byte_block in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(byte_block)
                    Hash_file = sha256_hash.hexdigest()

                    connection = sqlite3.connect('hashes.sqlite')
                    cursor = connection.cursor()

                    cursor.execute('SELECT * FROM files WHERE hash=?', (Hash_file,))
                    existing_file = cursor.fetchone()

                    if existing_file is None:
                        cursor.execute('INSERT INTO files (hash, file_path) VALUES (?, ?)', (Hash_file, str(file_path)))
                    else:
                        os.remove(file_path)
                        logging.error(f"Duplicate file deleted: {file_path} \n Hash:{Hash_file} \n")

                    connection.commit()
                    connection.close()

                    pbar.update(1)
                except PermissionError:
                    print(f"PermissionError: {file_path}")
                    logging.error(f"PermissionError: {file_path}")
                continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process files and store their hashes in a SQLite database.')
    parser.add_argument('start_path', metavar='start_path', type=str, help='Starting path for file search')
    args = parser.parse_args()

    start_path = args.start_path
    if not os.path.isdir(start_path):
        print(f"Error: {start_path} is not a valid directory.")
    else:
        create_database()
        process_files(start_path)