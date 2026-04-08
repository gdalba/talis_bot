import tkinter as tk
import subprocess
import os
import psutil
import win32gui
import win32process

class HealerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Healer Control")
        
        self.info_pid_label = tk.Label(root, text="Info PID (main char):")
        self.info_pid_label.pack(pady=5)
        self.info_pid_entry = tk.Entry(root)
        self.info_pid_entry.pack(pady=5)
        
        self.command_pid_label = tk.Label(root, text="Command PID (healer):")
        self.command_pid_label.pack(pady=5)
        self.command_pid_entry = tk.Entry(root)
        self.command_pid_entry.pack(pady=5)

        self.key_healing_label = tk.Label(root, text="Command to send (healer):")
        self.key_healing_label.pack(pady=5)
        self.key_healing_entry = tk.Entry(root)
        self.key_healing_entry.pack(pady=5)

        self.smart_button = tk.Button(root, text="Smart bot", command=self.smart_button)
        self.smart_button.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Healer", command=self.start_healer)
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Stop Healer", command=self.stop_healer)
        self.stop_button.pack(pady=10)
        
        self.info_label = tk.Label(root, text="Info Window Title: N/A\nCommand Window Title: N/A")
        self.info_label.pack(pady=10)
        
        self.process = None

    def smart_button(self):
        if self.process is None:
            print("Smart bot")
            info_pid = self.info_pid_entry.get()
            info_window_title = self.get_window_title(info_pid)
            self.process = subprocess.Popen(["python", "parse_game.py", str(info_pid)])
        return

    def start_healer(self):
        if self.process is None:
            print("Healer started.")
            info_pid = self.info_pid_entry.get()
            command_pid = self.command_pid_entry.get()
            key_healing = self.key_healing_entry.get()
            info_window_title = self.get_window_title(info_pid)
            command_window_title = self.get_window_title(command_pid)
            self.process = subprocess.Popen(["python", "healer.py", str(info_pid), str(command_pid), key_healing])
            self.info_label.config(text=f"Info Window Title: {info_window_title}\nCommand Window Title: {command_window_title}")
        return

    def stop_healer(self):
        if self.process is not None:
            self.process.terminate()
            self.process = None
            self.info_label.config(text="Info Window Title: N/A\nCommand Window Title: N/A")
            print("Healer stopped.")

    def update_info(self, info_window_title, command_window_title):
        self.info_label.config(text=f"Info Window Title: {info_window_title}\nCommand Window Title: {command_window_title}")

    def get_window_title(self, pid):
        def enum_windows_callback(hwnd, pid):
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid == pid:
                self.window_title = win32gui.GetWindowText(hwnd)
                return False
            return True

        self.window_title = "N/A"
        win32gui.EnumWindows(enum_windows_callback, pid)
        return self.window_title

if __name__ == "__main__":
    root = tk.Tk()
    app = HealerApp(root)
    root.mainloop()