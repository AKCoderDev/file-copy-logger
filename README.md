# file-copy-logger

File Copy Script with Long Path Support
This script is designed to recursively copy files and folders from a source directory to a target directory with the following features:

Support for NTFS long paths (over 260 characters)
Detailed log file for the copy process
Visual progress bar using tqdm
Handles unexpected interruptions (e.g., Ctrl+C)
Displays a summary of the copy process (number of files, size, errors, etc.)

Requirements
tqdm library



How It Works
Recursively scans the source_dir for all files and folders.

For each file:
Creates necessary folders in the destination.
Copies the file in 1MB chunks.
Logs progress every 5% or every 30 seconds.
Logs each operation and error.
On completion (or interruption), prints and saves a detailed summary.

How to Use
Set the source and target paths in the script:

source_dir = r'C:\PATH\TO\SOURCE'
target_dir = r'D:\PATH\TO\DESTINATION'
Run the script.


After completion, a log file like this will appear in the destination folder:


log_kopiowania_2025-04-15_12-32-10.txt
Log File Example

Started copying on: 2025-04-15 12:32:10
Copying: C:\source\file1.txt
File size: 5.23 MB
Copy progress file1.txt: 55.00% (3145728/5720000 bytes)
SUCCESS: C:\source\file1.txt -> D:\target\file1.txt
...
=== COPY SUMMARY ===
- Files found: 183
- Files copied: 183
- Source data size: 4.72 GB
- Copied data size: 4.72 GB
- Folders created: 32
- Errors during copy: 0

Benefits
Supports very long paths using \\?\ syntax.

Logs every file, including size and progress.

Robust to interruptions — will still generate a summary.
