import os
import shutil
import re
from tqdm import tqdm

def read_source_paths(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            source_paths = file.read().splitlines()
    else:
        source_paths = []

    if not source_paths:
        print("No source paths found in the file. Please enter the paths one by one (Type 'done' to stop):")
        while True:
            path_input = input()
            if path_input.lower() == 'done':
                break
            source_paths.append(path_input)

        with open(file_path, 'w') as file:
            file.write('\n'.join(source_paths))

    return source_paths

def create_or_select_file(prompt):
    while True:
        choice = input(f"{prompt} Do you want to create it in the current directory? (y/n): ").lower()
        if choice == 'y':
            file_name = input("Enter the file name (e.g., source_paths.txt): ")
            file_path = os.path.join(os.getcwd(), file_name)
            if not os.path.exists(file_path):
                return file_path
            else:
                print("A file with the same name already exists in the current directory.")
        elif choice == 'n':
            return input("Enter the full path to the file: ")

def create_or_select_folder(prompt):
    while True:
        choice = input(f"{prompt} Do you want to create it in the current directory? (y/n): ").lower()
        if choice == 'y':
            folder_name = input("Enter the folder name (e.g., destination_folder): ")
            return os.path.join(os.getcwd(), folder_name)
        elif choice == 'n':
            return input("Enter the full path to the folder: ")

def move_or_copy_files(source_paths, destination_folder):
    print("Select an action:")
    print("1. Move files")
    print("2. Copy files")

    choice = input("Enter the option number: ")

    if choice == "1":
        action_function = shutil.move
        action_name = "Moved"
    elif choice == "2":
        action_function = shutil.copy2  
        action_name = "Copied"
    else:
        print("Invalid option. Exiting.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_path in source_paths:
        expanded_path = os.path.expanduser(source_path)

        # Check if the source_path is a regex pattern
        if re.search(r'[*?[\]{}]', os.path.basename(expanded_path)):
            matching_files = [f for f in os.listdir(os.path.dirname(expanded_path)) if re.match(os.path.basename(expanded_path), f)]
            if not matching_files:
                print(f"No files found matching the pattern: {expanded_path}")
            else:
                for filename in matching_files:
                    source_file = os.path.join(os.path.dirname(expanded_path), filename)
                    destination_file = os.path.join(destination_folder, filename)
                    try:
                        # Use tqdm to show progress
                        with tqdm(total=os.path.getsize(source_file), unit='B', unit_scale=True, desc=f"{action_name} '{filename}'") as progress:
                            action_function(source_file, destination_file)
                            progress.update(os.path.getsize(source_file))
                        print(f"{action_name} '{filename}' to '{destination_folder}'")
                    except Exception as e:
                        print(f"Failed to {action_name.lower()} '{filename}': {e}")
        else:
            if not os.path.exists(expanded_path):
                print(f"File not found: {expanded_path}")
            else:
                filename = os.path.basename(expanded_path)
                destination_path = os.path.join(destination_folder, filename)

                try:
                    # Use tqdm to show progress
                    with tqdm(total=os.path.getsize(expanded_path), unit='B', unit_scale=True, desc=f"{action_name} '{filename}'") as progress:
                        action_function(expanded_path, destination_path)
                        progress.update(os.path.getsize(expanded_path))
                    print(f"{action_name} '{filename}' to '{destination_folder}'")
                except Exception as e:
                    print(f"Failed to {action_name.lower()} '{filename}': {e}")

if __name__ == "__main__":
    print(r"""
__/\\\\____________/\\\\__/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_        
 _\/\\\\\\________/\\\\\\_\/\\\\\\________/\\\\\\_\/\\\///////////__       
  _\/\\\//\\\____/\\\//\\\_\/\\\//\\\____/\\\//\\\_\/\\\_____________      
   _\/\\\\///\\\/\\\/_\/\\\_\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_____     
    _\/\\\__\///\\\/___\/\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////______    
     _\/\\\____\///_____\/\\\_\/\\\____\///_____\/\\\_\/\\\_____________   
      _\/\\\_____________\/\\\_\/\\\_____________\/\\\_\/\\\_____________  
       _\/\\\_____________\/\\\_\/\\\_____________\/\\\_\/\\\_____________ 
        _\///______________\///__\///______________\///__\///______________
                                      
    """)
    print("Move/Copy Multiple Files using regex \n")
    # Ask the user if the source_paths.txt file doesn't exist
    source_paths_file = "source_paths.txt"
    if not os.path.exists(source_paths_file):
        source_paths_file = create_or_select_file("source_paths.txt file not found.")

    # Ask the user if the destination folder doesn't exist
    destination_folder = "files"
    if not os.path.exists(destination_folder):
        destination_folder = create_or_select_folder("Destination folder not found.")

    source_paths = read_source_paths(source_paths_file)
    move_or_copy_files(source_paths, destination_folder)