import win32api
import win32con
import win32gui
import win32process
import time
import sys
from pynput.keyboard import Controller
import pytesseract
from PIL import Image
import pyautogui

pytesseract.pytesseract.tesseract_cmd = r'E:\Tesseract-OCR\tesseract.exe'

game_regions = {
        
        "Health": (0, 200, 200, 60),
        "Mana": (0, 200, 200, 60),
        }

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
        time.sleep(1)

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
    # improve OCR accuracy by applying image processing techniques
    gray_image = gray_image.point(lambda p: p > 190 and 255)  # Thresholding
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    extracted_text = pytesseract.image_to_string(gray_image, config=custom_config)    
    return extracted_text.strip()

def monitor_game_elements(pid, regions):
    """
    Monitor and capture multiple game elements based on defined regions.
    Args:
        pid (int): Process ID of the game.
        regions (dict): Dictionary mapping labels to region coordinates.
    """
    for label, region in regions.items():
        print(f"Capturing '{label}'... for PID {pid}")
        screenshot = capture_region(pid, region)
        if screenshot:
            #screenshot.show()  # Display the screenshot for debugging
            extracted_text = extract_text_from_image(screenshot)
            if extracted_text:
                print(f"{label}: {extracted_text}")
                if extracted_text == "786": #need to change if leader is different
                    print(f"Heal: '{label}'.")                    
            else:
                print(f"No text found in '{label}'.")
        else:
            print(f"Failed to capture '{label}'.")

class Healer:
    def __init__(self, info_pid, heal_key_1='6', heal_key_2='5', mana_key='9', heal_duration=15):
        self.info_pid = info_pid

        if heal_key_1.lower() != 'none':
            print(f"Using heal key 1: {heal_key_1}")
            self.heal_key_1 = heal_key_1  # First key in the routine (e.g., '6')
        elif heal_key_1.lower() == 'none':
            print("No heal key 1 provided.")
            self.heal_key_1 = None
            
        self.heal_key_2 = heal_key_2  # Second key in the routine (e.g., '5')
        self.mana_key = mana_key
        self.heal_duration = heal_duration  # Duration for the secondary key (e.g., 10-15 seconds)
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

    def start_healer(self,regions):
        """Runs the healing routine."""
        self.setup_window()
        
        if self.info_hwnd:
            #print(f"Starting healer for PID {self.info_pid} with routine keys '{self.heal_key_1}' and '{self.heal_key_2}'.")
            while True:
                monitor_game_elements(self.info_pid, regions)
                if self.heal_key_1:
                # Press heal_key_1
                    print(f"Pressing key '{self.heal_key_1}'.")
                    self.send_key(self.info_hwnd, self.heal_key_1)
                    time.sleep(0.5)

                print(f"Pressing mana key '{self.mana_key}'.")
                self.send_key(self.info_hwnd, self.mana_key)
                time.sleep(0.5)

                # Press heal_key_2 for the specified duration
                print(f"Pressing key '{self.heal_key_2}' for {self.heal_duration} seconds.")
                end_time = time.time() + self.heal_duration
                while time.time() < end_time:
                    self.send_key(self.info_hwnd, self.heal_key_2)
                    time.sleep(0.5)  # Adjust repeat frequency if necessary

                # Return to heal_key_1
                #print(f"Returning to key '{self.heal_key_1}'.")
                if not self.heal_key_1:
                    continue
                else:
                    self.send_key(self.info_hwnd, self.heal_key_1) # Return to heal_key_1
                    time.sleep(0.5) 
        else:
            print("Exiting: No valid game window found.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python healer.py <info_pid> <heal_key_1> <heal_key_2> <mana_key>")
        sys.exit(1)

    info_pid = int(sys.argv[1])
    heal_key_1 = str(sys.argv[2])  # First key in the routine (e.g., '6')
    heal_key_2 = str(sys.argv[3])  # Second key in the routine (e.g., '5')
    mana_key = str(sys.argv[4])  # Key to check for mana (e.g., '7')

    healer = Healer(info_pid=info_pid, heal_key_1=heal_key_1, heal_key_2=heal_key_2, mana_key=mana_key, heal_duration=15)
    healer.start_healer(regions=game_regions)
