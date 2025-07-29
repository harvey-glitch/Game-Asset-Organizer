import os

# list of acceptable file category and its corresponding extensions by the system
file_types = {
    "Images": [".png", ".jpg", ".jpeg"],
    "Models": [".fbx", ".glb", ".blend"],
    "Sounds": [".wav", ".mp3", ".ogg"],
    "Others": []
}

class AppUtility():
    # ---- CUSTOM METHODS ----
    def get_files_by_category(folder: str, category: str) -> list:
        # if the path if valid, continue
        if not os.path.isdir(folder):
            return
        
        # store all valid extensions in all categories
        extensions = sum(file_types.values(), [])
        files_found = [] # array to store found files

        # loop though the selected folder and stored each files foud
        for file_name in os.listdir(folder):
            # create a path (folder plus file name)
            file_path = os.path.join(folder, file_name)
            
            # make sure the path leads to a valid files, not folder
            if os.path.isfile(file_path):
                # extract the extension of the file example (image.jpg -> .jpg)
                file_exts = os.path.splitext(file_name)[1].lower()

                if category == "All":
                    # return all files
                    files_found.append(file_name)
                elif category == "Others":
                    # return files that are not in the list of file extensions
                    if file_exts not in extensions:
                        files_found.append(file_name)
                elif file_exts in file_types.get(category, []):
                    # return files that nly match the files extensions
                    files_found.append(file_name)

        return files_found # return the list of files

    def get_all_files(folder: str) -> list:
        # same as above, but return all files instead
        if not os.path.isdir(folder):
            return
        
        files_found = []

        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)

            if os.path.isfile(file_path):
                files_found.append(file_name)

        return files_found