# Talisman Script for fun

This application allows you to control a healer character in a game by sending commands based on information retrieved from another game window.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x.
- You have installed the required Python packages.
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

    ```txt
    MouseInfo==0.1.3
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
    ```

3. **Set up your environment:**

    I recommend creating a conda environment for this. currently using "talis"
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

2. **Enter the required information:**

    - **Info PID (main char):** The PID of the main character's game window.
    - **Teammates 1 tp 4:** The PID of teammamtes.
    - **Command to send (healer):** The key command to send to the healer's game window.

3. **Start the healer:**

    Click the "Start Healer" button to start sending commands to the healer's game window based on the information retrieved from the main character's game window.

4. **Stop the healer:**

    Click the "Stop Healer" button to stop sending commands.

## File Structure

- `script.py`: The main application script that provides the GUI and starts/stops the healer process.
- `healer.py`: The script that retrieves information from the game windows and sends commands to the healer's game window.

## Functions

### script.py

- [HealerApp.__init__(self, root)](http://_vscodecontentref_/0): Initializes the application window.
- [HealerApp.start_healer(self)](http://_vscodecontentref_/1): Starts the healer process.
- [HealerApp.stop_healer(self)](http://_vscodecontentref_/2): Stops the healer process.
- [HealerApp.update_info(self, info_window_title, command_window_title)](http://_vscodecontentref_/3): Updates the information labels in the application window.
- [HealerApp.get_window_title(self, pid)](http://_vscodecontentref_/4): Retrieves the window title for a given PID.

### healer.py

- [send_key(hwnd, key)](http://_vscodecontentref_/5): Sends a key command to a window.
- [find_game_window_title_by_pid(pid)](http://_vscodecontentref_/6): Finds the window title for a given PID.
- [find_game_window_by_title(title)](http://_vscodecontentref_/7): Finds the window handle for a given window title.
- [get_information_from_window(hwnd)](http://_vscodecontentref_/8): Retrieves information from a window.
- [monitor_health_and_heal(info_pid, command_pid, heal_key)](http://_vscodecontentref_/9): Monitors the health of the main character and sends heal commands to the healer.

## Contributing

To contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the project maintainer at [your-email@example.com].
