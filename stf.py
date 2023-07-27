import os
import re
import argparse
import sqlite3
from tika import parser as tika_parser
from datetime import datetime
from colorama import init, Fore
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Initialize colorama to support ANSI escape codes on Windows
init()

LOG_FOLDER = 'logs'

def read_fields_from_file(file_path):
    with open(file_path, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def extract_text_from_binary(file_path):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = f"[Tika - {timestamp}] Processing file: {file_path}"
    print(f"{Fore.CYAN}{output}{Fore.RESET}")
    save_log_to_file('tika_log.txt', output)

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

@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
def search_files_for_fields(fields_to_search, directory, database_file):
    if not os.path.exists(database_file):
        initialize_database(database_file)

    pattern = r'\b(?:' + '|'.join(re.escape(term) for term in fields_to_search) + r')\b'
    search_regex = re.compile(pattern, re.IGNORECASE)

    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    # Retrieve the maximum existing ID from the database to generate new unique IDs
    c.execute("SELECT MAX(ID) FROM search_results")
    max_id = c.fetchone()[0]

    if max_id is None:
        max_id = 0

    # Assign the timestamp value at the beginning of the function
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
                if search_regex.search(line):  # Use regex search instead of re.search
                    found_matches = True
                    matched_line = line.strip()
                    matched_content.append(matched_line)
                    # Find all matched terms in the line using the compiled regex
                    matched_fields.update(term for term in fields_to_search if re.search(r'\b{}\b'.format(re.escape(term)), matched_line, re.IGNORECASE))

            if found_matches:
                # Generate a new unique ID for this input
                max_id += 1
                unique_id = max_id

                file_type = clean_string(tika_parser.from_file(file_path)['metadata']['Content-Type'])

                # Insert into the database
                try:
                    c.execute("INSERT INTO search_results VALUES (?, ?, ?, ?, ?, ?)",
                              (unique_id, timestamp, file_path, file_type, ', '.join(matched_fields), '\n'.join(matched_content)))
                    conn.commit()
                    output = f"[SQL - {timestamp}] Inserted into database: {file_path}"
                    print(f"{Fore.MAGENTA}{output}{Fore.RESET}")
                    save_log_to_file('sql_log.txt', output)
                except Exception as e:
                    conn.rollback()
                    output = f"[SQL - {timestamp}] Error inserting into database: {e}"
                    print(f"{Fore.RED}{output}{Fore.RESET}")
                    save_log_to_file('sql_log.txt', output)

    conn.close()
    # Use the timestamp variable in the print statement at the end of the function
    output = f"[{timestamp}] Database insertion completed."
    print(f"{Fore.GREEN}{output}{Fore.RESET}")
    save_log_to_file('sql_log.txt', output)

def save_log_to_file(log_file, log_content):
    log_folder_path = os.path.join(os.getcwd(), LOG_FOLDER)
    os.makedirs(log_folder_path, exist_ok=True)

    log_file_path = os.path.join(log_folder_path, log_file)
    # Strip ANSI escape codes before writing to the log file
    clean_log_content = re.sub(r'\x1b\[\d+m', '', log_content)
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(clean_log_content + '\n')

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Search for terms in files recursively and save on SQLite database')
    arg_parser.add_argument('fields_file', type=str, help='Path to the file containing terms.')
    arg_parser.add_argument('directory', type=str, help='The directory to search recursively.')
    arg_parser.add_argument('database', type=str, nargs='?', default='results-db.sqlite', help='SQLite database file to store the results.')
    args = arg_parser.parse_args()

    fields_to_search = read_fields_from_file(args.fields_file)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = f"[{timestamp}] Searching for fields: {fields_to_search}"
    print(f"{Fore.YELLOW}{output}{Fore.RESET}")
    save_log_to_file('search_log.txt', output)

    search_files_for_fields(fields_to_search, args.directory, args.database)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = f"[{timestamp}] Search completed."
    print(f"{Fore.GREEN}{output}{Fore.RESET}")
    save_log_to_file('search_log.txt', output)