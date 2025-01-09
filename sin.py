import win32api
import win32con
import win32gui
import win32process
import time
import sys
from pynput.keyboard import Controller

class Sin:
    def __init__(self, info_pid, sin_key_1='6', sin_key_2='5', heal_key='0', sin_duration=15):
        self.info_pid = info_pid

        if sin_key_1.lower() != 'none':
            print(f"Using sin key 1: {sin_key_1}")
            self.sin_key_1 = sin_key_1  # First key in the routine (e.g., '6')
        elif sin_key_1.lower() == 'none':
            print("No sin key 1 provided.")
            self.sin_key_1 = None
            
        self.sin_key_2 = sin_key_2  # Second key in the routine (e.g., '5')
        self.heal_key = heal_key
        self.sin_duration = sin_duration  # Duration for the secondary key (e.g., 10-15 seconds)
        self.info_hwnd = None

    def send_key(self, hwnd, key):
        """Simulates pressing a key on the specified window."""
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)

    def find_game_window_title_by_pid(self, pid):
        """Find the window title for a given PID."""
        window_title = None

        def enum_windows_callback(window_hwnd, _):
            nonlocal window_title
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(window_hwnd)
                if window_pid == pid:
                    window_title = win32gui.GetWindowText(window_hwnd)
                    return False  # Stop enumeration once found
            except Exception as e:
                print(f"Error retrieving PID for window: {e}")
            return True  # Continue enumeration

        win32gui.EnumWindows(enum_windows_callback, None)
        return window_title

    def find_game_window_by_title(self, title):
        """Find the HWND of a window given its title."""
        hwnd = win32gui.FindWindow(None, title)
        return hwnd

    def setup_window(self):
        """Set up the HWND for the info_pid."""
        info_title = self.find_game_window_title_by_pid(self.info_pid)
        if info_title:
            self.info_hwnd = self.find_game_window_by_title(info_title)

    def start_siner(self):
        """Runs the sining routine."""
        self.setup_window()
        if self.info_hwnd:
            #print(f"Starting siner for PID {self.info_pid} with routine keys '{self.sin_key_1}' and '{self.sin_key_2}'.")
            while True:
                if self.sin_key_1:
                # Press sin_key_1
                    print(f"Pressing key '{self.sin_key_1}'.")
                    self.send_key(self.info_hwnd, self.sin_key_1)
                    time.sleep(0.5)

                print(f"Pressing heal key '{self.heal_key}'.")
                self.send_key(self.info_hwnd, self.heal_key)
                time.sleep(0.5)

                # Press sin_key_2 for the specified duration
                print(f"Pressing key '{self.sin_key_2}' for {self.sin_duration} seconds.")
                end_time = time.time() + self.sin_duration
                while time.time() < end_time:
                    self.send_key(self.info_hwnd, self.sin_key_2)
                    time.sleep(0.5)  # Adjust repeat frequency if necessary

                # Return to sin_key_1
                #print(f"Returning to key '{self.sin_key_1}'.")
                if not self.sin_key_1:
                    continue
                else:
                    self.send_key(self.info_hwnd, self.sin_key_1) # Return to sin_key_1
                    time.sleep(0.5) 
        else:
            print("Exiting: No valid game window found.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python siner.py <info_pid> <sin_key_1> <sin_key_2> <heal_key>")
        sys.exit(1)

    info_pid = int(sys.argv[1])
    sin_key_1 = str(sys.argv[2])  # First key in the routine (e.g., '6')
    sin_key_2 = str(sys.argv[3])  # Second key in the routine (e.g., '5')
    heal_key = str(sys.argv[4])  # Key to check for mana (e.g., '7')

    sin = Sin(info_pid=info_pid, sin_key_1=sin_key_1, sin_key_2=sin_key_2, heal_key=heal_key, sin_duration=15)
    sin.start_siner()
