import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time
import argparse

# Configure Logging (Shows professionalism)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_soup(url):
    """Fetches URL and returns BeautifulSoup object."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

def scrape_books(url, pages=1):
    """Scrapes book data from multiple pages."""
    all_books = []
    
    for page in range(1, pages + 1):
        logger.info(f"Scraping page {page}...")
        current_url = f"{url}catalogue/page-{page}.html" if page > 1 else url
        
        soup = get_soup(current_url)
        if not soup:
            break
            
        articles = soup.find_all('article', class_='product_pod')
        
        for article in articles:
            try:
                title = article.h3.a['title']
                price = article.find('p', class_='price_color').text
                availability = article.find('p', class_='instock availability').text.strip()
                rating = article.p['class'][1] if article.p else 'No Rating'
                
                all_books.append({
                    'Title': title,
                    'Price': price,
                    'Availability': availability,
                    'Rating': rating
                })
            except Exception as e:
                logger.warning(f"Error parsing item: {e}")
                continue
        
        # Be polite to the server
        time.sleep(1) 
        
    return all_books

def save_to_csv(data, filename):
    """Saves data to CSV using Pandas."""
    if not data:
        logger.warning("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    logger.info(f"Successfully saved {len(data)} items to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape books from toscrape.com')
    parser.add_argument('--pages', type=int, default=2, help='Number of pages to scrape')
    parser.add_argument('--output', type=str, default='books_data.csv', help='Output CSV filename')
    args = parser.parse_args()

    base_url = "http://books.toscrape.com/"
    logger.info(f"Starting scraper for {args.pages} pages...")
    
    data = scrape_books(base_url, pages=args.pages)
    save_to_csv(data, args.output)
    logger.info("Scraper finished.")

if __name__ == "__main__":
    main()