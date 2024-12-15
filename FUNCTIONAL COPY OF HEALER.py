import win32api
import win32con
import win32gui
import win32process
import time
from pynput.keyboard import Controller

keyboard = Controller()
HEAL_KEY = 'v'  # Replace with the actual key for the heal key

def send_key(hwnd, key):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)

def find_game_window_title_by_pid(pid):
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

    # Enumerate through all windows and check the PID
    win32gui.EnumWindows(enum_windows_callback, None)
    
    if window_title:
        return window_title
    else:
        print(f"No window found for PID {pid}.")
        return None

def find_game_window_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        return hwnd
    else:
        print(f"Window with title '{title}' not found.")
        return None

# Main function to send heal key to the game window
def monitor_health_and_heal(pid=None, title=None):
    hwnd = None
    if pid:
        window_title = find_game_window_title_by_pid(pid)
        if window_title:
            hwnd = find_game_window_by_title(window_title)
    elif title:
        hwnd = find_game_window_by_title(title)

    if hwnd:
        while True:
            print(f"Sending heal key to window with handle '{hwnd}'.")
            send_key(hwnd, HEAL_KEY)
            time.sleep(1)  # Adjust the sleep time as needed
    else:
        print("Exiting: No valid game window found.")

# Example usage
pid = 19820  # Replace with the actual PID of your game process
monitor_health_and_heal(pid=pid)

# Alternatively, you can use the title of the window instead of PID:
# monitor_health_and_heal(title="Game Window Title")