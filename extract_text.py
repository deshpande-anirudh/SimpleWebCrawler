from bs4 import BeautifulSoup
import requests

# Example URL
url = "https://en.wikipedia.org/wiki/Amitabh_Bachchan"
response = requests.get(url)

if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove all anchor tags
    for link in soup.find_all('a'):
        link.decompose()  # Removes the tag and its contents from the tree

    # Extract and display only the text content
    text_content = soup.get_text(separator="\n")  # Use separator to make it more readable
    print(text_content)
else:
    print("Failed to retrieve the page")
