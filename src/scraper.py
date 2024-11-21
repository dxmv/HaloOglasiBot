import requests
from bs4 import BeautifulSoup
from models.ad import Ad

class Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = "https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_to=400&cena_d_unit=4"
    
    def get_page_content(self, url: str):
        """
        Fetches the HTML content from the specified URL
        Args:
            url (str): The URL to fetch
        Returns:
            str or None: The HTML content if successful, None if failed
        """
        
        try:
            # Make GET request to the URL
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Will raise an exception for 4XX/5XX status codes
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def parse_apartments(self, html_content: str) -> list[Ad]:
        """
        Parses the HTML content to extract apartment information
        Args:
            html_content (str): Raw HTML content
        Returns:
            list[Ad]: List of Ad objects containing apartment details
        """
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        ads = soup.find_all('div', class_=[
            'product-item',
            'product-list-item',
            'Premium',
            'real-estates',
            'my-product-placeholder'
        ])
        
        return [Ad.from_div(ad) for ad in ads]
