import os
import shutil
from tkinter import filedialog, simpledialog, Tk
import getpass

# Configuration for dynamic slot handling
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

def ensure_directories_exist(base):
    # List of required directories
    required_dirs = ['Backups', 'Saves', 'TempSaves']

    # Loop through the list of required directories and ensure they exist
    for dir_name in required_dirs:
        # Construct the full path to the directory
        dir_path = os.path.join(base, dir_name)

        # Check if the directory exists
        if not os.path.exists(dir_path):
            # If the directory does not exist, create it
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

def hide_username_in_path(path):
    username = getpass.getuser()
    return path.replace(f"C:\\Users\\{username}", "C:\\Users\\<Username>")

def manage_backup_subdirs(backup_base_dir):
    """Manage and cycle backup subdirectories under the main backup directory."""
    existing_dirs = sorted(
        [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_') and os.path.isdir(os.path.join(backup_base_dir, d))],
        key=lambda x: int(x.split('_')[-1])
    )

    if existing_dirs:
        next_dir_index = int(existing_dirs[-1].split('_')[-1]) + 1
    else:
        next_dir_index = 1

    if next_dir_index <= 10:
        new_dir = os.path.join(backup_base_dir, f"full_backup_{next_dir_index}")
        os.makedirs(new_dir, exist_ok=True)
    else:
        # Rotate the directories when the index goes beyond 10
        shutil.rmtree(os.path.join(backup_base_dir, "full_backup_1"))
        for i in range(2, 11):
            os.rename(
                os.path.join(backup_base_dir, f"full_backup_{i}"),
                os.path.join(backup_base_dir, f"full_backup_{i - 1}")
            )
        new_dir = os.path.join(backup_base_dir, "full_backup_10")
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
    try:
        file_to_restore = f"save_{slot_number - 1}.sav"
        shutil.copy(os.path.join(latest_backup_dir, file_to_restore), base_url)
        return(True)
    except:
        return(False)

def load_save(base_url, slot_number):
    """Select a directory, clear 'TempSaves', and handle files based on whether the directory is a backup directory or not.
    In case of backup directories, only process the save file that matches the current slot."""
    if base_url is None:
        return None

    save_dir = os.path.join(base_url, "Saves")
    temp_save_dir = os.path.join(base_url, "TempSaves")
    backups_dir = os.path.join(base_url, "Backups")

    # Ensure the temporary directory exists and is empty
    if not os.path.exists(temp_save_dir):
        os.makedirs(temp_save_dir)
    else:
        # Clear all existing files in the directory
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
    specific_save_file = f"save_{slot_number - 1}.sav"

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

def create_save(base_url, slot_number):
    if base_url is None:
        return
    root = Tk()
    root.withdraw()
    target_directory = filedialog.askdirectory(initialdir=os.path.join(base_url, "Saves"))
    new_folder_name = simpledialog.askstring("New Folder Name", "Enter the name of the new folder:")
    if new_folder_name is None:
        return(None)
    new_folder_path = os.path.join(target_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    specific_save_file = f"save_{slot_number - 1}.sav"
    shutil.copy(os.path.join(base_url, specific_save_file), os.path.join(new_folder_path, specific_save_file))
    return(new_folder_name)
