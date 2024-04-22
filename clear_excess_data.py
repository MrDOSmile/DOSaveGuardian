import os
from main import find_game_directory_base_url

def delete_backup_files(directory, extensions):
    """ Delete files with specified extensions in subdirectories, ignoring any that contain 'backup'. """
    for root, dirs, files in os.walk(directory):
        # Modify the dirs list in-place to exclude directories containing 'backup'
        dirs[:] = [d for d in dirs if 'backup' not in d.lower()]

        if root == directory:  # Skip the root directory
            continue

        for file in files:
            if file.endswith(tuple(extensions)):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

delete_backup_files(find_game_directory_base_url(), ['.bak1', '.bak2', '.bak3'])