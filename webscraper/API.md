# API Documentation

Complete reference guide for the Web Scraper API.

## Table of Contents

- [Scraper](#scraper)
- [Parser](#parser)
- [Storage](#storage)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Utilities](#utilities)

---

## Scraper

### `Scraper(config: Dict[str, Any])`

Main scraper class for web data extraction.

#### Attributes

- `config`: Configuration dictionary
- `session`: Requests session with retry strategy
- `visited_urls`: Set of visited URLs
- `error_handler`: Error handler instance
- `rate_limiter`: Rate limiter instance

#### Methods

##### `scrape(url: str) -> Dict[str, Any]`

Scrape a single URL.

**Parameters:**

- `url` (str): URL to scrape

**Returns:**

- Dictionary containing extracted data

**Raises:**

- `NetworkError`: If network request fails

**Example:**

```python
from src.scraper import Scraper

config = {
    'url': 'https://example.com',
    'selectors': {'headings': 'h1, h2'},
    'timeout': 30
}
scraper = Scraper(config)
data = scraper.scrape('https://example.com')
```

##### `scrape_multiple(urls: List[str]) -> List[Dict[str, Any]]`

Scrape multiple URLs.

**Parameters:**

- `urls` (List[str]): List of URLs to scrape

**Returns:**

- List of data dictionaries

**Example:**

```python
urls = ['https://example.com', 'https://example.com/page2']
data_list = scraper.scrape_multiple(urls)
```

##### `get_error_summary() -> Dict[str, Any]`

Get error summary from scraping.

**Returns:**

- Dictionary with error count and details

##### `close() -> None`

Close the scraper session.

---

## Parser

### `HTMLParser()`

Main HTML parsing class.

#### Methods

##### `parse(html_content: str, base_url: str = "") -> BeautifulSoup`

Parse HTML content.

**Parameters:**

- `html_content` (str): HTML content as string
- `base_url` (str, optional): Base URL for relative links

**Returns:**

- BeautifulSoup object

**Raises:**

- `ParsingError`: If parsing fails

**Example:**

```python
from src.parser import HTMLParser

parser = HTMLParser()
soup = parser.parse("<html><body><h1>Test</h1></body></html>")
```

##### `extract_data(html_content: str, selectors: Dict[str, Any], base_url: str = "") -> Dict[str, Any]`

Extract data from HTML based on selectors.

**Parameters:**

- `html_content` (str): HTML content
- `selectors` (Dict): CSS selectors for extraction
- `base_url` (str, optional): Base URL

**Returns:**

- Dictionary with extracted data

**Example:**

```python
selectors = {
    'headings': 'h1, h2',
    'links': 'a'
}
data = parser.extract_data(html, selectors, 'https://example.com')
```

### `ElementExtractor(soup: BeautifulSoup, base_url: str = "")`

Extracts specific elements from parsed HTML.

#### Methods

##### `extract_titles(selector: str = "title") -> List[Dict[str, Any]]`

Extract page titles.

##### `extract_headings(selector: str = "h1, h2, h3, h4, h5, h6") -> List[Dict[str, Any]]`

Extract headings.

##### `extract_links(selector: str = "a") -> List[Dict[str, Any]]`

Extract links with URLs and text.

##### `extract_paragraphs(selector: str = "p") -> List[Dict[str, Any]]`

Extract paragraphs.

##### `extract_tables(selector: str = "table") -> List[Dict[str, Any]]`

Extract tables with headers and rows.

##### `extract_images(selector: str = "img") -> List[Dict[str, Any]]`

Extract images with src, alt, and title.

##### `extract_metadata() -> Dict[str, Any]`

Extract page metadata (title, meta tags, OG tags).

---

## Storage

### `StorageManager(output_directory: str = 'output')`

Manages data storage in multiple formats.

#### Methods

##### `save(data: Dict[str, Any], formats: List[str], prefix: str = '') -> Dict[str, str]`

Save data in multiple formats.

**Parameters:**

- `data` (Dict): Data to save
- `formats` (List[str]): Output formats ('json', 'csv', 'sqlite')
- `prefix` (str, optional): Filename prefix

**Returns:**

- Dictionary mapping format to filepath

**Example:**

```python
from src.storage import StorageManager

storage = StorageManager('output')
data = {
    'headings': [{'text': 'Title'}],
    'links': [{'text': 'Link', 'href': 'url'}]
}
files = storage.save(data, ['json', 'csv'])
```

### `JSONStorage(output_directory: str = 'output')`

Store data in JSON format.

#### Methods

##### `save(data: Dict[str, Any], filename: str = 'data.json') -> str`

Save data to JSON file.

**Returns:**

- Path to saved file

### `CSVStorage(output_directory: str = 'output')`

Store data in CSV format.

#### Methods

##### `save(data: Dict[str, Any], filename: str = 'data.csv') -> str`

Save data to CSV file.

**Returns:**

- Path to saved file

### `SQLiteStorage(output_directory: str = 'output', db_name: str = 'scraper.db')`

Store data in SQLite database.

#### Methods

##### `save(data: Dict[str, Any], table_name: str = 'scraped_data') -> str`

Save data to SQLite database.

**Returns:**

- Path to database file

---

## Configuration

### `ConfigLoader(config_path: str)`

Load and validate configuration from JSON file.

#### Methods

##### `load() -> Dict[str, Any]`

Load configuration from file.

**Returns:**

- Configuration dictionary

**Raises:**

- `ConfigurationError`: If configuration is invalid

**Example:**

```python
from src.config_loader import ConfigLoader

loader = ConfigLoader('config/scraper_config.json')
config = loader.load()
```

##### `get(key: str, default: Any = None) -> Any`

Get configuration value.

##### `get_url() -> str`

Get target URL.

##### `get_selectors() -> Dict[str, Any]`

Get CSS selectors.

##### `get_output_formats() -> List[str]`

Get output formats.

##### `get_timeout() -> int`

Get request timeout.

##### `get_rate_limit() -> float`

Get rate limit (requests per second).

---

## Error Handling

### `Logger()`

Singleton logger for the application.

#### Methods

##### `info(message: str) -> None`

Log info message.

##### `debug(message: str) -> None`

Log debug message.

##### `warning(message: str) -> None`

Log warning message.

##### `error(message: str, exc_info: bool = False) -> None`

Log error message.

##### `critical(message: str) -> None`

Log critical message.

**Example:**

```python
from src.error_handler import Logger

logger = Logger()
logger.info('Processing started')
logger.error('An error occurred', exc_info=True)
```

### `ErrorHandler()`

Handles and tracks scraping errors.

#### Methods

##### `handle_network_error(url: str, exception: Exception) -> None`

Handle network errors.

##### `handle_parsing_error(url: str, exception: Exception) -> None`

Handle parsing errors.

##### `handle_storage_error(file_path: str, exception: Exception) -> None`

Handle storage errors.

##### `get_error_summary() -> Dict[str, Any]`

Get error summary.

---

## Utilities

### `URLValidator`

Validates and processes URLs.

#### Static Methods

##### `is_valid_url(url: str) -> bool`

Check if URL is valid.

##### `normalize_url(url: str) -> str`

Normalize URL format.

##### `join_urls(base_url: str, relative_url: str) -> str`

Join base and relative URLs.

##### `get_domain(url: str) -> str`

Extract domain from URL.

**Example:**

```python
from src.utils import URLValidator

assert URLValidator.is_valid_url('https://example.com')
normalized = URLValidator.normalize_url('example.com')
joined = URLValidator.join_urls('https://example.com/', '../path')
```

### `RateLimiter(requests_per_second: float = 1.0)`

Implements rate limiting for requests.

#### Methods

##### `wait() -> None`

Wait to respect rate limit.

##### `reset() -> None`

Reset rate limiter.

**Example:**

```python
from src.utils import RateLimiter

limiter = RateLimiter(requests_per_second=0.5)
limiter.wait()  # Wait if needed
```

### `DataProcessor`

Processes and cleans extracted data.

#### Static Methods

##### `clean_text(text: str) -> str`

Remove extra whitespace from text.

##### `extract_text_content(element) -> str`

Extract text from BeautifulSoup element.

##### `extract_attribute(element, attribute: str, default: str = "") -> str`

Extract attribute from element.

##### `remove_duplicates(items: List[Dict]) -> List[Dict]`

Remove duplicate items from list.

---

## Example Usage

### Complete Scraping Workflow

```python
from src.config_loader import ConfigLoader
from src.scraper import Scraper
from src.storage import StorageManager

# Load configuration
loader = ConfigLoader('config/scraper_config.json')
config = loader.load()

# Run scraper
scraper = Scraper(config)
data = scraper.scrape(config['url'])

# Save data
storage = StorageManager(config['output_directory'])
storage.save(data, config['output_formats'])

# Check errors
errors = scraper.get_error_summary()
print(f"Errors: {errors['total_errors']}")

# Cleanup
scraper.close()
```

---

## Exception Hierarchy

```
Exception
├── ScraperError
│   ├── NetworkError
│   ├── ParsingError
│   ├── ConfigurationError
│   ├── StorageError
│   └── URLValidationError
```

---

**Last Updated**: 2024  
**Version**: 1.0.0
