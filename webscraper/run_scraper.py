#!/usr/bin/env python3
"""
Main entry point for the web scraper.
Provides CLI interface for running the scraper with custom configuration.
"""

import argparse
import json
import sys
import os
from datetime import datetime
from pathlib import Path

from src.scraper import Scraper
from src.parser import HTMLParser
from src.storage import StorageManager
from src.config_loader import ConfigLoader
from src.error_handler import Logger, ErrorHandler, ConfigurationError


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Create command-line argument parser.
    
    Returns:
        Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description='Web Scraper - Extract data from websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python run_scraper.py --config config/scraper_config.json
  python run_scraper.py --url https://shadowfox.in --format json csv
  python run_scraper.py --url https://example.com --follow-links --max-pages 5
        '''
    )
    
    # Configuration file
    parser.add_argument(
        '--config',
        '-c',
        type=str,
        default='config/scraper_config.json',
        help='Path to configuration file (default: config/scraper_config.json)'
    )
    
    # URL override
    parser.add_argument(
        '--url',
        '-u',
        type=str,
        help='Target URL (overrides config file)'
    )
    
    # Output formats
    parser.add_argument(
        '--format',
        '-f',
        nargs='+',
        choices=['json', 'csv', 'sqlite'],
        help='Output formats (default: json csv)'
    )
    
    # Output directory
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Output directory (overrides config file)'
    )
    
    # Follow links
    parser.add_argument(
        '--follow-links',
        action='store_true',
        help='Follow links in pages (pagination/crawling)'
    )
    
    # Max pages
    parser.add_argument(
        '--max-pages',
        type=int,
        help='Maximum number of pages to scrape'
    )
    
    # Rate limit
    parser.add_argument(
        '--rate-limit',
        type=float,
        help='Requests per second (default: 1.0)'
    )
    
    # Timeout
    parser.add_argument(
        '--timeout',
        type=int,
        help='Request timeout in seconds (default: 30)'
    )
    
    # Verbose
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    # Version
    parser.add_argument(
        '--version',
        action='version',
        version='Web Scraper 1.0.0'
    )
    
    return parser


def load_configuration(args) -> dict:
    """
    Load configuration from file and apply CLI overrides.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Configuration dictionary
    """
    logger = Logger()
    
    # Load config file
    config_path = args.config
    if not os.path.exists(config_path):
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    
    config_loader = ConfigLoader(config_path)
    config = config_loader.load()
    
    # Apply CLI overrides
    if args.url:
        config['url'] = args.url
        logger.info(f"URL overridden: {args.url}")
    
    if args.format:
        config['output_formats'] = args.format
        logger.info(f"Output formats set to: {args.format}")
    
    if args.output:
        config['output_directory'] = args.output
        logger.info(f"Output directory set to: {args.output}")
    
    if args.follow_links:
        config['follow_links'] = True
        logger.info("Link following enabled")
    
    if args.max_pages:
        config['max_pages'] = args.max_pages
        logger.info(f"Max pages set to: {args.max_pages}")
    
    if args.rate_limit:
        config['rate_limit'] = args.rate_limit
        logger.info(f"Rate limit set to: {args.rate_limit}")
    
    if args.timeout:
        config['timeout'] = args.timeout
        logger.info(f"Timeout set to: {args.timeout}")
    
    return config


def run_scraper(config: dict) -> dict:
    """
    Run the scraper with given configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Scraped data
    """
    logger = Logger()
    
    try:
        # Initialize scraper
        logger.info("Initializing scraper...")
        scraper = Scraper(config)
        
        # Get URL to scrape
        url = config.get('url')
        if not url:
            raise ConfigurationError("No URL specified in configuration")
        
        # Scrape
        logger.info(f"Starting web scraping from {url}")
        data = scraper.scrape(url)
        
        # Log errors if any
        error_summary = scraper.get_error_summary()
        if error_summary['total_errors'] > 0:
            logger.warning(
                f"Scraping completed with {error_summary['total_errors']} errors"
            )
        
        scraper.close()
        return data
    
    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}", exc_info=True)
        raise


def save_data(data: dict, config: dict) -> None:
    """
    Save scraped data to files.
    
    Args:
        data: Scraped data dictionary
        config: Configuration dictionary
    """
    logger = Logger()
    
    try:
        output_dir = config.get('output_directory', 'output')
        formats = config.get('output_formats', ['json', 'csv'])
        
        logger.info(f"Saving data to {output_dir}...")
        
        storage_manager = StorageManager(output_dir)
        
        # Generate timestamp for filename prefix
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        
        saved_files = storage_manager.save(data, formats, prefix=timestamp)
        
        logger.info("Data saved successfully:")
        for fmt, filepath in saved_files.items():
            if filepath:
                logger.info(f"  - {fmt.upper()}: {filepath}")
    
    except Exception as e:
        logger.error(f"Error saving data: {str(e)}", exc_info=True)
        raise


def print_summary(data: dict, config: dict) -> None:
    """
    Print summary of scraped data.
    
    Args:
        data: Scraped data dictionary
        config: Configuration dictionary
    """
    print("\n" + "="*60)
    print("SCRAPING SUMMARY")
    print("="*60)
    
    # Count items
    for key, items in data.items():
        if key == '_metadata':
            continue
        
        if isinstance(items, list):
            count = len(items)
            print(f"✓ {key.capitalize()}: {count} items")
        elif isinstance(items, dict):
            count = len(items)
            print(f"✓ {key.capitalize()}: {count} items")
    
    # Metadata
    if '_metadata' in data:
        meta = data['_metadata']
        print(f"\nURL: {meta.get('url', 'N/A')}")
        print(f"Status Code: {meta.get('status_code', 'N/A')}")
        print(f"Content Size: {meta.get('content_length', 'N/A')} bytes")
    
    print("="*60 + "\n")


def main():
    """Main entry point."""
    try:
        # Parse arguments
        parser = create_argument_parser()
        args = parser.parse_args()
        
        # Setup logging
        logger = Logger()
        
        if args.verbose:
            logger.info("Verbose mode enabled")
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_configuration(args)
        
        # Run scraper
        data = run_scraper(config)
        
        # Check for errors
        if 'error' in data:
            logger.error(f"Scraping failed: {data['error']}")
            print(f"\n✗ Error: {data['error']}")
            sys.exit(1)
        
        # Save data
        save_data(data, config)
        
        # Print summary
        print_summary(data, config)
        
        logger.info("Scraping completed successfully")
        print("✓ Scraping completed successfully!")
    
    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
