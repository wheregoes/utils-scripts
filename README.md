[DMF - Download multiple files from a file or user input and save on folder.](#dmfpy) <br />
[MMF- Move/Copy multiple files.](#mmfpy) <br />
[SFE - Separate files by extension](#sfepy) <br />
[HAM - ~Random~HashAccessMemories](#hampy) <br />
[RDF - Search recursively for duplicate files by calculating hash of every file and delete.](#rdfpy) <br />

# dmf.py
**Description** <br />
Download multiple files from a file or user input and save on folder. <br />

**Requirements:**
```pip install requests tqdm colorama```

**Features** <br />
:heavy_check_mark: Can choose to download one file at time or many you want using multi-thread option. <br />
:heavy_check_mark: Log when can't download a file. <br />
:heavy_check_mark: Log when can't download the file entirely. <br />
:heavy_check_mark: Cooldown and try again when fails to start downloading a file. <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
:heavy_minus_sign: Handle URLs from Clearnet and Deep/Dark web (.onion) together. <br />
:heavy_minus_sign: Improve the log registry (add status code etc). <br />
***Suggestions*** <br />

Usage:
```
python3 dmf.py [--multi-thread] [-T NUM_THREADS]
```

**To use with .onion websites you can use torsocks before the script e.g: ```torsocks python3 dmf.py```** <br />

# mmf.py
**Description** <br />
Move/Copy multiple files. <br />

**Requirements:**
```none```

**Features** <br />
:heavy_check_mark: Supports Regex. <br />
:heavy_check_mark: Move/copy files from differents folders. <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
:heavy_minus_sign: Handle permissionError when try to moving a file without necessary permissions (eg. read-only). <br />
***Suggestions***

Usage:
```
python3 mmf.py [--regex] [-cp] [-mv] [-nd] source_paths_file destination_folder

Move/Copy Multiple Files and Folders

positional arguments:
  source_paths_file   Path to the source_paths.txt file or enter paths one by one.
  destination_folder  Path to the destination folder.

options:
  -h, --help          Help
  --regex             Use regex to match files and folders in the source directory.
  -mv, --move-files   Move files/folders to the destination folder.
  -cp, --copy-files   Copy files/folders to the destination folder.
  -nd, --no-dir       Do not move/copy folders to the destination folder.
```

# sfe.py
**Description** <br />
Separate files by extension <br />

**Requirements:**
```pip install colorama```

**Features** <br />
:heavy_check_mark: Log when can't move/copy a file. <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
***Suggestions*** <br />

Usage:
```
usage: python3 sfe.py [-cp] [-mv] [-r] source_directory destination_directory

Separate files in folders by file extension

positional arguments:
  source_directory      Path to the source directory
  destination_directory Path to the destination directory

options:
  -h, --help            Help
  -cp, --copy-files     Copy files to destination directory
  -mv, --move-files     Move files to destination directory
  -r, --recursive       Recursively copy or move files
```


# ham.py
**Description** <br />
~Random~HashAccessMemories <br />

A script that provides a simple way to merge the cracked passwords to they respective usernames. <br />

Example:
```
cat any_leak_user_hash.txt
user01:16e029226d8960b2d7cba16cab5f7044
user02:a280638195f9e88fb2fbdfcd1283d7fa
email@gmail.com:fee22a6247e95d5a08769c51a861cb00

cat any_leak_dehashed_pass.txt
16e029226d8960b2d7cba16cab5f7044:n00b
a280638195f9e88fb2fbdfcd1283d7fa:daftpunk
fee22a6247e95d5a08769c51a861cb00:checkstfproject

```
The script will merge these two files, changing the hashes that has been dehashed.

The third file result will be:
``` 
cat any_leak_user:pass.txt
user01:n00b
user02:daftpunk
email@gmail.com:checkstfproject

```

**Requirements:**
```pip install tqdm```

**Future Updates** <br />
***Suggestions*** <br />

Usage:
```
usage: ham.py input_file dehashed_file [-o OUTPUT_FILE]

positional arguments:
  input_file            The file containing the usernames and hashes.
  dehashed_file         The file containing the hashes and cracked passwords.

options:
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file with matched usernames and passwords.
```


# rdf.py
**Description** <br />
Search recursively for duplicate files by calculating hash of every file and delete. <br />

**Requirements:**
```pip install tqdm sql```

**Features** <br />
:heavy_check_mark: Remove files recursively. <br />
:heavy_check_mark: Can handle large files. <br />
:heavy_check_mark: Log when can't remove a file.  <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
***Suggestions***

Usage:
```
python3 rdf.py start_path

Process files and store their hashes in a SQLite database.

positional arguments:
  start_path  Starting path for file search

options:
  -h, --help  Help
```
