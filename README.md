<div align="center">

# 🕷️ Novel Scraper

**Collect book/novel data from public websites for your projects**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-7C3AED?style=for-the-badge)](https://crummy.com/software/BeautifulSoup/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📚 **Scrape Books** | Title, author, description, genre, rating |
| 🔄 **Pagination** | Auto-handle multi-page catalogues |
| 🧹 **Data Cleaning** | Remove whitespace, format text |
| 💾 **Multiple Formats** | JSON, CSV output |
| ⏱️ **Rate Limiting** | Respect servers |
| 🔌 **API Import** | Import to novel-api |

## 🚀 Quick Start

```bash
# Clone
cd novel-scraper

# Install
pip install -r requirements.txt

# Scrape
python main.py
```

## 📸 Example Output

```
╔══════════════════════════════════════════════════════════════╗
║                    🕷️ Novel Scraper                          ║
╠══════════════════════════════════════════════════════════════╣
║  Target: https://books.toscrape.com                         ║
║  Delay:  1.0s between requests                              ║
╚══════════════════════════════════════════════════════════════╝

📖 Page 1/50
  ✓ A Light in the Attic - £51.77
  ✓ Tipping the Velvet - £53.74
  ✓ Soumission - £50.10
  ...

📖 Page 2/50
  ✓ Sharp Objects - £47.82
  ✓ In a Dark, Dark Wood - £19.63
  ...

╔══════════════════════════════════════════════════════════════╗
║  ✅ Complete!                                                ║
║  Total: 1000 books scraped                                  ║
║  Output: output/novels.json, output/novels.csv             ║
╚══════════════════════════════════════════════════════════════╝
```

## 📋 Usage

### Basic Scraping

```bash
# Scrape all books
python main.py

# Limit pages
python main.py --pages 10

# Limit books
python main.py --books 100
```

### With Options

```bash
python main.py \
  --pages 20 \
  --delay 2.0 \
  --output-json books.json \
  --output-csv books.csv
```

### Import to novel-api

```bash
python main.py import \
  --file output/novels.json \
  --api-url http://localhost:3000 \
  --token your_jwt_token
```

## 📊 Output Format

### JSON
```json
[
  {
    "id": "a-light-in-the-attic_198",
    "title": "A Light in the Attic",
    "url": "https://books.toscrape.com/...",
    "price": 51.77,
    "rating": 3,
    "in_stock": true,
    "stock_count": 22,
    "category": "Poetry",
    "cover_url": "https://.../cover.jpg",
    "description": "..."
  }
]
```

### CSV
```csv
id,title,price,rating,category,in_stock
a-light-in-the-attic,A Light in the Attic,51.77,3,Poetry,true
```

## 🏗️ Project Structure

```
novel-scraper/
├── main.py              # Entry point
├── scraper/
│   ├── __init__.py
│   ├── settings.py      # Configuration
│   ├── spiders/
│   │   └── novel_spider.py  # Main spider
│   └── utils.py         # Helpers
├── output/              # Scraped data
└── requirements.txt
```

## 🔧 Configuration

Edit `scraper/settings.py`:

```python
# Request settings
REQUEST_DELAY = 1.0  # seconds
MAX_RETRIES = 3
TIMEOUT = 30

# Scraping limits
MAX_PAGES = None      # None = all pages
MAX_BOOKS = None      # None = all books
INCLUDE_DETAILS = True

# Output
JSON_OUTPUT = "output/novels.json"
CSV_OUTPUT = "output/novels.csv"
```

## 🎯 Target Site

Currently targets **[books.toscrape.com](https://books.toscrape.com/)** - a safe sandbox for learning web scraping.

## ⚠️ Legal Notice

- ✅ Only scrape public data
- ✅ Respect robots.txt
- ✅ Add delays between requests
- ✅ Use for personal projects
- ❌ Don't overload servers
- ❌ Don't scrape copyrighted content

## 🔌 Extending

### Add New Site

```python
# scraper/spiders/my_spider.py
from scraper.spiders.base_spider import BaseSpider

class MySpider(BaseSpider):
    def parse_list(self, soup):
        # Parse listing page
        pass
    
    def parse_detail(self, soup):
        # Parse detail page
        pass
```

## 📋 Requirements

- Python 3.10+
- requests
- beautifulsoup4
- lxml
- pandas

## 🤝 Contributing

Contributions welcome! Add new scrapers, improve parsing.

## 📄 License

[MIT License](LICENSE)

---

<div align="center">

**[⬆ Back to Top](#️-novel-scraper)**


**Scrape responsibly! 🕷️**

</div>
