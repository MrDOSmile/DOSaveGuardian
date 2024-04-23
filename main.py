import os
import sys
import getpass
import shutil
from tkinter import filedialog, simpledialog, Tk
import sorter

save_mode = "save_0"  # Default save mode

def find_game_directory_base_url():
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
    username = getpass.getuser()
    path = path.replace("/", "\\")
    return(path.replace(f"C:\\Users\\{username}", "C:\\Users\\<Username>"))

# def mode_backup_files(base_url):
    # if base_url is None:
    #     return

    # global save_mode
    # extensions = ['.bak1', '.bak2', '.bak3', '.sav', '.onl', '.vdf']
    # # Include any file that has the mode string or "profile" in its name
    # files_to_backup = [f for f in os.listdir(base_url) if (os.path.splitext(f)[1] in extensions and save_mode in f) or "profile" in f.lower()]

    # if not files_to_backup:
    #     print("No files found to backup.")
    #     return

    # backup_folders = [d for d in os.listdir(base_url) if "backup" in d.lower()]
    # if not backup_folders:
    #     print("No backup directories found to store the files.")
    #     return

    # target_backup_folder = os.path.join(base_url, backup_folders[0])
    # for file in files_to_backup:
    #     src_path = os.path.join(base_url, file)
    #     dest_path = os.path.join(target_backup_folder, file)
    #     shutil.copy(src_path, dest_path)
    #     hidden_base = hide_username_in_path(base_url)
    #     hidden_target = hide_username_in_path(target_backup_folder)
    #     print(f"Copied '{file}' from '{hidden_base}' to '{hidden_target}'")

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

def choose_save_directory(base_url):
    if base_url is None:
        return None

    global save_mode
    root = Tk()
    root.withdraw()
    if save_mode == "save_0":
        initialdir = os.path.join(base_url,"Normal")
    elif save_mode == "save_1":
        initialdir = os.path.join(base_url, "Hardcore")
    folder_selected = filedialog.askdirectory(initialdir=initialdir)

    if folder_selected:
        save_files = [f for f in os.listdir(folder_selected) if save_mode in f]
        for file in save_files:
            src_path = os.path.join(folder_selected, file)
            dest_path = os.path.join(base_url, file)
            shutil.copy(src_path, dest_path)
            hidden_base = hide_username_in_path(base_url)
            hidden_target = hide_username_in_path(folder_selected)
            print(f"Copying '{file}' from '{hidden_target}' to '{hidden_base}'")
        print(f"Files containing '{save_mode}' have been copied to {hidden_base}")
        return folder_selected
    else:
        print("No directory was selected")
        return None

def create_and_copy_to_new_folder(base_url):
    if base_url is None:
        return

    global save_mode
    root = Tk()
    root.withdraw()
    if save_mode == "save_0":
        initialdir = os.path.join(base_url,"Normal")
    elif save_mode == "save_1":
        initialdir = os.path.join(base_url, "Hardcore")
    target_directory = filedialog.askdirectory(initialdir=initialdir, title="Select target directory for new folder")
    if not target_directory:
        print("No directory was selected")
        return

    new_folder_name = simpledialog.askstring("New Folder Name", "Enter the name of the new folder:", parent=root)
    if not new_folder_name:
        print("No folder name was provided")
        return

    new_folder_path = os.path.join(target_directory, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)
    hidden_target = hide_username_in_path(new_folder_path)
    print(f"New folder created at: {hidden_target}")

    extensions = ['.sav', '.onl', '.vdf']
    files_to_copy = [f for f in os.listdir(base_url) if os.path.splitext(f)[1] in extensions and save_mode in f or "profile" in f.lower()]
    for file in files_to_copy:
        src_path = os.path.join(base_url, file)
        dest_path = os.path.join(new_folder_path, file)
        shutil.copy(src_path, dest_path)
        hidden_base = hide_username_in_path(base_url)
        hidden_target = hide_username_in_path(new_folder_path)
        print(f"Copied '{file}' from '{hidden_base}' to '{hidden_target}'")

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

def show_main_help(current_mode):
    print("\n\033[35mHelp Menu:\033[0m")
    print("\033[32m0. Full Backup (All Files)\033[0m - Makes a full backup of Normal and Hardcore Saves to your 'Backup' folder.")
    if current_mode == "Hardcore":
        print("\033[34m1. Restore Backup World \033[35mAND PROFILE\033[0m\n   - This will load your last backup. If this doesn't work for you, select \033[34m'Load Save'\033[0m option!\n   \033[31m- MUST RESTART GAME IF YOU DIED!\033[0m")
    else:
        print("\033[34m1. Restore Backup\033[0m - Use this if you need to recover your game from your backup.\n   - This will load your last backup. If this doesn't work for you, select \033[34m'Load Save'\033[0m option!")
    print("\033[34m2. Load Save\033[0m - Choose a save file to load into the game.")
    print("\033[32m4. Create New Save\033[0m - Make a new folder anywhere on your computer and save copies of your game files there.")
    print("\033[33m5. Change Mode\033[0m - Changes the save types between Normal or Hardcore saves.")
    print("\033[33m6. This very help menu\033[0m - Displays explanations and guidance on what each menu option does.")
    print("\033[31m7. Quit\033[0m - Closes this program. Use this when you're done managing your game saves.\n")

def show_mode_help():
    print("\n\033[35mSelect Game Mode:\033[0m")
    print("\033[32m1. Normal Mode\033[0m - This mode is meant for the 'Normal' game session i.e. NON-Hardcore.")
    print("\033[31m2. Hardcore Mode\033[0m - This mode is meant for the 'Hardcore' game session.")
    print("\033[96m3. Sync and convert saves from modes\033[0m - This will automatically create and sync any saves you have\n   from Normal into Hardcore saves, and vice-versa.")

def introduction():
    os.system("cls")
    print("""
    \033[35mWelcome to the \033[32mDOSmile's\033[35m Remnant 2 Save Manager!\033[0m
    \033[96m-------------------------------------------------------------------------------\033[0m

    This utility helps you manage your game saves for 'Remnant2' stored under your Steam user profile.\n    Here are some key points about this program:

    - \033[34mBase Directory:\033[0m All operations are performed within your 'Saved Games' directory in your user profile, \n      ensuring your original game data remains secure and manageable.\n      - This is found under \033[35mC:\\Users\\<USERNAME>\\Saved Games\\Remnant2\\Steam\\<NUMBERS>\033[0m

    - \033[96mSave Modes:\033[0m The program operates in two main modes:
        1. \033[32mNormal Mode\033[0m - Intended for managing \033[32mNormal\033[0m game saves.
        2. \033[31mHardcore Mode\033[0m - Intended for managing \033[31mHardcore\033[0m game saves.
          (This is running the assumption that your \033[32m\033[32mfirst slot\033[0m is a \033[32mNormal\033[0m Save, and your \033[31msecond\033[0m is \033[31mHardcore\033[0m)

    - \033[33mBackup and Restore:\033[0m You can backup your saves into a dedicated 'Backup' folder and restore them when necessary.\n      - This ensures you can recover your game state after any unwanted changes or data loss.

    - \033[35mCustomization and Flexibility:\033[0m You can create new save folders, move saves between \033[32mNormal\033[0m\n      and \033[31mHardcore\033[0m modes, and ensure your game data is kept up-to-date across different playing styles.

    --------------
    Please choose an option from the main menu to start managing your game saves.\n    Remember to switch between \033[32mNormal\033[0m and \033[31mHardcore\033[0m modes based on your current game session requirements.""")

    input("    \033[96m-------------------------------------------------------------------------------\033[0m\n\033[31m    USE AT YOUR OWN RISK!\033[0m\n    Pressing enter will automatically create a full backup of you saves!\n    Please press enter if you have read and understand the introduction...\n")

def select_mode():
    global save_mode
    while True:
        print("\n\033[35mSelect Game Mode:\033[0m")
        print("\033[32m1. Normal Mode\033[0m")
        print("\033[31m2. Hardcore Mode\033[0m")
        print("\033[96m3. Sync and convert saves from modes\033[0m")
        print("\033[33m4. Help\033[0m")

        mode_choice = input("Enter your choice: ")
        os.system("cls")
        if mode_choice == "1":
            save_mode = "save_0"
            break
        elif mode_choice == "2":
            save_mode = "save_1"
            break
        elif mode_choice == "3":
            sorter.main()
        elif mode_choice == "4":
            show_mode_help()
        else:
            print("Please enter a valid number choice")

    current_mode = "Normal" if mode_choice == "1" else "Hardcore"
    print(f"\033[33mMode set to {current_mode}.\033[0m\n\n")
    return current_mode

def menu():
    base_url = find_game_directory_base_url()
    if base_url:
        full_backup_files(base_url)
    current_mode = select_mode()
    while True:
        if current_mode == "Normal":
            print(f"\033[92m{current_mode} \033[35mMain Menu:\033[0m")
        elif current_mode == "Hardcore":
            print(f"\033[31m{current_mode} \033[35mMain Menu:\033[0m")
        print("\033[96m0. Full Backup \033[31m(All Files)\033[0m")
        if current_mode == "Normal":
            print("\033[34m1. Restore Backup World\033[0m")
        elif current_mode == "Hardcore":
            print("\033[34m1. Restore Backup World \033[35mAND PROFILE\033[0m")
        print("\033[34m2. Load Save\033[0m")
        print("\033[32m3. Create New Save\033[0m")
        print("\033[33m4. Change Mode\033[0m")
        print("\033[33m5. Help\033[0m")
        print("\033[31m6. Quit\033[0m")

        choice = input("Enter your choice: ")
        os.system("cls")

        if choice == "0":
            if base_url:
                full_backup_files(base_url)
        elif choice == "1":
            if base_url:
                if current_mode == "Normal":
                    restore_from_backup(base_url)
                elif current_mode == "Hardcore":
                    restore_from_backup(base_url, profile=True)
        elif choice == "2":
            if base_url:
                choose_save_directory(base_url)
        elif choice == "3":
            if base_url:
                create_and_copy_to_new_folder(base_url)
        elif choice == "4":
            current_mode = select_mode()
        elif choice == "5":
            show_main_help(current_mode)
        elif choice == "6":
            print("\033[31mExiting Save Guardian\033[0m")
            sys.exit(0)
        else:
            print("\033[31mInvalid choice. Please enter a number from the menu.\033[0m")


if __name__ == "__main__":
    try:
        introduction()
        os.system("cls")
        menu()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")