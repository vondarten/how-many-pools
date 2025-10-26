import os
import pandas as pd
import random
import concurrent.futures
import threading
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("MAPS_API_KEY")
CSV_FILE_PATH = 'unified_points.csv'
IMAGE_OUTPUT_DIR = 'images'
ZOOM_LEVEL = 20
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 640
DOWNLOAD_CHANCE = 1.0 # 100% chance to download for each row
MAX_THREADS=5

# Create a lock for thread-safe DataFrame updates
df_lock = threading.Lock()


def download_satellite_image(api_key, latitude, longitude, zoom, output_filename, width=640, height=640):
    """
    Downloads a satellite image from Google Maps Static API.

    Args:
        api_key (str): Your Google Maps API key.
        latitude (float): The latitude for the center of the map.
        longitude (float): The longitude for the center of the map.
        zoom (int): The zoom level of the map (1-20).
        output_filename (str): The full path to save the image file.
        width (int): The width of the image in pixels.
        height (int): The height of the image in pixels.

    Returns:
        bool: True if download was successful, False otherwise.
    """
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        "center": f"{latitude},{longitude}",
        "zoom": zoom,
        "size": f"{width}x{height}",
        "maptype": "satellite",
        "key": api_key
    }

    try:
        response = requests.get(base_url, params=params, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(output_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Image successfully downloaded: {os.path.basename(output_filename)}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading for lat {latitude}, long {longitude}: {e}")
        return False


def download_and_update(row_data):
    """
    Downloads an image for a given row and updates the DataFrame in a thread-safe manner.
    """
    index, row = row_data
    
    # For each row, only attempt to download it in 10% of the cases
    if random.random() < DOWNLOAD_CHANCE:
        print(f"\nRow {index}: Attempting download...")

        # Sanitize the district name for the filename
        sanitized_distrito = str(row['distrito']).replace(' ', '_')

        # Construct the filename as specified
        filename = f"{index}_{sanitized_distrito}_{IMAGE_HEIGHT}_{IMAGE_WIDTH}_{ZOOM_LEVEL}.png"
        full_image_path = os.path.join(IMAGE_OUTPUT_DIR, filename)

        # Use the download function
        success = download_satellite_image(
            api_key=API_KEY,
            latitude=row['latitude'],
            longitude=row['longitude'],
            zoom=ZOOM_LEVEL,
            output_filename=full_image_path
        )

        # If the download was successful, update the DataFrame
        if success:
            with df_lock:
                # Use .at for efficient cell access
                df.at[index, 'downloaded'] = 1
                df.at[index, 'image_path'] = full_image_path
            print(f"Row {index}: Successfully downloaded and updated.")
        else:
            print(f"Row {index}: Download failed.")

# 1. Ensure the output directory for images exists
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)

# 2. Read the CSV file
try:
    df = pd.read_csv(CSV_FILE_PATH)
except FileNotFoundError:
    print(f"Error: The file '{CSV_FILE_PATH}' was not found.")
    exit()

# 3. Initialize columns if they don't exist
if 'downloaded' not in df.columns:
    df['downloaded'] = 0
if 'image_path' not in df.columns:
    df['image_path'] = ''

# 4. Identify rows that need downloading
rows_to_download = [
    (index, row)
    for index, row in df.iterrows()
    if row['downloaded'] != 1
]

# 5. Use ThreadPoolExecutor to download images in parallel
if rows_to_download:
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        print(f"Starting downloads with {MAX_THREADS} threads...")
        executor.map(download_and_update, rows_to_download)

# 6. Save the updated DataFrame back to the same CSV file
try:
    df.to_csv(CSV_FILE_PATH, index=False)
    print(f"\nProcessing complete. Updated CSV saved to '{CSV_FILE_PATH}'.")
except Exception as e:
    print(f"\nAn error occurred while saving the CSV file: {e}")