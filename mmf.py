import os
import shutil
import re
import logging
import datetime
import argparse

def setup_logger(log_filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a console handler for displaying log messages on the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create a file handler for the log file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

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

def move_or_copy_files(source_paths, destination_folder, logger, use_regex=False, move_files=False, copy_files=False):
    if move_files and copy_files:
        print("Please choose only one of -mv or --move-files, and -cp or --copy-files.")
        return

    if not move_files and not copy_files:
        print("Please specify either -mv or --move-files, or -cp or --copy-files.")
        return

    action_function = shutil.move if move_files else shutil.copy2
    action_name = "Moved" if move_files else "Copied"

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_path in source_paths:
        expanded_path = os.path.expanduser(source_path)

        if use_regex:
            matching_files = [f for f in os.listdir(os.path.dirname(expanded_path)) if re.match(os.path.basename(expanded_path), f)]
            if not matching_files:
                print(f"No files found matching the pattern: {expanded_path}")
            else:
                for filename in matching_files:
                    source_file = os.path.join(os.path.dirname(expanded_path), filename)
                    destination_file = os.path.join(destination_folder, filename)
                    try:
                        # Additional check for directories when using -mv argument
                        if not os.path.isdir(source_file) or not move_files:
                            action_function(source_file, destination_file)
                            print(f"{action_name} '{source_file}' to '{destination_folder}'")
                    except Exception as e:
                        error_message = f"Failed to {action_name.lower()} '{source_file}': {e}"
                        logger.warning(error_message)
        else:
            if not os.path.exists(expanded_path):
                print(f"File not found: {expanded_path}")
            else:
                if os.path.isdir(expanded_path) and move_files:  # Check if the source_path is a directory and move_files is True
                    print(f"Skipping folder: {expanded_path}")
                    # Log a warning when trying to move a folder
                    logger.warning(f"Warning: Cannot move '{expanded_path}' as it is a directory.")
                else:
                    filename = os.path.basename(expanded_path)
                    destination_path = os.path.join(destination_folder, filename)

                    try:
                        action_function(expanded_path, destination_path)
                        print(f"{action_name} '{expanded_path}' to '{destination_folder}'")
                    except IsADirectoryError:
                        error_message = f"Warning: Cannot {action_name.lower()} '{expanded_path}' as it is a directory."
                        logger.warning(error_message)
                    except Exception as e:
                        error_message = f"Failed to {action_name.lower()} '{expanded_path}': {e}"
                        logger.warning(error_message)

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
    print("Move/Copy Multiple Files \n")

    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Move/Copy Multiple Files")
    parser.add_argument("source_paths_file", nargs="?", default="source_paths.txt", help="Path to the source_paths.txt file or enter paths one by one.")
    parser.add_argument("destination_folder", help="Path to the destination folder.")
    parser.add_argument("--regex", action="store_true", help="Use regex to match files in the source directory.")
    move_copy_group = parser.add_mutually_exclusive_group(required=True)
    move_copy_group.add_argument("-mv", "--move-files", action="store_true", help="Move files to the destination folder.")
    move_copy_group.add_argument("-cp", "--copy-files", action="store_true", help="Copy files to the destination folder.")
    args = parser.parse_args()

    source_paths_file = args.source_paths_file
    destination_folder = args.destination_folder

    # Set up the logger to save warnings in a log file with a timestamp
    log_filename = f"mmf-error-log{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    logger = setup_logger(log_filename)

    source_paths = read_source_paths(source_paths_file)
    move_or_copy_files(source_paths, destination_folder, logger, use_regex=args.regex, move_files=args.move_files, copy_files=args.copy_files)