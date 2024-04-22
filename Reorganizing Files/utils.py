import os
import getpass

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