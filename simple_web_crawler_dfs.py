import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class SimpleWebCrawler:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_pages = set()

    def crawl(self, url):
        if len(self.visited_pages) >= self.max_pages:
            return

        # Normalize and avoid revisiting the same page
        normalized_url = url.split('#')[0].rstrip('/')
        if normalized_url in self.visited_pages:
            return

        # Mark this URL as visited before parsing to avoid infinite loops
        self.visited_pages.add(normalized_url)

        try:
            response = requests.get(normalized_url, timeout=5)
            response.raise_for_status()  # Raise error for bad status codes

            # Parse the page content
            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"Crawling: {normalized_url}")

            # Extract and display links
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(normalized_url, link['href'])
                absolute_url = absolute_url.split('#')[0].rstrip('/')
                if absolute_url.startswith("http") and absolute_url not in self.visited_pages:
                    print(f"Found link: {absolute_url}")
                    self.crawl(absolute_url)

        except requests.RequestException as e:
            print(f"Error crawling {normalized_url}: {e}")


if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Amitabh_Bachchan"
    crawler = SimpleWebCrawler(start_url, max_pages=5)
    crawler.crawl(start_url)
