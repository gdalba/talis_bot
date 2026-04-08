import win32gui
import win32process
import time
import pyautogui
import pytesseract
from PIL import Image
import sys

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

def get_window_handle_and_rect(pid):
    """
    Get the handle and bounding rectangle of a window belonging to the specified process ID (PID).
    Args:
        pid (int): Process ID of the target application.
    Returns:
        tuple: Window handle and rectangle coordinates (left, top, right, bottom).
    """
    window_info = {"handle": None, "rect": None}

    def enum_windows_callback(hwnd, target_pid):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == target_pid:
            window_info["handle"] = hwnd
            window_info["rect"] = win32gui.GetWindowRect(hwnd)
            return False  # Stop enumeration when a match is found

    win32gui.EnumWindows(enum_windows_callback, pid)
    return window_info["handle"], window_info["rect"]

def capture_region(pid, region):
    """
    Capture a screenshot of a specific region relative to the game window.
    Args:
        pid (int): Process ID of the target application.
        region (tuple): Region coordinates (left, top, right, bottom) relative to the game window.
    Returns:
        Image: Screenshot of the specified region.
    """
    window_handle, window_rect = get_window_handle_and_rect(pid)
    if window_handle and window_rect:
        # Bring the window to the foreground and wait for it to stabilize
        win32gui.SetForegroundWindow(window_handle)
        time.sleep(2)

        # Calculate absolute region coordinates
        left, top, _, _ = window_rect
        absolute_region = (
            left + region[0],
            top + region[1],
            left + region[2],
            top + region[3]
        )
        return pyautogui.screenshot(region=absolute_region)
    else:
        print(f"No window found for PID {pid}.")
        return None

def extract_text_from_image(image):
    """
    Extract text from an image using OCR.
    Args:
        image (Image): Screenshot image to process.
    Returns:
        str: Extracted text from the image.
    """
    gray_image = image.convert("L")  # Convert to grayscale for better OCR accuracy
    extracted_text = pytesseract.image_to_string(gray_image)
    return extracted_text.strip()

def monitor_game_elements(pid, regions):
    """
    Monitor and capture multiple game elements based on defined regions.
    Args:
        pid (int): Process ID of the game.
        regions (dict): Dictionary mapping labels to region coordinates.
    """
    for label, region in regions.items():
        print(f"Capturing '{label}'...")
        screenshot = capture_region(pid, region)
        if screenshot:
            screenshot.show()  # Display the screenshot for debugging
            extracted_text = extract_text_from_image(screenshot)
            print(f"{label}: {extracted_text}")
        else:
            print(f"Failed to capture '{label}'.")

def print_mouse_coordinates():
    """
    Print real-time mouse coordinates to help define regions on the screen.
    Use this tool to determine the (x, y) coordinates for regions of interest.
    """
    try:
        print("Press CTRL+C to stop capturing mouse coordinates.")
        while True:
            x, y = pyautogui.position()
            print(f"Mouse coordinates: ({x}, {y})")
            time.sleep(1)  # Adjust the delay as needed
    except KeyboardInterrupt:
        print("Mouse coordinate capture stopped.")

def main():
    """
    Main function to monitor a game's screen elements or capture mouse coordinates.
    Run the script with a PID to monitor elements or use coordinate mode for region discovery.
    """
    if len(sys.argv) == 2:
        pid = int(sys.argv[1])
        print(f"Monitoring game screen for PID {pid}")

        # Define regions for game elements (left, top, right, bottom relative to the window)
        game_regions = {
            "Health Bar": (70, 40, 270, 90),
        }

        # Monitor defined game regions
        monitor_game_elements(pid, game_regions)
    else:
        print("Usage: python parse_game.py <PID>")
        print("To identify regions, use the mouse coordinate capture tool.")
        print_mouse_coordinates()

if __name__ == "__main__":
    main()
