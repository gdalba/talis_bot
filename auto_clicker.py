from time import sleep
from mouse import get_game_hwnd, left, right
import pygetwindow
import win32api
import win32con


leader_hwnd = None
leader_title = None
teammate_1_hwnd = None
teammate_1_title = None
teammate_2_hwnd = None
teammate_2_title = None
teammate_3_hwnd = None
teammate_3_title = None
teammate_4_hwnd = None
teammate_4_title = None


# Define a list of specific clicks with their coordinates
clicks = [
    (1280, 48), # reset view
    (719,50) # cwc entry (view reset)
]

#clicks with 0 or 1 for left and right click, and order of clicks
routine_clicks = [
    (1280, 48, 0), #reset view
    (719, 50, 0), #cwc entry (view reset)
    (719, 50, 1), #cwc open menu
    (318, 418, 0) #cwc enter
]


def testing_clicker():
        # Get the game window handle
    hwnd = get_game_hwnd()
    if not hwnd:
        print("Game window not found.")
        return

    print(f"Game window handle: {hwnd}")
    # Execute the clicks on the game window
    for x, y in clicks:
        print(f"Clicking at ({x}, {y})")
        left(hwnd, x, y)
        sleep(1)  # Add a delay between clicks if needed

def debug_mode():
    #do it recursively (until the user wants to stop)
    while True:
        hwnd = get_game_hwnd()
        if not hwnd:
            print("Game window not found.")
            return
        
        print(f"Game window handle: {hwnd}")

        # ask for coordinates
        
        #cwc()
        
        print("X:")
        x = input()
        if x.lower() == 'q':  # Allow quitting with 'q'
            break
        x = int(x)
        print("Y:")
        y = input()
        if y.lower() == 'q':  # Allow quitting with 'q'
            break
        y = int(y)
        
        print(f"Clicking at ({x}, {y})")
        left(hwnd, x, y)
        
        print("\nEnter 'q' at any time to quit, or continue with new coordinates.")

def routine_mode():
    # Get the game window handle
    hwnd = get_game_hwnd()
    if not hwnd:
        print("Game window not found.")
        return

    print(f"Game window handle: {hwnd}")
    # Execute the clicks on the game window    
    for x, y, click_type in routine_clicks:
        if click_type == 0:
            print(f"Clicking at ({x}, {y})")
            left(hwnd, x, y)
            sleep(1)
        elif click_type == 1:
            print(f"Clicking at ({x}, {y})")
            right(hwnd, x, y)
            sleep(1)  # Add a delay between clicks if needed

def send_key(hwnd, key):
    """Simulates pressing a key on the specified window."""
    if key.lower() == 'esc':
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_ESCAPE, 0)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_ESCAPE, 0)
        return
    else:
        win32api.SendMessage(hwnd, win32con.WM_KEYDOWN, ord(key.upper()), 0)
        win32api.SendMessage(hwnd, win32con.WM_KEYUP, ord(key.upper()), 0)

def define_teammates():
    global leader_hwnd, leader_title, teammate_1_hwnd, teammate_1_title, teammate_2_hwnd, teammate_2_title, teammate_3_hwnd, teammate_3_title, teammate_4_hwnd, teammate_4_title

    hwnd_list = []
    hwnd = ''
    
    # Get all open windows if name has "Bot Master" in it
    window_info = []  # List to store [hwnd, title] pairs
    
    for window in pygetwindow.getWindowsWithTitle("Bot Master"):
        hwnd_list.append(window._hWnd)
        window_info.append([window._hWnd, window.title])


    #for hwnd, title in window_info:
    #    print(f"HWND: {hwnd}, Title: {title}") 

    teammates = {
        "Leader": "monkito - Bot Master",
        "Teammate 1": "CJShy - Bot Master",
        "Teammate 2": "CJSky - Bot Master",
        "Teammate 3": "CJStar - Bot Master",
        "Teammate 4": "CjSpace - Bot Master"
    }

    window_handles = {}  # Dictionary to store hwnd and titles

    for x, j in window_info:
        #print(f"testing hwnd and window: {x} {j}")
        
        for role, expected_title in teammates.items():
            if expected_title in j:
                window_handles[role] = {"hwnd": x, "title": j}
                print(f"{role} handle: {x}")
                print(f"{role} title: {j}")
                break  # Stop checking other roles once a match is found

    # Check if all teammates were found
    if len(window_handles) == len(teammates):
        print("All game windows found:")
        for role, info in window_handles.items():
            print(f"{role}: {info}")
    else:
        print("Some game windows were not found.")

    
    leader_hwnd = window_handles.get("Leader", {}).get("hwnd")
    leader_title = window_handles.get("Leader", {}).get("title")
    teammate_1_hwnd = window_handles.get("Teammate 1", {}).get("hwnd")
    teammate_1_title = window_handles.get("Teammate 1", {}).get("title")
    teammate_2_hwnd = window_handles.get("Teammate 2", {}).get("hwnd")
    teammate_2_title = window_handles.get("Teammate 2", {}).get("title")
    teammate_3_hwnd = window_handles.get("Teammate 3", {}).get("hwnd")
    teammate_3_title = window_handles.get("Teammate 3", {}).get("title")
    teammate_4_hwnd = window_handles.get("Teammate 4", {}).get("hwnd")
    teammate_4_title = window_handles.get("Teammate 4", {}).get("title")



def cwc():      
    define_teammates()
    # step 1 = create team
    send_key(leader_hwnd, 'f')

    # Define team coordinates
    team_coords = [
        {"member_hwnd": teammate_1_hwnd, "member_title": teammate_1_title, "right_click": (577, 245), "invite_click": (597, 290)},
        {"member_hwnd": teammate_2_hwnd, "member_title": teammate_2_title, "right_click": (577, 255), "invite_click": (597, 300)},
        {"member_hwnd": teammate_3_hwnd, "member_title": teammate_3_title, "right_click": (577, 265), "invite_click": (597, 310)},
        {"member_hwnd": teammate_4_hwnd, "member_title": teammate_4_title, "right_click": (577, 285), "invite_click": (597, 330)}
    ]
    team_coords_and_leader = [
        {"member_hwnd": leader_hwnd, "member_title": leader_title, "right_click": (577, 245), "invite_click": (597, 290)},
        {"member_hwnd": teammate_1_hwnd, "member_title": teammate_1_title, "right_click": (577, 245), "invite_click": (597, 290)},
        {"member_hwnd": teammate_2_hwnd, "member_title": teammate_2_title, "right_click": (577, 255), "invite_click": (597, 300)},
        {"member_hwnd": teammate_3_hwnd, "member_title": teammate_3_title, "right_click": (577, 265), "invite_click": (597, 310)},
        {"member_hwnd": teammate_4_hwnd, "member_title": teammate_4_title, "right_click": (577, 285), "invite_click": (597, 330)}
    ]

    # Common accept coordinates for all team members
    accept_coords = (658, 400)

    # First block: Right click on all members
    for member in team_coords:
        x, y = member["right_click"]
        print(f"Right clicking at ({x}, {y})")
        right(leader_hwnd, x, y)
        sleep(0.5)

        x, y = member["invite_click"]
        print(f"Clicking invite at ({x}, {y})")
        left(leader_hwnd, x, y)
        sleep(0.5)

    sleep(1)  # Pause between blocks

    # Third block: All members accept invites
    for member in team_coords:
        x, y = accept_coords
        print(f"Accepting invite for member {member['member_hwnd']} ({member['member_title']}) at ({x}, {y})")
        left(member["member_hwnd"], x, y)
        sleep(0.5)

    # Close team menu
    send_key(leader_hwnd, 'esc')

    for member in team_coords_and_leader:
        # Reset view
        print(f"Resetting view for member {member['member_hwnd']} ({member['member_title']})")
        left(member["member_hwnd"], 1280, 48)
        sleep(1)

        sleep(1)  # Pause between blocks

        # Open CWC menu
        print(f"Opening CWC menu for member {member['member_hwnd']} ({member['member_title']})")
        right(member["member_hwnd"], 719, 50)
        sleep(1)

        sleep(1)  # Pause between blocks

    for member in team_coords_and_leader:
        print(f"Entering CWC for member {member['member_hwnd']} ({member['member_title']})")
        # Enter CWC
        left(member["member_hwnd"], 339, 380)
        sleep(1)

    '''
    CONTINUE HERE!!!!!!!!!!
    '''


    #(1280, 48, 0), #reset view
    #(719, 50, 0), #cwc entry (view reset)
    #(719, 50, 1), #cwc open menu
    #(318, 418, 0) #cwc enter
        '''
        for clicks in routine_clicks:
            x, y, click_type = clicks
            if click_type == 0:
                print(f"Clicking at ({x}, {y})")
                left(member["member_hwnd"], x, y)
                sleep(1)
            elif click_type == 1:
                print(f"Clicking at ({x}, {y})")
                right(member["member_hwnd"], x, y)
                sleep(1)
        '''






'''    print(f"Game window handle: {hwnd}")
    # Execute the clicks on the game window
    for x, y in clicks:
        print(f"Clicking at ({x}, {y})")
        left(hwnd, x, y)
        sleep(1)  # Add a delay between clicks if needed'''

def main():    
    #choose the mode
    print("Choose the mode:")
    print("1. Auto Clicker")
    print("2. Debug Mode")
    print("3. Routine Mode.")
    print("4. CWC")    
    choice = input("Enter your choice: ")
    if choice == '1':
        testing_clicker()
    elif choice == '2':
        debug_mode()
    elif choice == '3':
        routine_mode()
    elif choice == '4':
        cwc()
    else:
        print("Invalid choice.")
        return

if __name__ == "__main__":
    main()