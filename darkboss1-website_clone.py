import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to download the HTML content and media files of a website
def download_website(url, folder_name):
    try:
        # Download HTML from URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Request for {url} failed!")
            return
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create folder if not exists
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save HTML file
        with open(os.path.join(folder_name, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print(f"HTML content saved in '{folder_name}/index.html'!")

        # Download media files (images, CSS, JS)
        download_media_files(url, soup, folder_name)

    except Exception as e:
        print(f"Error: {str(e)}")

# Function to download media files
def download_media_files(base_url, soup, folder_name):
    media_tags = {
        "img": "src",
        "link": "href",
        "script": "src"
    }

    for tag, attribute in media_tags.items():
        elements = soup.find_all(tag)
        for element in elements:
            media_url = element.get(attribute)
            if media_url:
                media_url = urljoin(base_url, media_url)
                media_name = os.path.basename(urlparse(media_url).path)
                save_path = os.path.join(folder_name, media_name)

                # Download the media file
                try:
                    media_response = requests.get(media_url)
                    if media_response.status_code == 200:
                        with open(save_path, 'wb') as media_file:
                            media_file.write(media_response.content)
                        print(f"Media file '{media_name}' saved!")
                except Exception as e:
                    print(f"Error downloading media file: {str(e)}")

# Main function
def main():
    url = input("Enter the website URL to clone (e.g., https://www.example.com): ")
    folder_name = input("Enter the folder name (e.g., my_website): ")

    download_website(url, folder_name)

if __name__ == "__main__":
    main()
