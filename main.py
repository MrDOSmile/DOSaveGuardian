from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.tooltip import Tooltip
from save_manager import *

app = Ursina()

window.borderless = False
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.exit_button.enabled = False
window.collider_counter.enabled = False
window.color = color.black

action_log = []
restore_profile = None

base = find_game_directory_base_url()
ensure_directories_exist(base)
global slots
slots = 0
global num_backups_to_keep
num_backups_to_keep = 10  # Default number of backups to keep

def update_action_log(action):
    action_log.insert(0, action)
    if len(action_log) > 5:
        action_log.pop()
    actions_text.text = '\n'.join(action_log)

def backup():
    print('Full Backup initiated.')
    full_backup_files(base, num_backups_to_keep)
    update_action_log('Full backup successful')

def load():
    print('Loading from folder.')
    temp_dir = load_save(base, slots)
    if temp_dir is not None:
        update_action_log(f'Loaded file from {hide_username_in_path(temp_dir)}')
    else:
        update_action_log('No save was selected')

def create(key):
    if key == 'enter':
        global new_save_name
        global slots
        new_save_name = input_field.text
        input_field.text = ""
        if len(new_save_name) == 0:
            swap_main_menu()
            update_action_log("No name was entered")
        else:
            swap_main_menu()
            worked = call_create_save(new_save_name, slots)
            if worked:
                update_action_log(f"Created new save called {new_save_name}")
            else:
                update_action_log("Cancelled choosing a target location")

def cancel_create():
    input_field.text = ""
    update_action_log("Cancelled creating a new save")
    swap_main_menu()

def call_create_save(new_save_name, slots):
    worked = create_save(new_save_name, slots)
    return(worked)

def select_slot(value):
    global slots
    slots = value
    slot_text.text = f'Selected Character Slot: {value+1}'
    slot_text_data.text = f'Selected Character Slot: {value+1}'

def world_restore():
    global slots
    worked = restore_world_from_backup(base, slots)
    swap_main_menu()
    if worked:
        update_action_log(f'World data restored for slot {slots+1}')
    else:
        update_action_log('No backup exists or checksum mismatch')

def profile_restore():
    global slots
    worked = restore_profile_from_backup(base)
    swap_main_menu()
    if worked:
        update_action_log(f'Profile data restored for slot {slots+1}')
    else:
        update_action_log('No backup exists or checksum mismatch')

def both_restore():
    global slots
    worked = restore_profile_and_world(base, slots)
    swap_main_menu()
    if worked:
        update_action_log(f'Profile and World data restored for slot {slots+1}')
    else:
        update_action_log('No backup exists or checksum mismatch')

def cancel_restore():
    update_action_log('Restoring from backup was cancelled')
    swap_main_menu()

def swap_backup_menu():
    restore_confirmation.enabled = True
    main_menu.enabled = False
    create_save_menu.enabled = False

def swap_main_menu():
    restore_confirmation.enabled = False
    main_menu.enabled = True
    create_save_menu.enabled = False
    help_menu.enabled = False

def swap_create_save():
    main_menu.enabled = False
    restore_confirmation.enabled = False
    create_save_menu.enabled = True

def show_help():
    help_menu.enabled = True
    main_menu.enabled = False

def set_backup_limit():
    global num_backups_to_keep
    try:
        limit = int(backup_limit_field.text)
        if limit < 1:
            update_action_log("Backup limit must be at least 1")
        else:
            num_backups_to_keep = limit
            update_action_log(f"Backup limit set to {num_backups_to_keep}")
    except ValueError:
        update_action_log("Invalid backup limit")

main_menu = Entity(enabled=True, scale=(7,7,7))

dropdown = DropdownMenu('   Select character slot', buttons=[
    DropdownMenuButton(f'Character Slot: {i+1}', on_click=Func(select_slot, i), color=color.dark_gray) for i in check_number_of_save_slots(base)
], parent=main_menu, scale=(0.4,0.04), color=color.dark_gray)
dropdown.position = (-0.2, 0.4)

slot_text = Text(text=f'Selected Character Slot: {slots+1}', position=(0, 0.2), origin=(0, 0), color=color.white, scale=(2), parent=main_menu)
backup_button = Button(text='Full Backup', color=color.azure, y=0.1, scale_y=0.1, on_click=backup, parent=main_menu)
restore_button = Button(text='Restore from Backup', color=color.blue, y=0, scale_y=0.1, on_click=swap_backup_menu, parent=main_menu)
load_button = Button(text='Load World Save', color=color.orange, y=-0.15, scale_y=0.1, on_click=load, parent=main_menu)
create_button = Button(text='Create New Save', color=color.green, y=-0.25, scale_y=0.1, on_click=swap_create_save, parent=main_menu)
help_button = Button(text='Help', color=color.white, y=-0.35, scale_y=0.1, on_click=show_help, parent=main_menu, text_color=color.black)
actions_text = Text(text='', position=(0, -0.5), origin=(0, 0), color=color.white, parent=main_menu)

# Backup limit input
backup_limit_field = InputField(text=str(num_backups_to_keep),
                                placeholder="Backup Limit",
                                max_lines=1,
                                origin=(0,0),
                                scale=(0.2, 0.04),
                                position=(0.5, 0.5),
                                parent=main_menu,
                                color=color.dark_gray)
backup_limit_button = Button(text='Set Backup Limit',
                             color=color.yellow,
                             text_color=color.black,
                             position=(0.5, 0.35),
                             scale=(0.5, 0.04),
                             on_click=set_backup_limit,
                             parent=main_menu)
# Adjust text size to fit the button
backup_limit_button.text_entity.scale *= 0.7

# Defining tooltips for main menu buttons
backup_button.tooltip = Tooltip(f"-Will copy all files from '{hide_username_in_path(find_game_directory_base_url())}' to the 'Backups' folder there.\n-You can set the maximum number of backups.\n-The newest save is the highest number always.\n-Character slot selection is irrelevant here, as it backs up all of the data.")
restore_button.tooltip = Tooltip(f"---ONLY USE ON MAIN MENU OF GAME!!---\n\n-Will restore the latest backup [highest numbered], using your selected character's save slot.\n-It only restores that character's data.\n-If you need to load an earlier save, use 'Load Save', and navigate to your 'Backups' folder, and load a lower number.\n-If you need to load an earlier 'Profile' save, at the moment, it must be done manually.")
load_button.tooltip = Tooltip("---ONLY USE ON MAIN MENU OF GAME!!---\n\n-Opens up a window to have you select a folder [defaults to the folder called 'Saves'].\n-Regardless of which character you created the save with, this will change that world data into one your currently selected character can use.\n\n[Quick tip: You can use the search bar in the window to find a save you want quickly!]")
create_button.tooltip = Tooltip("-Prompts you for the name of your new save.\n-A new folder will be created under that name.\n-Then choose a folder you will save it to\n-This will save your current profile and world data as a new save.")
help_button.tooltip = Tooltip("Click to view the help and documentation.")

# Restore confirmation popup
restore_confirmation = Entity(enabled=False, scale=(7,7,7))
slot_text_data = Text(text=f'Selected Character Slot: {slots+1}', position=(0, 0.15), origin=(0, 0), color=color.white, scale=(2), parent=restore_confirmation)
confirmation_text = Text(text="Please choose an option to restore that type of data:", position=(0,0.1), origin=(0,0), color=color.white, parent=restore_confirmation, scale=1.2)
profile_button = Button(parent=restore_confirmation, text='Profile Data', y=0, x=-0.35, color=color.violet, scale_y=0.1, scale_x=0.4, on_click=profile_restore)
world_button = Button(parent=restore_confirmation, text='World Data', y=0, x=0.35, color=color.red, scale_y=0.1, scale_x=0.4, on_click=world_restore)
both_button = Button(parent=restore_confirmation, text='Both', y=0, x=0, color=color.lime, scale_y=0.1, scale_x=0.2, on_click=both_restore)
cancel_button = Button(parent=restore_confirmation, text='Cancel', y=-0.15, x=0, color=color.orange, scale_y=0.1, scale_x=0.4, on_click=cancel_restore)

# Defining tooltips for profile restore menu
profile_button.tooltip = Tooltip("Profile data contains the data associated to your character and not your world. Things like your inventory, unlocks, builds, etc. and whether or not your HardCore character is still alive.\n\n[NOTE: If your hardcore character has died, use this option. The game MUST be restarted in order for your character to be alive again.]")
world_button.tooltip = Tooltip("World data contains the data of your world progress. It will save your shop inventories, current world progression, last checkpoint, etc. This is the most common option when loading a backup.")
both_button.tooltip = Tooltip("This loads both your Profile data and your World data at the same time from your 'Backups'. Niche use case, but the option is there.")
cancel_button.tooltip = Tooltip("Used if you don't want to restore anything, and want to return to the main menu.")

create_save_menu = Entity(enabled=False)
enter_save_name_text = Text(text=f'Click the text box\nEnter the name of your new save\nPress enter to submit\nChoose folder to save it there', position=(0, 0.75), origin=(0, 0), color=color.white, scale=(10), parent=create_save_menu)
cancel_button_input_field = Button(parent=create_save_menu, text='Cancel', y=-1.5, x=0, color=color.orange, scale_y=0.5, scale_x=2, on_click=cancel_create)
input_field = InputField(text="",
                         placeholder="Name your save here. Make sure it's something you can find later.",
                         max_lines=1,
                         origin=(0,0),
                         scale=(10, 0.75),
                         position=(0, -0.5),
                         parent=create_save_menu,
                         input=create,
                         color=color.dark_gray)

# Help Menu
help_menu = Entity(enabled=False)
help_text = Text(text="""
Welcome to the Remnant 2 Save Manager!

This tool allows you to manage your game saves effectively.
Here are the available options:

- **Select Character Slot**: Choose which character slot to manage.
- **Full Backup**: Creates a backup of your current saves. You can set how many backups to keep.
- **Restore from Backup**: Restores your profile and/or world data from the latest backup.
- **Load World Save**: Load a specific world save from a selected folder.
- **Create New Save**: Save your current game state as a new save with a custom name.
- **Set Backup Limit**: Define how many backups you want to keep.
- **Help**: View this help information.

**Tips:**
- Always ensure you are on the main menu of the game before restoring saves.
- Use tooltips by hovering over buttons for more detailed information.

""",
position=(0, 0.5), origin=(0, 0), color=color.white, scale=7, parent=help_menu)
back_button = Button(parent=help_menu, text='Back to Main Menu', y=-1.4, x=0, color=color.azure, scale_y=0.4, scale_x=5, on_click=swap_main_menu)

app.run()
