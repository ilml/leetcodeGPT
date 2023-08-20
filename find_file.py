import os
import sys

def find_file_by_number(directory, number):
    # List all files in the given directory
    files = os.listdir(directory)
    
    # Filter files that start with the given number followed by '.'
    matching_files = [f for f in files if f.startswith(number+'.')]
    
    # Return the first matching file or None if no matches
    return os.path.abspath(os.path.join(directory, matching_files[0])) if matching_files else None

directory = sys.argv[1]
number = "1"
file_name = find_file_by_number(directory, number)
if file_name:
    print(f"Found: {file_name}")
else:
    print("No matching file found.")
