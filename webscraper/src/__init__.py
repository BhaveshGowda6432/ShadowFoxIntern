"""
Web Scraper Package
A modular Python application for web data extraction.
"""

from src.scraper import Scraper
from src.parser import HTMLParser
from src.storage import StorageManager
from src.config_loader import ConfigLoader
from src.error_handler import Logger, ErrorHandler

__version__ = "1.0.0"
__author__ = "Web Scraper Team"

__all__ = [
    'Scraper',
    'HTMLParser',
    'StorageManager',
    'ConfigLoader',
    'Logger',
    'ErrorHandler'
]
