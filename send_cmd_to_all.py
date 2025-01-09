import win32api
import win32con
import win32gui
import time
import sys
from pynput.keyboard import Controller

keyboard = Controller()

def send_key(hwnd, key):
    win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
    win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)

def find_game_window_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    if hwnd:
        return hwnd
    else:
        print(f"Window with title '{title}' not found.")
        return None

def get_information_from_window(hwnd):
    window_text = win32gui.GetWindowText(hwnd)
    return window_text

def send_cmd_to_all(info_title, command_title, cmd_key):
    info_hwnd = find_game_window_by_title(info_title)
    command_hwnd = find_game_window_by_title(command_title)

    
    if info_hwnd and command_hwnd and cmd_key:
        if cmd_key == "p":
            #press nonstop
            while True:
                send_key(command_hwnd, cmd_key)
        info = get_information_from_window(info_hwnd)
        print(f"Information from window: {info}")
        print(f"Sending command key '{cmd_key}' to window with handle '{command_hwnd}'.")
        send_key(command_hwnd, cmd_key)
        # Adjust the sleep time as needed
    else:
        print("Exiting: No valid game window found or command key not provided.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python send_cmd_to_all.py <info_title> <command_title> <cmd_key>")
        sys.exit(1)
    
    info_title = str(sys.argv[1])
    command_title = str(sys.argv[2])
    cmd_key = str(sys.argv[3])
    
    send_cmd_to_all(info_title, command_title, cmd_key)