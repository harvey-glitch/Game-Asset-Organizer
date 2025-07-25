import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from typing import Callable

class ProcessWindow():
    def __init__(self, parent: tk.Tk, folder_path: str, files: list[str], file_types: dict, on_btn_click: Callable[[str, str], None]):
        self.parent = parent  # reference to the parent window
        self.folder_path = folder_path  # path of the folder being organized
        self.files = files  # list of files to process
        self.file_types = file_types  # dictionary of file types and extensions
        self.on_btn_click = on_btn_click  # callback function for button click

        # UI component placeholders that will be initialized later in setup_ui
        self.label = None
        self.organize_btn = None
        self.total_txt = None
        self.text_area = None
        self.text_area = None
        self.selected_type = tk.StringVar()
        self.new_window = tk.Toplevel(parent)

        self.file_num = 0  # tracks the total number of found files

        self.setup_ui() # method to create the ui

    def setup_ui(self):
        # set the windows title and size
        self.new_window.title("Result Window")
        self.new_window.geometry("450x550")

        self.parent.attributes("-disabled", True)
        self.new_window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Header
        self.label = tk.Label(self.new_window, text=f"Scanned files in:\n{self.folder_path}", wraplength=430, pady=10)
        self.label.pack(fill="x")

        dropdown_frame = tk.Frame(self.new_window)
        dropdown_frame.pack(fill="x", padx=10, pady=(10, 0))

        # create a label to display the total files found
        self.total_txt = tk.Label(self.new_window, text=f"Total found files: {self.file_num}", anchor="w")
        self.total_txt.pack(fill="x", padx=10, pady=(10, 0))

        # create a label for drop down indicator
        dropdown_label = tk.Label(dropdown_frame, text="Filter by file type:", anchor="w")
        dropdown_label.pack(side="left")

        # create a dropdown using combo box
        self.selected_type.set("All") # set the dropdown default value to "All"
        options = ["All"] + list(self.file_types.keys()) # add options to the drop down
        dropdown = ttk.Combobox(dropdown_frame, textvariable=self.selected_type, values=options, state="readonly")
        dropdown.pack(side="left", expand=True, fill="x")
        dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_file_display())

        # create a scrollable test area for displaying all files per selected category
        self.text_area = scrolledtext.ScrolledText(self.new_window, width=60, height=20)
        self.text_area.pack(padx=10, pady=(5, 0), fill="both", expand=True)

        self.update_file_display()  # Populate text area

        # lastly, creata a button for organizing the file
        self.organize_btn = tk.Button(self.new_window, text="Organize files", bg="green", fg="white", command=self.organize_file)
        self.organize_btn.pack(pady=25)

    def update_file_display(self):
        self.text_area.configure(state="normal") # enabling editing on the text area
        self.text_area.delete("1.0", tk.END) # clear its content first

        selected = self.selected_type.get() # store the value of selectec option in the drop down
        filtered_files = []

        # if the dropdown option is set to "All" display all files
        if selected == "All":
            filtered_files = self.files

        # if set to "Others" display unrecognized files
        elif selected == "Others":
            # try to get all know file extensions
            known_exts = [ext for exts in self.file_types.values() for ext in exts]

            for file in self.files:
                if not any(file.lower().endswith(ext) for ext in known_exts):
                    filtered_files.append(file)

        # if set to specific option (images, audios etc)
        else:
            # get all accepted extension in selected category
            allowed_exts = self.file_types.get(selected, [])
            for file in self.files:
                if any(file.lower().endswith(ext) for ext in allowed_exts):
                    filtered_files.append(file)
        
        # Update text and count
        self.file_num = 0
        for file in filtered_files:
            self.text_area.insert(tk.END, f"{file}\n")
            self.file_num += 1

        # make sure to disable the text area after populating it
        self.text_area.configure(state="disabled")

        # display the total files found in selected category
        self.total_txt.configure(text=f"Total found files: {self.file_num}")

    def on_close(self):
        self.parent.attributes("-disabled", False)
        self.new_window.destroy()

    def on_exit(self):
        self.new_window.destroy()

    def organize_file(self):
        selected = self.selected_type.get()
        self.on_btn_click(self.folder_path, selected)
