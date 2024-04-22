import os
import getpass
import shutil
from tkinter import filedialog, simpledialog, Tk

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