# stf.py
**Description** <br />
Search for terms in files recursively and save on SQLite database. <br />

**Requirements:**
```pip install tika sql colorama tenacity```

**Features** <br />
:heavy_check_mark: Uses Apache Tika to handle binary files (the script search terms even inside of Microsoft Office document formats, PDF etc. See the full list: https://tika.apache.org/2.8.0/formats.html). <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
:heavy_check_mark: Support to regex. <br />
:heavy_check_mark: Improve the processing speed. <br />
***Suggestions***

Usage:
```
usage: stf.py [-h] [terms_file] [directory] [database]

Search for terms in files recursively and save on SQLite database

positional arguments:
  terms_file   Path to the file containing terms.
  directory    The directory to search recursively.
  database     SQLite database file to store the results.

options:
  -h, --help   Help
```

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
python3 mmf.py [--regex] (-mv | -cp) [source_paths_file] [destination_folder]

positional arguments:
  source_paths_file   Path to the source_paths.txt file or enter paths one by one.
  destination_folder  Path to the destination folder.

options:
  -h, --help          Help
  --regex             Use regex to match files in the source directory.
  -mv, --move-files   Move files to the destination folder.
  -cp, --copy-files   Copy files to the destination folder.
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
python3 sfe.py [-h] [-cp] [-mv] [source_directory] [destination_directory]
```

# rdf.py
**Description** <br />
Search recursively for duplicate files by calculating hash of every file and delete. <br />

**Requirements:**
```pip install tqdm```

**Features** <br />
:heavy_check_mark: Remove files recursively (user input the directory or where the script is). <br />
:heavy_check_mark: Can handle large files. <br />
:heavy_check_mark: Log when can't remove a file.  <br />
:heavy_check_mark: Can be used in background. <br />

**Future Updates** <br />
***Suggestions***
