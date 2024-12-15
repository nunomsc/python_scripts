import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import csv
import time
import random
import os

# Base URL (without page number)
base_url = "https://www.gog.com/en/games?order=asc:title&hideDLCs=true&page=138"

# Parse the URL and extract query parameters
parsed_url = urlparse(base_url)
query_params = parse_qs(parsed_url.query)

# Extract the page number and store it in a variable
page_number = query_params.get("page", [None])[0]

# File name for saving data
csv_filename = "product_titles.csv"

# Check if the file exists
file_exists = os.path.isfile(csv_filename)

# Initialize page number
page = 57

# Infinite loop (or set a specific range if needed)
while page < 139:
    # Construct the URL with the incremented page number
    url = f"{base_url}{page}"
    print(f"Fetching data from: {url}")

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <span> elements within <product-title>
        product_titles = soup.find_all("product-title")
        spans = [title.find("span").text for title in product_titles if title.find("span")]

        # Open the file in append mode and save the data
        with open(csv_filename, mode="a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)

            # Write header only if it's the first time
            if not file_exists:
                writer.writerow(["Product Title"])
                file_exists = True

            for span in spans:
                writer.writerow([span])

        print(f"Data from page {page} saved to {csv_filename}")

    else:
        print(f"Failed to retrieve data from page {page}. Status code: {response.status_code}")

    # Increment the page number
    page += 1

    # Random delay between 1 and 5 minutes
    delay = random.randint(60, 300)  # Delay in seconds (1 minute to 5 minutes)
    print(f"Waiting for {delay} seconds before the next request...")
    time.sleep(delay)
