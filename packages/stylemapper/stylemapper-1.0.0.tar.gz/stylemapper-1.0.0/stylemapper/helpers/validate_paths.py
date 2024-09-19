from pathlib import Path
import os
import sys


def main():
    pass


def is_css_file(file_path: str):
    if not os.path.exists(file_path):
        return False
    
    try:
        if not str(file_path).endswith(".css"):
            return False
    except TypeError:
        return False
    
    return True


def is_html_file(file_path):
    # First, check file ends in correct extension
    try:
        if not str(file_path).endswith(".html"):
            return False
    except TypeError:
        return False

    # Second, check file exists
    if not os.path.exists(file_path):
        return False

    return True


# Checks folder path to see if it contains at least 1 html file
def retrieve_html_paths(folder_path, max_dives=3, current_dive=0):
    path = Path(folder_path)
    html_files = []

    if current_dive > max_dives:
        return html_files
    
    # Iterate through the contents of the directory
    try:
        for file_path in path.iterdir():
            if is_html_file(file_path): # If it's an HTML file, append its path to the list
                html_files.append(file_path)
            elif file_path.is_dir(): # If it's a directory, recurse into it
                html_files.extend(retrieve_html_paths(file_path, max_dives, current_dive + 1))
    except FileNotFoundError:
        sys.exit(f"'{folder_path}' is not a valid folder. Please try again")

    print(html_files)
        

    # Convert all 'path' objects into strings.
    html_files = list(map(str, html_files))
    return html_files


def clean_filepath_name(exact_path: str) -> str:
    return Path(exact_path).name


if __name__ == "__main___":
    main()