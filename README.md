# 🕷️ Novel Scraper

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)](https://github.com/manggaladev/novel-scraper)

A Python web scraper for collecting book/novel data from public websites. Output in JSON/CSV format for seeding the [novel-api](https://github.com/manggaladev/novel-api) database.

## ✨ Features

- 📚 **Scrape book data** - Title, author, description, genre, rating, cover URL
- 🔄 **Pagination support** - Automatically handles multi-page catalogues
- 🧹 **Data cleaning** - Removes extra whitespace, formats text properly
- 💾 **Multiple output formats** - JSON and CSV support
- ⏱️ **Rate limiting** - Respects server with configurable delays
- 🔍 **Detailed info** - Fetches book details from detail pages
- 🔌 **API integration** - Import scraped data to novel-api

## 🛠️ Tech Stack

- **Python 3.10+**
- **Requests** - HTTP client
- **BeautifulSoup4** - HTML parsing
- **lxml** - Fast XML/HTML parser
- **Pandas** - Data processing

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/manggaladev/novel-scraper.git
cd novel-scraper

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Scraping

```bash
# Scrape with default settings
python main.py scrape

# Specify number of pages
python main.py scrape --pages 10

# Limit number of books
python main.py scrape --max-books 100
```

### Output Formats

```bash
# JSON output (default)
python main.py scrape --output books.json

# CSV output
python main.py scrape --output books.csv

# Both formats
python main.py scrape --output-json books.json --output-csv books.csv
```

### Import to novel-api

```bash
# Import scraped data to novel-api
python main.py import --file books.json --api-url http://localhost:3000
```

## 🎯 Target Site

Currently targets **[books.toscrape.com](https://books.toscrape.com/)** - a safe sandbox for practicing web scraping.

## 📁 Project Structure

```
novel-scraper/
├── main.py              # Entry point
├── scraper/
│   ├── __init__.py
│   ├── base.py          # Base scraper class
│   └── books_toscrape.py # Site-specific scraper
├── output/              # Scraped data
├── scripts/
├── requirements.txt
└── README.md
```

## 📄 License

[MIT License](LICENSE) © 2026 manggaladev

## 🔗 Links

- [GitHub Repository](https://github.com/manggaladev/novel-scraper)
- [novel-api](https://github.com/manggaladev/novel-api) - REST API for novels
- [Issues](https://github.com/manggaladev/novel-scraper/issues)
