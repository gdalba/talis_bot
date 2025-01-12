import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import psutil
import win32gui
import win32api
import win32con
import win32process
import subprocess
import time
import pyautogui
import os
import signal 

class CommandFive:
    def __init__(self, root):        
        self.style = Style(theme='morph')
        self.root = self.style.master
        self.root.title("Command Team")       

        team_frame = tk.Frame(root)
        team_frame.pack(pady=10)

        self.info_pid_label = tk.Label(team_frame, text="Info PID (main char):")
        self.info_pid_label.pack(side=tk.LEFT, pady=5)
        self.info_pid_entry = tk.Entry(team_frame)
        self.info_pid_entry.pack(side=tk.LEFT, pady=5)
        
        self.t1_pid_label = tk.Label(team_frame, text="Teammate 1:")
        self.t1_pid_label.pack(side=tk.LEFT, pady=5)
        self.t1_pid_entry = tk.Entry(team_frame)
        self.t1_pid_entry.pack(side=tk.LEFT, pady=5)

        self.t2_pid_label = tk.Label(team_frame, text="Teammate 2:")
        self.t2_pid_label.pack(side=tk.LEFT, pady=5)
        self.t2_pid_entry = tk.Entry(team_frame)
        self.t2_pid_entry.pack(side=tk.LEFT, pady=5)
        
        team_frame_2 = tk.Frame(root)
        team_frame_2.pack(pady=10)

        self.t3_pid_label = tk.Label(team_frame_2, text="Teammate 3:")
        self.t3_pid_label.pack(side=tk.LEFT, pady=5)
        self.t3_pid_entry = tk.Entry(team_frame_2)
        self.t3_pid_entry.pack(side=tk.LEFT, pady=5)

        self.t4_pid_label = tk.Label(team_frame_2, text="Teammate 4:")
        self.t4_pid_label.pack(side=tk.LEFT, pady=5)
        self.t4_pid_entry = tk.Entry(team_frame_2)
        self.t4_pid_entry.pack(side=tk.LEFT, pady=5)

        send_command_frame = tk.Frame(root)
        send_command_frame.pack(pady=5)

        self.key_cmd_label = tk.Label(send_command_frame, text="Command to send (all):")
        self.key_cmd_label.pack(side=tk.LEFT, pady=5)
        self.key_cmd_entry = tk.Entry(send_command_frame)
        self.key_cmd_entry.pack(side=tk.LEFT, pady=5)

        self.start_button = ttk.Button(send_command_frame, text="Send command", command=self.start_cmd)
        self.start_button.pack(side=tk.LEFT, pady=10)

        '''self.start_mount_button = ttk.Button(send_command_frame, text="K", command=self.start_k_cmd)
        self.start_mount_button.pack(side=tk.LEFT, pady=10)        

        self.start_follow_button = ttk.Button(send_command_frame, text="P", command=self.start_p_cmd)
        self.start_follow_button.pack(side=tk.LEFT, pady=10)        

        self.stop_button = ttk.Button(send_command_frame, text="Stop P", command=self.stop_p_cmd)
        self.stop_button.pack(side=tk.LEFT, pady=10)'''

        '''self.identify_elements = ttk.Button(leader_finding_frame, text="Screenshot and identify leader", command=self.screenshot_and_identify, bootstyle="info")
        self.identify_elements.pack(side=tk.LEFT, pady=10)'''

        '''self.automate_leader_finding = ttk.Button(leader_finding_frame, text="Automate leader finding", command=self.automate_leader_finding, bootstyle="primary")
        self.automate_leader_finding.pack(side=tk.LEFT, pady=10)'''

        healer_frame = tk.Frame(root)
        healer_frame.pack(pady=10)

        healer_1_pid_label = tk.Label(healer_frame, text="Healer PID 1")
        healer_1_pid_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.healer_1_pid_entry = tk.Entry(healer_frame)
        self.healer_1_pid_entry.grid(row=0, column=1, padx=5, pady=5)

        healer_2_pid_label = tk.Label(healer_frame, text="Healer PID 2")
        healer_2_pid_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.healer_2_pid_entry = tk.Entry(healer_frame)
        self.healer_2_pid_entry.grid(row=1, column=1, padx=5, pady=5)

        healer_3_pid_label = tk.Label(healer_frame, text="Healer PID 3")
        healer_3_pid_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.healer_3_pid_entry = tk.Entry(healer_frame)
        self.healer_3_pid_entry.grid(row=2, column=1, padx=5, pady=5)

        monk_pid_label = tk.Label(healer_frame, text="Monk PID")
        monk_pid_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.monk_pid_entry = tk.Entry(healer_frame)
        self.monk_pid_entry.grid(row=3, column=1, padx=5, pady=5)

        wiz_1_pid_label = tk.Label(healer_frame, text="Wizard PID 1")
        wiz_1_pid_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.wiz_1_pid_entry = tk.Entry(healer_frame)
        self.wiz_1_pid_entry.grid(row=4, column=1, padx=5, pady=5)

        wiz_2_pid_label = tk.Label(healer_frame, text="Wizard PID 2")
        wiz_2_pid_label.grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.wiz_2_pid_entry = tk.Entry(healer_frame)
        self.wiz_2_pid_entry.grid(row=3, column=3, padx=5, pady=5)

        sin_pid_label = tk.Label(healer_frame, text="Sin PID")
        sin_pid_label.grid(row=4, column=2, padx=5, pady=5, sticky="w")
        self.sin_pid_entry = tk.Entry(healer_frame)
        self.sin_pid_entry.grid(row=4, column=3, padx=5, pady=5)       


        # Healing Key 1
        tk.Label(healer_frame, text="Healing Key 1 (regen/shield/none):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.healing_key_entry = tk.Entry(healer_frame)
        self.healing_key_entry.insert(0, "6")  # Default to '6'
        self.healing_key_entry.grid(row=0, column=3, padx=5, pady=5)

        # Healing Key 2
        tk.Label(healer_frame, text="Healing Key 2 (main heal):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.healing_key_entry_2 = tk.Entry(healer_frame)
        self.healing_key_entry_2.insert(0, "5")  # Default to '5'
        self.healing_key_entry_2.grid(row=1, column=3, padx=5, pady=5)

        # Mana Regeneration Key
        tk.Label(healer_frame, text="Mana Regeneration Key:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.mana_regeneration_entry = tk.Entry(healer_frame)
        self.mana_regeneration_entry.insert(0, "9")  # Default to '0'
        self.mana_regeneration_entry.grid(row=2, column=3, padx=5, pady=5)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        '''self.healing_start = ttk.Button(button_frame, text="Start Healer", command=self.start_healer)
        self.healing_start.pack(side=tk.LEFT, pady=5)

        #next button is immediately besides Start healer
        self.healing_stop = ttk.Button(button_frame, text="Stop Healer", command=self.stop_healer)
        self.healing_stop.pack(side=tk.LEFT, pady=5)'''

        healing_toggle_frame = ttk.Frame(root)
        healing_toggle_frame.pack(pady=10)

        self.is_healing = False
        self.healing_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start Healer", 
            bootstyle="success", 
            command=self.toggle_healer
        )
        self.healing_toggle.pack(side=tk.LEFT, pady=5)

        self.is_monk = False
        self.monk_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start Monk", 
            bootstyle="success", 
            command=self.toggle_monk
        )        
        self.monk_toggle.pack(side=tk.LEFT, pady=5)

        self.is_sin = False
        self.sin_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start Sin", 
            bootstyle="success", 
            command=self.toggle_sin
        )
        self.sin_toggle.pack(side=tk.LEFT, pady=5)

        self.is_following = False
        self.follow_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start Follow", 
            bootstyle="success", 
            command=self.toggle_follow
        )
        self.follow_toggle.pack(side=tk.LEFT, pady=10)

        self.is_BOSSwiz = False

        self.BOSSwiz_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start BOSSwiz", 
            bootstyle="success", 
            command=self.toggle_BOSSwizard
        )
        self.BOSSwiz_toggle.pack(side=tk.LEFT, pady=10)
        
        self.is_AOEwiz = False
        self.AOEwiz_toggle = ttk.Button(
            healing_toggle_frame, 
            text="Start AOEwiz", 
            bootstyle="success", 
            command=self.toggle_AOEwiz
        )
        self.AOEwiz_toggle.pack(side=tk.LEFT, pady=10)

        self.refresh_button = ttk.Button(healing_toggle_frame, text="Refresh PIDs", command=self.refresh_pid_list, bootstyle="secondary")
        self.refresh_button.pack(side=tk.LEFT, pady=10)

        self.hop_on_mount_button = ttk.Button(healing_toggle_frame, text="Mount", command=self.start_k_cmd, bootstyle="info")
        self.hop_on_mount_button.pack(side=tk.LEFT, pady=10)

        '''self.monk_start = ttk.Button(button_frame, text="Start Monk", command=self.start_monk)
        self.monk_start.pack(side=tk.LEFT, pady=5)

        self.monk_stop = ttk.Button(button_frame, text="Stop Monk", command=self.stop_monk)
        self.monk_stop.pack(side=tk.LEFT, pady=5)'''

        self.info_label = tk.Label(root, text="Detected PIDs (client.exe):")
        self.info_label.pack(pady=10)
        
        self.pid_list_text = tk.Text(root, height=10, width=50)
        self.pid_list_text.pack(pady=10)

        
        self.process = None
        
        # Initial refresh of PIDs
        self.refresh_pid_list()

        # Initialize subprocess tracking
        self.healer_processes = []
        self.monk_process = None
        self.follow_command_process = []
        self.follow_processes = None
        self.AOEwiz_processes = []        
        self.BOSSwiz_processes = []
        self.sin_process = None

    def toggle_healer(self):
         # Toggle the healing state
        self.is_healing = not self.is_healing
        
        # Update button text and style dynamically
        if self.is_healing:
            self.healing_toggle.config(text="Stop Healer", bootstyle="danger")
            self.start_healer()
        else:
            self.healing_toggle.config(text="Start Healer", bootstyle="success")
            self.stop_healer()

    def toggle_monk(self):
        # Toggle the monk state
        self.is_monk = not self.is_monk
        
        # Update button text and style dynamically
        if self.is_monk:
            self.monk_toggle.config(text="Stop Monk", bootstyle="danger")
            self.start_monk()
        else:
            self.monk_toggle.config(text="Start Monk", bootstyle="success")
            self.stop_monk()

    def toggle_follow(self):
    # Toggle the follow state
        self.is_following = not self.is_following

        # Update button text and style dynamically
        if self.is_following:
            self.follow_toggle.config(text="Stop Follow", bootstyle="danger")
            self.start_p_cmd()
        else:
            self.follow_toggle.config(text="Start Follow", bootstyle="success")
            self.stop_p_cmd()

    def toggle_AOEwiz(self):
        self.is_AOEwiz = not self.is_AOEwiz

        # Update button text and style dynamically
        if self.is_AOEwiz:
            self.AOEwiz_toggle.config(text="Stop AOEwiz", bootstyle="danger")
            self.start_AOEwiz()
        else:
            self.AOEwiz_toggle.config(text="Start AOEwiz", bootstyle="success")
            self.stop_AOEwiz()

    def toggle_BOSSwizard(self):
        self.is_BOSSwiz = not self.is_BOSSwiz

        # Update button text and style dynamically
        if self.is_BOSSwiz:
            self.BOSSwiz_toggle.config(text="Stop BOSSwiz", bootstyle="danger")
            self.start_BOSSwiz()
        else:
            self.BOSSwiz_toggle.config(text="Start BOSSwiz", bootstyle="success")
            self.stop_BOSSwiz()

    def toggle_sin(self):
        self.is_sin = not self.is_sin

        # Update button text and style dynamically
        if self.is_sin:
            self.sin_toggle.config(text="Stop Sin", bootstyle="danger")
            self.start_sin()
        else:
            self.sin_toggle.config(text="Start Sin", bootstyle="success")
            self.stop_sin()

    def start_monk(self):
        monk_pid = self.monk_pid_entry.get()
        if monk_pid:
            try:
                self.monk_process = subprocess.Popen(
                    ["python", "monk.py", monk_pid],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Started monk for PID {monk_pid}.")
            except Exception as e:
                print(f"Error starting monk: {e}")

    def stop_monk(self):
        if self.monk_process:
            try:
                os.kill(self.monk_process.pid, signal.SIGTERM)
                print(f"Monk with PID {self.monk_process.pid} stopped.")
            except Exception as e:
                print(f"Error stopping monk with PID {self.monk_process.pid}: {e}")
            self.monk_process = None
        else:
            print("No monk process is running.")

    def start_healer(self):
        """Starts the healer subprocess."""
        self.healer_processes = []
        healer1_pid = self.healer_1_pid_entry.get()
        healer2_pid = self.healer_2_pid_entry.get()
        healer3_pid = self.healer_3_pid_entry.get()
        heal_key = self.healing_key_entry.get()
        heal_key_2 = self.healing_key_entry_2.get()
        mana_key = self.mana_regeneration_entry.get()

        if healer1_pid and healer2_pid and heal_key and heal_key_2 and mana_key:
            try:                
                healers = [healer1_pid, healer2_pid, healer3_pid]
                for healer_pid in healers:
                    if healer_pid:  
                # Start healer.py as a subprocess
                        self.healer_process = subprocess.Popen(
                            ["python", "healer.py", str(healer_pid), heal_key, heal_key_2, mana_key],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started healer with heal key '{heal_key}' and '{heal_key_2} and mana key {mana_key}'.")
                        self.healer_processes.append(self.healer_process)
            except Exception as e:
                print(f"Error starting healer: {e}")
        elif healer1_pid or healer2_pid and heal_key and heal_key_2 and mana_key:
            try:
                healers = [healer1_pid]
                for healer_pid in healers:
                    if healer_pid:
                        # Start healer.py as a subprocess
                        self.healer_process = subprocess.Popen(
                            ["python", "healer.py", str(healer_pid), heal_key, heal_key_2, mana_key],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started healer for PID {healer1_pid} with heal key '{heal_key}' and '{heal_key_2} and mana key {mana_key}'.")
                        self.healer_processes.append(self.healer_process)
            except Exception as e:
                print(f"Error starting healer: {e}")
        elif healer2_pid and heal_key and heal_key_2 and mana_key:
            try:
                healers = [healer2_pid]
                for healer_pid in healers:
                    if healer_pid:
                        # Start healer.py as a subprocess
                        self.healer_process = subprocess.Popen(
                            ["python", "healer.py", str(healer_pid), heal_key, heal_key_2, mana_key],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started healer for PID {healer2_pid} with heal key '{heal_key}' and '{heal_key_2} and mana key {mana_key}'.")
                        self.healer_processes.append(self.healer_process)
            except Exception as e:
                print(f"Error starting healer: {e}")
        elif healer3_pid and heal_key and heal_key_2 and mana_key:
            try:
                healers = [healer3_pid]
                for healer_pid in healers:
                    if healer_pid:
                        # Start healer.py as a subprocess
                        self.healer_process = subprocess.Popen(
                            ["python", "healer.py", str(healer_pid), heal_key, heal_key_2, mana_key],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started healer for PID {healer3_pid} with heal key '{heal_key}' and '{heal_key_2} and mana key {mana_key}'.")
                        self.healer_processes.append(self.healer_process)
            except Exception as e:
                print(f"Error starting healer: {e}")                
        else:
            print("Please provide both Info PID and Healing Key.")         

    def stop_healer(self):
        """Stops all running healer subprocesses."""
        if self.healer_processes:
            #print(self.healer_processes)
            for process in self.healer_processes:
                try:
                    os.kill(process.pid, signal.SIGTERM)
                    print(f"Healer with PID {process.pid} stopped.")
                except Exception as e:
                    print(f"Error stopping healer with PID {process.pid}: {e}")
            
            # Clear the process list after stopping
            self.healer_processes.clear()
            print("All healers stopped.")
        else:
            print("No healer processes are running.")

    def start_sin(self):
        sin_pid = self.sin_pid_entry.get()
        if sin_pid:
            try:
                self.sin_process = subprocess.Popen(
                    ["python", "sin.py", sin_pid],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                print(f"Started sin for PID {sin_pid}.")
            except Exception as e:
                print(f"Error starting sin: {e}")

    def stop_sin(self):
        if self.sin_process:
            try:
                os.kill(self.sin_process.pid, signal.SIGTERM)
                print(f"Sin with PID {self.sin_process.pid} stopped.")
            except Exception as e:
                print(f"Error stopping sin with PID {self.sin_process.pid}: {e}")
            self.sin_process = None
        else:
            print("No sin process is running.")
            
    def start_AOEwiz(self):
        self.AOEwiz_processes = []
        wiz1_pid = self.wiz_1_pid_entry.get()
        wiz2_pid = self.wiz_2_pid_entry.get()
        print(wiz1_pid)
        print(wiz2_pid)
        if wiz1_pid and wiz2_pid:
            try:
                wizs = [wiz1_pid, wiz2_pid]
                for wiz_pid in wizs:
                    if wiz_pid:
                        # Start AOEwiz.py as a subprocess
                        self.AOEwiz_process = subprocess.Popen(
                            ["python", "AOEwiz.py", str(wiz_pid)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started AOEwiz for PID {wiz_pid}.")
                        self.AOEwiz_processes.append(self.AOEwiz_process)
            except Exception as e:
                print(f"Error starting AOEwiz: {e}")
        elif wiz1_pid or wiz2_pid:
            if wiz1_pid:
                try:
                    wizs = [wiz1_pid]
                    for wiz_pid in wizs:
                        if wiz_pid:
                            # Start AOEwiz.py as a subprocess
                            self.AOEwiz_process = subprocess.Popen(
                                ["python", "AOEwiz.py", str(wiz_pid)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            print(f"Started AOEwiz for PID {wiz1_pid}.")
                            self.AOEwiz_processes.append(self.AOEwiz_process)
                except Exception as e:
                    print(f"Error starting AOEwiz: {e}")
            elif wiz2_pid:
                try:
                    wizs = [wiz2_pid]
                    for wiz_pid in wizs:
                        if wiz_pid:
                            # Start AOEwiz.py as a subprocess
                            self.AOEwiz_process = subprocess.Popen(
                                ["python", "AOEwiz.py", str(wiz_pid)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            print(f"Started AOEwiz for PID {wiz2_pid}.")
                            self.AOEwiz_processes.append(self.AOEwiz_process)
                except Exception as e:
                    print(f"Error starting AOEwiz: {e}")        
        else:
            print("Please provide both wiz PID.")

    def stop_AOEwiz(self):
        """Stops all running AOEwiz subprocesses."""
        if self.AOEwiz_processes:
            for process in self.AOEwiz_processes:
                try:
                    os.kill(process.pid, signal.SIGTERM)
                    print(f"AOEwiz with PID {process.pid} stopped.")
                except Exception as e:
                    print(f"Error stopping AOEwiz with PID {process.pid}: {e}")
            
            # Clear the process list after stopping
            self.AOEwiz_processes.clear()
            print("All AOEwiz stopped.")
        else:
            print("No AOEwiz processes are running.")

    def start_BOSSwiz(self):
        self.BOSSwiz_processes = []
        wiz1_pid = self.wiz_1_pid_entry.get()
        wiz2_pid = self.wiz_2_pid_entry.get()
        if wiz1_pid and wiz2_pid:
            try:
                wizs = [wiz1_pid, wiz2_pid]
                for wiz_pid in wizs:
                    if wiz_pid:
                        # Start AOEwiz.py as a subprocess
                        self.BOSSwiz_process = subprocess.Popen(
                            ["python", "BOSSwiz.py", str(wiz_pid)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        print(f"Started BOSSwiz for PID {wiz_pid}.")
                        self.BOSSwiz_processes.append(self.BOSSwiz_process)
            except Exception as e:
                print(f"Error starting BOSSwiz: {e}")
        elif wiz1_pid or wiz2_pid:
            if wiz1_pid:
                try:
                    wizs = [wiz1_pid]
                    for wiz_pid in wizs:
                        if wiz_pid:
                            # Start AOEwiz.py as a subprocess
                            self.BOSSwiz_process = subprocess.Popen(
                                ["python", "BOSSwiz.py", str(wiz_pid)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            print(f"Started BOSSwiz for PID {wiz1_pid}.")
                            self.BOSSwiz_processes.append(self.BOSSwiz_process)
                except Exception as e:
                    print(f"Error starting BOSSwiz: {e}")
            elif wiz2_pid:
                try:
                    wizs = [wiz2_pid]
                    for wiz_pid in wizs:
                        if wiz_pid:
                            # Start AOEwiz.py as a subprocess
                            self.BOSSwiz_process = subprocess.Popen(
                                ["python", "BOSSwiz.py", str(wiz_pid)],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            print(f"Started BOSSwiz for PID {wiz2_pid}.")
                            self.BOSSwiz_processes.append(self.BOSSwiz_process)
                except Exception as e:
                    print(f"Error starting BOSSwiz: {e}")
        else:
            print("Please provide both wiz PID.")
    
    def stop_BOSSwiz(self):
        """Stops all running BOSSwiz subprocesses."""
        if self.BOSSwiz_processes:
            for process in self.BOSSwiz_processes:
                try:
                    os.kill(process.pid, signal.SIGTERM)
                    print(f"BOSSwiz with PID {process.pid} stopped.")
                except Exception as e:
                    print(f"Error stopping BOSSwiz with PID {process.pid}: {e}")
            
            # Clear the process list after stopping
            self.BOSSwiz_processes.clear()
            print("All BOSSwiz stopped.")
        else:
            print("No BOSSwiz processes are running.")

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
                            checked_pids = {int(teammate_pid): False for teammate_pid in teammates if teammate_pid}
                            for _ in range(len(checked_pids)):
                                    
                                if checked_pids[teammate_pid]:
                                    continue  # Skip if already checked

                                print(f"Checking for Team Leader for PID {teammate_pid}.")
                                process = subprocess.Popen(["python", "find_leader.py", str(teammate_pid)],
                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                        text=True)
                                stdout, stderr = process.communicate()
                                if "Team Leader found" in stdout:
                                    print(f"Team Leader found for PID {teammate_pid}.")
                                    print(f"Sending 'p' key to window title: {window_title}")
                                    pyautogui.press('p')
                                    continue  # move on to the next teammate
                                else:
                                    print(f"Team Leader not found for PID {teammate_pid}.")
                                    print("Cycling through teammates.")
                                    pyautogui.press('tab')                                    
                                    time.sleep(1)  # Wait for the tab key to take effect
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

        # Configure grid weights for alignment
        self.pid_list_text.columnconfigure(0, weight=1)  # For PID and Window Title
        self.pid_list_text.columnconfigure(1, weight=0)  # For Role Dropdown
        self.pid_list_text.columnconfigure(2, weight=0)  # For Action Dropdown

        # Display PIDs with dropdown menus in a neat grid
        if pid_name_pairs:
            for row, (pid, window_title) in enumerate(pid_name_pairs):
                # PID and Window Title Label
                label = tk.Label(
                    self.pid_list_text,
                    text=f"PID: {pid}, Window Title: {window_title}",
                    anchor="w",
                    justify="left"
                )
                label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

                # Dropdown for assigning roles
                role_options = ["Set as Info", "Set as T1", "Set as T2", "Set as T3", "Set as T4"]
                role_combo = ttk.Combobox(self.pid_list_text, state="readonly", values=role_options, width=18)
                role_combo.grid(row=row, column=1, padx=5, pady=5)

                # Dropdown for additional actions
                action_options = ["Set as H1", "Set as H2", "Set as H3", "Set as Monk", "Set as W1", "Set as W2", "Set as Sin"]
                action_combo = ttk.Combobox(self.pid_list_text, state="readonly", values=action_options, width=18)
                action_combo.grid(row=row, column=2, padx=5, pady=5)

                # Bind events to both dropdowns
                role_combo.bind(
                    "<<ComboboxSelected>>",
                    lambda event, pid=pid, combo=role_combo: self.assign_pid_to_entry(pid, combo.get())
                )
                action_combo.bind(
                    "<<ComboboxSelected>>",
                    lambda event, pid=pid, action_combo=action_combo: self.assign_pid_to_entry(pid, action_combo.get())
                )
        else:
            tk.Label(self.pid_list_text, text="No processes found for client.exe.").grid(row=0, column=0, sticky="w", padx=10, pady=5)

    def assign_pid_to_entry(self, pid, action):
        # Handle the PID assignment logic to the appropriate entry field
        if action == "Set as Info":
            self.info_pid_entry.delete(0, tk.END)
            self.info_pid_entry.insert(0, pid)
        elif action == "Set as T1":
            self.t1_pid_entry.delete(0, tk.END)
            self.t1_pid_entry.insert(0, pid)
        elif action == "Set as T2":
            self.t2_pid_entry.delete(0, tk.END)
            self.t2_pid_entry.insert(0, pid)
        elif action == "Set as T3":
            self.t3_pid_entry.delete(0, tk.END)
            self.t3_pid_entry.insert(0, pid)
        elif action == "Set as T4":
            self.t4_pid_entry.delete(0, tk.END)
            self.t4_pid_entry.insert(0, pid)
        elif action == "Set as W1":
            self.wiz_1_pid_entry.delete(0, tk.END)
            self.wiz_1_pid_entry.insert(0, pid)
        elif action == "Set as W2":
            self.wiz_2_pid_entry.delete(0, tk.END)
            self.wiz_2_pid_entry.insert(0, pid)
        elif action == "Set as H1":
            self.healer_1_pid_entry.delete(0, tk.END)
            self.healer_1_pid_entry.insert(0, pid)
        elif action == "Set as H2":
            self.healer_2_pid_entry.delete(0, tk.END)
            self.healer_2_pid_entry.insert(0, pid)
        elif action == "Set as H3":
            self.healer_3_pid_entry.delete(0, tk.END)
            self.healer_3_pid_entry.insert(0, pid)
        elif action == "Set as Monk":
            self.monk_pid_entry.delete(0, tk.END)
            self.monk_pid_entry.insert(0, pid)
        elif action == "Set as Sin":
            self.sin_pid_entry.delete(0, tk.END)
            self.sin_pid_entry.insert(0, pid)

    def start_k_cmd(self):
        info_pid = self.info_pid_entry.get()
        cmd_key = 'k'
        if info_pid and cmd_key:
            info_pid = int(info_pid)
            cmd_key = str(cmd_key)
        
            info_window_title = self.get_window_title(info_pid)
            #print(f"Info Window Title: {info_window_title}")
            
            teammate_pids = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
            for teammate_pid in teammate_pids:
                if teammate_pid:
                    teammate_pid = int(teammate_pid)
                    window_title = self.get_window_title(teammate_pid)
                    print(f"Sending command '{cmd_key}' to window title: {window_title}")
                    subprocess.Popen(["python", "send_cmd_to_all.py", info_window_title, window_title, cmd_key])

    def start_p_cmd(self):
        info_pid = self.info_pid_entry.get()
        cmd_key = 'p'
        
        if info_pid and cmd_key:
            info_pid = int(info_pid)
            cmd_key = str(cmd_key)

            
            info_window_title = self.get_window_title(info_pid)
            self.follow_processes = []
            teammate_pids = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
            for teammate_pid in teammate_pids:
                if teammate_pid:
                    teammate_pid = int(teammate_pid)
                    window_title = self.get_window_title(teammate_pid)
                    print(f"Sending command '{cmd_key}' to window title: {window_title}")
                    process = subprocess.Popen(["python", "send_cmd_to_all.py", info_window_title, window_title, cmd_key],
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    text=True)
                    self.follow_processes.append(process)
                    print(f"Started follow command for PID {teammate_pid}.")

    def stop_p_cmd(self):
        """Stops all running healer subprocesses."""
        if self.follow_processes:
            print(self.follow_processes)
            for process in self.follow_processes:
                try:
                    os.kill(process.pid, signal.SIGTERM)
                    print(f"Command p with PID {process.pid} stopped.")                    
                except Exception as e:
                    print(f"Error stopping command p with PID {process.pid}: {e}")
            
            # Clear the process list after stopping
            self.follow_processes.clear()
            print("All follow commands stopped.")
        else:
            print("No follow commands are running.")                

    def start_cmd(self):
        info_pid = self.info_pid_entry.get()
        cmd_key = self.key_cmd_entry.get()
        
        if info_pid and cmd_key:
            info_pid = int(info_pid)
            cmd_key = str(cmd_key)

            if cmd_key == "p":
                info_window_title = self.get_window_title(info_pid)
                self.follow_processes = []
                teammate_pids = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
                for teammate_pid in teammate_pids:
                    if teammate_pid:
                        teammate_pid = int(teammate_pid)
                        window_title = self.get_window_title(teammate_pid)
                        print(f"Sending command '{cmd_key}' to window title: {window_title}")
                        process = subprocess.Popen(["python", "send_cmd_to_all.py", info_window_title, window_title, cmd_key],
                                                       stdout=subprocess.PIPE,
                                                       stderr=subprocess.PIPE,
                                                       text=True)
                        self.follow_processes.append(process)
                        print(f"Started follow command for PID {teammate_pid}.")
            else:           
                info_window_title = self.get_window_title(info_pid)
                print(f"Info Window Title: {info_window_title}")
                
                teammate_pids = [self.t1_pid_entry.get(), self.t2_pid_entry.get(), self.t3_pid_entry.get(), self.t4_pid_entry.get()]
                for teammate_pid in teammate_pids:
                    if teammate_pid:
                        teammate_pid = int(teammate_pid)
                        window_title = self.get_window_title(teammate_pid)
                        print(f"Sending command '{cmd_key}' to window title: {window_title}")
                        subprocess.Popen(["python", "send_cmd_to_all.py", info_window_title, window_title, cmd_key])

            print("Command sent.")            
            
        else:
            print("Please enter the Info PID and the command.")
    
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