import tkinter as tk
from tkinter import filedialog
from typing import Callable

class MainWindowControl():
    def __init__(self, root : tk.Tk, on_folder_selected: Callable[[str], None]):
        self.root = root
        self.label = tk.Label
        self.button = tk.Button
        
        self.setup_ui()

        self.on_folder_selected = on_folder_selected

    def setup_ui(self):
        self.root.title("Game File Organizer")
        self.root.geometry("300x150")

        # create a header for window
        self.label = tk.Label(self.root, text="Select a folder to scan and organize", pady=10)
        self.label.pack()

        # create a button for selecting folder to scan and organize
        self.button = tk.Button(self.root, text="Select folder", bg= "green", fg="white", command=self.select_folder)
        self.button.pack(pady=20)

    def on_exit(self):
        self.root.attributes("-disabled", False)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.on_folder_selected(folder_path)
        