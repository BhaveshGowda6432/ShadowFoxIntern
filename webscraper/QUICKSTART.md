# Quick Start Guide

Get up and running with the Web Scraper in 5 minutes!

## Step 1: Installation (1 minute)

```bash
# Navigate to project directory
cd web-scraper-project

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration (1 minute)

Edit `config/scraper_config.json`:

```json
{
  "url": "https://shadowfox.in",
  "selectors": {
    "headings": "h1, h2, h3",
    "links": "a",
    "paragraphs": "p"
  },
  "output_formats": ["json", "csv"],
  "timeout": 30,
  "rate_limit": 1.0
}
```

## Step 3: Run the Scraper (1 minute)

```bash
# Basic usage (uses config file)
python run_scraper.py

# Or with custom URL
python run_scraper.py --url https://example.com --format json csv

# See all options
python run_scraper.py --help
```

## Step 4: Check Results (1 minute)

Output files are saved in the `output/` directory:

- `data.json` - Structured JSON format
- `data.csv` - Spreadsheet format
- Check `logs/scraper.log` for execution details

## Step 5: Customize (optional)

Modify selectors in `config/scraper_config.json` to extract different elements:

```json
{
  "selectors": {
    "article_titles": "article h2",
    "custom_content": ".my-class",
    "navigation": "nav a"
  }
}
```

## Common Tasks

### Scrape with Pagination

```bash
python run_scraper.py --url https://example.com --follow-links --max-pages 5
```

### Export to All Formats

```bash
python run_scraper.py --url https://example.com --format json csv sqlite
```

### Adjust Rate Limiting

```bash
python run_scraper.py --url https://example.com --rate-limit 0.5
```

### Increase Timeout

```bash
python run_scraper.py --url https://example.com --timeout 60
```

## Troubleshooting

### No Data Extracted?

1. Check if selectors match the website
2. Inspect page source to find correct selectors
3. Update `config/scraper_config.json`

### Connection Timeout?

```bash
python run_scraper.py --url https://example.com --timeout 60
```

### Too Many Requests Error?

```bash
python run_scraper.py --url https://example.com --rate-limit 0.5
```

## Docker Usage

```bash
# Build image
docker build -t webscraper .

# Run with Docker
docker run -v $(pwd)/output:/app/output webscraper --url https://example.com
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Run tests: `pytest`
- View logs: `cat logs/scraper.log`

## Support

If you need help:

1. Check the README.md
2. Review logs in `logs/scraper.log`
3. Verify CSS selectors match your target website
4. Try increasing timeout or reducing rate limit
