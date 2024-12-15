import pyautogui
import win32gui
import win32process
import time
from PIL import Image
import pytesseract
import sys

# Specify the Tesseract executable path if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

def get_window_rect(pid):
    window_rect = None

    def enum_windows_callback(hwnd, pid):
        nonlocal window_rect
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        if window_pid == pid:
            window_rect = win32gui.GetWindowRect(hwnd)
            return False
        return True

    win32gui.EnumWindows(enum_windows_callback, pid)
    return window_rect

def capture_screenshot(pid, region):
    window_rect = get_window_rect(pid)
    if window_rect:
        left, top, right, bottom = window_rect
        region = (left + region[0], top + region[1], left + region[2], top + region[3])
        screenshot = pyautogui.screenshot(region=region)
        return screenshot
    else:
        print(f"No window found for PID {pid}.")
        return None

def extract_health_from_screenshot(screenshot):
    # Convert the screenshot to grayscale
    gray_screenshot = screenshot.convert("L")
    # Use OCR to extract text from the screenshot
    health_text = pytesseract.image_to_string(gray_screenshot)
    # Process the extracted text to get the health value
    health_value = parse_health_text(health_text)
    return health_value

def parse_health_text(health_text):
    # Implement the logic to parse the health value from the extracted text
    # This is a placeholder implementation and should be adjusted based on the actual text format
    try:
        health_value = int(health_text.strip())
        return health_value
    except ValueError:
        return None

def report_health(pid, region):
    screenshot = capture_screenshot(pid, region)
    if screenshot:
        health_value = extract_health_from_screenshot(screenshot)
        if health_value is not None:
            print(f"Health value: {health_value}")
        else:
            print("Failed to extract health value.")
    else:
        print("Failed to capture screenshot.")

def print_mouse_coordinates():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Mouse coordinates: ({x}, {y})", end="\r")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped mouse coordinates tracking.")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        info_pid = int(sys.argv[1])
        print(f"Monitoring health for PID {info_pid}")
        region = (148, 71, 200, 200)  # Replace with the actual region coordinates (left, top, right, bottom)
        report_health(info_pid, region)
        print("Press Ctrl+C to stop.")
        print_mouse_coordinates()
    else:
        print("Usage: python parse_game.py <info_pid>")
        sys.exit(1)