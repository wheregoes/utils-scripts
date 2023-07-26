import os
import re
import argparse
import sqlite3
from tika import parser as tika_parser
from datetime import datetime
from colorama import init, Fore

# Initialize colorama to support ANSI escape codes on Windows
init()

def read_fields_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def extract_text_from_binary(file_path):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"{Fore.CYAN}[Tika - {timestamp}] Processing file: {file_path}{Fore.RESET}")
    parsed = tika_parser.from_file(file_path)
    return parsed['content'] if 'content' in parsed else ''

def clean_string(s):
    # Replace unsupported characters with an empty string
    return ''.join(c for c in s if c.isprintable())

def initialize_database(database_file):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Create a new table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS search_results 
                 (ID INTEGER PRIMARY KEY, Timestamp TEXT, Path TEXT, Type TEXT, Match TEXT, Match_Content TEXT)''')

    conn.commit()
    conn.close()

def search_files_for_fields(fields_to_search, directory, database_file):
    if not os.path.exists(database_file):
        initialize_database(database_file)

    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Retrieve the maximum existing ID from the database to generate new unique IDs
    c.execute("SELECT MAX(ID) FROM search_results")
    max_id = c.fetchone()[0]

    if max_id is None:
        max_id = 0

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.isfile(file_path):
                continue
            file_content = extract_text_from_binary(file_path)
            if not file_content:
                continue

            found_matches = False
            matched_fields = set()
            matched_content = []

            for line_number, line in enumerate(file_content.splitlines(), start=1):
                for field in fields_to_search:
                    if re.search(r'(?i)\b{}\b'.format(re.escape(field)), line):
                        found_matches = True
                        matched_fields.add(field)
                        matched_content.append(line.strip())

            if found_matches:
                # Generate a new unique ID for this input
                max_id += 1
                unique_id = max_id

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file_type = clean_string(tika_parser.from_file(file_path)['metadata']['Content-Type'])

                # Insert into the database
                try:
                    c.execute("INSERT INTO search_results VALUES (?, ?, ?, ?, ?, ?)",
                              (unique_id, timestamp, file_path, file_type, ', '.join(matched_fields), '\n'.join(matched_content)))
                    conn.commit()
                    print(f"{Fore.MAGENTA}[SQL - {timestamp}] Inserted into database: {file_path}{Fore.RESET}")
                except Exception as e:
                    conn.rollback()
                    print(f"{Fore.RED}[SQL - {timestamp}] Error inserting into database: {e}{Fore.RESET}")

    conn.close()
    print(f"{Fore.GREEN}[{timestamp}] Database insertion completed.{Fore.RESET}")

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Search for terms in files recursively and save on SQLite database')
    arg_parser.add_argument('fields_file', type=str, help='Path to the file containing terms.')
    arg_parser.add_argument('directory', type=str, help='The directory to search recursively.')
    arg_parser.add_argument('database', type=str, nargs='?', default='results-db.sqlite', help='SQLite database file to store the results.')
    args = arg_parser.parse_args()

    fields_to_search = read_fields_from_file(args.fields_file)
    print(f"{Fore.YELLOW}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Searching for fields: {fields_to_search}{Fore.RESET}")
    search_files_for_fields(fields_to_search, args.directory, args.database)

    print(f"{Fore.GREEN}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Search completed.{Fore.RESET}")