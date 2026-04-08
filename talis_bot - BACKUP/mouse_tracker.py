import pyautogui
import time
import os

def clear_console():
    # Clear the console based on the operating system
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def clear_line():
    # Use \r to return to the start of the line
    print('\r', end='')

def absolute_mouse_position():
    try:
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            
            # Create the position text
            position_str = f'Mouse Position: X: {x}, Y: {y}'
            
            # Clear the previous line and print the new position
            clear_console()
            print(position_str)
            
            # Small delay to prevent high CPU usage
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print('\nProgram terminated by user')

def relative_mouse_position():
    try:
        # Get the initial mouse position
        initial_x, initial_y = pyautogui.position()
        
        while True:
            # Get the current mouse position
            x, y = pyautogui.position()
            
            # Calculate the relative position
            rel_x = x - initial_x
            rel_y = y - initial_y
            
            # Create the position text
            position_str = f'Mouse Position: X: {rel_x}, Y: {rel_y}'
            
            # Clear the previous line and print the new position
            #clear_line()
            #print(position_str, end='', flush=True)
            clear_console()
            print(position_str)
            # Small delay to prevent high CPU usage
            time.sleep(0.1)
        
    except KeyboardInterrupt:
        print('\nProgram terminated by user')

def main():
    # Ask if want relative or absolute
    print("Do you want to track the mouse position in relative or absolute coordinates?")
    print("1. Absolute")
    print("2. Relative")
    choice = input("Enter your choice: ")

    if choice == '1':
        absolute_mouse_position()
    elif choice == '2':
        relative_mouse_position()
    else:
        print("Invalid choice. Exiting.")

if __name__ == '__main__':
    main()