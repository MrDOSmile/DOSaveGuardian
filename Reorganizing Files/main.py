from utils import find_game_directory_base_url
from user_interface import show_main_help, select_mode, choose_save_directory, create_and_copy_to_new_folder, introduction
from backup_restore import full_backup_files, restore_from_backup
import os
import sys

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
