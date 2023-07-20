import os
import requests
import time
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def download_file(url, destination_folder):
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
                    downloaded_size = 0
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        file.write(data)
                        downloaded_size += len(data)

                progress_bar.close()

                # Verify integrity after download
                if downloaded_size != total_size:
                    print(f"Failed to download the complete file: {file_name}")
                    return False

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

def download_files_with_threading(urls_to_download, destination_folder, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(download_file, url, destination_folder) for url in urls_to_download]

        for future in as_completed(futures):
            if not future.result():
                print(f"Failed to download: {future.result()}")

def download_files_from_file(file_path, destination_folder, num_threads):
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

    download_files_with_threading(urls_to_download, destination_folder, num_threads)

def main():
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
    
    parser = argparse.ArgumentParser(description="Download Multiple Files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--multi-thread", action="store_true", help="Use multi-threaded download")
    parser.add_argument("-T", "--threads", type=int, default=4, help="Number of threads for multi-threaded download (default=4)")
    args = parser.parse_args()

    # File containing URLs to download, one URL per line
    urls_file_path = "urls_to_download.txt"

    # Destination folder where files will be saved
    destination_folder = "downloads"

    if args.multi_thread:
        download_files_from_file(urls_file_path, destination_folder, args.threads)
    else:
        download_files_from_file(urls_file_path, destination_folder, 1)  # Set num_threads to 1 for File-per-File download

if __name__ == "__main__":
    main()