import os
import sorter
from user_interface import show_mode_help

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