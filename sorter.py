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
    """Process directories to find and copy specific files, copying only if save files are present."""
    target_dir_normal = os.path.join(root_dir, 'Normal')
    target_dir_hardcore = os.path.join(root_dir, 'Hardcore')

    print("Processing directories...")
    create_dir_if_not_exists(target_dir_normal)
    create_dir_if_not_exists(target_dir_hardcore)

    exclude_dirs = {'Normal', 'Hardcore'}

    for subdir, dirs, files in os.walk(root_dir, topdown=True):
        dirs[:] = [d for d in dirs if 'backup' not in d.lower() and d not in exclude_dirs]
        if subdir == root_dir:
            continue

        for file in files:
            if "save_0" in file or "save_1" in file or "profile" in file:
                hidden_sub = hide_username_in_path(subdir)
                print(f"Found file {file} in {hidden_sub}")

        for file in files:
            full_file_path = os.path.join(subdir, file)
            relative_path = os.path.relpath(subdir, start=root_dir)

            if "save_0" in file:
                normal_path = os.path.join(target_dir_normal, relative_path, file)
                copy_file(full_file_path, normal_path)
            if "save_1" in file:
                hardcore_path = os.path.join(target_dir_hardcore, relative_path, file)
                copy_file(full_file_path, hardcore_path)
            if "profile" in file:
                normal_path = os.path.join(target_dir_normal, relative_path, file)
                hardcore_path = os.path.join(target_dir_hardcore, relative_path, file)
                copy_file(full_file_path, normal_path)
                copy_file(full_file_path, hardcore_path)

def sync_files(src_dir, target_dir, src_suffix, target_suffix):
    """Sync files from source directory to target directory with specific conditions."""
    hidden_src = hide_username_in_path(src_dir)
    hidden_target = hide_username_in_path(target_dir)
    print(f"Syncing files from {hidden_src} to {hidden_target}...")

    for subdir, dirs, files in os.walk(src_dir):
        for file in files:
            if src_suffix in file or 'profile' in file:
                new_file_name = file.replace(src_suffix, target_suffix) if src_suffix in file else file
                target_subdir = subdir.replace(src_dir, target_dir)
                target_file_path = os.path.join(target_subdir, new_file_name)

                if not os.path.exists(target_file_path):
                    os.makedirs(target_subdir, exist_ok=True)
                    shutil.copy(os.path.join(subdir, file), target_file_path)
                    hidden_target = hide_username_in_path(target_file_path)
                    print(f"Copied {file} to {hidden_target}")

def main():
    print("Starting the game save management script...")
    root_directory = find_game_directory_base_url()
    if root_directory:
        try:
            process_directory(root_directory)
            normal_dir = os.path.join(root_directory, 'Normal')
            hardcore_dir = os.path.join(root_directory, 'Hardcore')
            sync_files(normal_dir, hardcore_dir, 'save_0', 'save_1')
            sync_files(hardcore_dir, normal_dir, 'save_1', 'save_0')
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("No valid game directory found.")

if __name__ == "__main__":
    main()
