from tkinter import filedialog, simpledialog, Tk

from utils import hide_username_in_path

import shutil
import sorter
import os

def show_mode_help():
    print("\n\033[35mSelect Game Mode:\033[0m")
    print("\033[32m1. Normal Mode\033[0m - This mode is meant for the 'Normal' game session i.e. NON-Hardcore.")
    print("\033[31m2. Hardcore Mode\033[0m - This mode is meant for the 'Hardcore' game session.")
    print("\033[96m3. Sync and convert saves from modes\033[0m - This will automatically create and sync any saves you have\n   from Normal into Hardcore saves, and vice-versa.")

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