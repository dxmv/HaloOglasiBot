import requests
from bs4 import BeautifulSoup
import time
from scraper import Scraper
from storage.database import ApartmentStorage

def main():
    """
    Main function to orchestrate the scraping process
    """
    # Initialize storage and scraper
    storage = ApartmentStorage()
    scraper = Scraper()
    
    # Fetch and parse apartments
    html_content = scraper.get_page_content(scraper.base_url)
    all_apartments = scraper.parse_apartments(html_content)
    
    # Filter new apartments
    new_apartments = storage.get_new_apartments(all_apartments)
    
    # Save new apartments
    for apartment in new_apartments:
        storage.save_apartment(apartment)
        
    # Print new findings
    if new_apartments:
        print(f"Found {len(new_apartments)} new apartments!")
        for apt in new_apartments:
            print(f"New: {apt.title} - {apt.price}")
    else:
        print("No new apartments found.")

if __name__ == "__main__":
    main()