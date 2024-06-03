import os

def list_files(start_path):
    result = {}
    for root, dirs, files in os.walk(start_path):
        current_dir = result
        folders = root.split(os.sep)[1:]
        for folder in folders:
            if folder not in current_dir:
                current_dir[folder] = {}
            current_dir = current_dir[folder]
        for file in files:
            current_dir[file] = None
    return result

# Example usage:
directory_structure = list_files('static/resources')
print(directory_structure)