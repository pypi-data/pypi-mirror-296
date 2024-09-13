import os
import zipfile
from .utils import print_logic

def zip_folders_by_type(base_folder: str, file_types: dict, GLOBAL_QUIET: bool):
    for folder_type in file_types.keys():
        folder_path = os.path.join(base_folder, folder_type)

        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            zip_file_name = f"{folder_type}.zip"
            zip_file_path = os.path.join(base_folder, zip_file_name)
            
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname=arcname)
            
            print_logic(f"Zipped {folder_type} folder into {zip_file_name}", 'yellow', GLOBAL_QUIET)