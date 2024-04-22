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
        menus.config_menu()
        config = mode_config.read_config()
        save_slot = menus.choose_save_slot()
        print(save_slot)
        print(menus.get_mode_for_slot(config, save_slot))
        input()

if __name__ == "__main__":
    main()