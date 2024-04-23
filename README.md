
# README for Game Save Manager

## Overview

The Game Save Manager is a Python-based utility designed to help users manage save files for the game "Remnant2" on Windows platforms. It provides functionalities such as creating and updating save slot configurations, backing up and restoring save files, and managing saves in an organized manner. The utility ensures that players can maintain multiple save states and recover from data loss or corruption issues efficiently.

## Features

- **Dynamic Save Slot Configuration**: Allows users to dynamically define and manage 'Normal' and 'Hardcore' save slots based on their preferences.
- **Full Backup**: Performs a complete backup of save files to a designated backup directory, supporting easy recovery and version control of game saves.
- **Restore Backup**: Enables users to restore saves from the most recent backup, with optional profile data restoration for 'Hardcore' slots.
- **Manage and Organize Saves**: Supports creating new save folders, transferring saves, and ensuring saves are properly maintained across different directories.
- **User-Friendly Interface**: Uses a simple command-line menu for navigating through various options, making it easy to use without prior technical knowledge.

## Installation

1. **Prerequisites**:
   - Python 3.12.3 or higher. If you do not have Python installed, download it from [here](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe).
   - Access to Windows OS with administrative privileges (to manage file paths and directories).

2. **Setup**:
   - Clone or download this repository to your local machine.
   - Navigate to the project directory in a command prompt or terminal.
   - To simplify the launch process, a `launch.bat` file is provided. Double-click on this file to start the utility.

## Usage

1. **Configuration**:
   - Upon first launch, you'll be prompted to configure the save slots for 'Normal' and 'Hardcore' modes by entering slot numbers.
   - The configuration will be saved in `config.json` in the script directory, which you can update anytime by selecting the 'config' option from the main menu.

2. **Backup Saves**:
   - Choose the "Full Backup" option from the main menu to backup all save files to the designated backup directory.

3. **Restore Saves**:
   - Select "Restore Backup" to restore a save file from the most recent backup. For 'Hardcore' mode, you also have the option to restore profile data.

4. **Manage Saves**:
   - Use "Load Save" to load a specific save or "Create New Save" to create and copy saves to a new folder, providing additional options for save data management.

5. **Other Options**:
   - Use the "Help" option for detailed instructions on each feature or "Change Slot" to switch between different configured save slots.

## Troubleshooting

In case of any issues:
- Ensure that the game "Remnant2" is correctly installed and that the game directories are accessible.
- Verify that Python and necessary permissions are correctly set up on your system.
- Check the console for error messages which can provide more information on what might be going wrong.

## Conclusion

The Game Save Manager is a robust tool designed to enhance your gaming experience by providing sophisticated management of your game saves. It helps prevent data loss and allows flexible management of multiple save states, ensuring that you can enjoy your gaming without worrying about save file management.

For further assistance or feedback, please feel free to open an issue in the repository or contact the development team.
