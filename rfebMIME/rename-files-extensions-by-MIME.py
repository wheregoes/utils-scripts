import magic
import os
import argparse

def read_extension_mappings(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            pass

    with open(file_path, 'r') as file:
        return {line.strip().split(',')[0]: line.strip().split(',')[1] for line in file if ',' in line}

def rename_file_with_extension(file_path, extension_mapping):
    file_type = magic.from_file(file_path, mime=True)
    expected_extension = extension_mapping.get(file_type)

    if expected_extension:
        current_extension = os.path.splitext(file_path)[1]
        if current_extension == expected_extension:
            print(f"'{file_path}' already has the correct extension '{expected_extension}'. Skipping.")
        else:
            new_file_path = os.path.splitext(file_path)[0] + expected_extension
            os.rename(file_path, new_file_path)
            print(f"Renamed '{file_path}' to '{new_file_path}'")
    else:
        print(f"Unknown file type '{file_type}' for '{file_path}'.")
        user_input = input(f"Do you want to add the MIME type '{file_type}' to the extension list? (y/n): ").lower()
        if user_input == 'y':
            new_extension = input("Enter the extension to use (including the dot, e.g., '.txt'): ")
            with open('extensions.txt', 'a') as file:
                file.write(f"{file_type},{new_extension}\n")
            extension_mapping[file_type] = new_extension
            rename_file_with_extension(file_path, extension_mapping)

def process_directory(directory, extension_mapping, recursive):
    if recursive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                rename_file_with_extension(os.path.join(root, file), extension_mapping)
    else:
        for file in os.listdir(directory):
            full_path = os.path.join(directory, file)
            if os.path.isfile(full_path):
                rename_file_with_extension(full_path, extension_mapping)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="Directory to process files in")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively process files in subdirectories")
    args = parser.parse_args()

    extension_mapping = read_extension_mappings('extensions.txt')
    process_directory(args.directory, extension_mapping, args.recursive)

if __name__ == "__main__":
    main()
