import os
import requests
import time
import logging
from tqdm import tqdm

def download_file_with_retry(url, destination_folder):
    retries = 3
    delay_times = [5, 30, 60]

    for attempt in range(retries):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = url.split('/')[-1]
                destination_path = os.path.join(destination_folder, file_name)

                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024  # 1 KB
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name)

                with open(destination_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)

                progress_bar.close()
                print(f"File downloaded: {file_name}")
                return True
            else:
                print(f"Failed to download file from {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading file from {url}: {e}")

        if attempt < retries - 1:
            print(f"Retrying in {delay_times[attempt]} seconds...")
            time.sleep(delay_times[attempt])

    # If download failed after all retries, log the error
    log_file = os.path.join(destination_folder, 'download_failures.log')
    logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s - %(message)s')
    logging.error(f"Failed to download file from {url}")

    return False

def download_files_from_file(file_path, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            urls_to_download = file.read().splitlines()
    else:
        urls_to_download = []
        while True:
            url_input = input("Enter the URL to download (or 'done' to finish): ")
            if url_input.lower() == 'done':
                break
            urls_to_download.append(url_input)

        with open(file_path, 'w') as file:
            file.write('\n'.join(urls_to_download))

    for url in urls_to_download:
        success = download_file_with_retry(url, destination_folder)
        if not success:
            print(f"Failed to download: {url}")

if __name__ == "__main__":
    print(r"""
__/\\\\\\\\\\\\_____/\\\\____________/\\\\__/\\\\\\\\\\\\\\\_        
 _\/\\\////////\\\__\/\\\\\\________/\\\\\\_\/\\\///////////__       
  _\/\\\______\//\\\_\/\\\//\\\____/\\\//\\\_\/\\\_____________      
   _\/\\\_______\/\\\_\/\\\\///\\\/\\\/_\/\\\_\/\\\\\\\\\\\_____     
    _\/\\\_______\/\\\_\/\\\__\///\\\/___\/\\\_\/\\\///////______    
     _\/\\\_______\/\\\_\/\\\____\///_____\/\\\_\/\\\_____________   
      _\/\\\_______/\\\__\/\\\_____________\/\\\_\/\\\_____________  
       _\/\\\\\\\\\\\\/___\/\\\_____________\/\\\_\/\\\_____________ 
        _\////////////_____\///______________\///__\///______________
                                      
    """)
    print("Download Multiple Files \n")
    # File containing URLs to download, one URL per line
    urls_file_path = "urls_to_download.txt"

    # Destination folder where files will be saved
    destination_folder = "downloads"

    download_files_from_file(urls_file_path, destination_folder)