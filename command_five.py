import tkinter as tk
import psutil
import win32gui
import win32api
import win32con
import win32process
import subprocess
import time
import pyautogui

class CommandFive:
    def __init__(self, root):
        self.root = root
        self.root.title("Command Team")
        
        self.info_pid_label = tk.Label(root, text="Info PID (main char):")
        self.info_pid_label.pack(pady=5)
        self.info_pid_entry = tk.Entry(root)
        self.info_pid_entry.pack(pady=5)
        
        self.t1_pid_label = tk.Label(root, text="Teammate 1:")
        self.t1_pid_label.pack(pady=5)
        self.t1_pid_entry = tk.Entry(root)
        self.t1_pid_entry.pack(pady=5)

        self.t2_pid_label = tk.Label(root, text="Teammate 2:")
        self.t2_pid_label.pack(pady=5)
        self.t2_pid_entry = tk.Entry(root)
        self.t2_pid_entry.pack(pady=5)

        self.t3_pid_label = tk.Label(root, text="Teammate 3:")
        self.t3_pid_label.pack(pady=5)
        self.t3_pid_entry = tk.Entry(root)
        self.t3_pid_entry.pack(pady=5)

        self.t4_pid_label = tk.Label(root, text="Teammate 4:")
        self.t4_pid_label.pack(pady=5)
        self.t4_pid_entry = tk.Entry(root)
        self.t4_pid_entry.pack(pady=5)

        self.key_cmd_label = tk.Label(root, text="Command to send (all):")
        self.key_cmd_label.pack(pady=5)
        self.key_cmd_entry = tk.Entry(root)
        self.key_cmd_entry.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Send command", command=self.start_cmd)
        self.start_button.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh PIDs", command=self.refresh_pid_list)
        self.refresh_button.pack(pady=10)

        self.identify_elements = tk.Button(root, text="Screenshot and identify leader", command=self.screenshot_and_identify)
        self.identify_elements.pack(pady=10)

        self.automate_leader_finding = tk.Button(root, text="Automate leader finding", command=self.automate_leader_finding)
        self.automate_leader_finding.pack(pady=10)
        
        self.info_label = tk.Label(root, text="Detected PIDs (client.exe):")
        self.info_label.pack(pady=10)
        
        self.pid_list_text = tk.Text(root, height=10, width=50)
        self.pid_list_text.pack(pady=10)
        
        self.process = None
        
        # Initial refresh of PIDs
        self.refresh_pid_list()

    def screenshot_and_identify(self):
        info_pid = self.info_pid_entry.get()
        if info_pid:
            info_pid = int(info_pid)
            # Run parse_game.py with the info_pid, iterating over t1, t2, t3, t4
            teammates = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
            for teammate_pid in teammates:
                if teammate_pid:
                    subprocess.Popen(["python", "find_leader.py", str(teammate_pid)])
                    time.sleep(2)       
            
            #subprocess.Popen(["python", "find_leader.py", str(info_pid)])
        else:
            print("Please enter the Info PID.")   

    def automate_leader_finding(self):
        info_pid = self.info_pid_entry.get()
        if info_pid:
            info_pid = int(info_pid)
            teammates = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
            for teammate_pid in teammates:
                if teammate_pid:
                    teammate_pid = int(teammate_pid)
                    window_title = self.get_window_title(teammate_pid)
                    if window_title:
                        hwnd = win32gui.FindWindow(None, window_title)
                        if hwnd:
                            win32gui.SetForegroundWindow(hwnd)
                            #time.sleep(1)  # Wait for the window to be in the foreground
                            for _ in range(4):  # Assuming there are at most 4 teammates to cycle through
                                process = subprocess.Popen(["python", "find_leader.py", str(teammate_pid)],
                                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                 text=True
                                )
                                stdout, stderr = process.communicate()
                                if "Team Leader found" in stdout:
                                    print(f"Team Leader found for PID {teammate_pid}.")
                                    print(f"Sending 'p' key to window title: {window_title}")
                                    pyautogui.press('p')
                                    break
                                else:
                                    print(f"Team Leader not found for PID {teammate_pid}.")
                                    print("Cycling through teammates.")
                                    pyautogui.press('tab')
                                    #time.sleep(1)  # Wait for the tab key to take effect
                            else:
                                continue  # Continue to the next teammate if the loop completes without breaking
                            break  # Break the outer loop if the leader is found
                            

        else:
            print("Please enter the Info PID.")






    def refresh_pid_list(self):
        # Clear previous widgets from the PID list section
        for widget in self.pid_list_text.winfo_children():
            widget.destroy()

        # Get all PIDs for processes named 'client.exe'
        pid_name_pairs = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name'])
                if pinfo['name'].lower() == 'client.exe':
                    window_title = self.get_window_title(pinfo['pid'])
                    pid_name_pairs.append((pinfo['pid'], window_title))
            except psutil.NoSuchProcess:
                pass

        # Display PIDs and add buttons
        if pid_name_pairs:
            for pid, window_title in pid_name_pairs:
                frame = tk.Frame(self.pid_list_text)
                frame.pack(anchor="w", pady=2, padx=5)

                label = tk.Label(frame, text=f"PID: {pid}, Window Title: {window_title}")
                label.pack(side="left", padx=5)

                # Buttons to assign PIDs to entry fields
                tk.Button(frame, text="Set as Info", command=lambda p=pid: self.info_pid_entry.insert(0, p)).pack(side="left", padx=5)
                tk.Button(frame, text="Set as T1", command=lambda p=pid: self.t1_pid_entry.insert(0, p)).pack(side="left", padx=5)
                tk.Button(frame, text="Set as T2", command=lambda p=pid: self.t2_pid_entry.insert(0, p)).pack(side="left", padx=5)
                tk.Button(frame, text="Set as T3", command=lambda p=pid: self.t3_pid_entry.insert(0, p)).pack(side="left", padx=5)
                tk.Button(frame, text="Set as T4", command=lambda p=pid: self.t4_pid_entry.insert(0, p)).pack(side="left", padx=5)
        else:
            tk.Label(self.pid_list_text, text="No processes found for client.exe.").pack(anchor="w", pady=5, padx=5)

    def start_cmd(self):
        info_pid = self.info_pid_entry.get()
        t1_pid = self.t1_pid_entry.get()
        t2_pid = self.t2_pid_entry.get()
        t3_pid = self.t3_pid_entry.get()
        t4_pid = self.t4_pid_entry.get()
        cmd_key = self.key_cmd_entry.get()
        
        if info_pid and t1_pid and t2_pid and t3_pid and t4_pid and cmd_key:
            info_pid = int(info_pid)
            t1_pid = int(t1_pid)
            t2_pid = int(t2_pid)
            t3_pid = int(t3_pid)
            t4_pid = int(t4_pid)
            cmd_key = str(cmd_key)
            
            info_window_title = self.get_window_title(info_pid)
            t1_window_title = self.get_window_title(t1_pid)
            t2_window_title = self.get_window_title(t2_pid)
            t3_window_title = self.get_window_title(t3_pid)
            t4_window_title = self.get_window_title(t4_pid)
            
            print(f"Info Window Title: {info_window_title}")
            
            # Send the command to all teammates
            for window_title in [t1_window_title, t2_window_title, t3_window_title, t4_window_title]:
                print(f"Sending command '{cmd_key}' to window title: {window_title}")
                subprocess.Popen(["python", "send_cmd_to_all.py", info_window_title, window_title, cmd_key])

            print("Command sent.")
        else:
            print("Please enter all PIDs and the command.")
    
    def get_window_title(self, pid):
        def enum_windows_callback(hwnd, param):
            try:
                _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
                if window_pid == param['pid']:
                    window_text = win32gui.GetWindowText(hwnd)
                    if window_text:  # Ignore windows without titles
                        param['title'] = window_text
                        return False  # Stop enumeration
            except Exception as e:
                print(f"Error accessing hwnd: {hwnd}, error: {e}")
            return True

        param = {'pid': pid, 'title': "N/A"}
        try:
            win32gui.EnumWindows(enum_windows_callback, param)
        except Exception as e:
            print(f"Error enumerating windows: {e}")
        return param['title']

if __name__ == "__main__":

    root = tk.Tk()
    app = CommandFive(root)
    root.mainloop()