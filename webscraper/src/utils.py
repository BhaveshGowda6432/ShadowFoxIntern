"""
Utility functions for the web scraper.
Contains helper functions for URL validation, rate limiting, and data processing.
"""

import time
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from src.error_handler import Logger, URLValidationError


class URLValidator:
    """Validates and normalizes URLs."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        Validate if a string is a valid URL.
        
        Args:
            url: URL string to validate
            
        Returns:
            True if valid, False otherwise
        """
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """
        Normalize a URL.
        
        Args:
            url: URL to normalize
            
        Returns:
            Normalized URL
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    @staticmethod
    def join_urls(base_url: str, relative_url: str) -> str:
        """
        Join base URL with relative URL.
        
        Args:
            base_url: Base URL
            relative_url: Relative URL
            
        Returns:
            Joined absolute URL
        """
        return urljoin(base_url, relative_url)
    
    @staticmethod
    def get_domain(url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url: URL string
            
        Returns:
            Domain name
        """
        parsed = urlparse(url)
        return parsed.netloc


class RateLimiter:
    """Implements rate limiting for polite scraping."""
    
    def __init__(self, requests_per_second: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_second: Number of requests allowed per second
        """
        self.requests_per_second = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0
    
    def wait(self) -> None:
        """Wait to respect rate limit."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
    
    def reset(self) -> None:
        """Reset rate limiter."""
        self.last_request_time = 0


class DataProcessor:
    """Processes and cleans extracted data."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        return ' '.join(text.split())
    
    @staticmethod
    def extract_text_content(element) -> str:
        """
        Extract text content from an element.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            Extracted text
        """
        if element is None:
            return ""
        return DataProcessor.clean_text(element.get_text())
    
    @staticmethod
    def extract_attribute(element, attribute: str, default: str = "") -> str:
        """
        Extract attribute from an element.
        
        Args:
            element: BeautifulSoup element
            attribute: Attribute name
            default: Default value if attribute not found
            
        Returns:
            Attribute value
        """
        if element is None:
            return default
        return element.get(attribute, default)
    
    @staticmethod
    def remove_duplicates(items: List[Dict]) -> List[Dict]:
        """
        Remove duplicate items from list.
        
        Args:
            items: List of dictionaries
            
        Returns:
            List with duplicates removed
        """
        seen = set()
        unique_items = []
        for item in items:
            item_str = str(sorted(item.items()))
            if item_str not in seen:
                seen.add(item_str)
                unique_items.append(item)
        return unique_items
    
    @staticmethod
    def paginate_list(items: List[Any], page_size: int) -> List[List[Any]]:
        """
        Paginate a list.
        
        Args:
            items: List to paginate
            page_size: Size of each page
            
        Returns:
            List of pages
        """
        return [items[i:i + page_size] for i in range(0, len(items), page_size)]


class TimingUtils:
    """Utility functions for timing operations."""
    
    def __init__(self):
        """Initialize timing utility."""
        self.start_time = None
        self.end_time = None
    
    def start(self) -> None:
        """Start timer."""
        self.start_time = time.time()
    
    def stop(self) -> float:
        """
        Stop timer and return elapsed time.
        
        Returns:
            Elapsed time in seconds
        """
        self.end_time = time.time()
        return self.elapsed()
    
    def elapsed(self) -> float:
        """
        Get elapsed time.
        
        Returns:
            Elapsed time in seconds
        """
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time
    
    def format_elapsed(self) -> str:
        """
        Format elapsed time as string.
        
        Returns:
            Formatted time string
        """
        elapsed = self.elapsed()
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
