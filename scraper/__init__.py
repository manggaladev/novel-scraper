"""
Novel Scraper Package
=====================

A web scraper for collecting novel data from public websites.
"""

from .spiders.novel_spider import NovelSpider

__version__ = "1.0.0"
__author__ = "manggaladev"

__all__ = ["NovelSpider"]
