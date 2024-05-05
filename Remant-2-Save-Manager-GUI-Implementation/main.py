from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from save_manager import *

app = Ursina()

window.borderless = False
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.exit_button.enabled = False
window.collider_counter.enabled = False

slots = 1  # Variable to store the chosen slot as an integer

# List to store the last 5 actions
action_log = []
restore_profile = None

# Defining the base directory for the files.
base = find_game_directory_base_url()

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
    update_action_log('Full backup succesful')

def restore():
    print('Restore from Backup initiated.')
    restore_confirmation.enabled = True
    restore_from_backup(base, slots, restore_profile)
    update_action_log(f'Restored save for save slot {slots}')

def create_save():
    print('Creating new save.')
    new_folder_name = create_and_copy_to_new_folder(base, slots)
    update_action_log(f'Created new save called {new_folder_name}')

# Function to update the selected slot
def select_slot(value):
    global slots
    slots = value
    slot_text.text = f'Selected Slot: {value}'

# Confirmation for restoring profile
def confirm_restore():
    global restore_profile
    restore_profile = True
    print(f'Restore profile: {restore_profile}')
    restore_confirmation.enabled = False
    update_action_log('Profile restoration confirmed.')

def cancel_restore():
    global restore_profile
    restore_profile = False
    print(f'Restore profile: {restore_profile}')
    restore_confirmation.enabled = False
    update_action_log('Profile restoration cancelled.')

dropdown = DropdownMenu('Select Slot', buttons=[
    DropdownMenuButton(f'Slot {i}', on_click=Func(select_slot, i)) for i in range(1, 6)
])
dropdown.position = (-0.12, 0.4)

slot_text = Text(text='Default is save slot 1', position=(0, 0.45), origin=(0, 0), color=color.white)

backup_button = Button(text='Full Backup', color=color.azure, y=0.1, scale_y=0.1, on_click=backup)
restore_button = Button(text='Restore from Backup', color=color.orange, y=0, scale_y=0.1, on_click=restore)
create_button = Button(text='Create New Save', color=color.green, y=-0.1, scale_y=0.1, on_click=create_save)

actions_text = Text(text='', position=(0, -0.4), origin=(0, 0), color=color.white)

# Restore confirmation popup
restore_confirmation = Entity(enabled=False)
confirm_button = Button(parent=restore_confirmation, text='Yes', y=0, x=-0.1, color=color.lime, scale_y=0.1, on_click=confirm_restore)
cancel_button = Button(parent=restore_confirmation, text='No', y=0, x=0.1, color=color.red, scale_y=0.1, on_click=cancel_restore)

app.run()