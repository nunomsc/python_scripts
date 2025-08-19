import os
import glob

def rename_images_in_folder(folder_path, base_name):
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    # Find all image files in the folder (e.g., .jpg, .png)
    image_files = glob.glob(os.path.join(folder_path, "*.*"))
    
    # Filter out only the files that are images (you can add more extensions if needed)
    image_files = [f for f in image_files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not image_files:
        print("No images found in the specified folder.")
        return

    # Sort files to ensure consistent ordering
    image_files.sort()

    # Loop through all images and rename them
    for i, file_path in enumerate(image_files):
        # Extract file extension
        extension = os.path.splitext(file_path)[1]
        
        # Create new file name with zero-padded numbering (e.g., amanda_01.jpg)
        new_name = f"{base_name}-0{i+1:02d}{extension}"
        
        # Get the full path for the new name
        new_path = os.path.join(folder_path, new_name)
        
        # Rename the image
        os.rename(file_path, new_path)

    print(f"Renamed {len(image_files)} images successfully!")

# Example usage
folder_path = input("Enter the folder path where the images are located: ")
base_name = input("Enter the base name for the images: ")

rename_images_in_folder(folder_path, base_name)
