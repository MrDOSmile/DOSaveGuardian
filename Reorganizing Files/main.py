import help
import menus
import mode_config
import utils

def main():
    # if not mode_config.check_config_exists():
    #     mode_config.create_config()
    #     config = mode_config.read_config()
    # else:
    #     config = mode_config.read_config()

    while True:
        if not mode_config.check_config_exists():
            config_data = menus.config_menu()
        else:
            config_data = mode_config.read_config()

        save_slot = menus.choose_save_slot()
        mode = utils.get_mode_for_slot(config_data, save_slot)
        while True:
            menus.display_mode_specific_menu(mode, save_slot)
            input()


if __name__ == "__main__":
    main()