import help
import menus
import mode_config
import utils
import backup_restore

def main():
    base = utils.find_game_directory_base_url()
    while True:
        if not mode_config.check_config_exists():
            config_data = menus.config_menu()
        else:
            config_data = mode_config.read_config()

        try: #Checking is save_slot has been created, if not, go to choose save_slot menu
            mode = utils.get_mode_for_slot(config_data, save_slot)
            print(config_data, save_slot, mode)
            backup_restore.create_and_copy_to_new_folder(base, save_slot)

        except: # save_slot menu if save_slot hasn't been created
            save_slot = menus.choose_save_slot()




if __name__ == "__main__":
    main()