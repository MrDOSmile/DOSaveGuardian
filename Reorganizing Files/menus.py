from mode_config import check_config_exists, create_config, read_config
from backup_restore import full_backup_files, find_game_directory_base_url, choose_save_directory, create_and_copy_to_new_folder
import json
import os

def config_menu():
    """Main function to coordinate the check, creation, reading, and modification of the config."""
    if not check_config_exists():
        print("Config file does not exist. Creating new config.")
        create_config()
    else:
        while True:
            print("\nMenu:")
            print("1. Read config")
            print("2. Change config")
            print("3. Continue")
            action = input("Choose an option (1, 2, or 3): ")
            if action == '1':
                return(read_config())
            elif action == '2':
                create_config()
                return(read_config())
            elif action == '3':
                print("Continuing program.")
                break
            else:
                print("Invalid input, please enter 1, 2, or 3.")

def choose_save_slot():
    config_data = read_config()
    available_slots = config_data['Normal'] + config_data['Hardcore']
    available_slots.sort()

    while True:
        print("\nChoose your current save slot:")
        for slot in available_slots:
            print(f"{slot}. Save Slot {slot}")

        try:
            slot_choice = int(input(f"Select an option (1-{max(available_slots)}): "))
            if slot_choice in available_slots:
                return slot_choice
            else:
                print(f"Invalid input, please enter a number between 1 and {max(available_slots) + 1}.")
        except ValueError:
            print("Please enter a valid number.")

def display_mode_specific_menu(mode, slot):
    """
    Displays a menu with options based on the mode (Normal or Hardcore) associated with the chosen slot.
    :param slot: The chosen save slot (1-5).
    """
    try:
        nonfunc = "This feature isn't fully implemented yet"
        base_url = find_game_directory_base_url()
        print(f"\nSave Slot {slot} is configured as {mode} mode.")

        common_options = {
            '0': "Full backup",
            '1': "Restore Backup",
            '2': "Load Save",
            '3': "Create Save",
            '4': "Help",
            '5': "Back"
        }

        # Display common options
        for key, option in common_options.items():
            print(f"{key}. {option}")

        # If mode is Hardcore, add extra options for restore type

        action = input("Choose an option: ").lower()
        if action == "0":
            full_backup_files(base_url)
        elif action == "1":
            if mode == 'Hardcore':
                print("1a. Restore World Only")
                print("1b. Restore World and Profile")
            else:
                print(nonfunc)
            # restore_from_backup(base_url, profile=False)
            print(nonfunc)
        elif action == "2":
            choose_save_directory(base_url)
        elif action == "3":
            create_and_copy_to_new_folder(base_url)
        elif action == "4":
            print(nonfunc)
        elif action == "5":
            print(nonfunc)
    except ValueError as e:
        print(e)