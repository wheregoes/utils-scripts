import os
import shutil
import argparse
import logging
from colorama import init, Fore, Style

init(autoreset=True)

def copy_file(source_path, destination_path):
    shutil.copy(source_path, destination_path)
    return f"{Fore.GREEN}Copied{Style.RESET_ALL}: {source_path} to {destination_path}"

def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)
    return f"{Fore.CYAN}Moved{Style.RESET_ALL}: {source_path} to {destination_path}"

def separate_files_by_extension(source_dir, destination_dir, action):
    os.makedirs(destination_dir, exist_ok=True)

    action_functions = {
        'copy': copy_file,
        'move': move_file,
    }

    action_function = action_functions.get(action)
    if action_function is None:
        print(f"Invalid action: {action}. Use 'copy' or 'move'.")
        exit(1)

    for root, _, files in os.walk(source_dir):
        for filename in files:
            source_path = os.path.join(root, filename)
            extension = os.path.splitext(filename)[1].lower()
            destination_folder = os.path.join(destination_dir, extension.strip('.'))
            os.makedirs(destination_folder, exist_ok=True)
            destination_path = os.path.join(destination_folder, filename)

            try:
                print(action_function(source_path, destination_path))
            except PermissionError as e:
                print(f"{Fore.RED}PermissionError{Style.RESET_ALL}: {e} - {source_path} was not {action}ed.")
                logging.error(f"PermissionError: {e} - {source_path} was not {action}ed.")
                continue

if __name__ == "__main__":
    
    banner = r"""
_____/\\\\\\\\\\\____/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\_        
 ___/\\\/////////\\\_\/\\\///////////__\/\\\///////////__       
  __\//\\\______\///__\/\\\_____________\/\\\_____________      
   ___\////\\\_________\/\\\\\\\\\\\_____\/\\\\\\\\\\\_____     
    ______\////\\\______\/\\\///////______\/\\\///////______    
     _________\////\\\___\/\\\_____________\/\\\_____________   
      __/\\\______\//\\\__\/\\\_____________\/\\\_____________  
       _\///\\\\\\\\\\\/___\/\\\_____________\/\\\\\\\\\\\\\\\_ 
        ___\///////////_____\///______________\///////////////__
"""

    print(banner)

    logging.basicConfig(filename='sfbe-errors.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description="Separate files in folders by file extension")
    parser.add_argument("source_directory", help="Path to the source directory")
    parser.add_argument("destination_directory", nargs="?", help="Path to the destination directory")
    parser.add_argument("-cp", "--copy-files", action="store_true", help="Copy files to destination directory")
    parser.add_argument("-mv", "--move-files", action="store_true", help="Move files to destination directory")
    args = parser.parse_args()

    # Check if only one argument is provided
    if args.copy_files and args.move_files:
        print("Error: Please specify either --copy-files (-cp) or --move-files (-mv), not both.")
        exit(1)
    elif not args.copy_files and not args.move_files:
        print("Error: Please specify either --copy-files (-cp) or --move-files (-mv).")
        exit(1)

    separate_files_by_extension(args.source_directory, args.destination_directory, 'copy' if args.copy_files else 'move')
