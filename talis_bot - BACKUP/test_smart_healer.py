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

cords_team = {
    "yourself": [0, 0],
    "member_1": [0, 0],
    "member_2": [0, 0],
    "member_3": [0, 0],
    "member_4": [0, 0],
}

cords_move = {
    "stop": [0, 0],
    "right": [0, 0],
    "left": [0, 0],
    "up": [0, 0],
    "down": [0, 0],
    "minimize": [0, 0],
    "mouse_reset": [0, 0],
}

cords_game = {
    "deleter_ok": [0, 0],
    "jackstraw_ok": [0, 0],
    "revive_ok": [0, 0],
    "loot": [0, 0],
    "pickup": [0, 0],
    "reset_view": [0, 0],
    "world_map": [0, 0]
}

cords_bc = {
    "surrounds": [0, 0],
    "surr_input": [0, 0],
    "first_link": [0, 0],
    "rich_man": [0, 0],
    "rich_sell": [0, 0],
    "initial_slot": [0, 0],
    "ok_confirm": [0, 0],
    "sell_button": [0, 0],
    "purchase": [0, 0],
    "buy_charm": [0, 0],
    "buy_item": [0, 0],
    "fairy_teleport": [0, 0],
    "din_woods": [0, 0],
    "block_list": [0, 0],
    "team_name": [0, 0],
    "team_up": [0, 0],
    "photo": [0, 0],
    "leave_team": [0, 0],
    "team_info": [0, 0],
    "team_join": [0, 0],
    "skull": [0, 0],
    "skull_enter": [0, 0],
    "altar_npc": [0, 0],
    "altar_enter": [0, 0],
    "npc_leave": [0, 0],
    "exit": [0, 0],
    "treasure_box": [0, 0],
    "pick_up": [0, 0],
    "center_screen": [0, 0]

}


def set_coords_by_resolution(resolution):
    """Configura as coordenadas globais com base na resolução."""
    global cords_team, cords_move, cords_game

    if resolution == "800*600":
        cords_move.update({
            "stop": [695, 115],
            "right": [696, 115],
            "left": [694, 115],
            "up": [695, 114],
            "down": [695, 116],
            "minimize": [771, 127],
            "mouse_reset": [679, 180],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [327, 249],
            "jackstraw_ok": [325, 251],
            "revive_ok": [404, 384],
            "loot": [400, 300],
            "pickup": [450, 476],
            "reset_view": [643, 58],
            "world_map": [542, 23]
        })

    elif resolution == "1024*768":
        cords_move.update({
            "stop": [919, 115],
            "right": [920, 115],
            "left": [918, 115],
            "up": [919, 114],
            "down": [919, 116],
            "minimize": [995, 126],
            "mouse_reset": [900, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [439, 335],
            "jackstraw_ok": [439, 336],
            "revive_ok": [515, 469],
            "loot": [505, 390],
            "pickup": [447, 479],
            "reset_view": [866, 58],
            "world_map": [654, 105]
        })

        cords_bc.update({
            "surrounds": [975, 58],
            "surr_input": [590, 540],
            "first_link": [299, 261],
            "rich_man": [345, 258],  # 240, 327
            "rich_sell": [271, 429],
            "initial_slot": [450, 327],
            "ok_confirm": [439, 333],
            "sell_button": [478, 713],
            "purchase": [282, 395],
            "buy_charm": [194, 327],
            "buy_item": [182, 712],
            "fairy_teleport": [466, 361],
            "din_woods": [299, 590],
            "block_list": [705, 192],
            "team_name": [571, 253],
            "team_up": [603, 323],
            "photo": [46, 49],
            "leave_team": [88, 98],
            "team_info": [15, 494],
            "team_join": [437, 335],
            "skull": [470, 405],
            "skull_enter": [258, 364],
            "altar_npc": [370, 380],  # 380, 320
            "altar_enter": [308, 336],
            "npc_leave": [513, 302],
            "exit": [301, 364],
            "treasure_box": [520, 269],
            "pick_up": [450, 478],
            "center_screen": [510, 370]
        })

    elif resolution == "1280*720":
        cords_move.update({
            "stop": [1175, 115],
            "right": [1176, 115],
            "left": [1174, 115],
            "up": [1175, 114],
            "down": [1175, 116],
            "minimize": [1253, 128],
            "mouse_reset": [1158, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [567, 311],
            "jackstraw_ok": [567, 311],
            "revive_ok": [643, 445],
            "loot": [631, 363],
            "pickup": [447, 479],
            "reset_view": [1123, 59],
            "world_map": [786, 83]

        })

    elif resolution == "1280*800":
        cords_move.update({
            "stop": [1175, 115],
            "right": [1176, 115],
            "left": [1174, 115],
            "up": [1175, 114],
            "down": [1175, 116],
            "minimize": [1253, 128],
            "mouse_reset": [1158, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [30, 210],
            "member_2": [30, 285],
            "member_3": [30, 365],
            "member_4": [30, 445],
        })

        cords_game.update({
            "deleter_ok": [568, 350],
            "jackstraw_ok": [565, 351],
            "revive_ok": [643, 484],
            "loot": [640, 402],
            "pickup": [447, 479],
            "reset_view": [1124, 58],
            "world_map": [787, 120]
        })

    elif resolution == "1920*1080":
        cords_move.update({
            "stop": [1815, 115],
            "right": [1816, 115],
            "left": [1814, 115],
            "up": [1815, 114],
            "down": [1815, 116],
            "minimize": [1891, 128],
            "mouse_reset": [1798, 182],
        })

        cords_team.update({
            "yourself": [45, 45],
            "member_1": [25, 205],
            "member_2": [25, 285],
            "member_3": [25, 365],
            "member_4": [25, 445],
        })

        cords_game.update({
            "deleter_ok": [887, 480],
            "jackstraw_ok": [888, 483],
            "revive_ok": [964, 614],
            "loot": [960, 533],
            "pickup": [447, 479],
            "reset_view": [1761, 58],
            "world_map": [1106, 253]
        })

    else:
        raise ValueError(f"Resolução não suportada: {resolution}")

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
    resolution = int(sys.argv[5])  # Screen resolution (e.g., '1280*720')

    set_coords_by_resolution(resolution)  # Set coordinates based on your screen resolution

    healer = Healer(info_pid=info_pid, heal_key_1=heal_key_1, heal_key_2=heal_key_2, mana_key=mana_key, heal_duration=15)
    healer.start_healer(regions=cords_team)
