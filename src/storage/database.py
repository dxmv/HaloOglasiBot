import sqlite3
from typing import List, Optional
from models.ad import Ad

class ApartmentStorage:
    def __init__(self, db_path: str = "/data/apartments.db"):
        # Initialize the database path in a writable directory
        self.db_path = db_path
        # Initialize the database by creating necessary tables
        self.init_db()

    def init_db(self):
        """Initialize the database with necessary tables"""
        # Connect to the SQLite database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create the 'seen_apartments' table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seen_apartments (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    link TEXT,
                    price TEXT,
                    location TEXT,
                    area TEXT,
                    rooms TEXT,
                    floor TEXT,
                    image_url TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Commit the changes to the database
            conn.commit()

    def is_new_apartment(self, ad_id: str) -> bool:
        """Check if an apartment is new (not in database)"""
        # Connect to the SQLite database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Query the database to check if the apartment ID exists
            cursor.execute('SELECT id FROM seen_apartments WHERE id = ?', (ad_id,))
            # Return True if the apartment is not found, indicating it's new
            return cursor.fetchone() is None

    def save_apartment(self, ad: Ad):
        """Save an apartment to the database"""
        # Connect to the SQLite database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insert or replace the apartment details into the 'seen_apartments' table
            cursor.execute('''
                INSERT OR REPLACE INTO seen_apartments 
                (id, title, link, price, location, area, rooms, floor, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ad.id, ad.title, ad.link, ad.price, ad.location,
                ad.area, ad.rooms, ad.floor, ad.image_url
            ))
            # Commit the changes to the database
            conn.commit()

    def get_new_apartments(self, ads: List[Ad]) -> List[Ad]:
        """Filter out previously seen apartments"""
        # Return a list of new apartments by checking each ad's ID
        return [ad for ad in ads if self.is_new_apartment(ad.id)] 