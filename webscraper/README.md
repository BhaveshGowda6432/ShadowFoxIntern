# Python Web Scraping and Data Extraction System

A production-quality, modular Python application for scraping data from websites with robust error handling, multiple output formats, and comprehensive logging.

## 📋 Features

### Core Features

- **Multi-format Data Extraction**: Extract titles, headings, links, paragraphs, tables, images, and metadata
- **Multiple Output Formats**: Save to JSON, CSV, and SQLite database
- **Robust Error Handling**: Comprehensive error handling with detailed logging
- **Rate Limiting**: Polite scraping with configurable request delays
- **Pagination Support**: Automatically follow links and scrape multiple pages
- **Configuration Management**: JSON-based configuration system with validation
- **CLI Interface**: Easy-to-use command-line interface
- **Logging System**: Detailed logging with file and console output
- **Testing Suite**: Comprehensive unit and integration tests
- **Docker Support**: Ready for containerized deployment

### Advanced Features

- Session management with retry strategy
- User-Agent headers for polite scraping
- Domain-aware link following (prevents off-domain crawling)
- Duplicate detection and removal
- Flexible CSS selector configuration
- Metadata extraction (Open Graph tags, canonical links, etc.)
- Rate limiting by requests per second
- Comprehensive error logging and tracking

## 📁 Project Structure

```
web-scraper-project/
│
├── src/
│   ├── __init__.py
│   ├── scraper.py           # Main scraping logic
│   ├── parser.py            # HTML parsing and extraction
│   ├── storage.py           # Data storage (JSON, CSV, SQLite)
│   ├── config_loader.py     # Configuration management
│   ├── error_handler.py     # Error handling and logging
│   └── utils.py             # Utility functions
│
├── config/
│   └── scraper_config.json  # Configuration file
│
├── output/                  # Scraped data output
│   ├── data.csv
│   └── data.json
│
├── logs/                    # Application logs
│   └── scraper.log
│
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py      # Scraper tests
│   └── test_parser.py       # Parser tests
│
├── run_scraper.py           # Main entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd web-scraper-project
   ```

2. **Create virtual environment** (Optional but recommended)

   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Scraper

#### Basic Usage

```bash
# Use default configuration
python run_scraper.py

# Use custom configuration file
python run_scraper.py --config config/scraper_config.json
```

#### Advanced Usage

```bash
# Scrape specific URL
python run_scraper.py --url https://shadowfox.in --format json csv

# Enable pagination/link following with max pages
python run_scraper.py --url https://example.com --follow-links --max-pages 5

# Custom output directory
python run_scraper.py --url https://example.com --output my_output

# Adjust rate limiting and timeout
python run_scraper.py --url https://example.com --rate-limit 0.5 --timeout 60

# Verbose mode
python run_scraper.py --verbose
```

## ⚙️ Configuration

### Configuration File Format (JSON)

Edit `config/scraper_config.json`:

```json
{
  "url": "https://shadowfox.in",
  "selectors": {
    "title": "title",
    "headings": "h1, h2, h3, h4, h5, h6",
    "links": "a",
    "paragraphs": "p",
    "tables": "table",
    "images": "img"
  },
  "output_formats": ["json", "csv", "sqlite"],
  "output_directory": "output",
  "crawl_depth": 1,
  "timeout": 30,
  "rate_limit": 1.0,
  "follow_links": false,
  "max_pages": 5
}
```

### Configuration Parameters

| Parameter          | Type    | Description                       | Default         |
| ------------------ | ------- | --------------------------------- | --------------- |
| `url`              | string  | Target URL to scrape              | Required        |
| `selectors`        | object  | CSS selectors for data extraction | Required        |
| `output_formats`   | array   | Output formats: json, csv, sqlite | ["json", "csv"] |
| `output_directory` | string  | Directory for output files        | "output"        |
| `crawl_depth`      | integer | Depth of crawling                 | 1               |
| `timeout`          | integer | Request timeout in seconds        | 30              |
| `rate_limit`       | float   | Requests per second               | 1.0             |
| `follow_links`     | boolean | Follow pagination links           | false           |
| `max_pages`        | integer | Maximum pages to scrape           | 10              |

### Custom Selectors

You can define custom CSS selectors for any HTML elements:

```json
{
  "selectors": {
    "article_titles": "article h2",
    "navigation": "nav a",
    "custom_content": ".custom-class"
  }
}
```

## 📤 Output Formats

### JSON Output

```json
{
  "headings": [
    { "tag": "h1", "text": "Main Title" },
    { "tag": "h2", "text": "Subtitle" }
  ],
  "links": [
    { "text": "Home", "href": "https://example.com/" },
    { "text": "About", "href": "https://example.com/about" }
  ],
  "metadata": {
    "title": "Page Title",
    "og_tags": {}
  }
}
```

### CSV Output

```csv
category,tag,text
headings,h1,Main Title
headings,h2,Subtitle
links,,Home
...
```

### SQLite Database

- Automatically creates database with scraped data
- Includes metadata table for tracking
- One table per scrape with timestamp

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_parser.py
pytest tests/test_scraper.py
```

### Run with Coverage

```bash
pytest --cov=src tests/
```

### Test Categories

#### Unit Tests

- Parser functionality
- URL validation
- Configuration validation
- Storage operations

#### Integration Tests

- Full scraping workflow
- Error handling
- Data transformation

## 📚 Module Documentation

### scraper.py

Main scraping module. Handles:

- HTTP requests with retry strategy
- Session management
- Pagination and link following
- Error tracking

**Key Classes:**

- `Scraper`: Main scraper class

### parser.py

HTML parsing and data extraction. Handles:

- HTML parsing with BeautifulSoup
- Element extraction (headings, links, tables, etc.)
- Metadata extraction
- Data cleaning

**Key Classes:**

- `HTMLParser`: Main parser
- `ElementExtractor`: Element extraction

### storage.py

Data storage in multiple formats. Handles:

- JSON serialization
- CSV export
- SQLite database

**Key Classes:**

- `StorageManager`: Manages all storage formats
- `JSONStorage`: JSON storage
- `CSVStorage`: CSV storage
- `SQLiteStorage`: SQLite storage

### config_loader.py

Configuration management. Handles:

- Loading JSON configuration
- Configuration validation
- Parameter access

**Key Classes:**

- `ConfigLoader`: Loads and manages configuration
- `ConfigurationValidator`: Validates configuration

### error_handler.py

Error handling and logging. Handles:

- Custom exceptions
- Logging setup
- Error tracking

**Key Classes:**

- `Logger`: Singleton logger
- `ErrorHandler`: Error tracking

### utils.py

Utility functions. Includes:

- URL validation and normalization
- Rate limiting
- Data processing
- Timing utilities

**Key Classes:**

- `URLValidator`: URL validation
- `RateLimiter`: Rate limiting
- `DataProcessor`: Data processing
- `TimingUtils`: Timing operations

## 🐳 Docker Usage

### Build Docker Image

```bash
docker build -t webscraper .
```

### Run with Docker

```bash
docker run -v $(pwd)/output:/app/output webscraper --url https://example.com
```

### Using Docker Compose

```bash
# Basic usage
docker-compose up

# With custom command
docker-compose run scraper --url https://example.com --format json --verbose

# Build and run
docker-compose up --build
```

## 📝 Logging

Logs are automatically saved to `logs/scraper.log`.

### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for specific failures
- **CRITICAL**: Critical errors that may cause termination

### Log Example

```
2024-01-15 10:30:45 - webscraper - INFO - Starting scrape of https://example.com
2024-01-15 10:30:46 - webscraper - DEBUG - Fetching https://example.com
2024-01-15 10:30:47 - webscraper - INFO - Successfully scraped https://example.com
2024-01-15 10:30:48 - webscraper - INFO - Data saved to JSON: output/data.json
```

## 🔍 Example Workflows

### Basic Website Scraping

```bash
python run_scraper.py --url https://shadowfox.in
```

### Multi-format Export

```bash
python run_scraper.py --url https://example.com --format json csv sqlite
```

### Website Crawling

```bash
python run_scraper.py --url https://example.com --follow-links --max-pages 10
```

### Custom Output and Settings

```bash
python run_scraper.py \
  --url https://example.com \
  --output my_data \
  --rate-limit 0.5 \
  --timeout 60 \
  --format json csv \
  --verbose
```

## 🛡️ Error Handling

The scraper handles various error scenarios:

1. **Network Errors**
   - Connection timeouts
   - HTTP errors
   - DNS resolution failures

2. **Parsing Errors**
   - Invalid HTML
   - Missing elements
   - Malformed data

3. **Storage Errors**
   - File I/O errors
   - Database errors
   - Permission issues

4. **Configuration Errors**
   - Invalid URL format
   - Missing required fields
   - Invalid selectors

All errors are logged and tracked. Use `get_error_summary()` to view error details.

## 📊 Rate Limiting

The scraper implements polite scraping with configurable rate limiting:

```json
{
  "rate_limit": 1.0
}
```

- `1.0` = 1 request per second (default)
- `0.5` = 1 request every 2 seconds
- `2.0` = 2 requests per second

## 🔐 Best Practices

1. **Respect robots.txt**: Always check the website's robots.txt
2. **Rate Limiting**: Use appropriate delays between requests
3. **User-Agent**: The scraper includes a proper User-Agent header
4. **Error Handling**: Check logs for errors and adjust configuration
5. **Legal Compliance**: Ensure scraping complies with website's TOS and laws

## 🤝 Contributing

To extend or modify the scraper:

1. Create new modules in `src/`
2. Add corresponding tests in `tests/`
3. Update configuration if needed
4. Document changes in README

## 📄 License

This project is provided as-is for educational purposes.

## 🆘 Troubleshooting

### Issue: Connection Timeout

**Solution**: Increase timeout value

```bash
python run_scraper.py --url https://example.com --timeout 60
```

### Issue: Too Many Requests Error

**Solution**: Reduce rate limit

```bash
python run_scraper.py --url https://example.com --rate-limit 0.5
```

### Issue: No Data Extracted

**Solution**: Verify CSS selectors in configuration

```bash
# Check page source to confirm selectors
# Update selectors in config/scraper_config.json
```

### Issue: Permission Denied on Output

**Solution**: Check directory permissions

```bash
chmod 777 output/
```

## 📞 Support

For issues, questions, or improvements:

1. Check the logs in `logs/scraper.log`
2. Review the configuration file
3. Verify CSS selectors match target website
4. Check internet connection and target website availability

## 🎯 Future Enhancements

- [ ] JavaScript rendering support (Selenium/Playwright)
- [ ] Proxy support for distributed scraping
- [ ] Advanced filtering and data validation
- [ ] API endpoint for remote scraping
- [ ] Web dashboard for monitoring
- [ ] Scheduled scraping tasks
- [ ] Machine learning-based data extraction

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Python**: 3.8+
