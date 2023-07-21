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

# dmf.py
**Description** <br />
Download multiple files from a file or user input and save on folder. <br />

**Requirements:**
```pip install tqdm```
```pip install requests```

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
python3 dmf.py --multi-thread -T 10

See -h for options
```

**To use with .onion websites you can use torsocks before the script e.g: ```torsocks python3 dmf.py```** <br />

# mmf.py
**Description** <br />
Move/Copy multiple files using (or not) Regex <br />

**Requirements:**
```none```

**Features** <br />
:heavy_check_mark: Supports Regex <br />
:heavy_check_mark: Move/copy files from differents folders <br />
:heavy_check_mark: Can be used in background. <br />
:heavy_check_mark: 

**Future Updates** <br />
:heavy_minus_sign: Handle permissionError when try to moving a file without necessary permissions (eg. read-only). <br />
***Suggestions***

Usage:
```
python3 mmf.py [--regex] (-mv | -cp) [source_paths_file] destination_folder

positional arguments:
  source_paths_file   Path to the source_paths.txt file or enter paths one by one.
  destination_folder  Path to the destination folder.

options:
  -h, --help          show this help message and exit
  --regex             Use regex to match files in the source directory.
  -mv, --move-files   Move files to the destination folder.
  -cp, --copy-files   Copy files to the destination folder.
```
