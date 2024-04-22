import os
import shutil
import getpass
from main import hide_username_in_path

def create_dir_if_not_exists(path):
    """Ensure directory exists, if not, create it."""
    if not os.path.exists(path):
        os.makedirs(path)
        path = hide_username_in_path(path)
        print(f"Created directory: {path}")

def copy_file(src, dest):
    """Copy file from source to destination, ensuring directory structure."""
    create_dir_if_not_exists(os.path.dirname(dest))
    shutil.copy(src, dest)
    src = hide_username_in_path(src)
    dest = hide_username_in_path(dest)
    print(f"Copied file from {src} to {dest}")

def find_game_directory_base_url():
    """Locate the base directory for game saves."""
    username = getpass.getuser()
    base_dir = f"C:\\Users\\{username}\\Saved Games\\Remnant2\\Steam"
    hidden_base = hide_username_in_path(base_dir)
    print(f"Looking for game directory at {hidden_base}")

    if not os.path.exists(base_dir):
        print("Base directory not found. Please check proper game installation.")
        return None

    first_dir = os.listdir(base_dir)[0] if os.listdir(base_dir) else None
    if first_dir:
        hidden_first = hide_username_in_path(first_dir)
        print(f"Using subdirectory {hidden_first} under base directory.")
        return os.path.join(base_dir, first_dir)
    else:
        print("No subdirectories found under base directory.")
        return None

def process_directory(root_dir):
    """Process directories to find and copy specific files to corresponding slots."""
    slots = [os.path.join(root_dir, f'Slot {i+1}') for i in range(5)]

    for slot in slots:
        create_dir_if_not_exists(slot)

    exclude_dirs = {'Slot 1', 'Slot 2', 'Slot 3', 'Slot 4', 'Slot 5'}

    for subdir, dirs, files in os.walk(root_dir, topdown=True):
        dirs[:] = [d for d in dirs if 'backup' not in d.lower() and d not in exclude_dirs]
        if subdir == root_dir:
            continue

        for file in files:
            if any(f"save_{i}" in file or "profile" in file for i in range(5)):
                hidden_sub = hide_username_in_path(subdir)
                print(f"Found file {file} in {hidden_sub}")

        for file in files:
            full_file_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(subdir, start=root_dir)
            for i in range(5):
                if f"save_{i}" in file or "profile" in file:
                    slot_path = os.path.join(slots[i], relative_path, file)
                    copy_file(full_file_path, slot_path)

def main():
    print("Starting the game save management script...")
    root_directory = find_game_directory_base_url()
    if root_directory:
        try:
            process_directory(root_directory)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No valid game directory found.")

if __name__ == "__main__":
    main()
