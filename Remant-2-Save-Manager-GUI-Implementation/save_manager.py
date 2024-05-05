import os
import sys
import json
import shutil
from tkinter import filedialog, simpledialog, Tk
import getpass

# Configuration for dynamic slot handling
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

def check_config_exists():
    return os.path.exists(config_path)

def create_config():
    normal_list, hardcore_list = [], []
    config_data = {"Normal": normal_list, "Hardcore": hardcore_list}
    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)

def read_config():
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def find_game_directory_base_url():
    username = getpass.getuser()
    base_dir = f"C:\\Users\\{username}\\Saved Games\\Remnant2\\Steam"
    if not os.path.exists(base_dir):
        return None
    first_dir = os.listdir(base_dir)[0] if os.listdir(base_dir) else None
    if first_dir:
        return os.path.join(base_dir, first_dir)
    return None

def hide_username_in_path(path):
    username = getpass.getuser()
    return path.replace(f"C:\\Users\\{username}", "C:\\Users\\<Username>")

def manage_backup_subdirs(backup_base_dir):
    existing_dirs = sorted(
        [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_') and os.path.isdir(os.path.join(backup_base_dir, d))],
        key=lambda x: int(x.split('_')[-1])
    )
    if existing_dirs:
        next_dir_index = int(existing_dirs[-1].split('_')[-1]) + 1
    else:
        next_dir_index = 1
    new_dir = os.path.join(backup_base_dir, f"full_backup_{next_dir_index}")
    os.makedirs(new_dir, exist_ok=True)
    return new_dir

def full_backup_files(base_url):
    if base_url is None:
        return
    backup_base_dir = os.path.join(base_url, 'Backups')
    os.makedirs(backup_base_dir, exist_ok=True)
    current_backup_dir = manage_backup_subdirs(backup_base_dir)
    files_to_backup = [f for f in os.listdir(base_url) if os.path.splitext(f)[1] in ['.bak1', '.bak2', '.bak3', '.sav', '.onl', '.vdf']]
    for file in files_to_backup:
        shutil.copy(os.path.join(base_url, file), os.path.join(current_backup_dir, file))

def restore_from_backup(base_url, slot_number, restore_profile=False):
    if base_url is None:
        return
    backup_base_dir = os.path.join(base_url, "Backups")
    if not os.path.exists(backup_base_dir):
        return
    latest_backup_dir = os.path.join(backup_base_dir, "full_backup_10")
    file_to_restore = f"save_{slot_number - 1}.sav"
    shutil.copy(os.path.join(latest_backup_dir, file_to_restore), base_url)

def create_and_copy_to_new_folder(base_url, slot_number):
    if base_url is None:
        return
    root = Tk()
    root.withdraw()
    target_directory = filedialog.askdirectory(initialdir=os.path.join(base_url, "Saves"))
    new_folder_name = simpledialog.askstring("New Folder Name", "Enter the name of the new folder:")
    new_folder_path = os.path.join(target_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    specific_save_file = f"save_{slot_number - 1}.sav"
    shutil.copy(os.path.join(base_url, specific_save_file), os.path.join(new_folder_path, specific_save_file))
    return(new_folder_name)

if __name__ == "__main__":
    if not check_config_exists():
        create_config()
    base_url = find_game_directory_base_url()
    full_backup_files(base_url)  # Perform a full backup
    restore_from_backup(base_url, 1, True)  # Example slot and profile restoration
    create_and_copy_to_new_folder(base_url, 1)  # Example folder creation and file copying
