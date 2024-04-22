import json
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

def check_config_exists():
    """Check if the config.json file exists in the same directory as the script."""
    config_path = os.path.join(script_dir, 'config.json')
    return os.path.exists(config_path)

def create_config():
    config_path = os.path.join(script_dir, 'config.json')

    while True:
        # Get input for 'Normal' slots
        normal_input = input("Enter the save slot numbers for 'Normal' separated by commas (e.g., 1, 2, 3): ")
        normal_list = [int(n.strip(' []{}<>();:')) for n in normal_input.split(',') if n.strip(' []{}<>();:').isdigit()]

        # Get input for 'Hardcore' slots
        hardcore_input = input("Enter the save slot numbers for 'Hardcore' separated by commas (e.g., 4, 5): ")
        hardcore_list = [int(n.strip(' []{}<>();:')) for n in hardcore_input.split(',') if n.strip(' []{}<>();:').isdigit()]

        # Check for duplicates between 'Normal' and 'Hardcore'
        if set(normal_list) & set(hardcore_list):
            print("Duplicate slots found between 'Normal' and 'Hardcore'. Please start over.")
            continue

        # If no duplicates found, break out of the loop
        break

    config_data = {
        "Normal": normal_list,
        "Hardcore": hardcore_list
    }

    with open(config_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print("Created config.json with data:", config_data)

def read_config():
    """Read and print the content of the config.json located in the same directory as the script."""
    config_path = os.path.join(script_dir, 'config.json')
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
    # print("Config data:", config_data)
    return config_data
