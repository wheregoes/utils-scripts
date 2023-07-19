import os
import requests
from tqdm import tqdm

def download_file(url, destination_folder):
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
        else:
            print(f"Failed to download file from {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading file from {url}: {e}")

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
        download_file(url, destination_folder)

if __name__ == "__main__":
    # File containing URLs to download, one URL per line
    urls_file_path = "urls_to_download.txt"

    # Destination folder where files will be saved
    destination_folder = "downloads"

    download_files_from_file(urls_file_path, destination_folder)