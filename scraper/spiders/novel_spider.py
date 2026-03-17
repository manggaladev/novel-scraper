"""
Novel Spider
============

Main spider for scraping book/novel data from books.toscrape.com
"""

import time
import logging
from typing import List, Optional, Generator
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .. import settings
from ..utils import (
    clean_text,
    clean_price,
    parse_rating,
    clean_availability,
    generate_book_id,
    validate_book_data,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NovelSpider:
    """
    Spider for scraping book data from books.toscrape.com
    
    This spider:
    - Respects robots.txt (books.toscrape.com allows all bots)
    - Uses a polite User-Agent
    - Adds delay between requests
    - Handles pagination automatically
    - Extracts detailed book information
    
    Example:
        spider = NovelSpider()
        books = spider.scrape_all()
        spider.save_to_json(books, "output/novels.json")
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(settings.HEADERS)
        self.books_scraped = 0
        self.pages_scraped = 0
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a web page.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None on failure
        """
        for attempt in range(settings.MAX_RETRIES):
            try:
                logger.info(f"Fetching: {url}")
                response = self.session.get(url, timeout=settings.TIMEOUT)
                response.raise_for_status()
                
                # Add delay to respect server
                time.sleep(settings.REQUEST_DELAY)
                
                return BeautifulSoup(response.text, 'lxml')
                
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < settings.MAX_RETRIES - 1:
                    time.sleep(settings.REQUEST_DELAY * 2)  # Longer delay on retry
                    
        logger.error(f"Failed to fetch {url} after {settings.MAX_RETRIES} attempts")
        return None
    
    def parse_book_card(self, article, current_url: str) -> Optional[dict]:
        """
        Parse a book card from the listing page.
        
        Args:
            article: BeautifulSoup article element
            current_url: Current page URL for resolving relative links
            
        Returns:
            Dictionary with book data
        """
        try:
            # Get title and URL
            title_elem = article.find('h3').find('a')
            title = clean_text(title_elem.get('title', ''))
            book_url = urljoin(current_url, title_elem.get('href', ''))
            
            # Get price
            price_elem = article.find('p', class_='price_color')
            price = clean_price(price_elem.text if price_elem else None)
            
            # Get rating
            rating_elem = article.find('p', class_='star-rating')
            rating = parse_rating(rating_elem.get('class', []) if rating_elem else None)
            
            # Get availability
            avail_elem = article.find('p', class_='instock availability')
            availability = clean_availability(avail_elem.text if avail_elem else None)
            
            # Get image URL
            img_elem = article.find('img')
            image_url = urljoin(current_url, img_elem.get('src', '')) if img_elem else None
            
            book = {
                'id': generate_book_id(book_url),
                'title': title,
                'url': book_url,
                'price': price,
                'rating': rating,
                'in_stock': availability['in_stock'],
                'stock_count': availability['stock_count'],
                'cover_url': image_url,
            }
            
            return book if validate_book_data(book) else None
            
        except Exception as e:
            logger.error(f"Error parsing book card: {e}")
            return None
    
    def parse_book_detail(self, book: dict) -> dict:
        """
        Fetch and parse detailed book information from detail page.
        
        Args:
            book: Basic book dictionary from listing
            
        Returns:
            Enhanced book dictionary with details
        """
        soup = self.fetch_page(book['url'])
        if not soup:
            return book
        
        try:
            # Get product information table
            table = soup.find('table', class_='table table-striped')
            if table:
                rows = table.find_all('tr')
                for row in rows:
                    header = row.find('th').text.strip()
                    value = row.find('td').text.strip()
                    
                    if header == 'UPC':
                        book['upc'] = value
                    elif header == 'Product Type':
                        book['product_type'] = value
                    elif header == 'Price (excl. tax)':
                        book['price_excl_tax'] = clean_price(value)
                    elif header == 'Price (incl. tax)':
                        book['price_incl_tax'] = clean_price(value)
                    elif header == 'Tax':
                        book['tax'] = clean_price(value)
                    elif header == 'Availability':
                        availability = clean_availability(value)
                        book['in_stock'] = availability['in_stock']
                        book['stock_count'] = availability['stock_count']
                    elif header == 'Number of reviews':
                        book['review_count'] = int(value)
            
            # Get description
            desc_elem = soup.find('div', id='product_description')
            if desc_elem:
                desc_sibling = desc_elem.find_next_sibling('p')
                book['description'] = clean_text(desc_sibling.text if desc_sibling else None)
            else:
                book['description'] = ""
            
            # Get category from breadcrumb
            breadcrumb = soup.find('ul', class_='breadcrumb')
            if breadcrumb:
                links = breadcrumb.find_all('a')
                if len(links) >= 3:
                    book['category'] = clean_text(links[2].text)
            
            # Get cover image (higher resolution)
            img_container = soup.find('div', class_='item active')
            if img_container:
                img = img_container.find('img')
                if img:
                    book['cover_url'] = urljoin(settings.BASE_URL, img.get('src', ''))
            
            logger.info(f"Scraped details for: {book['title']}")
            
        except Exception as e:
            logger.error(f"Error parsing book detail: {e}")
        
        return book
    
    def get_next_page_url(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        """
        Find the next page URL from pagination.
        
        Args:
            soup: Current page BeautifulSoup object
            current_url: Current page URL
            
        Returns:
            Next page URL or None if no more pages
        """
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_link = next_btn.find('a')
            if next_link:
                return urljoin(current_url, next_link.get('href'))
        return None
    
    def scrape_all(self, start_url: str = None) -> List[dict]:
        """
        Scrape all books from the catalogue, handling pagination.
        
        Args:
            start_url: Starting URL for scraping
            
        Returns:
            List of book dictionaries
        """
        if start_url is None:
            start_url = settings.CATALOGUE_URL
            
        books = []
        current_url = start_url
        page_count = 0
        
        logger.info("Starting scraping...")
        logger.info(f"Target: {settings.BASE_URL}")
        logger.info(f"Request delay: {settings.REQUEST_DELAY}s")
        logger.info("-" * 50)
        
        while current_url:
            # Check if we've reached max pages
            if settings.MAX_PAGES and page_count >= settings.MAX_PAGES:
                logger.info(f"Reached max pages limit: {settings.MAX_PAGES}")
                break
            
            page_count += 1
            self.pages_scraped = page_count
            
            logger.info(f"\n{'='*20} Page {page_count} {'='*20}")
            
            # Scrape current page
            soup = self.fetch_page(current_url)
            if not soup:
                break
            
            # Parse books from page
            articles = soup.find_all('article', class_='product_pod')
            logger.info(f"Found {len(articles)} books on page")
            
            for article in articles:
                if settings.MAX_BOOKS and self.books_scraped >= settings.MAX_BOOKS:
                    break
                
                book = self.parse_book_card(article, current_url)
                if book:
                    if settings.INCLUDE_DETAILS:
                        book = self.parse_book_detail(book)
                    books.append(book)
                    self.books_scraped += 1
            
            # Check if we've reached max books
            if settings.MAX_BOOKS and self.books_scraped >= settings.MAX_BOOKS:
                logger.info(f"Reached max books limit: {settings.MAX_BOOKS}")
                break
            
            # Find next page
            current_url = self.get_next_page_url(soup, current_url)
        
        logger.info("\n" + "=" * 50)
        logger.info(f"Scraping complete!")
        logger.info(f"Total pages: {page_count}")
        logger.info(f"Total books: {len(books)}")
        
        return books
    
    def close(self):
        """Close the requests session."""
        self.session.close()


def main():
    """Main entry point for the spider."""
    spider = NovelSpider()
    
    try:
        books = spider.scrape_all()
        
        # Save results
        from ..utils import save_to_json, save_to_csv
        
        save_to_json(books, "output/novels.json")
        save_to_csv(books, "output/novels.csv")
        
    finally:
        spider.close()


if __name__ == "__main__":
    main()
