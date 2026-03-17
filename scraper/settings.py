"""
Scraper Settings
================

Configuration settings for the web scraper.
"""

# Target website settings
BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue/category/books_1/index.html"

# Request settings
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

# Rate limiting (in seconds)
REQUEST_DELAY = 1  # Delay between requests to respect server
MAX_RETRIES = 3
TIMEOUT = 30

# Output settings
OUTPUT_DIR = "output"
JSON_OUTPUT = f"{OUTPUT_DIR}/novels.json"
CSV_OUTPUT = f"{OUTPUT_DIR}/novels.csv"

# Scraping limits (set to None for unlimited)
MAX_PAGES = None  # Maximum pages to scrape (None = all)
MAX_BOOKS = None  # Maximum books to scrape (None = all)

# Data settings
INCLUDE_DETAILS = True  # Whether to fetch detailed book info from detail pages

# Logging settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
