# 🕷️ Novel Scraper

A Python web scraper for collecting book/novel data from public websites. Output in JSON/CSV format for seeding the [novel-api](https://github.com/manggaladev/novel-api) database.

## ✨ Features

- 📚 **Scrape book data** - Title, author, description, genre, rating, cover URL, etc.
- 🔄 **Pagination support** - Automatically handles multi-page catalogues
- 🧹 **Data cleaning** - Removes extra whitespace, formats text properly
- 💾 **Multiple output formats** - JSON and CSV support
- ⏱️ **Rate limiting** - Respects server with configurable delays
- 🔍 **Detailed info** - Fetches book details from detail pages
- 🔌 **API integration** - Import scraped data to novel-api

## 🎯 Target Site

Currently targets **[books.toscrape.com](https://books.toscrape.com/)** - a safe sandbox for practicing web scraping.

## 📋 Prerequisites

- Python 3.9+
- pip or uv package manager

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/manggaladev/novel-scraper.git
cd novel-scraper
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python main.py
```

Results will be saved to `output/novels.json` and `output/novels.csv`.

## 📖 Usage

### Basic Usage

```bash
# Scrape all books (default)
python main.py

# Scrape only 5 pages
python main.py --pages 5

# Scrape only 100 books
python main.py --books 100

# Faster scraping (skip detailed info)
python main.py --no-details

# Custom delay between requests
python main.py --delay 0.5
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--pages N` | Maximum pages to scrape | All |
| `--books N` | Maximum books to scrape | All |
| `--no-details` | Skip detailed book info | False |
| `--output-dir DIR` | Output directory | output |
| `--json FILE` | JSON output filename | novels.json |
| `--csv FILE` | CSV output filename | novels.csv |
| `--delay SECONDS` | Delay between requests | 1.0 |

## 📁 Project Structure

```
novel-scraper/
├── scraper/
│   ├── __init__.py
│   ├── spiders/
│   │   ├── __init__.py
│   │   └── novel_spider.py    # Main spider class
│   ├── settings.py             # Configuration
│   └── utils.py                # Helper functions
├── output/
│   ├── novels.json             # Scraped data (JSON)
│   └── novels.csv              # Scraped data (CSV)
├── scripts/
│   └── import_to_api.py        # API import script
├── main.py                     # Entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## 📊 Output Format

### JSON Structure

```json
[
  {
    "id": "1",
    "title": "A Light in the Attic",
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "price": 25.99,
    "rating": 3,
    "in_stock": true,
    "stock_count": 22,
    "cover_url": "https://books.toscrape.com/media/cache/fe/72/fe72f053b9f8...jpg",
    "upc": "a897fe39b1053632",
    "category": "Poetry",
    "description": "A collection of poems and drawings...",
    "review_count": 0
  }
]
```

### CSV Columns

| Column | Description |
|--------|-------------|
| id | Unique identifier |
| title | Book title |
| url | Source URL |
| price | Price in GBP |
| rating | Star rating (1-5) |
| in_stock | Availability status |
| stock_count | Number in stock |
| cover_url | Cover image URL |
| category | Book category/genre |
| description | Book description |
| upc | Universal Product Code |
| review_count | Number of reviews |

## 🔌 Import to novel-api

After scraping, you can import the data to your [novel-api](https://github.com/manggaladev/novel-api) instance:

```bash
# Set API URL
export NOVEL_API_URL=http://localhost:3000

# Set API key (if required)
export NOVEL_API_KEY=your-api-key

# Run import
python scripts/import_to_api.py output/novels.json

# Or with options
python scripts/import_to_api.py output/novels.json \
    --api-url http://localhost:3000 \
    --api-key your-api-key \
    --delay 0.5

# Dry run (validate without importing)
python scripts/import_to_api.py output/novels.json --dry-run
```

## ⚖️ Ethics & Best Practices

This scraper follows ethical scraping practices:

1. **Respects robots.txt** - books.toscrape.com allows all bots
2. **Polite User-Agent** - Identifies as a standard browser
3. **Rate limiting** - Default 1 second delay between requests
4. **Retry handling** - Graceful handling of failed requests
5. **Server-friendly** - Doesn't overload target server

```python
# Check robots.txt before scraping
# https://books.toscrape.com/robots.txt

User-agent: *
Disallow:
# All bots allowed!
```

## 🔧 Configuration

Edit `scraper/settings.py` to customize:

```python
# Target website
BASE_URL = "https://books.toscrape.com"

# Rate limiting
REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3

# Limits
MAX_PAGES = None  # Set to limit pages
MAX_BOOKS = None  # Set to limit books

# Features
INCLUDE_DETAILS = True  # Fetch detailed info
```

## 🛠️ Extending for Other Sites

To scrape other websites:

1. Create a new spider in `scraper/spiders/`
2. Update CSS selectors to match target site
3. Modify `parse_book_card()` and `parse_book_detail()`
4. Update settings with new base URL

### Example: Creating a New Spider

```python
from scraper.spiders.novel_spider import NovelSpider

class GutenbergSpider(NovelSpider):
    BASE_URL = "https://www.gutenberg.org"
    
    def parse_book_card(self, article):
        # Customize parsing logic
        book = {
            'title': article.find('span', class_='title').text,
            'author': article.find('span', class_='author').text,
            # ...
        }
        return book
```

## 📝 Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest

# Run tests
pytest tests/
```

### Code Style

```bash
# Format code
pip install black
black scraper/ main.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- [books.toscrape.com](https://books.toscrape.com/) for providing a safe scraping sandbox
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

