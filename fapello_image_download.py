import os
import requests

# Base URL and starting page number
base_url = 'https://fapello.com/content/s/a/sabrina-lynn/2000/sabrina-lynn_'
start_page = 1000

# Number of images to download
num_images = 1000

# Output directory to save the images
output_dir = 'downloaded_images'
os.makedirs(output_dir, exist_ok=True)

# Function to download an image from a URL
def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded image {filename}')
        else:
            print(f'Failed to download {url}. Status code: {response.status_code}')
    except Exception as e:
        print(f'Failed to download {url}. Error: {e}')

# Main script to download sequential images
for i in range(start_page, start_page + num_images):
    url = f'{base_url}{str(i).zfill(4)}.jpg'
    filename = os.path.join(output_dir, f'sabrina-lynn_{str(i).zfill(4)}.jpg')
    download_image(url, filename)

print('Image downloading complete!')
