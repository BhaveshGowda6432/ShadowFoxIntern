"""
Error handling and logging module for the web scraper.
Handles all exceptions, errors, and logging operations.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional, Dict, Any


class ScraperError(Exception):
    """Base exception class for scraper-related errors."""
    pass


class NetworkError(ScraperError):
    """Exception for network-related errors."""
    pass


class ParsingError(ScraperError):
    """Exception for HTML parsing errors."""
    pass


class ConfigurationError(ScraperError):
    """Exception for configuration-related errors."""
    pass


class StorageError(ScraperError):
    """Exception for storage-related errors."""
    pass


class URLValidationError(ScraperError):
    """Exception for URL validation errors."""
    pass


class Logger:
    """Custom logger for the web scraper."""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger."""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up logging configuration."""
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        
        log_file = os.path.join(logs_dir, 'scraper.log')
        
        # Create logger
        self._logger = logging.getLogger('WebScraper')
        self._logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in self._logger.handlers:
            self._logger.removeHandler(handler)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler (detailed)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self._logger.addHandler(file_handler)
        
        # Console handler (simple)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self._logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the logger instance."""
        return self._logger
    
    def info(self, message: str) -> None:
        """Log info message."""
        self._logger.info(message)
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        self._logger.debug(message)
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        self._logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False) -> None:
        """Log error message."""
        self._logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str) -> None:
        """Log critical message."""
        self._logger.critical(message)


class ErrorHandler:
    """Error handler for scraper operations."""
    
    def __init__(self):
        """Initialize error handler."""
        self.logger = Logger()
        self.error_count = 0
        self.error_log: list = []
    
    def handle_network_error(self, url: str, exception: Exception) -> None:
        """Handle network errors."""
        error_msg = f"Network error while accessing {url}: {str(exception)}"
        self.logger.error(error_msg)
        self.error_count += 1
        self.error_log.append({
            'type': 'NetworkError',
            'url': url,
            'message': str(exception),
            'timestamp': datetime.now().isoformat()
        })
    
    def handle_parsing_error(self, url: str, exception: Exception) -> None:
        """Handle parsing errors."""
        error_msg = f"Parsing error for {url}: {str(exception)}"
        self.logger.error(error_msg)
        self.error_count += 1
        self.error_log.append({
            'type': 'ParsingError',
            'url': url,
            'message': str(exception),
            'timestamp': datetime.now().isoformat()
        })
    
    def handle_storage_error(self, file_path: str, exception: Exception) -> None:
        """Handle storage errors."""
        error_msg = f"Storage error while saving to {file_path}: {str(exception)}"
        self.logger.error(error_msg)
        self.error_count += 1
        self.error_log.append({
            'type': 'StorageError',
            'file_path': file_path,
            'message': str(exception),
            'timestamp': datetime.now().isoformat()
        })
    
    def handle_configuration_error(self, exception: Exception) -> None:
        """Handle configuration errors."""
        error_msg = f"Configuration error: {str(exception)}"
        self.logger.error(error_msg)
        self.error_count += 1
        self.error_log.append({
            'type': 'ConfigurationError',
            'message': str(exception),
            'timestamp': datetime.now().isoformat()
        })
    
    def handle_validation_error(self, field: str, value: str, exception: Exception) -> None:
        """Handle validation errors."""
        error_msg = f"Validation error for {field} '{value}': {str(exception)}"
        self.logger.error(error_msg)
        self.error_count += 1
        self.error_log.append({
            'type': 'ValidationError',
            'field': field,
            'value': value,
            'message': str(exception),
            'timestamp': datetime.now().isoformat()
        })
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get error summary."""
        return {
            'total_errors': self.error_count,
            'errors': self.error_log
        }
    
    def reset_errors(self) -> None:
        """Reset error tracking."""
        self.error_count = 0
        self.error_log = []
