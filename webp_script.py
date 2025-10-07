from PIL import Image
import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')

def process_image(file_info, folder, backup_folder, quality, lossless):
    """
    Process a single image: move to backup, convert to WebP.
    """
    input_path = file_info
    filename = os.path.basename(input_path)
    backup_path = os.path.join(backup_folder, filename)

    # WebP output path
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(folder, f"{name}_webp.webp")

    if os.path.exists(output_path):
        return f"Skipped {input_path}, {output_path} already exists."

    try:
        # Move original to backup
        shutil.move(input_path, backup_path)

        # Open image
        img = Image.open(backup_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Save as WebP
        img.save(output_path, "WEBP", quality=quality, lossless=lossless)

        return f"Converted {backup_path} → {output_path}"
    except Exception as e:
        return f"Failed {input_path}: {e}"

def compress_and_convert(folder, backup_folder, quality=80, lossless=False, max_workers=4):
    """
    Convert all images in a specified folder to WebP using multiple threads.
    """
    os.makedirs(backup_folder, exist_ok=True)
    files_to_process = [
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith(supported_formats)
    ]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_image, file_info, folder, backup_folder, quality, lossless)
            for file_info in files_to_process
        ]

        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    folder = input("Enter the folder path: ").strip()
    backup_folder = input("Enter the backup folder path: ").strip()
    quality = input("Enter WebP quality (0-100, default 80): ").strip()
    quality = int(quality) if quality.isdigit() else 80
    lossless_input = input("Use lossless WebP? (y/n, default n): ").strip().lower()
    lossless = lossless_input == 'y'
    max_threads = input("Enter number of threads (default 4): ").strip()
    max_threads = int(max_threads) if max_threads.isdigit() else 4

    compress_and_convert(folder, backup_folder, quality, lossless, max_threads)
