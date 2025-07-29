import tkinter as tk
import os
import shutil
import app_utility as utils

from tkinter import messagebox
from home_ui import HomeUI
from operation_ui import OperationUI
from app_utility import AppUtility

class AppControl():
    def __init__(self):
        # create and initialize variables
        self.root = tk.Tk()
        self.main_window = HomeUI(self.root, self.start_scanning)
        self.result_window = None # set to none as this will be use later on

    def start_scanning(self, folder_path):
        raw_files = AppUtility.get_all_files(folder_path)

        # handle if the selected folder is empty
        if not raw_files:
            messagebox.showinfo("No files!", "The selected folder might be empty.")
            return
        
        # display the result window which consist of a list of all found files, and organize button
        self.result_window = OperationUI(self.root, folder_path, utils.file_types, self.start_organizing)

    def start_organizing(self, folder_path, category):
        # make sure to disable the process window to avoid unnecessary interaction during the process
        self.result_window.new_window.attributes("-disabled", True)
        moved_files = 0 # tracks the total of files that moved

        # get the filtered files based on drop down option
        filtered_files = AppUtility.get_files_by_category(folder_path, category)

        # loop through all available files in the filtered files
        for file_name in filtered_files:
            # create a path for each files
            file_path = os.path.join(folder_path, file_name)
            
            # skip folders
            if not os.path.isfile(file_path):
                continue

            # extract the extension of the file example (image.jpg -> .jpg)
            file_exts = os.path.splitext(file_name)[1].lower()
            moved_to_category = False # mark the file as not move yet

            # loop though file types dictionary, key and pairs
            for folder_name, exts in utils.file_types.items():
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
            messagebox.showinfo("No Files Found", f"No '{category}' files were found to organize.")
            self.result_window.new_window.attributes("-disabled", False)
            return

        self.on_completed()
    
    def on_completed(self):
        # safety re-enable the process window before destroy
        self.result_window.new_window.attributes("-disabled", False)

        self.result_window.on_exit()
        self.main_window.on_exit()
        messagebox.showinfo("Sucess", "Files has been organized!")

    def run_app(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppControl()
    app.run_app()