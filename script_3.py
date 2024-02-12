import os
import time

import requests


# Function to download images from URLs in a text file
def download_images_from_file(file_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read URLs from the text file
    with open(file_path, 'r') as file:
        urls = file.readlines()

    # Iterate through each URL and download the corresponding image
    for index, url in enumerate(urls):
        url = url.strip()  # Remove leading/trailing whitespace and newline characters
        print(f'Downloading image {index + 1}/{len(urls)} from URL: {url}')
        
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Extract the file name from the URL
                file_name = os.path.basename(url)
                # Determine the file path to save the image
                file_path = os.path.join(output_folder, file_name)
                # Write the image content to a file
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Successfully downloaded image: {file_name}')
            else:
                print(f'Failed to download image: {url}. Status code: {response.status_code}')
        except Exception as e:
            print(f'Error downloading image: {url}. {e}')
            continue

# Example usage:
file_path = 'Afrodisiac.txt'  # Path to the text file containing image URLs
output_folder = 'txt_downloaded_images'  # Folder to save downloaded images
download_images_from_file(file_path, output_folder)
