from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from save_manager import *

app = Ursina()

window.borderless = False
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.exit_button.enabled = False
window.collider_counter.enabled = False
window.color = color.black

slots = 1  # Variable to store the chosen slot as an integer

# List to store the last 5 actions
action_log = []
restore_profile = None

# Defining the base directory for the files.
base = find_game_directory_base_url()
ensure_directories_exist(base)

def update_action_log(action):
    # Add the new action at the start of the list
    action_log.insert(0, action)
    # Keep only the last 5 actions
    if len(action_log) > 5:
        action_log.pop()
    # Update the displayed text
    actions_text.text = '\n'.join(action_log)

def backup():
    print('Full Backup initiated.')
    full_backup_files(base)
    update_action_log('Full backup successful')

def load():
    print('Loading from folder.')
    temp_dir = load_save(base, slots)
    if temp_dir is not None:
        update_action_log(f'Loaded file from {hide_username_in_path(temp_dir)}')
    else:
        update_action_log('No save was selected')

def create():
    print('Creating new save.')
    new_folder_name = create_save(base, slots)
    if new_folder_name is not None:
        update_action_log(f'Created new save called {hide_username_in_path(new_folder_name)}')
    else:
        update_action_log('No new save was made')

# Function to update the selected slot
def select_slot(value):
    global slots
    slots = value
    slot_text.text = f'Selected Slot: {value}'

# Confirmation for restoring profile
def profile_restore():
    global restore_profile
    restore_profile = True
    print(f'Restore profile: {restore_profile}')
    worked = restore_from_backup(base, slots, restore_profile)
    swap_menus()
    if worked:
        update_action_log('Restored world and profile data')
    else:
        update_action_log('No backup exists for current save slot')

def no_profile_restore():
    global restore_profile
    restore_profile = False
    print(f'Restore profile: {restore_profile}')
    worked = restore_from_backup(base, slots, restore_profile)
    swap_menus()
    if worked:
        update_action_log('Restored just world data')
    else:
        update_action_log('No backup exists for current save slot')

def cancel_restore():
    update_action_log('Restoring from backup was cancelled')
    swap_menus()

def swap_menus():
    restore_confirmation.enabled = not restore_confirmation.enabled
    main_menu.enabled = not main_menu.enabled

main_menu = Entity(enabled=True, scale=(7,7,7))
dropdown = DropdownMenu('Select Slot', buttons=[
    DropdownMenuButton(f'Slot {i}', on_click=Func(select_slot, i), color=color.dark_gray) for i in range(1, 6)
], parent=main_menu, scale=(0.4,0.04), color=color.dark_gray)
dropdown.position = (-0.15, 0.4)
slot_text = Text(text='Selected Slot: 1', position=(0, 0.45), origin=(0, 0), color=color.white, scale=(1.2), parent=main_menu)
backup_button = Button(text='Full Backup', color=color.azure, y=0.1, scale_y=0.1, on_click=backup, parent=main_menu)
restore_button = Button(text='Restore from Backup', color=color.blue, y=0, scale_y=0.1, on_click=swap_menus, parent=main_menu)
load_button = Button(text='Load Save', color=color.orange, y=-0.15, scale_y=0.1, on_click=load, parent=main_menu)
create_button = Button(text='Create New Save', color=color.green, y=-0.25, scale_y=0.1, on_click=create, parent=main_menu)
actions_text = Text(text='', position=(0, -0.4), origin=(0, 0), color=color.white, parent=main_menu)

# Restore confirmation popup
restore_confirmation = Entity(enabled=False, scale=(7,7,7))
confirmation_text = Text(text="Would you like to restore your profile as well?", position=(0,0.1), origin=(0,0), color=color.white, parent=restore_confirmation, scale=1.2)
yes_button = Button(parent=restore_confirmation, text='Yes', y=0, x=-0.1, color=color.lime, scale_y=0.1, scale_x=0.2, on_click=profile_restore)
no_button = Button(parent=restore_confirmation, text='No', y=0, x=0.1, color=color.red, scale_y=0.1, scale_x=0.2, on_click=no_profile_restore)
cancel_button = Button(parent=restore_confirmation, text='Cancel', y=-0.1, x=0, color=color.orange, scale_y=0.1, scale_x=0.4, on_click=cancel_restore)

app.run()