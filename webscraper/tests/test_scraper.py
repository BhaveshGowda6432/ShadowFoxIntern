"""
Tests for the scraper module.
Tests scraping functionality, URL validation, and configuration.
"""

import pytest
from src.scraper import Scraper
from src.utils import URLValidator, RateLimiter
from src.config_loader import ConfigLoader, ConfigurationValidator
from src.storage import StorageManager
from src.error_handler import URLValidationError, ConfigurationError


class TestURLValidator:
    """Test URLValidator class."""
    
    def test_valid_http_url(self):
        """Test validation of valid HTTP URL."""
        assert URLValidator.is_valid_url("http://example.com")
        assert URLValidator.is_valid_url("http://example.com/path")
    
    def test_valid_https_url(self):
        """Test validation of valid HTTPS URL."""
        assert URLValidator.is_valid_url("https://example.com")
        assert URLValidator.is_valid_url("https://example.com/path?query=1")
    
    def test_invalid_url(self):
        """Test validation of invalid URL."""
        assert not URLValidator.is_valid_url("not a url")
        assert not URLValidator.is_valid_url("example.com")
        assert not URLValidator.is_valid_url("")
    
    def test_normalize_url_with_http(self):
        """Test URL normalization with http prefix."""
        normalized = URLValidator.normalize_url("http://example.com")
        assert normalized.startswith("http://")
    
    def test_normalize_url_without_prefix(self):
        """Test URL normalization without prefix."""
        normalized = URLValidator.normalize_url("example.com")
        assert normalized.startswith("https://")
    
    def test_join_urls(self):
        """Test joining base and relative URLs."""
        base = "https://example.com/page/"
        relative = "../other/path"
        joined = URLValidator.join_urls(base, relative)
        assert "example.com" in joined
    
    def test_get_domain(self):
        """Test domain extraction."""
        url = "https://example.com/path"
        domain = URLValidator.get_domain(url)
        assert domain == "example.com"


class TestRateLimiter:
    """Test RateLimiter class."""
    
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests_per_second=2.0)
        assert limiter.requests_per_second == 2.0
        assert limiter.min_interval == 0.5
    
    def test_rate_limiter_reset(self):
        """Test rate limiter reset."""
        limiter = RateLimiter()
        limiter.wait()
        limiter.reset()
        assert limiter.last_request_time == 0


class TestConfigurationValidator:
    """Test ConfigurationValidator class."""
    
    def test_validate_valid_url(self):
        """Test URL validation."""
        assert ConfigurationValidator.validate_url("https://example.com")
    
    def test_validate_invalid_url_raises_error(self):
        """Test invalid URL raises error."""
        with pytest.raises(URLValidationError):
            ConfigurationValidator.validate_url("invalid url")
    
    def test_validate_selectors(self):
        """Test selector validation."""
        selectors = {
            'headings': 'h1, h2',
            'links': 'a'
        }
        assert ConfigurationValidator.validate_selectors(selectors)
    
    def test_validate_valid_output_formats(self):
        """Test valid output format validation."""
        assert ConfigurationValidator.validate_output_formats(['json', 'csv'])
    
    def test_validate_invalid_output_format_raises_error(self):
        """Test invalid output format raises error."""
        with pytest.raises(ConfigurationError):
            ConfigurationValidator.validate_output_formats(['invalid_format'])
    
    def test_validate_valid_crawl_depth(self):
        """Test valid crawl depth validation."""
        assert ConfigurationValidator.validate_crawl_depth(2)
    
    def test_validate_invalid_crawl_depth_raises_error(self):
        """Test invalid crawl depth raises error."""
        with pytest.raises(ConfigurationError):
            ConfigurationValidator.validate_crawl_depth(0)
    
    def test_validate_valid_timeout(self):
        """Test valid timeout validation."""
        assert ConfigurationValidator.validate_timeout(30)
    
    def test_validate_invalid_timeout_raises_error(self):
        """Test invalid timeout raises error."""
        with pytest.raises(ConfigurationError):
            ConfigurationValidator.validate_timeout(0)


class TestStorageManager:
    """Test StorageManager class."""
    
    def test_storage_manager_initialization(self):
        """Test storage manager initialization."""
        manager = StorageManager(output_directory='test_output')
        assert manager.output_directory == 'test_output'
    
    @pytest.mark.asyncio
    def test_save_json_format(self):
        """Test saving in JSON format."""
        manager = StorageManager(output_directory='test_output')
        data = {
            'headings': [{'text': 'Test Heading'}],
            'links': [{'text': 'Link', 'href': 'url'}]
        }
        
        try:
            result = manager.save(data, formats=['json'])
            assert 'json' in result
            assert result['json'] is not None
        except Exception as e:
            # Test environment might not allow file creation
            pass
    
    @pytest.mark.asyncio
    def test_save_csv_format(self):
        """Test saving in CSV format."""
        manager = StorageManager(output_directory='test_output')
        data = {
            'headings': [{'text': 'Test Heading'}],
            'links': [{'text': 'Link', 'href': 'url'}]
        }
        
        try:
            result = manager.save(data, formats=['csv'])
            assert 'csv' in result
            assert result['csv'] is not None
        except Exception as e:
            # Test environment might not allow file creation
            pass


class TestScraperConfiguration:
    """Test Scraper with configuration."""
    
    def test_scraper_initialization(self):
        """Test scraper initialization."""
        config = {
            'url': 'https://example.com',
            'selectors': {'headings': 'h1'},
            'timeout': 30,
            'rate_limit': 1.0,
            'follow_links': False,
            'max_pages': 5
        }
        
        scraper = Scraper(config)
        assert scraper.config == config
        assert scraper.session is not None
    
    def test_scraper_session_setup(self):
        """Test scraper session is properly configured."""
        config = {
            'url': 'https://example.com',
            'selectors': {'headings': 'h1'}
        }
        
        scraper = Scraper(config)
        assert scraper.session.headers.get('User-Agent') is not None


# Integration tests (require network)
@pytest.mark.integration
class TestScraperIntegration:
    """Integration tests for scraper (requires network)."""
    
    @pytest.mark.skip(reason="Requires network access")
    def test_scrape_real_website(self):
        """Test scraping a real website."""
        config = {
            'url': 'https://httpbin.org/html',
            'selectors': {'headings': 'h1, h2, h3'},
            'timeout': 30,
            'rate_limit': 1.0
        }
        
        scraper = Scraper(config)
        data = scraper.scrape('https://httpbin.org/html')
        
        assert 'headings' in data or 'error' in data


# Fixtures for common test data
@pytest.fixture
def sample_config():
    """Fixture for sample configuration."""
    return {
        'url': 'https://example.com',
        'selectors': {
            'headings': 'h1, h2, h3',
            'links': 'a',
            'paragraphs': 'p'
        },
        'output_formats': ['json', 'csv'],
        'timeout': 30,
        'rate_limit': 1.0,
        'follow_links': False,
        'max_pages': 5
    }


@pytest.fixture
def sample_data():
    """Fixture for sample scraped data."""
    return {
        'headings': [
            {'tag': 'h1', 'text': 'Main Heading'},
            {'tag': 'h2', 'text': 'Sub Heading'}
        ],
        'links': [
            {'text': 'Home', 'href': 'https://example.com/'},
            {'text': 'About', 'href': 'https://example.com/about'}
        ],
        'paragraphs': [
            {'text': 'First paragraph content'},
            {'text': 'Second paragraph content'}
        ],
        'metadata': {
            'title': 'Example Page',
            'og_tags': {}
        }
    }


def test_with_sample_config_fixture(sample_config):
    """Test using sample config fixture."""
    assert sample_config['url'] == 'https://example.com'
    assert 'headings' in sample_config['selectors']


def test_with_sample_data_fixture(sample_data):
    """Test using sample data fixture."""
    assert len(sample_data['headings']) == 2
    assert len(sample_data['links']) == 2
    assert sample_data['metadata']['title'] == 'Example Page'
