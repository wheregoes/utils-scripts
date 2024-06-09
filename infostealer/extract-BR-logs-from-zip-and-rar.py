import os
import sys
import zipfile
import rarfile
import shutil
from tqdm import tqdm

def create_destination_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_next_available_folder_name(folder_path):
    base_folder_path = folder_path
    counter = 1
    while os.path.exists(folder_path):
        folder_path = f"{base_folder_path}_{counter:02d}"
        counter += 1
    return folder_path

def count_relevant_folders_in_zip(zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            return sum(1 for member in zip_ref.namelist() if member.endswith('/') and member.split('/')[-2].startswith('BR'))
    except NotImplementedError as e:
        print(f"Skipping {zip_path}: {e}")
        return 0

def count_relevant_folders_in_rar(rar_path):
    with rarfile.RarFile(rar_path, 'r') as rar_ref:
        return sum(1 for member in rar_ref.infolist() if member.isdir() and member.filename.split('/')[-2].startswith('BR'))

def extract_from_zip(zip_path, dest_folder, password=None):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            relevant_folders = [member for member in zip_ref.namelist() if member.endswith('/') and member.split('/')[-2].startswith('BR')]
            with tqdm(total=len(relevant_folders), desc=f"Processing {os.path.basename(zip_path)}") as pbar:
                for member in relevant_folders:
                    folder_name = member.split('/')[-2]
                    dest_path = get_next_available_folder_name(os.path.join(dest_folder, folder_name))
                    create_destination_dir(dest_path)
                    for file in zip_ref.namelist():
                        if file.startswith(member) and not file.endswith('/'):
                            with zip_ref.open(file, pwd=password.encode() if password else None) as source, \
                                 open(os.path.join(dest_path, os.path.basename(file)), 'wb') as target:
                                shutil.copyfileobj(source, target)
                    pbar.update(1)
    except NotImplementedError as e:
        print(f"Skipping {zip_path}: {e}")

def extract_from_rar(rar_path, dest_folder, password=None):
    with rarfile.RarFile(rar_path, 'r') as rar_ref:
        relevant_folders = [member for member in rar_ref.infolist() if member.isdir() and member.filename.split('/')[-2].startswith('BR')]
        with tqdm(total=len(relevant_folders), desc=f"Processing {os.path.basename(rar_path)}") as pbar:
            for member in relevant_folders:
                folder_name = member.filename.split('/')[-2]
                dest_path = get_next_available_folder_name(os.path.join(dest_folder, folder_name))
                create_destination_dir(dest_path)
                for file in rar_ref.infolist():
                    if file.filename.startswith(member.filename) and not file.isdir():
                        file_dest_path = os.path.join(dest_path, os.path.relpath(file.filename, member.filename))
                        os.makedirs(os.path.dirname(file_dest_path), exist_ok=True)
                        with rar_ref.open(file, pwd=password) as source, open(file_dest_path, 'wb') as target:
                            shutil.copyfileobj(source, target)
                pbar.update(1)

def process_archives(archive_dir, dest_folder, password=None):
    create_destination_dir(dest_folder)
    archive_files = [os.path.join(root, file)
                     for root, _, files in os.walk(archive_dir)
                     for file in files if file.endswith('.zip') or file.endswith('.rar')]

    total_relevant_folders = 0
    for file_path in archive_files:
        if file_path.endswith('.zip'):
            total_relevant_folders += count_relevant_folders_in_zip(file_path)
        elif file_path.endswith('.rar'):
            total_relevant_folders += count_relevant_folders_in_rar(file_path)

    with tqdm(total=total_relevant_folders, desc="Processing all archives") as pbar:
        for file_path in archive_files:
            if file_path.endswith('.zip'):
                extract_from_zip(file_path, dest_folder, password)
            elif file_path.endswith('.rar'):
                extract_from_rar(file_path, dest_folder, password)
            pbar.update(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract-BR-logs-from-zip-and-rar.py <path/to/files> [password]")
        sys.exit(1)

    archive_dir = sys.argv[1]
    dest_folder = 'extracted-br-logs'
    password = sys.argv[2] if len(sys.argv) > 2 else None

    process_archives(archive_dir, dest_folder, password)