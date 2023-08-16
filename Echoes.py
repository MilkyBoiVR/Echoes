import tkinter as tk
from tkinter import PhotoImage, Menu, filedialog
from tkinter import ttk
import subprocess
import pyautogui
import time
import os
import json
from PIL import Image, ImageTk
import sys
import ctypes
import win32gui

class MilkyBoiVREchoesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MilkyBoiVR Echoes")
        self.root.iconbitmap("appicon.ico")
        self.root.attributes("-topmost", True)  # Make the window always on top

        # Hide the console window
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

        # Load background image
        self.bg_image = Image.open("background.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.root.geometry(f"{self.bg_image.width}x{self.bg_image.height}")

        self.load_settings()
        self.create_menu()
        self.create_preset_buttons()
        self.create_custom_section()
        self.create_settings_section()

    def load_settings(self):
        self.settings_file = "settings.json"

        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {
                "echovr_path": r"C:\Program Files\Oculus\Software\Software\ready-at-dawn-echo-arena\bin\win10\echovr.exe"
            }

    def save_settings(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file)

    def create_menu(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

    def create_preset_buttons(self):
        presets_frame = ttk.LabelFrame(self.root, text="PRESETS")
        presets_frame.pack(fill="both", padx=10, pady=10)

        button_frame = tk.Frame(presets_frame)
        button_frame.pack()

        self.commands = [
            ("3v3 Bots", "-level mpl_arena_a -gametype Echo_Arena_First_Match -region euw"),
            ("Private", "-level mpl_arena_a -gametype Echo_Arena_Private -region euw"),
            ("Social Lobby", "-level mpl_lobby_b2 -gametype social_2.0 -region euw")
        ]

        for label, args in self.commands:
            ttk.Button(button_frame, text=label, command=lambda cmd=f'"{self.settings["echovr_path"]}"', args=args: self.close_echovr_and_run(cmd, args)).pack(side="left", padx=5)

    def create_custom_section(self):
        custom_frame = ttk.LabelFrame(self.root, text="CUSTOM")
        custom_frame.pack(fill="both", padx=10, pady=10)

        self.level_var = tk.StringVar(value="")
        self.gametype_var = tk.StringVar(value="")

        level_dropdown = ttk.Combobox(custom_frame, textvariable=self.level_var, values=[
            "mpl_lobby_b2",
            "mpl_tutorial_lobby",
            "mpl_arena_a",
            "mpl_tutorial_arena",
            "mpl_combat_fission",
            "mpl_combat_combustion",
            "mpl_combat_dyson",
            "mpl_combat_gauss"
        ])
        level_dropdown.set("Select Level")
        level_dropdown.pack(pady=5)

        gametype_dropdown = ttk.Combobox(custom_frame, textvariable=self.gametype_var, values=[
            "Social_2.0_Private",
            "Social_2.0_NPE",
            "Social_2.0",
            "Echo_Arena",
            "Echo_Arena_Tournament",
            "Echo_Arena_Public_AI",
            "Echo_Arena_Practice_AI",
            "Echo_Arena_Private_AI",
            "Echo_Arena_First_Match",
            "Echo_Demo",
            "Echo_Demo_Public",
            "Echo_Arena_NPE",
            "Echo_Arena_Private",
            "Echo_Combat",
            "Echo_Combat_Tournament",
            "Echo_Combat_Private",
            "Echo_Combat_Public_AI",
            "Echo_Combat_Practice_AI",
            "Echo_Combat_Private_AI",
            "Echo_Combat_First_Match"
        ])
        gametype_dropdown.set("Select Gametype")
        gametype_dropdown.pack(pady=5)

        ttk.Button(custom_frame, text="START CUSTOM", command=self.start_custom).pack(pady=10)

    def create_settings_section(self):
        settings_frame = ttk.LabelFrame(self.root, text="SETTINGS")
        settings_frame.pack(fill="both", padx=10, pady=10)

        ttk.Button(settings_frame, text="CHANGE FILE PATH", command=self.change_file_path).pack(pady=5)
        self.file_path_label = ttk.Label(settings_frame, text=f"File Path: {self.settings['echovr_path']}", font=("Helvetica", 8))
        self.file_path_label.pack(pady=2)

    def start_custom(self):
        level = self.level_var.get()
        gametype = self.gametype_var.get()

        if level and gametype:
            cmd = f'"{self.settings["echovr_path"]}" -level {level} -gametype {gametype} -region euw'
            self.close_echovr_and_run(cmd)
        else:
            print("Please select a level and gametype.")

    def close_echovr_and_run(self, cmd, args=""):
        subprocess.run(["taskkill", "/f", "/im", "echovr.exe"], shell=True)  # Close Echo VR
        time.sleep(1)
        subprocess.Popen(f"{cmd} {args}", shell=True)  # Launch Echo VR

    def change_file_path(self):
        file_path = filedialog.askopenfilename(filetypes=[("EXE Files", "*.exe")])
        if file_path:
            self.settings["echovr_path"] = file_path
            self.save_settings()
            self.file_path_label.config(text=f"File Path: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MilkyBoiVREchoesApp(root)
    root.mainloop()
