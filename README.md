# README for Game Save Manager

## Overview

The Game Save Manager is a Python-based graphical utility for Windows, designed to manage save files for "Remnant2". It simplifies managing multiple save states, ensuring data integrity against loss or corruption with a user-friendly interface.

## Features

- **Save Slot Selection**: Choose from five save slots via a dropdown menu. The default slot is set to slot 1, but you can manage any slot at your discretion.
- **Full Backup and Restore**: Supports complete backups of the currently active save files and provides restore functionality for the last backup of the current save slot.
- **Profile vs. World Data**:
  - **World Data**: Consists of map configurations, shop inventories, checkpoint locations, and specific world settings.
  - **Profile Data**: Includes character-specific information such as inventory, levels, and vital status—important for 'Hardcore' mode where character death is permanent.
- **Interactive GUI**: Features dropdown menus and action buttons for easy operation.

## Installation and Running

1. **Prerequisites**:
   - Python 3.12.3 or higher. Install from [Python's official site](https://www.python.org/downloads/). Ensure to add Python to the 'PATH' during installation.
   - Administrative privileges on Windows for file management.

2. **Setup**:
   - Download or clone this repository to your computer.
   - Navigate to the project directory and run the `launch.bat` file. This script automatically installs necessary Python modules and starts the utility.

## Usage

- **Manage Saves**:
  - **Load Saves**: Load any save from any slot into the currently selected slot.
  - **Backup Saves**: Backup all current save files from the active slot to a designated backup directory, including profile data. This feature provides a rolling window of 10 full backups, allowing for recovery from different points in time.
  - **Restore Saves**: Restore the last backup for the currently active slot, with an option to include profile data or just world data. If you accidentally overwrite your last full backup, you can always load a previous backup from the "Load Saves" option.
- **Last Actions Log**: Maintains a log of the last five actions performed, displayed at the bottom of the GUI, helping track operations.

## Troubleshooting

- Ensure that "Remnant2" is properly installed and that the game directories are accessible.
- Verify correct Python installation and necessary permissions.
- Some bugs may exist; if you encounter issues, feel free to leave a comment on the GitHub repository for assistance or to report the bug.

## Conclusion

Game Save Manager enhances your gaming experience by providing sophisticated management of your game saves, supporting both data loss prevention and flexible management of save states. Enjoy seamless gaming sessions with robust save file management.

For additional help or feedback, please contact the development team or open an issue in the GitHub repository.
