import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os

# Connect to the MySQL database
def create_connection():
    return mysql.connector.connect(
        host='localhost',  # e.g., 'localhost'
        user='root',
        password='newpassword',
        database='minhadatabase'
    )

def insert_image(image_path, image_name, site_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Read the image file
        with open(image_path, 'rb') as file:
            image_data = file.read()
        
        # Get the current date and time
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Insert image data into the database
        cursor.execute('''
        INSERT INTO images (filename, filedata, creation_date, site_id) VALUES (%s, %s, %s, %s)
        ''', (image_name, image_data, creation_date, site_id))
        conn.commit()
        print(f"Image '{image_name}' inserted successfully")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_images_from_folder(folder_path, site_id):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Add other image formats if needed
            image_path = os.path.join(folder_path, filename)
            insert_image(image_path, filename, site_id)

def retrieve_image(image_id, output_path):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        
        # Retrieve image data from the database
        cursor.execute('''
        SELECT filename, filedata FROM images WHERE id = %s
        ''', (image_id,))
        result = cursor.fetchone()
        
        if result:
            image_name, image_data = result
            # Write the image data to an output file
            with open(output_path, 'wb') as file:
                file.write(image_data)
            print(f"Image '{image_name}' saved to '{output_path}'")
        else:
            print("Image not found")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Example usage:
# Insert all images from a folder into the database
folder_path = 'amanda.rodrigues'
site_id = 5
insert_images_from_folder(folder_path, site_id)

# Retrieve an image from the database
retrieve_image(1, 'output_image.jpg')
