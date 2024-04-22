import os
import shutil
from utils import hide_username_in_path
from utils import find_game_directory_base_url

def full_backup_files(base_url):
    if base_url is None:
        return

    # Identify the primary backup directory
    backup_dirs = [d for d in os.listdir(base_url) if "backup" in d.lower()]
    if not backup_dirs:
        print("No backup directories found to store the files. Creating a new backup directory.")
        backup_base_dir = os.path.join(base_url, 'Backups')
        os.makedirs(backup_base_dir, exist_ok=True)
        print(f"Created a new backup directory at: {hide_username_in_path(backup_base_dir)}")
    else:
        backup_base_dir = os.path.join(base_url, backup_dirs[0])

    # Manage backup subdirectories
    current_backup_dir = manage_backup_subdirs(backup_base_dir)

    # Perform the backup
    extensions = ['.bak1', '.bak2', '.bak3', '.sav', '.onl', '.vdf']
    files_to_backup = [f for f in os.listdir(base_url) if os.path.splitext(f)[1] in extensions]
    if not files_to_backup:
        print("No files found to backup.")
        return

    for file in files_to_backup:
        src_path = os.path.join(base_url, file)
        dest_path = os.path.join(current_backup_dir, file)
        shutil.copy(src_path, dest_path)
        hidden_path = hide_username_in_path(src_path)
        hidden_dest = hide_username_in_path(dest_path)
        print(f"Performed full backup of '{file}' from '{hidden_path}' to '{hidden_dest}'")

def manage_backup_subdirs(backup_base_dir):
    # Find existing backup directories and sort them
    existing_dirs = sorted(
        [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_') and os.path.isdir(os.path.join(backup_base_dir, d))],
        key=lambda x: int(x.split('_')[-1])
    )

    if existing_dirs:
        next_dir_index = int(existing_dirs[-1].split('_')[-1]) + 1
    else:
        next_dir_index = 1

    if next_dir_index <= 10:
        # Create the next directory in sequence
        new_dir = os.path.join(backup_base_dir, f"full_backup_{next_dir_index}")
        os.makedirs(new_dir, exist_ok=True)
        return new_dir
    else:
        # Rotate the directories when the index goes beyond 10
        # Delete the oldest directory and shift all others down
        shutil.rmtree(os.path.join(backup_base_dir, "full_backup_1"))
        for i in range(2, 11):
            os.rename(
                os.path.join(backup_base_dir, f"full_backup_{i}"),
                os.path.join(backup_base_dir, f"full_backup_{i - 1}")
            )
        # Create a new directory 'full_backup_10'
        new_dir = os.path.join(backup_base_dir, "full_backup_10")
        os.makedirs(new_dir, exist_ok=True)
        return new_dir

def restore_from_backup(base_url, profile=False):
    if base_url is None:
        print("Base directory not provided.")
        return

    # Identify all folders containing the word 'backup' in their names
    backup_folders = [os.path.join(base_url, d) for d in os.listdir(base_url) if "backup" in d.lower() and os.path.isdir(os.path.join(base_url, d))]
    if not backup_folders:
        print("No backup directories found.")
        return

    # From those folders, find the latest 'full_backup_<n>' directory
    latest_backup_dir = None
    highest_num = -1
    for folder in backup_folders:
        sub_dirs = [d for d in os.listdir(folder) if d.startswith("full_backup_") and d[12:].isdigit()]
        for sub_dir in sub_dirs:
            num = int(sub_dir[12:])  # Extract the number part from 'full_backup_<n>'
            if num > highest_num:
                highest_num = num
                latest_backup_dir = os.path.join(folder, sub_dir)

    if not latest_backup_dir:
        print("No 'full_backup_<n>' directories found in any backup folder.")
        return

    # Determine which files to restore
    if profile:
        file_criteria = lambda f: save_mode in f or "profile" in f.lower()
    else:
        file_criteria = lambda f: save_mode in f

    backup_files = [f for f in os.listdir(latest_backup_dir) if file_criteria(f)]
    for file in backup_files:
        src_path = os.path.join(latest_backup_dir, file)
        dest_path = os.path.join(base_url, file)
        shutil.copy(src_path, dest_path)
        hidden_base = hide_username_in_path(base_url)
        hidden_target = hide_username_in_path(latest_backup_dir)
        print(f"Restored '{file}' from '{hidden_target}' to '{hidden_base}'")