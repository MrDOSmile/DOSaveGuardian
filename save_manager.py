import os
import re
import shutil
import hashlib
import json
from tkinter import filedialog, simpledialog, Tk
import getpass

# Configuration for dynamic slot handling
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

def ensure_directories_exist(base):
    required_dirs = ['Backups', 'Saves', 'TempSaves']
    for dir_name in required_dirs:
        dir_path = os.path.join(base, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: {dir_path}")
        else:
            print(f"Directory already exists: {dir_path}")

def find_game_directory_base_url():
    username = getpass.getuser()
    base_dir = f"C:\\Users\\{username}\\Saved Games\\Remnant2\\Steam"
    if not os.path.exists(base_dir):
        return None
    first_dir = os.listdir(base_dir)[0] if os.listdir(base_dir) else None
    if first_dir:
        return os.path.join(base_dir, first_dir)
    return None

def check_number_of_save_slots(base):
    pattern = re.compile(r'save_(\d+)\.sav$')
    save_slots = []
    for filename in os.listdir(base):
        match = pattern.match(filename)
        if match:
            slot_number = int(match.group(1))
            save_slots.append(slot_number)
    return(save_slots)

def hide_username_in_path(path):
    username = getpass.getuser()
    return path.replace(f"C:\\Users\\{username}", "C:\\Users\\USERNAME")

def manage_backup_subdirs(backup_base_dir, num_backups_to_keep):
    existing_dirs = sorted(
        [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_') and os.path.isdir(os.path.join(backup_base_dir, d))],
        key=lambda x: int(x.split('_')[-1])
    )
    if existing_dirs:
        next_dir_index = int(existing_dirs[-1].split('_')[-1]) + 1
    else:
        next_dir_index = 1
    if next_dir_index <= num_backups_to_keep:
        new_dir = os.path.join(backup_base_dir, f"full_backup_{next_dir_index}")
        os.makedirs(new_dir, exist_ok=True)
    else:
        # Rotate the directories when the index goes beyond the set limit
        oldest_backup_dir = os.path.join(backup_base_dir, "full_backup_1")
        shutil.rmtree(oldest_backup_dir)
        for i in range(2, num_backups_to_keep + 1):
            old_dir = os.path.join(backup_base_dir, f"full_backup_{i}")
            new_dir_name = f"full_backup_{i - 1}"
            new_dir = os.path.join(backup_base_dir, new_dir_name)
            os.rename(old_dir, new_dir)
        new_dir = os.path.join(backup_base_dir, f"full_backup_{num_backups_to_keep}")
        os.makedirs(new_dir, exist_ok=True)
    return new_dir

def calculate_checksum(file_path):
    """Calculate SHA-256 checksum of the given file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def full_backup_files(base_url, num_backups_to_keep):
    if base_url is None:
        return
    backup_base_dir = os.path.join(base_url, 'Backups')
    os.makedirs(backup_base_dir, exist_ok=True)
    current_backup_dir = manage_backup_subdirs(backup_base_dir, num_backups_to_keep)
    files_to_backup = [f for f in os.listdir(base_url) if os.path.splitext(f)[1] in ['.bak1', '.bak2', '.bak3', '.sav', '.onl', '.vdf']]
    checksum_dict = {}
    for file in files_to_backup:
        src_file = os.path.join(base_url, file)
        dest_file = os.path.join(current_backup_dir, file)
        shutil.copy(src_file, dest_file)
        # Calculate checksum
        checksum = calculate_checksum(dest_file)
        checksum_dict[file] = checksum
    # Save checksums to a file in the backup directory
    checksum_file = os.path.join(current_backup_dir, 'checksums.json')
    with open(checksum_file, 'w') as f:
        json.dump(checksum_dict, f)

def restore_world_from_backup(base_url, slot_number):
    if base_url is None:
        return False
    backup_base_dir = os.path.join(base_url, "Backups")
    if not os.path.exists(backup_base_dir):
        return False
    # Find the latest backup directory
    try:
        backup_dirs = [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_')]
        if not backup_dirs:
            return False
        latest_backup_dir = max(backup_dirs, key=lambda x: int(x.split('_')[-1]))
        latest_backup_path = os.path.join(backup_base_dir, latest_backup_dir)
    except Exception as e:
        print(f"Error finding the latest backup directory: {e}")
        return False
    # Load checksums
    checksum_file = os.path.join(latest_backup_path, 'checksums.json')
    try:
        with open(checksum_file, 'r') as f:
            checksum_dict = json.load(f)
    except Exception as e:
        print(f"Error loading checksum file: {e}")
        return False
    try:
        file_to_restore = f"save_{slot_number}.sav"
        src_file = os.path.join(latest_backup_path, file_to_restore)
        dest_file = os.path.join(base_url, file_to_restore)
        shutil.copy(src_file, dest_file)
        # Verify checksum
        restored_checksum = calculate_checksum(dest_file)
        expected_checksum = checksum_dict.get(file_to_restore)
        if restored_checksum != expected_checksum:
            print(f"Checksum mismatch for {file_to_restore}")
            return False
        return True
    except Exception as e:
        print(f"Error restoring file: {e}")
        return False

def restore_profile_from_backup(base_url):
    if base_url is None:
        return False
    backup_base_dir = os.path.join(base_url, "Backups")
    if not os.path.exists(backup_base_dir):
        return False
    # Find the latest backup directory
    try:
        backup_dirs = [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_')]
        if not backup_dirs:
            return False
        latest_backup_dir = max(backup_dirs, key=lambda x: int(x.split('_')[-1]))
        latest_backup_path = os.path.join(backup_base_dir, latest_backup_dir)
    except Exception as e:
        print(f"Error finding the latest backup directory: {e}")
        return False
    # Load checksums
    checksum_file = os.path.join(latest_backup_path, 'checksums.json')
    try:
        with open(checksum_file, 'r') as f:
            checksum_dict = json.load(f)
    except Exception as e:
        print(f"Error loading checksum file: {e}")
        return False
    try:
        file_to_restore = f"profile.sav"
        src_file = os.path.join(latest_backup_path, file_to_restore)
        dest_file = os.path.join(base_url, file_to_restore)
        shutil.copy(src_file, dest_file)
        # Verify checksum
        restored_checksum = calculate_checksum(dest_file)
        expected_checksum = checksum_dict.get(file_to_restore)
        if restored_checksum != expected_checksum:
            print(f"Checksum mismatch for {file_to_restore}")
            return False
        return True
    except Exception as e:
        print(f"Error restoring file: {e}")
        return False

def restore_profile_and_world(base_url, slots):
    prestored = restore_profile_from_backup(base_url)
    wrestored = restore_world_from_backup(base_url, slots)
    restored = prestored and wrestored
    return(restored)

def load_save(base_url, slot_number):
    if base_url is None:
        return None
    save_dir = os.path.join(base_url, "Saves")
    temp_save_dir = os.path.join(base_url, "TempSaves")
    backups_dir = os.path.join(base_url, "Backups")
    # Ensure the temporary directory exists and is empty
    if not os.path.exists(temp_save_dir):
        os.makedirs(temp_save_dir)
    else:
        for file in os.listdir(temp_save_dir):
            file_path = os.path.join(temp_save_dir, file)
            os.remove(file_path)
    root = Tk()
    root.withdraw()
    chosen_dir = filedialog.askdirectory(initialdir=save_dir, title="Select the directory containing the save files")
    if not chosen_dir:
        print("No directory was selected.")
        return None
    # Check if the chosen directory is within the Backups directory or its subdirectories
    is_backup_dir = os.path.abspath(chosen_dir).startswith(os.path.abspath(backups_dir))
    # Determine the correct filename to process
    specific_save_file = f"save_{slot_number}.sav"
    if is_backup_dir:
        # If the chosen directory is a backup directory, only handle the specific save file
        file_path = os.path.join(chosen_dir, specific_save_file)
        if os.path.exists(file_path):
            dest_path = os.path.join(temp_save_dir, specific_save_file)
            shutil.copy(file_path, dest_path)
            print(f"Backup file '{specific_save_file}' has been processed and prepared in temporary storage.")
        else:
            print(f"The specific backup file '{specific_save_file}' does not exist in the selected backup directory.")
            return None
    else:
        # Process all .sav files in the chosen directory
        files_to_copy = [f for f in os.listdir(chosen_dir) if f.endswith('.sav')]
        for file_name in files_to_copy:
            src_path = os.path.join(chosen_dir, file_name)
            new_file_name = specific_save_file if file_name.startswith("save_") and file_name.endswith(".sav") else file_name
            dest_path = os.path.join(temp_save_dir, new_file_name)
            shutil.copy(src_path, dest_path)
            print(f"File '{file_name}' has been copied and renamed to '{new_file_name}' in temporary storage.")
    # Copy the relevant save file back to the base_url
    temp_file_path = os.path.join(temp_save_dir, specific_save_file)
    if os.path.exists(temp_file_path):
        final_dest_path = os.path.join(base_url, specific_save_file)
        shutil.copy(temp_file_path, final_dest_path)
        print(f"File '{specific_save_file}' has been copied back to the game base directory.")
    return temp_save_dir

def create_save(save_name, slot_number):
    base_url = find_game_directory_base_url()
    if base_url is None:
        return
    root = Tk()
    root.withdraw()
    target_directory = filedialog.askdirectory(initialdir=os.path.join(base_url, "Saves"))
    if not target_directory:
        return(False)
    new_folder_path = os.path.join(target_directory, save_name)
    os.makedirs(new_folder_path, exist_ok=True)
    specific_save_file = f"save_{slot_number}.sav"
    shutil.copy(os.path.join(base_url, specific_save_file), os.path.join(new_folder_path, specific_save_file))
    return(True)
