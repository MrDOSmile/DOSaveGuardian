from mode_config import check_config_exists, create_config, read_config
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
                read_config()
            elif action == '2':
                create_config()
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
        print(f"{max(available_slots) + 1}. Return to main menu")

        try:
            slot_choice = int(input(f"Select an option (1-{max(available_slots) + 1}): "))
            if slot_choice in available_slots:
                return slot_choice
            elif slot_choice == max(available_slots) + 1:
                print("Returning to main menu...")
                break
            else:
                print(f"Invalid input, please enter a number between 1 and {max(available_slots) + 1}.")
        except ValueError:
            print("Please enter a valid number.")

def display_mode_specific_menu(slot):
    """
    Displays a menu with options based on the mode (Normal or Hardcore) associated with the chosen slot.
    :param slot: The chosen save slot (1-5).
    """
    # Load the configuration data
    config_data = read_config()
    try:
        # Determine the mode for the slot
        mode = get_mode_for_slot(config_data, slot)
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
        if mode == 'Hardcore':
            print("1a. Restore World Only")
            print("1b. Restore World and Profile")

        action = input("Choose an option: ").lower()
        # Logic to handle user's action based on choice goes here...
        # For example:
        # if action == '0':
        #     full_backup_function()
        # elif action == '1':
        #     restore_backup_function()
        # And so on...

    except ValueError as e:
        print(e)

def main_menu():
    print("1. Mode selection per save")
    print("2. Save slot selection")
    print("3. ")