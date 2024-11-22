import asyncio
from telegram import Bot
from telegram.error import TelegramError, RetryAfter
import os
from scraper import Scraper
from storage.database import ApartmentStorage
import schedule
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get telegram token from environment variable
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

async def send_apartment_to_telegram(bot: Bot, apartment):
    """Send apartment details to Telegram channel"""
    message = (
        f"🏠 *New Apartment Listed!*\n\n"
        f"*{apartment.title}*\n"
        f"💰 Price: {apartment.price}\n"
        f"📍 Location: {apartment.location}\n"
        f"📐 Area: {apartment.area}\n"
        f"🚪 Rooms: {apartment.rooms}\n"
        f"🏢 Floor: {apartment.floor}\n\n"
        f"[View Listing]({apartment.link})"
    )
    
    try:
        if apartment.image_url and apartment.image_url != "No image":
            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=apartment.image_url,
                caption=message,
                parse_mode='Markdown'
            )
        else:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                parse_mode='Markdown'
            )
    except TelegramError as e:
        print(f"Failed to send message: {e}")

async def scrape_and_notify():
    """Scrape apartments and send new ones to Telegram"""
    bot = Bot(token=TELEGRAM_TOKEN)
    storage = ApartmentStorage()
    scraper = Scraper()
    
    try:
        html_content = scraper.get_page_content(scraper.base_url)
        all_apartments = scraper.parse_apartments(html_content)
        new_apartments = storage.get_new_apartments(all_apartments)
        
        for apartment in new_apartments:
            storage.save_apartment(apartment)
            try:
                await send_apartment_to_telegram(bot, apartment)
                # Increase delay between messages to 3 seconds
                await asyncio.sleep(3)
            except RetryAfter as e:
                # Wait the required time before retrying
                print(f"Rate limit hit. Waiting {e.retry_after} seconds...")
                await asyncio.sleep(e.retry_after)
                await send_apartment_to_telegram(bot, apartment)
            
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        try:
            await bot.close()
        except RetryAfter:
            # Ignore rate limit errors during cleanup
            pass

def run_scraper():
    """Run the scraper asynchronously"""
    asyncio.run(scrape_and_notify())

def main():
    """Main function to schedule scraping"""
    if not TELEGRAM_TOKEN or not CHANNEL_ID:
        raise ValueError("Please set TELEGRAM_TOKEN and CHANNEL_ID environment variables")
    
    # Schedule the job to run every 5 minutes
    schedule.every(30).seconds.do(run_scraper)
    
    # Run first scrape immediately
    run_scraper()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 