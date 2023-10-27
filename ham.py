import argparse
from tqdm import tqdm

def crack_hashes(input_file, dehashed_file, output_file):
    to_crack_dict = {}

    with open(input_file, 'r') as file:
        for line_number, line in tqdm(enumerate(file, 1), desc=f"Processing {input_file}", unit="line"):
            try:
                username, hash_value = line.strip().split(':')
                to_crack_dict[hash_value] = username
            except ValueError as e:
                print(f"Error in file '{input_file}', line {line_number}: {line.strip()} - {e}")

    output_lines = set()
    with open(dehashed_file, 'r') as file:
        for line_number, line in tqdm(enumerate(file, 1), desc=f"Processing {dehashed_file}", unit="line"):
            try:
                hash_value, password = line.strip().split(':')
                if hash_value in to_crack_dict:
                    output_lines.add(f"{to_crack_dict[hash_value]}:{password}")
            except ValueError as e:
                print(f"Error in file '{dehashed_file}', line {line_number}: {line.strip()} - {e}")

    with open(output_file, 'w') as file:
        for line in sorted(output_lines):
            file.write(f"{line}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A script to compare and match hashes between two files.')
    parser.add_argument('input_file', help='The file containing the usernames and hashes.')
    parser.add_argument('dehashed_file', help='The file containing the hashes and cracked passwords.')
    parser.add_argument('-o', '--output_file', default='cracked_hashes_output.txt', help='Output file with matched usernames and passwords.')
    
    args = parser.parse_args()
    crack_hashes(args.input_file, args.dehashed_file, args.output_file)