import requests
from bs4 import BeautifulSoup
import os
import urllib

# The URL to scrape
url = "https://docs.llamaindex.ai/en/latest/"

# The directory to store files in
output_dir = "./llamaindex-docs/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all links to .html files
links = soup.find_all("a", href=True)

for link in links:
    href = link["href"]

    # Exclude external link and # links
    if not href.startswith("http") and not href.startswith("#") and href != ".":

        filename = href.replace("/", "_") + ".html"

        # Make a full URL if necessary
        href = urllib.parse.urljoin(url, href)

        # Fetch the .html file
        print(f"downloading {href}")
        file_response = requests.get(href)

        # Write it to a file
        file_name = os.path.join(output_dir, filename)
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(file_response.text)
