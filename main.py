#!/usr/bin/env python3
"""
Novel Scraper - Main Entry Point
=================================

Run the scraper and save results to JSON/CSV.

Usage:
    python main.py                    # Scrape all books
    python main.py --pages 5          # Scrape only 5 pages
    python main.py --books 100        # Scrape only 100 books
    python main.py --no-details       # Skip detailed info (faster)
"""

import argparse
import logging
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.spiders.novel_spider import NovelSpider
from scraper.settings import JSON_OUTPUT, CSV_OUTPUT
from scraper.utils import save_to_json, save_to_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the scraper."""
    parser = argparse.ArgumentParser(
        description="Scrape book/novel data from books.toscrape.com"
    )
    
    parser.add_argument(
        '--pages',
        type=int,
        default=None,
        help='Maximum number of pages to scrape (default: all)'
    )
    
    parser.add_argument(
        '--books',
        type=int,
        default=None,
        help='Maximum number of books to scrape (default: all)'
    )
    
    parser.add_argument(
        '--no-details',
        action='store_true',
        help='Skip fetching detailed book information (faster)'
    )
    
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for results (default: output)'
    )
    
    parser.add_argument(
        '--json',
        default=None,
        help='JSON output filename (default: novels.json)'
    )
    
    parser.add_argument(
        '--csv',
        default=None,
        help='CSV output filename (default: novels.csv)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    args = parser.parse_args()
    
    # Override settings from command line
    import scraper.settings as settings
    if args.pages:
        settings.MAX_PAGES = args.pages
    if args.books:
        settings.MAX_BOOKS = args.books
    if args.no_details:
        settings.INCLUDE_DETAILS = False
    if args.delay:
        settings.REQUEST_DELAY = args.delay
    
    # Set output paths
    output_dir = args.output_dir
    json_file = args.json or f"{output_dir}/novels.json"
    csv_file = args.csv or f"{output_dir}/novels.csv"
    
    # Print banner
    logger.info("=" * 60)
    logger.info("  📚 NOVEL SCRAPER")
    logger.info("=" * 60)
    logger.info(f"  Target: {settings.BASE_URL}")
    logger.info(f"  Max Pages: {settings.MAX_PAGES or 'Unlimited'}")
    logger.info(f"  Max Books: {settings.MAX_BOOKS or 'Unlimited'}")
    logger.info(f"  Include Details: {settings.INCLUDE_DETAILS}")
    logger.info(f"  Request Delay: {settings.REQUEST_DELAY}s")
    logger.info("=" * 60)
    
    # Run scraper
    spider = NovelSpider()
    
    try:
        books = spider.scrape_all()
        
        if books:
            # Save results
            logger.info("\n" + "=" * 60)
            logger.info("Saving results...")
            logger.info("=" * 60)
            
            save_to_json(books, json_file)
            save_to_csv(books, csv_file)
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ SCRAPING COMPLETE!")
            logger.info("=" * 60)
            logger.info(f"  Total books: {len(books)}")
            logger.info(f"  JSON file: {json_file}")
            logger.info(f"  CSV file: {csv_file}")
            logger.info("=" * 60)
            
            # Print sample
            if books:
                logger.info("\n📖 Sample book:")
                sample = books[0]
                for key, value in list(sample.items())[:6]:
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:50] + "..."
                    logger.info(f"  {key}: {value}")
        else:
            logger.warning("No books were scraped!")
            
    except KeyboardInterrupt:
        logger.info("\n⚠️  Scraping interrupted by user")
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise
        
    finally:
        spider.close()


if __name__ == "__main__":
    main()
