import cv2
import os

class FolderController:
    def __init__(self, folder_path, max_size_gb):
        self.folder_path = folder_path
        self.max_size_gb = max_size_gb

    def check_folder_size(self):
        # Calculate the current folder size
        folder_size = sum(os.path.getsize(os.path.join(self.folder_path, filename)) for filename in os.listdir(self.folder_path))
        
        # Convert the maximum size from GB to bytes
        max_size_bytes = self.max_size_gb * (1024 ** 3)
        
        if folder_size > max_size_bytes:
            cv2.destroyAllWindows()            
            # Stop the script
            print(f"Folder size exceeded {self.max_size_gb} GB. Stopping the script.")
            exit()
            
    def record_name_creator(self, record_file_name):
        # Split the filename into the base name and extension
        base_name, extension = record_file_name.rsplit('.', 1)
        
        # Add the number at the end of the base name
        new_filename = f"{base_name}_{self.record_counter()}.{extension}"
        return new_filename
        