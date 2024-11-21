import requests
from bs4 import BeautifulSoup
import time

# Base URL for apartment listings with price filter set to 400
HALO_OGLASI_URL = "https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?cena_d_to=400&cena_d_unit=4"




def get_page_content(url: str):
    """
    Fetches the HTML content from the specified URL
    Args:
        url (str): The URL to fetch
    Returns:
        str or None: The HTML content if successful, None if failed
    """
    # Headers to make the request appear as if it's coming from a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an exception for 4XX/5XX status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def parse_apartments(html_content: str) -> list[dict]:
    """
    Parses the HTML content to extract apartment information
    Args:
        html_content (str): Raw HTML content
    Returns:
        list: List of dictionaries containing apartment details
    """
    if not html_content:
        return []
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all divs with the specific classes
    # Note: When classes are space-separated in HTML, you need to provide them as a list to BeautifulSoup
    ads = soup.find_all('div', class_=[
        'product-item',
        'product-list-item',
        'Premium',
        'real-estates',
        'my-product-placeholder'
    ])
    c = 0
    for ad in ads:
        # Extract data-id
        data_id = ad.get('data-id')

        # Extract title
        title_element = ad.find('h3', class_='product-title')
        title = title_element.text.strip() if title_element else "No title"

        # Extract link
        link = title_element.find("a")['href'] if title_element else "No link"

        # Extract price
        price_element = ad.find('div', class_='central-feature')
        price = price_element.contents[0].contents[0].text.strip() if price_element else "No price"
        print(f"Price {c}: {price}")

        # Extract location
        places = ad.find('ul', class_='subtitle-places')
        location = ', '.join([li.text.strip() for li in places.find_all('li')]) if places else "No location"

        product_features = ad.find('ul', class_='product-features')
        values = product_features.find_all('div', class_='value-wrapper') if product_features else []
        # Extract area
        area = values[0].text.strip() if values else "No area"
        # Extract rooms
        rooms = values[1].text.strip() if values else "No rooms"
        # Extract floor
        floor = values[2].text.strip() if values else "No floor"

        # Extract image
        image = ad.find('img')
        image_url = image.get('src') if image else "No image"
    return []

def main():
    """
    Main function to orchestrate the scraping process
    """
    # Step 1: Fetch the webpage content
    html_content = get_page_content(HALO_OGLASI_URL)
    
    if html_content:
        # Step 2: Parse the content and extract apartment information
        apartments = parse_apartments(html_content)
        
        # Step 3: Display the results
        for apt in apartments:
            print(f"\nTitle: {apt['title']}")
            print(f"Price: {apt['price']}")
            print(f"Location: {apt['location']}")
            print("-" * 50)

if __name__ == "__main__":
    main()