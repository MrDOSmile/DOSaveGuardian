import os
import getpass
import shutil

def hide_username_in_path(path):
    username = getpass.getuser()
    path = path.replace("/", "\\")
    return path.replace(f"C:\\Users\\{username}", "C:\\Users\\<Username>")

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

def get_mode_for_slot(config_data, slot_number):
    """
    Determines whether the selected slot number is in 'Normal' or 'Hardcore' mode.
    :param config_data: Dictionary with configuration data.
    :param slot_number: Selected slot number.
    :return: Mode ('Normal' or 'Hardcore') for the slot number.
    """
    if slot_number in config_data['Normal']:
        return 'Normal'
    elif slot_number in config_data['Hardcore']:
        return 'Hardcore'
    else:
        raise ValueError(f"Slot number {slot_number} is not configured in any mode.")