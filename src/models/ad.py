from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup, Tag

@dataclass
class Ad:
    """Class representing an apartment advertisement"""
    id: str
    title: str
    link: str
    price: str
    location: str
    area: str
    rooms: str
    floor: str
    image_url: str
    
    @classmethod
    def from_div(cls, ad: Tag) -> 'Ad':
        """Create an Ad instance from a BeautifulSoup div element"""
        # Extract data-id
        data_id = ad.get('data-id', 'No ID')

        # Extract title and link
        title_element = ad.find('h3', class_='product-title')
        title = title_element.text.strip() if title_element else "No title"
        link = title_element.find("a")['href'] if title_element else "No link"

        # Extract price
        price_element = ad.find('div', class_='central-feature')
        price = price_element.contents[0].contents[0].text.strip() if price_element else "No price"

        # Extract location
        places = ad.find('ul', class_='subtitle-places')
        location = ', '.join([li.text.strip() for li in places.find_all('li')]) if places else "No location"

        # Extract features (area, rooms, floor)
        product_features = ad.find('ul', class_='product-features')
        values = product_features.find_all('div', class_='value-wrapper') if product_features else []
        area = values[0].text.strip() if len(values) > 0 else "No area"
        rooms = values[1].text.strip() if len(values) > 1 else "No rooms"
        floor = values[2].text.strip() if len(values) > 2 else "No floor"

        # Extract image
        image = ad.find('img')
        image_url = image.get('src') if image else "No image"

        return cls(
            id=data_id,
            title=title,
            link=link,
            price=price,
            location=location,
            area=area,
            rooms=rooms,
            floor=floor,
            image_url=image_url
        ) 

    def __repr__(self) -> str:
        return f"Ad(id={self.id}, title={self.title}, link={self.link}, price={self.price}, location={self.location}, area={self.area}, rooms={self.rooms}, floor={self.floor}, image_url={self.image_url})"