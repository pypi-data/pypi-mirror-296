import os
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

DOWNLOAD_FOLDER = 'downloads'
DOWNLOAD_FILE = 'downloads.txt'

def extract_file_name_from_url(url):
    print(url)
    fragment = urllib.parse.urlparse(url).fragment
    decoded_fragment = urllib.parse.unquote(fragment)
    return decoded_fragment or "a.rar"

def download_file(original_url, url, folder):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Extract the file name from the original URL
        file_name = extract_file_name_from_url(original_url)
        file_path = os.path.join(folder, file_name)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress = (downloaded_size / total_size) * 100 if total_size > 0 else 0
                    progress_bar = '=' * int(progress / 2)
                    print(f"\r[{progress_bar:<50}] {progress:.2f}%", end='')

        print(f"\nDownloaded: {file_name}")
    else:
        print(f"Failed to download from {url}")


def find_download_link(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')

    for script in script_tags:
        if 'window.open' in script.text:
            match = re.search(r'window\.open\("([^"]+)"', script.text)
            if match:
                download_url = match.group(1)
                return download_url

    return None


def read_urls_from_file(file_path):
    urls = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        print(f"File {file_path} does not exist.")
    return urls


def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    print(
        "This tool currently only supports fuckingfast.co links. If you are trying to download something from somewhere else, it might not work.")

    choice = input("Type 'read' to read URLs from downloads.txt or 'input' to enter URLs manually: ").strip().lower()

    if choice == 'read':
        urls = read_urls_from_file(DOWNLOAD_FILE)
        if not urls:
            print(f"No URLs found in {DOWNLOAD_FILE}.")
    elif choice == 'input':
        urls = []
        print("Enter the URLs (press Enter without typing anything to stop):")
        while True:
            url = input("Enter URL: ").strip()
            if not url:
                break
            urls.append(url)
    else:
        print("Invalid choice. Exiting.")
        return

    for url in urls:
        download_link = find_download_link(url)
        if download_link:
            download_file(url, download_link, DOWNLOAD_FOLDER)
        else:
            print(f"No download link found for {url}")


if __name__ == '__main__':
    main()
    print("Press any key to exit.")
    input()
