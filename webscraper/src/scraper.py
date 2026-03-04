"""
Main scraper module for the web scraper.
Handles HTTP requests, pagination, and coordination of scraping operations.
"""

from typing import Dict, List, Any, Set, Optional
from urllib.parse import urljoin, urlparse
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.error_handler import Logger, ErrorHandler, NetworkError
from src.parser import HTMLParser
from src.utils import RateLimiter, URLValidator, TimingUtils


class Scraper:
    """Main web scraper class."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize scraper.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.logger = Logger()
        self.error_handler = ErrorHandler()
        self.parser = HTMLParser()
        self.rate_limiter = RateLimiter(config.get('rate_limit', 1.0))
        self.timing = TimingUtils()
        
        # Setup requests session
        self.session = self._setup_session()
        
        # Tracking
        self.visited_urls: Set[str] = set()
        self.scraped_data: List[Dict[str, Any]] = []
    
    def _setup_session(self) -> requests.Session:
        """
        Setup requests session with retry strategy.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=['GET', 'HEAD', 'OPTIONS']
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return session
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single URL.
        
        Args:
            url: URL to scrape
            
        Returns:
            Scraped data dictionary
        """
        self.timing.start()
        
        try:
            # Normalize and validate URL
            url = URLValidator.normalize_url(url)
            if not URLValidator.is_valid_url(url):
                raise NetworkError(f"Invalid URL: {url}")
            
            self.logger.info(f"Starting scrape of {url}")
            
            # Scrape the main page
            page_data = self._scrape_page(url)
            
            # Handle pagination if configured
            if self.config.get('follow_links', False):
                page_data = self._handle_pagination(url, page_data)
            
            self.timing.stop()
            self.logger.info(f"Scraping completed in {self.timing.format_elapsed()}")
            
            return page_data
        
        except NetworkError as e:
            self.error_handler.handle_network_error(url, e)
            return {'error': str(e), 'url': url}
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {str(e)}", exc_info=True)
            self.error_handler.handle_network_error(url, e)
            return {'error': str(e), 'url': url}
    
    def _scrape_page(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single page.
        
        Args:
            url: URL to scrape
            
        Returns:
            Extracted data from the page
        """
        try:
            # Rate limiting
            self.rate_limiter.wait()
            
            # Fetch page
            self.logger.debug(f"Fetching {url}")
            response = self._fetch_page(url)
            
            if response.status_code != 200:
                raise NetworkError(f"HTTP {response.status_code}: {response.reason}")
            
            # Mark as visited
            self.visited_urls.add(url)
            
            # Parse and extract data
            self.logger.debug(f"Parsing content from {url}")
            selectors = self.config.get('selectors', {})
            extracted_data = self.parser.extract_data(response.text, selectors, url)
            
            # Add metadata
            extracted_data['_metadata'] = {
                'url': url,
                'status_code': response.status_code,
                'content_length': len(response.content),
                'encoding': response.encoding
            }
            
            self.logger.info(f"Successfully scraped {url}")
            return extracted_data
        
        except NetworkError as e:
            raise
        except Exception as e:
            self.error_handler.handle_network_error(url, e)
            raise NetworkError(f"Error scraping {url}: {str(e)}")
    
    def _fetch_page(self, url: str, timeout: Optional[int] = None) -> requests.Response:
        """
        Fetch page content.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
            
        Returns:
            Response object
            
        Raises:
            NetworkError: If fetch fails
        """
        try:
            timeout = timeout or self.config.get('timeout', 30)
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            raise NetworkError(f"Request timeout for {url}")
        except requests.exceptions.ConnectionError:
            raise NetworkError(f"Connection error for {url}")
        except requests.exceptions.HTTPError as e:
            raise NetworkError(f"HTTP error for {url}: {str(e)}")
        except Exception as e:
            raise NetworkError(f"Error fetching {url}: {str(e)}")
    
    def _handle_pagination(self, base_url: str, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle pagination by following links.
        
        Args:
            base_url: Base URL to scrape
            initial_data: Data from initial page
            
        Returns:
            Combined data from all pages
        """
        try:
            all_data = initial_data.copy()
            max_pages = self.config.get('max_pages', 10)
            crawl_depth = self.config.get('crawl_depth', 1)
            
            # Extract links from initial data
            links = initial_data.get('links', [])
            pages_scraped = 1
            
            for link in links:
                if pages_scraped >= max_pages:
                    break
                
                href = link.get('href', '')
                if not href or href in self.visited_urls:
                    continue
                
                # Validate link is from same domain
                base_domain = URLValidator.get_domain(base_url)
                link_domain = URLValidator.get_domain(href)
                
                if base_domain != link_domain:
                    continue
                
                try:
                    self.logger.info(f"Following link: {href}")
                    page_data = self._scrape_page(href)
                    
                    # Merge data
                    for key, value in page_data.items():
                        if key == '_metadata':
                            continue
                        
                        if key not in all_data:
                            all_data[key] = []
                        
                        if isinstance(value, list) and isinstance(all_data[key], list):
                            all_data[key].extend(value)
                    
                    pages_scraped += 1
                
                except Exception as e:
                    self.logger.warning(f"Error following link {href}: {str(e)}")
                    continue
            
            self.logger.info(f"Pagination complete: scraped {pages_scraped} pages")
            return all_data
        
        except Exception as e:
            self.logger.error(f"Error during pagination: {str(e)}")
            return initial_data
    
    def scrape_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Scrape multiple URLs.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of scraped data
        """
        self.logger.info(f"Starting scrape of {len(urls)} URLs")
        all_data = []
        
        for idx, url in enumerate(urls, 1):
            self.logger.info(f"Scraping URL {idx}/{len(urls)}: {url}")
            try:
                data = self.scrape(url)
                all_data.append(data)
            except Exception as e:
                self.logger.error(f"Error scraping {url}: {str(e)}")
        
        self.logger.info(f"Completed scraping of {len(urls)} URLs")
        return all_data
    
    def get_error_summary(self) -> Dict[str, Any]:
        """
        Get error summary.
        
        Returns:
            Error summary dictionary
        """
        return self.error_handler.get_error_summary()
    
    def close(self) -> None:
        """Close the scraper session."""
        if self.session:
            self.session.close()
            self.logger.info("Scraper session closed")
