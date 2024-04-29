import json

def has_user_agreed():
    """Check if the user has already agreed to the terms."""
    try:
        with open('agreement.json', 'r') as file:
            agreement = json.load(file)
        return agreement.get('agreed', False)
    except FileNotFoundError:
        return False

def save_user_agreement():
    """Save user's agreement to the terms in a JSON file."""
    with open('agreement.json', 'w') as file:
        json.dump({'agreed': True}, file)

def confirm_understanding(section):
    """Prompt user to type 'Understood' to confirm understanding of the section."""
    response = input("Type 'Understood' to continue: ")
    if response.lower() != 'understood':
        print("You did not confirm understanding. The program will now exit.")
        exit()

def program_introduction():
    if has_user_agreed():
        return  # User has already agreed, skip the introduction

    print("Welcome to the Game Save Manager for Remnant2\n")

    # Save Locations and Handling
    print("Save Locations and Handling:")
    print("The program manages game saves located typically in 'C:\\Users\\<Username>\\Saved Games\\Remnant2\\Steam'. "
          "It handles save files by allowing dynamic configuration of save slots, enabling backups, restores, "
          "and safe transfer of save data across different directories.")
    confirm_understanding("Save Locations and Handling")

    # Proper Usage
    print("\nProper Usage:")
    print("To ensure effective use of this utility, always change save slots only through the main menu screen. "
          "This prevents data corruption. Backups must be performed manually before making significant changes or updates to your saves.")
    confirm_understanding("Proper Usage")

    # Terms of Use
    print("\nTerms of Use:")
    print("1. The Game Save Manager is provided 'as is' and without warranties of any kind, express or implied.")
    print("2. The user agrees to back up data regularly and acknowledges that the creator is not responsible for data loss.")
    print("3. The user must follow documented procedures for operations such as backup and restore.")
    print("4. Modification of the software or its misuse is strictly prohibited and absolves the creator of any liability.")
    print("5. Use of this tool for commercial purposes without prior consent is prohibited.")
    confirm_understanding("Terms of Use")

    # Important Warning
    print("\nImportant Warning:")
    print("Incorrect use of this utility can lead to data loss or corruption.")
    confirm_understanding("Important Warning")

    # Disclaimer
    print("\nDisclaimer:")
    print("The creator of this program, DOSmile, is not responsible for any damage to your save files or game data resulting from incorrect usage.")
    confirm_understanding("Disclaimer")

    # User Agreement
    print("\nUser Agreement:")
    print("Type 'Agree' to acknowledge that you have read, understood, and agree to the terms of use, important warnings, and the disclaimer above.")
    user_response = input("Type here: ")
    if user_response.lower() == 'agree':
        print("Thank you for agreeing to the terms. You may now use the Game Save Manager.")
        save_user_agreement()
    else:
        print("You have chosen not to agree to the terms. The program will now exit.")
        exit()

# To see the introduction in action, you would call this function like so:
# program_introduction()
