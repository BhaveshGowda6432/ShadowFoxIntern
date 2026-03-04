"""
Configuration loader module for the web scraper.
Loads and validates configuration from JSON files.
"""

import json
import os
from typing import Dict, Any, List, Optional
from src.error_handler import ConfigurationError, Logger, URLValidationError
from src.utils import URLValidator


class ConfigurationValidator:
    """Validates configuration data."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        if not URLValidator.is_valid_url(url):
            raise URLValidationError(f"Invalid URL format: {url}")
        return True
    
    @staticmethod
    def validate_selectors(selectors: Dict[str, Any]) -> bool:
        """Validate CSS selectors."""
        if not isinstance(selectors, dict):
            raise ConfigurationError("Selectors must be a dictionary")
        
        for key, value in selectors.items():
            if not isinstance(value, (str, dict)):
                raise ConfigurationError(f"Selector for '{key}' must be string or dict")
        
        return True
    
    @staticmethod
    def validate_output_formats(formats: List[str]) -> bool:
        """Validate output formats."""
        valid_formats = {'csv', 'json', 'sqlite'}
        
        if not isinstance(formats, list):
            raise ConfigurationError("Output formats must be a list")
        
        for fmt in formats:
            if fmt.lower() not in valid_formats:
                raise ConfigurationError(
                    f"Invalid output format: {fmt}. "
                    f"Valid formats: {', '.join(valid_formats)}"
                )
        
        return True
    
    @staticmethod
    def validate_crawl_depth(depth: int) -> bool:
        """Validate crawl depth."""
        if not isinstance(depth, int):
            raise ConfigurationError("Crawl depth must be an integer")
        
        if depth < 1:
            raise ConfigurationError("Crawl depth must be at least 1")
        
        return True
    
    @staticmethod
    def validate_timeout(timeout: int) -> bool:
        """Validate timeout value."""
        if not isinstance(timeout, int):
            raise ConfigurationError("Timeout must be an integer")
        
        if timeout < 1:
            raise ConfigurationError("Timeout must be at least 1 second")
        
        return True


class ConfigLoader:
    """Loads configuration from JSON file."""
    
    def __init__(self, config_path: str):
        """
        Initialize config loader.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = config_path
        self.logger = Logger()
        self.config: Dict[str, Any] = {}
        self.validator = ConfigurationValidator()
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file.
        
        Returns:
            Configuration dictionary
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not os.path.exists(self.config_path):
            raise ConfigurationError(f"Configuration file not found: {self.config_path}")
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            self._validate_config()
            return self.config
        
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Invalid JSON in configuration file: {str(e)}")
        except Exception as e:
            raise ConfigurationError(f"Error loading configuration: {str(e)}")
    
    def _validate_config(self) -> None:
        """Validate configuration data."""
        # Validate required fields
        required_fields = ['url', 'selectors']
        
        for field in required_fields:
            if field not in self.config:
                raise ConfigurationError(f"Missing required field: {field}")
        
        # Validate URL
        self.validator.validate_url(self.config['url'])
        
        # Validate selectors
        self.validator.validate_selectors(self.config['selectors'])
        
        # Validate output formats if provided
        if 'output_formats' in self.config:
            self.validator.validate_output_formats(self.config['output_formats'])
        
        # Validate crawl depth if provided
        if 'crawl_depth' in self.config:
            self.validator.validate_crawl_depth(self.config.get('crawl_depth', 1))
        
        # Validate timeout if provided
        if 'timeout' in self.config:
            self.validator.validate_timeout(self.config.get('timeout', 30))
        
        self.logger.info("Configuration validation successful")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def get_url(self) -> str:
        """Get target URL."""
        return self.get('url')
    
    def get_selectors(self) -> Dict[str, Any]:
        """Get CSS selectors."""
        return self.get('selectors', {})
    
    def get_output_formats(self) -> List[str]:
        """Get output formats."""
        formats = self.get('output_formats', ['json', 'csv'])
        # Convert to lowercase for consistency
        return [fmt.lower() for fmt in formats]
    
    def get_crawl_depth(self) -> int:
        """Get crawl depth."""
        return self.get('crawl_depth', 1)
    
    def get_timeout(self) -> int:
        """Get request timeout."""
        return self.get('timeout', 30)
    
    def get_rate_limit(self) -> float:
        """Get rate limit (requests per second)."""
        return self.get('rate_limit', 1.0)
    
    def get_output_directory(self) -> str:
        """Get output directory."""
        return self.get('output_directory', 'output')
    
    def get_follow_links(self) -> bool:
        """Get follow links setting."""
        return self.get('follow_links', False)
    
    def get_max_pages(self) -> int:
        """Get maximum number of pages to scrape."""
        return self.get('max_pages', 10)
