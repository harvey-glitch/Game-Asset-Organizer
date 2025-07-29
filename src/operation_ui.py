import tkinter as tk
from app_utility import AppUtility
from tkinter import ttk
from tkinter import scrolledtext
from typing import Callable

# responsible for creating an interface for main operation
class OperationUI():
    # ---- INITIALIZATION ----
    def __init__(self, root: tk.Tk, folder_path: str, file_types: dict, click_event: Callable[[str, str], None]):
        self.root = root
        self.folder_path = folder_path
        self.click_event = click_event
        self.file_types = file_types

        self.file_count = 0
        self.file_count_text = None
        self.file_list_text = None
        self.category = tk.StringVar()
        self.new_window = tk.Toplevel(root)

        self.create_main_interface() # method to create the ui

    # ----  INTERFACE METHODS ----
    def create_main_interface(self):
        self.create_window()
        self.create_header()
        self.create_dropdown()
        self.create_file_list()
        self.create_button()

        self.root.attributes("-disabled", True)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_window(self):
        # set the windows title and size
        self.new_window.title("Result Window")
        self.new_window.geometry("450x550")

    def create_header(self):
        header_text = tk.Label(self.new_window, text=f"Scanned files in:\n{self.folder_path}")
        header_text.pack(fill="x", pady=10)

    def create_dropdown(self):
        # create a base frame for dropdown
        dropdown_frame = tk.Label(self.new_window)
        dropdown_frame.pack(fill="x", padx=10, pady=(10, 0))

        # display the total files based on selected dropdown option
        self.file_count_text = tk.Label(self.new_window, text=f"Total found files: {self.file_count}", anchor="w")
        self.file_count_text.pack(fill="x", padx=10, pady=(10, 0))
        
        # create a label for dropdown prompt
        dropdown_label = tk.Label(dropdown_frame, text="Filter by file type:", anchor="w")
        dropdown_label.pack(side="left")

        # create a dropdown using combo box
        self.category.set("All") # set the dropdown default value to "All"
        options = ["All"] + list(self.file_types.keys()) # add options to the drop down
        dropdown = ttk.Combobox(dropdown_frame, textvariable=self.category, values=options, state="readonly")
        dropdown.pack(side="left", expand=True, fill="x")
        dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_file_list())

    def create_file_list(self):
        # create a scrollable test area for displaying all files per selected category
        self.file_list_text = scrolledtext.ScrolledText(self.new_window, width=60, height=20)
        self.file_list_text.pack(padx=10, pady=(5, 0), fill="both", expand=True)

        self.update_file_list()

    def create_button(self):
        # creata a button for organizing the file
        self.organize_btn = tk.Button(
            self.new_window, text="Organize files", bg="green", fg="white", command=self.organize_file)
        self.organize_btn.pack(pady=25)

    # --- CUSTOM METHODS ----
    def update_file_list(self):
        self.file_list_text.configure(state="normal") # enabling editing on the text area
        self.file_list_text.delete("1.0", tk.END) # clear its content first

        file_category = self.category.get()
        filtered_files = AppUtility.get_files_by_category(self.folder_path, file_category)

        # Update text and count
        self.file_count = 0
        for file in filtered_files:
            self.file_list_text.insert(tk.END, f"{file}\n")
            self.file_count += 1

        # make sure to disable the text area after populating it
        self.file_list_text.configure(state="disabled")

        # display the total files found in selected category
        self.file_count_text.configure(text=f"Total found files: {self.file_count}")

    def on_close(self):
        self.root.attributes("-disabled", False)
        self.new_window.destroy()

    def on_exit(self):
        self.new_window.destroy()

    def organize_file(self):
        selected = self.category.get()
        self.click_event(self.folder_path, selected)
