import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self):
        pass

    def fetch_url(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text content from <p> tags
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            return "\n".join(paragraphs)

        except requests.exceptions.HTTPError as http_err:
            print(f"\nHTTP error occurred for URL {url}: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"\nRequest error occurred for URL {url}: {req_err}")
        return None

    def scrape(self, urls):
        results = {}
        for url in urls:
            print(f"\nScraping URL: {url}")
            content = self.fetch_url(url)
            if content:
                results[url] = content
            else:
                results[url] = "Failed to fetch content. See error logs for details."
        return results