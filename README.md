# Talisman Script for fun v1.0

This app allows you to control up to 3 healers, 1 monk, and 2 wizards through intuitive input clicks.
## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x.
- You have installed the required Python packages from requirements.txt. This set of scripts have tesseract as a requirement, installing it is not as intuitive, so either manually skim over every script and delete tesseract-related command, or install it.
- You are using a Windows operating system (required for `win32api` and `win32gui`).

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/gdalba/talis_bot.git
    cd talis_bot
    ```

2. **Install the required Python packages:**

    ```sh
    pip install -r requirements.txt
    ```

    Ensure your `requirements.txt` includes the following packages:

    ```
    txtMouseInfo==0.1.3
    packaging==24.2
    pillow==11.0.0
    psutil==6.1.0
    PyAutoGUI==0.9.54
    PyGetWindow==0.0.9
    PyMsgBox==1.0.9
    pynput==1.7.7
    pyperclip==1.9.0
    PyRect==0.2.0
    PyScreeze==1.0.1
    pytesseract==0.3.13
    pytweening==1.2.0
    pywin32==308
    six==1.17.0
    ttkbootstrap==1.10.1
    ```

3. **Set up your environment:**

    I recommend creating a conda environment for this. Currently using "talis"
    ```sh
    conda activate talis
    ```

## Usage

1. **Run the main application:**

    You can now run command_five.py to find the most up-to-date version.
    ```sh
    python command_five.py
    ```

    This will open the bot application window.

2. **What every UI element means:**

    - `**Info PID (main char):**` The PID of the main character's game window. Usually for the tank of the team.
    - `**Teammates 1 to 4:**` The PID of teammates.
    - `**Command to send (all):**` The key command to send to all game window. For instance, I set 'k' to be mount, every open client then mounts at the same time.
    - `**Healer PIDs (1 to 3):**` Where you will identify the clients of your healer characters. Note that you do not need to have 3 healer clients open/identified.
    - `**Monk PID**` Where you will identify the client of your monk character
    - `**Wizard PIDs (1 to 2):**` Where you will identify the clients of your wizard characters.
    - `**Healing key 1 (regen/shield/none):**` Recommended to identify shields, regen heal, or none for pure repeat healing command. Defaults to 6.
    - `**Healing key 2 (main heal):**` Required for the main heal. Defaults to 5.
    - `**Mana Regeneration key:**` Required for mana regeneration. Defaults to 9.
    - `**Start Healer:**` Starts the healing routine, on click stops for all identified healers.
    - `**Start Monk:**` Starts monk routine, on click stops.
    - `**Start follow:**` Starts follow routine for every identified teammate (1 to 4). Note that you must manually identify target to be followed.
    - `**Start BOSSwiz:**` Starts wizard DPS routine, on click stops for all identified wizards.
    - `**Start AOEwiz:**` Starts multiple mobs AOE routine, on click stops for all identified wizards.
    - `**Refresh PIDs:**` If you close/open new clients, clicking on this button will update the list of clients at the bottom of the applcation.
    - `**Mount:**` Alternate default mount button (using 'k' as default key).

3. **Detected PIDs (client.exe):**

    Talisman Online runs through client.exe applications. When you run command_five.py, you will automatically receive a list of open client.exe. You can then assign directly through that list to the respective elements (for instance, choosing 'H1' to 'PID 35516' will assign that client to the 'healer PID 1' tab.

## File Structure

- `command_five.py`: The main application script that provides the GUI and offers control to all options.
- `healer.py`: The script that retrieves information from the game windows and sends commands to the healer's game window.
- `AOEwiz.py`: AOE routine for wizard.
- `BOSSwiz.py`: Single target routine for wizard.
- `monk.py`: Tank routine.
- `send_cmd_to_all.py`: Controls the distribution of single key commands.
- `sin.py`: [NOT IMPLEMENTED] controls Assassin routine.
-  `find_leader.py`: [NOT USED] Automatically finds main character PID to follow.
-  `mouse_tracker.py`: use it manually running `python mouse_tracker.py` to track absolute coordinates of the screen, or relative to initial point (where the mouse started).
-  `auto_clicker.py`: [WIP] This script currently has four modes: 1. Auto Clicker - tests based on given list of x,y coordinates; 2. Debug mode - allows you to provide as many x, y coordinates (one by one) and execute mouse left click; 3. Routine mode - to implement standard routines of commands; and 4. cwc - current WIP of a automatic bot for 5 clients to run through CWC.
-  `mouse.py`: Not my work, all credit goes to Tonirogerion (TonyR0XX) for providing the script. All I did was make it find window handle (hwnd) automatically.

## Contributing

To contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

## License

No license lmfao.
