#!/usr/bin/env python3
"""
Import to API Script
====================

Script for importing scraped novel data to the novel-api database.
"""

import argparse
import json
import logging
import os
import sys
import time
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIImporter:
    """
    Import scraped data to novel-api.
    
    Example:
        importer = APIImporter("http://localhost:3000", "your-api-key")
        importer.import_from_json("output/novels.json")
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        batch_size: int = 10,
        delay: float = 0.5
    ):
        """
        Initialize the API importer.
        
        Args:
            base_url: Base URL of the novel-api
            api_key: API key for authentication
            batch_size: Number of items per batch request
            delay: Delay between requests in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.environ.get('NOVEL_API_KEY', '')
        self.batch_size = batch_size
        self.delay = delay
        
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
    
    def transform_book_to_novel(self, book: dict) -> dict:
        """
        Transform book data from scraper format to API format.
        
        Args:
            book: Book dictionary from scraper
            
        Returns:
            Novel dictionary for API
        """
        novel = {
            'title': book.get('title', 'Unknown Title'),
            'author': book.get('author', 'Unknown Author'),
            'description': book.get('description', ''),
            'genre': book.get('category', 'General'),
            'coverUrl': book.get('cover_url') or book.get('coverUrl'),
            'rating': book.get('rating'),
            'sourceUrl': book.get('url'),
            'externalId': book.get('id') or book.get('upc'),
        }
        
        # Remove None values
        return {k: v for k, v in novel.items() if v is not None}
    
    def import_novel(self, novel: dict) -> bool:
        """
        Import a single novel to the API.
        
        Args:
            novel: Novel dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/novels",
                json=novel,
                timeout=30
            )
            
            if response.status_code in (200, 201):
                logger.info(f"✓ Imported: {novel.get('title')}")
                return True
            elif response.status_code == 409:
                logger.info(f"→ Already exists: {novel.get('title')}")
                return True
            else:
                logger.error(f"✗ Failed to import {novel.get('title')}: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            logger.error(f"✗ Error importing {novel.get('title')}: {e}")
            return False
    
    def import_batch(self, novels: List[dict]) -> dict:
        """
        Import multiple novels in batch.
        
        Args:
            novels: List of novel dictionaries
            
        Returns:
            Dictionary with success and failure counts
        """
        results = {'success': 0, 'failed': 0, 'skipped': 0}
        
        for i, novel in enumerate(novels, 1):
            logger.info(f"[{i}/{len(novels)}] Importing: {novel.get('title')}")
            
            success = self.import_novel(novel)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            # Add delay between requests
            if self.delay > 0 and i < len(novels):
                time.sleep(self.delay)
        
        return results
    
    def import_from_json(self, filepath: str) -> dict:
        """
        Import novels from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Dictionary with import results
        """
        logger.info(f"Loading data from {filepath}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                books = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load JSON file: {e}")
            return {'success': 0, 'failed': 0, 'skipped': 0, 'error': str(e)}
        
        logger.info(f"Found {len(books)} books to import")
        
        # Transform books to novels
        novels = [self.transform_book_to_novel(book) for book in books]
        
        # Import in batches
        return self.import_batch(novels)
    
    def check_api_health(self) -> bool:
        """
        Check if the API is accessible.
        
        Returns:
            True if API is healthy, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            return response.status_code == 200
        except:
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import scraped novel data to novel-api"
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        default='output/novels.json',
        help='Path to the JSON file to import (default: output/novels.json)'
    )
    
    parser.add_argument(
        '--api-url',
        default=os.environ.get('NOVEL_API_URL', 'http://localhost:3000'),
        help='Base URL of the novel-api (default: http://localhost:3000)'
    )
    
    parser.add_argument(
        '--api-key',
        default=None,
        help='API key for authentication (or set NOVEL_API_KEY env var)'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=10,
        help='Number of items per batch (default: 10)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=0.5,
        help='Delay between requests in seconds (default: 0.5)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate data without importing'
    )
    
    args = parser.parse_args()
    
    # Create importer
    importer = APIImporter(
        base_url=args.api_url,
        api_key=args.api_key,
        batch_size=args.batch_size,
        delay=args.delay
    )
    
    # Check API health
    logger.info(f"Checking API at {args.api_url}...")
    if not importer.check_api_health():
        logger.warning("⚠️  API health check failed. Make sure the API is running.")
        logger.warning("    Continuing anyway...")
    
    if args.dry_run:
        logger.info("🔍 Dry run mode - validating data only")
        
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                books = json.load(f)
            
            logger.info(f"Found {len(books)} books")
            
            for book in books[:5]:  # Show first 5
                novel = importer.transform_book_to_novel(book)
                logger.info(f"  - {novel.get('title')}: {novel.get('author')}")
            
            if len(books) > 5:
                logger.info(f"  ... and {len(books) - 5} more")
            
            logger.info("✓ Data validation complete")
            return
        except Exception as e:
            logger.error(f"✗ Validation failed: {e}")
            return
    
    # Import data
    logger.info("=" * 50)
    logger.info("Starting import...")
    logger.info("=" * 50)
    
    results = importer.import_from_json(args.input)
    
    logger.info("=" * 50)
    logger.info("Import complete!")
    logger.info(f"  ✓ Success: {results['success']}")
    logger.info(f"  ✗ Failed:  {results['failed']}")
    if results.get('skipped'):
        logger.info(f"  → Skipped: {results['skipped']}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
