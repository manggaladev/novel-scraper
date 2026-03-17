"""
Utility Functions
=================

Helper functions for data cleaning and text processing.
"""

import json
import csv
import os
import re
import logging
from typing import Optional, List, Any

logger = logging.getLogger(__name__)


def clean_text(text: Optional[str]) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    
    return text


def clean_price(price_str: Optional[str]) -> Optional[float]:
    """
    Extract numeric price from string.
    
    Args:
        price_str: Price string (e.g., "£25.99")
        
    Returns:
        Float price value or None
    """
    if not price_str:
        return None
    
    # Extract numeric value
    match = re.search(r'[\d,.]+', price_str)
    if match:
        try:
            return float(match.group().replace(',', ''))
        except ValueError:
            return None
    return None


def parse_rating(rating_class: Optional[str]) -> int:
    """
    Parse rating from star class names.
    
    Args:
        rating_class: CSS class containing rating (e.g., "Three")
        
    Returns:
        Integer rating (1-5)
    """
    if not rating_class:
        return 0
    
    rating_map = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
    }
    
    # Find rating word in class
    rating_class_lower = rating_class.lower()
    for word, value in rating_map.items():
        if word in rating_class_lower:
            return value
    
    return 0


def clean_availability(availability_str: Optional[str]) -> dict:
    """
    Parse availability string to extract stock information.
    
    Args:
        availability_str: Availability text (e.g., "In stock (22 available)")
        
    Returns:
        Dictionary with 'in_stock' and 'stock_count' keys
    """
    if not availability_str:
        return {'in_stock': False, 'stock_count': 0}
    
    in_stock = 'in stock' in availability_str.lower()
    
    # Extract stock count
    match = re.search(r'\((\d+) available\)', availability_str)
    stock_count = int(match.group(1)) if match else 0
    
    return {
        'in_stock': in_stock,
        'stock_count': stock_count
    }


def generate_book_id(url: str) -> str:
    """
    Generate a unique ID from book URL.
    
    Args:
        url: Book detail page URL
        
    Returns:
        Unique identifier string
    """
    # Extract ID from URL pattern like /catalogue/book/title_123/index.html
    match = re.search(r'/(\d+)/index\.html$', url)
    if match:
        return match.group(1)
    
    # Fallback: use last part of URL
    parts = url.rstrip('/').split('/')
    return parts[-1] if parts else 'unknown'


def format_genre(category: str) -> str:
    """
    Format category/genre text.
    
    Args:
        category: Raw category string
        
    Returns:
        Formatted genre string
    """
    if not category:
        return "Unknown"
    
    # Capitalize each word
    return ' '.join(word.capitalize() for word in category.split('_'))


def validate_book_data(book: dict) -> bool:
    """
    Validate that book data has required fields.
    
    Args:
        book: Book dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['title', 'url']
    return all(field in book and book[field] for field in required_fields)


def save_to_json(data: List[dict], filepath: str) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        data: List of dictionaries to save
        filepath: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✓ Saved {len(data)} items to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")
        return False


def save_to_csv(data: List[dict], filepath: str) -> bool:
    """
    Save data to a CSV file.
    
    Args:
        data: List of dictionaries to save
        filepath: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    if not data:
        logger.warning("No data to save to CSV")
        return False
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Get all unique keys from all dictionaries
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        logger.info(f"✓ Saved {len(data)} items to {filepath}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save CSV: {e}")
        return False


def load_from_json(filepath: str) -> List[dict]:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Input file path
        
    Returns:
        List of dictionaries
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"✓ Loaded {len(data)} items from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return []
