
import urllib.request
import zipfile
import io
import os
import shutil

url = "https://www.kaggle.com/api/v1/datasets/download/pratyushpuri/retail-fashion-boutique-data-sales-analytics-2025"
save_path = "data"
os.makedirs(save_path, exist_ok=True)

print(f"Downloading from {url}...")
try:
    # Use fancy opener to handle redirects if any, though urlopen usually handles them.
    # We might need a user-agent.
    req = urllib.request.Request(
        url, 
        data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    
    with urllib.request.urlopen(req) as response:
        content = response.read()
        print("Downloaded. Unzipping...")
        try:
            z = zipfile.ZipFile(io.BytesIO(content))
            z.extractall(save_path)
            print(f"Extracted to {save_path}")
            print("Files:", os.listdir(save_path))
        except zipfile.BadZipFile:
             print("Error: The downloaded file is not a valid zip file.")
             print("First 500 bytes:", content[:500])
except Exception as e:
    print(f"An error occurred: {e}")
