import tkinter as tk
from tkinter import filedialog
from typing import Callable

# responsible for creating an default app interface
class HomeUI():
    # ---- INITIALIZATION ----
    def __init__(self, root : tk.Tk, event: Callable[[str], None]):
        self.root = root # reference to the parent window
        self.event = event # ca
        self.create_main_interface()

    # ---- INTERFACE METHODS ----
    def create_main_interface(self):
        self.create_window()
        self.create_header()
        self.create_button()

    def create_window(self):
        self.root.title("Game Asset Organizer")
        self.root.geometry("300x150")

    def create_header(self):
        label = tk.Label(self.root, text="Select a folder to scan and organize")
        label.pack(pady=10)
        
    def create_button(self):      
        button = tk.Button(self.root, text="Select Folder", bg="green", fg="white", command=self.select_folder)
        button.pack(pady=20, expand=True)

    # ---- CUSTOM METHODS ----
    def on_exit(self):
        self.root.attributes("-disabled", False)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.event(folder)
        