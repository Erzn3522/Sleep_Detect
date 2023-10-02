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