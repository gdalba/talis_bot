import win32api
import win32con
import win32gui
import win32process
import time
import sys
from pynput.keyboard import Controller

class AOEwiz:
    def __init__(self, info_pid, stun_key_1='6', atk_key_2='5', mana_key='8', AOEwiz_duration=15):
        self.info_pid = info_pid
        self.stun_key_1 = stun_key_1
        self.atk_key_2 = atk_key_2
        self.AOEwiz_duration = AOEwiz_duration
        self.mana_key = mana_key
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
            return True
        
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

    def start_AOEwiz(self):
        """Runs the AOEwiz routine."""
        self.setup_window()
        if self.info_hwnd:
            print(f"Starting AOEwiz for PID {self.info_pid}.")
            while True:
                
                # Press stun_key_1                
                self.send_key(self.info_hwnd, self.stun_key_1)
                time.sleep(1)
                
                # Press atk_key_2
                self.send_key(self.info_hwnd, self.atk_key_2)
                
                end_time = time.time() + self.AOEwiz_duration
                
                while time.time() < end_time:
                    self.send_key(self.info_hwnd, self.atk_key_2)
                    time.sleep(1)
                
                # Press mana_key
                self.send_key(self.info_hwnd, self.mana_key)
                time.sleep(1)

                self.send_key(self.info_hwnd, self.stun_key_1)
                time.sleep(1) # Repeat the cycle
        else:
            print("Could not find game window.")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python AOEwiz.py <PID>")
        sys.exit(1)

    info_pid = int(sys.argv[1])
    AOEwiz_bot = AOEwiz(info_pid=info_pid, stun_key_1='6', atk_key_2='5', mana_key='8', AOEwiz_duration=15)
    AOEwiz_bot.start_AOEwiz()

                



