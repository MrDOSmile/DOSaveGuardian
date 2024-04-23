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
    """Check if the config.json file exists in the script directory."""
    return os.path.exists(config_path)

def create_config():
    """Create or update the config.json file to define Normal and Hardcore slots dynamically."""
    while True:
        os.system("cls")
        normal_input = input(f"Enter the save slot numbers for {color('Normal', "green")} separated by commas (e.g., 1, 2, 3): ")
        normal_list = [int(n.strip()) for n in normal_input.split(',') if n.strip().isdigit()]

        hardcore_input = input(f"Enter the save slot numbers for {color('Hardcore', "red")} separated by commas (e.g., 4, 5): ")
        hardcore_list = [int(n.strip()) for n in hardcore_input.split(',') if n.strip().isdigit()]

        if set(normal_list) & set(hardcore_list):
            print(f"Duplicate slots found between {color('Normal', "green")} and {color('Hardcore', "red")}. Please start over.")
            continue

        config_data = {
            "Normal": normal_list,
            "Hardcore": hardcore_list
        }

        with open(config_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        print("Config file created or updated.")
        break

def read_config():
    """Read configuration data from config.json."""
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def select_save_slot():
    """Prompt user to select a save slot from configured options."""
    while True:
        config_data = read_config()
        print(f"\n{color("Select a save slot:", "purple")}")
        all_slots = {**dict.fromkeys(config_data['Normal'], 'Normal'), **dict.fromkeys(config_data['Hardcore'], 'Hardcore')}
        for slot, mode in sorted(all_slots.items()):
            if mode == "Normal":
                print(f"{slot}: {color(mode, "green")}")
            else:
                print(f"{slot}: {color(mode, "red")}")
        slot_choice = input(f"Enter slot number or type {color("'config'", "purple")} to update slot configuration: ")
        if slot_choice.lower() == 'config':
            create_config()
            continue
        try:
            slot_choice = int(slot_choice)
            if slot_choice in all_slots:
                return slot_choice, all_slots[slot_choice]
            else:
                print("Invalid slot number. Please try again.")
        except ValueError:
            print("Please enter a valid number or 'config'.")

def find_game_directory_base_url():
    """Find the base directory for game saves based on the username."""
    username = getpass.getuser()
    base_dir = f"C:\\Users\\{username}\\Saved Games\\Remnant2\\Steam"
    if not os.path.exists(base_dir):
        print("Base directory not found. Please check proper game installation.")
        return None

    first_dir = os.listdir(base_dir)[0] if os.listdir(base_dir) else None
    if first_dir:
        return os.path.join(base_dir, first_dir)
    else:
        print("No subdirectories found under base directory.")
        return None

def hide_username_in_path(path):
    """Utility function to hide the username in a file path."""
    username = getpass.getuser()
    path = path.replace("/", "\\")
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

    # Identify the primary backup directory
    backup_dirs = [d for d in os.listdir(base_url) if "backup" in d.lower()]
    if not backup_dirs:
        print("No backup directories found to store the files. Creating a new backup directory.")
        backup_base_dir = os.path.join(base_url, 'Backups')
        os.makedirs(backup_base_dir, exist_ok=True)
        print(f"Created a new backup directory at: {hide_username_in_path(backup_base_dir)}")
    else:
        backup_base_dir = os.path.join(base_url, backup_dirs[0])

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

def find_latest_backup_dir(backup_base_dir):
    """Find the latest backup directory based on naming convention 'full_backup_<index>'."""
    backup_dirs = [d for d in os.listdir(backup_base_dir) if d.startswith('full_backup_')]
    if not backup_dirs:
        return None  # No backup directories found
    # Sort directories by the index and select the latest
    latest_backup_dir = sorted(backup_dirs, key=lambda x: int(x.split('_')[-1]), reverse=True)[0]
    return os.path.join(backup_base_dir, latest_backup_dir)

def restore_from_backup(base_url, slot_number, restore_profile=False):
    """Restore a backup for a specified slot number, optionally including profile data."""
    if base_url is None:
        print("Base directory not provided.")
        return

    backup_base_dir = os.path.join(base_url, "Backups")
    if not os.path.exists(backup_base_dir):
        print("No backup directory found.")
        return

    latest_backup_dir = find_latest_backup_dir(backup_base_dir)
    if latest_backup_dir is None:
        print("No backup directories found.")
        return

    file_to_restore = f"save_{slot_number - 1}.sav"
    additional_files = ['profile.sav'] if restore_profile else []

    backup_files = [f for f in os.listdir(latest_backup_dir) if f in [file_to_restore] + additional_files]
    if not backup_files:
        print(f"No backup found for slot {slot_number} in the latest backup.")
        return

    for file in backup_files:
        src_path = os.path.join(latest_backup_dir, file)
        shutil.copy(src_path, base_url)
        print(f"Restored '{file}' from backup in '{hide_username_in_path(latest_backup_dir)}'.")


def create_and_copy_to_new_folder(base_url, slot_number):
    """Create a new folder in a selected directory and copy specific save data and profile data from base_url."""
    if base_url is None:
        return

    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Let the user choose the directory where the new folder will be created
    target_directory = filedialog.askdirectory(initialdir=os.path.join(base_url, "Saves"), title="Select the target directory for the new folder")
    if not target_directory:
        print("No target directory selected")
        return

    # Prompt for the new folder name within the chosen directory
    new_folder_name = simpledialog.askstring("New Folder Name", "Enter the name of the new folder:", parent=root)
    if not new_folder_name:
        print("No folder name was provided")
        return

    new_folder_path = os.path.join(target_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    print(f"New folder created at: {hide_username_in_path(new_folder_path)}")

    specific_save_file = f"save_{slot_number - 1}.sav"
    profile_file = "profile.sav"
    extensions = ['.bak1', '.bak2', '.bak3', '.sav', '.onl', '.vdf']

    files_to_copy = [f for f in os.listdir(base_url) if os.path.splitext(f)[1] in extensions and (f == specific_save_file or f == profile_file)]
    for file in files_to_copy:
        src_path = os.path.join(base_url, file)
        dest_path = os.path.join(new_folder_path, file)
        shutil.copy(src_path, dest_path)
        print(f"Copied '{file}' from '{hide_username_in_path(src_path)}' to '{hide_username_in_path(dest_path)}'.")

def choose_save_directory(base_url, slot_number):
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

def color(text, color_name):
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'purple': '\033[35m',
        'cyan': '\033[36m',
        'lightgray': '\033[37m',
        'darkgray': '\033[90m',
        'lightred': '\033[91m',
        'lightgreen': '\033[92m',
        'lightyellow': '\033[93m',
        'lightblue': '\033[94m',
        'lightpurple': '\033[95m',
        'lightcyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m',
    }
    return f"{colors.get(color_name, colors['end'])}{text}{colors['end']}"



# Import statements and all other function definitions remain as previously defined

def menu():
    base_url = find_game_directory_base_url()
    if not base_url:
        print("Failed to find the game directory. Please ensure the game is properly installed.")
        return
    else:
        full_backup_files(base_url)  # Perform a full backup after ensuring the Saves directory exists

    while True:
        slot_number, mode = select_save_slot()
        save_dir = os.path.join(base_url, "Saves")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            print(f"'Saves' directory created at: {hide_username_in_path(save_dir)}")

        while True:
            if mode == "Normal":
                print(f"\n{color(mode, "green")} {color("Main Menu", "purple")}:")
            else:
                print(f"\n{color(mode, "red")} {color("Main Menu", "purple")}:")
            print(f"1. {color("Full Backup", "cyan")}")
            print(f"2. {color("Restore Backup", "blue")}")
            print(f"3. {color("Load Save", "lightblue")}")
            print(f"4. {color("Create New Save", "green")}")
            print(f"5. {color("Help", "yellow")}")
            print(f"6. {color("Change Slot", 'purple')}")
            print(f"7. {color("Quit", "red")}")

            choice = input("Enter your choice: ")
            os.system("cls")

            if choice == "1":
                full_backup_files(base_url)
            elif choice == "2":
                if mode == "Hardcore":
                    restore_profile = input(f"This is meant for {color("Hardcore", "red")}.\nIf your character died, you must restore profile and restart your game.\nRestore profile data as well? ({color("yes", "green")}/{color("no", "red")}): ").lower() == 'yes'
                else:
                    restore_profile = False
                restore_from_backup(base_url, slot_number, restore_profile)
            elif choice == "3":
                choose_save_directory(base_url, slot_number)
            elif choice == "4":
                create_and_copy_to_new_folder(base_url, slot_number)  # Pass slot_number here
            elif choice == "5":
                print("Help information...")
            elif choice == "6":
                break  # Exit the inner loop to re-select a save slot
            elif choice == "7":
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number from the menu.")

if __name__ == "__main__":
    if not check_config_exists():
        create_config()
    try:
        os.system("cls")
        menu()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
