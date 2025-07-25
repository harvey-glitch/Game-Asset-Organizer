from main_ui import MainWindowControl
from process_ui import ProcessWindow
import tkinter as tk
import os
import shutil
from tkinter import messagebox

# specified the accepted file extensions and thei corresponding folder
file_types = {
    "Images": [".png", ".jpg", ".jpeg"],
    "Models": [".fbx", ".glb", ".blend"],
    "Sounds": [".wav", ".mp3", ".ogg"],
    "Others": []
}

class MainAppControl():
    def __init__(self):
        # create and initialize variables
        self.root = tk.Tk()
        self.main_window = MainWindowControl(self.root, self.start_scanning)
        self.result_window = None # set to none as this will be use later on

    def start_scanning(self, folder_path):
        found_files = [] # stores all found files in the selecte folder

        # loop though all available files
        for files in os.listdir(folder_path):
            file_path = os.path.join(folder_path, files)
            # check if the path leads t an actual file before storing
            if os.path.isfile(file_path):
                found_files.append(files)

        # handle if the selected folder is empty
        if not found_files:
            messagebox.showinfo("No files!", "The selected folder might be empty.")
            return
        
        # display the result window which consist of a list of all found files, and organize button
        self.result_window = ProcessWindow(self.root, folder_path, found_files, file_types, self.start_organizing)

    def start_organizing(self, folder_path, dropdown_option):
        # make sure to disable the process window to avoid unnecessary interaction during the process
        self.result_window.new_window.attributes("-disabled", True)
        moved_files = 0 # tracks the total of files that moved

        # get the filtered files based on drop down option
        filtered_files = self.get_filtered_files(folder_path, dropdown_option)

        # loop through all available files in the filtered files
        for file_name, file_exts in filtered_files:
            # create a path for each files
            file_path = os.path.join(folder_path, file_name)
            moved_to_category = False # mark the file as not move yet

            # loop though file types dictionary, key and pairs
            for folder_name, exts in file_types.items():
                # check if the file extension is valid
                if file_exts in exts:
                    # create a folder
                    dest_folder = os.path.join(folder_path, folder_name)
                    os.makedirs(dest_folder, exist_ok=True)

                    # move the file
                    shutil.move(file_path, os.path.join(dest_folder, file_name))
                    moved_files += 1 # increment the number of files moved
                    moved_to_category = True # mark as move into the category
                    break

            # if not move to category, meaning the file is not recognized
            if not moved_to_category:
                # create a folder inside the selected folder
                other_folder = os.path.join(folder_path, "Others")
                os.makedirs(other_folder, exist_ok=True)

                # move the file
                shutil.move(file_path, os.path.join(other_folder, file_name))
                moved_files += 1  # increment the number of files moved

        # if theres no file is moved, meaning the category is empty, throw a warning message
        if moved_files == 0:
            messagebox.showinfo("No Files Found", f"No '{dropdown_option}' files were found to organize.")
            self.result_window.new_window.attributes("-disabled", False)
            return

        self.on_completed()

    def get_filtered_files(self, folder_path, dropdown_option):
        # get all known accepted file extensions
        known_exts = [ext for exts in file_types.values() for ext in exts]
        filtered_files = [] # empty array to store filtered files

        # dropdown option is not equall to ALL or others
        # store accepted file extentions based on selected category
        if dropdown_option not in ("All", "Others"):
            avail_exts = file_types.get(dropdown_option, [])

        # loop though selected folder and store all files in "file_name"
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # make sure were moving an actual file, not folder
            if not os.path.isfile(file_path):
                continue

            # separate the extensition from the file name example image.jpg -> ".jpg"
            _, file_ext = os.path.splitext(file_name)
            file_ext = file_ext.lower() # make sure the extension is in lower case

            # Filtering logic
            # if the option is Others, skipped all know extensions
            if dropdown_option == "Others":
                if file_ext in known_exts:
                    continue

            # skipped all files except on the selected category
            elif dropdown_option != "All":
                if file_ext not in avail_exts:
                    continue

            # populate the array based on filtered files
            filtered_files.append((file_name, file_ext))

        return filtered_files # return the array
    
    def on_completed(self):
        # safety re-enable the process window before destroy
        self.result_window.new_window.attributes("-disabled", False)

        self.result_window.on_exit()
        self.main_window.on_exit()
        messagebox.showinfo("Sucess", "Files has been organized!")

    def run_app(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainAppControl()
    app.run_app()