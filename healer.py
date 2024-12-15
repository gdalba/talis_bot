import win32api
import win32con
import win32gui
import win32process
import time
import sys
from pynput.keyboard import Controller

keyboard = Controller()

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

def get_information_from_window(hwnd):
    # Implement the logic to get information from the window
    # For example, you can use win32gui.GetWindowText to get the window title
    window_text = win32gui.GetWindowText(hwnd)
    return window_text

# Main function to get information from one window and send heal key to another window
def monitor_health_and_heal(info_pid=None, info_title=None, command_pid=None, command_title=None, heal_key=None):
    info_hwnd = None
    command_hwnd = None

    if info_pid:
        info_window_title = find_game_window_title_by_pid(info_pid)
        if info_window_title:
            info_hwnd = find_game_window_by_title(info_window_title)
    elif info_title:
        info_hwnd = find_game_window_by_title(info_title)

    if command_pid:
        command_window_title = find_game_window_title_by_pid(command_pid)
        if command_window_title:
            command_hwnd = find_game_window_by_title(command_window_title)
    elif command_title:
        command_hwnd = find_game_window_by_title(command_title)

    if info_hwnd and command_hwnd and heal_key:
        while True:
            info = get_information_from_window(info_hwnd)
            print(f"Information from window: {info}")
            print(f"Sending heal key '{heal_key}' to window with handle '{command_hwnd}'.")
            send_key(command_hwnd, heal_key)
            time.sleep(1)  # Adjust the sleep time as needed
    else:
        print("Exiting: No valid game window found or heal key not provided.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python healer.py <info_pid> <command_pid> <heal_key>")
        sys.exit(1)
    
    info_pid = int(sys.argv[1])
    command_pid = int(sys.argv[2])
    heal_key = str(sys.argv[3])
    
    monitor_health_and_heal(info_pid=info_pid, command_pid=command_pid, heal_key=heal_key)