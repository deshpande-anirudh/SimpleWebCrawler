import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

class SimpleWebCrawler:
    def __init__(self, start_url, max_pages=10):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited_pages = set()

    def crawl(self):
        queue = deque([self.start_url])

        while queue and len(self.visited_pages) < self.max_pages:
            url = queue.popleft()

            # Normalize URL and check if visited
            normalized_url = url.split('#')[0].rstrip('/')
            if normalized_url in self.visited_pages:
                continue

            try:
                response = requests.get(normalized_url, timeout=5)
                response.raise_for_status()  # Raise error for bad status codes

                # Mark this URL as visited
                self.visited_pages.add(normalized_url)
                print(f"Crawling: {normalized_url}")

                # Parse the page content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract and queue links
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(normalized_url, link['href'])
                    absolute_url = absolute_url.split('#')[0].rstrip('/')
                    if absolute_url.startswith("http") and absolute_url not in self.visited_pages:
                        print(f"Found link: {absolute_url}")
                        queue.append(absolute_url)

            except requests.RequestException as e:
                print(f"Error crawling {normalized_url}: {e}")

if __name__ == "__main__":
    start_url = "https://en.wikipedia.org/wiki/Amitabh_Bachchan"
    crawler = SimpleWebCrawler(start_url, max_pages=5)
    crawler.crawl()
