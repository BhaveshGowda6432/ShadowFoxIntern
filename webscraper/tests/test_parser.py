"""
Tests for the parser module.
Tests HTML parsing and data extraction functionality.
"""

import pytest
from bs4 import BeautifulSoup
from src.parser import HTMLParser, ElementExtractor


class TestElementExtractor:
    """Test ElementExtractor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_html = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Main Heading</h1>
                <h2>Sub Heading</h2>
                <p>First paragraph with content.</p>
                <p>Second paragraph with more content.</p>
                <a href="https://example.com">Link Text</a>
                <a href="/relative/path">Relative Link</a>
                <img src="image.jpg" alt="Test Image" title="Image Title" />
                <table>
                    <tr><th>Header 1</th><th>Header 2</th></tr>
                    <tr><td>Data 1</td><td>Data 2</td></tr>
                    <tr><td>Data 3</td><td>Data 4</td></tr>
                </table>
            </body>
        </html>
        """
        
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')
        self.extractor = ElementExtractor(self.soup, base_url="https://example.com")
    
    def test_extract_titles(self):
        """Test title extraction."""
        titles = self.extractor.extract_titles()
        assert len(titles) > 0
        assert any('Test Page' in str(t) for t in titles)
    
    def test_extract_headings(self):
        """Test heading extraction."""
        headings = self.extractor.extract_headings()
        assert len(headings) == 2
        assert any('Main Heading' in str(h) for h in headings)
        assert any('Sub Heading' in str(h) for h in headings)
    
    def test_extract_paragraphs(self):
        """Test paragraph extraction."""
        paragraphs = self.extractor.extract_paragraphs()
        assert len(paragraphs) == 2
        assert any('First paragraph' in str(p) for p in paragraphs)
    
    def test_extract_links(self):
        """Test link extraction."""
        links = self.extractor.extract_links()
        assert len(links) == 2
        assert any('Link Text' in str(l) for l in links)
        assert any('https://example.com' in str(l) for l in links)
    
    def test_extract_images(self):
        """Test image extraction."""
        images = self.extractor.extract_images()
        assert len(images) == 1
        assert any('image.jpg' in str(i) for i in images)
        assert any('Test Image' in str(i) for i in images)
    
    def test_extract_tables(self):
        """Test table extraction."""
        tables = self.extractor.extract_tables()
        assert len(tables) == 1
        assert tables[0]['headers'] == ['Header 1', 'Header 2']
        assert len(tables[0]['rows']) == 2
    
    def test_extract_metadata(self):
        """Test metadata extraction."""
        metadata = self.extractor.extract_metadata()
        assert 'title' in metadata
        assert metadata['title'] == 'Test Page'
        assert 'meta_tags' in metadata


class TestHTMLParser:
    """Test HTMLParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = HTMLParser()
        self.sample_html = """
        <html>
            <head><title>Test</title></head>
            <body>
                <h1>Heading</h1>
                <p>Content</p>
            </body>
        </html>
        """
    
    def test_parse_valid_html(self):
        """Test parsing valid HTML."""
        soup = self.parser.parse(self.sample_html)
        assert soup is not None
        assert soup.find('title').string == 'Test'
    
    def test_parse_empty_html_raises_error(self):
        """Test parsing empty HTML raises ParsingError."""
        with pytest.raises(Exception):
            self.parser.parse("")
    
    def test_extract_data_with_selectors(self):
        """Test data extraction with selectors."""
        selectors = {
            'headings': 'h1',
            'paragraphs': 'p'
        }
        
        data = self.parser.extract_data(self.sample_html, selectors)
        
        assert 'headings' in data
        assert 'paragraphs' in data
        assert len(data['headings']) > 0
        assert len(data['paragraphs']) > 0


@pytest.fixture
def parser():
    """Fixture for parser instance."""
    return HTMLParser()


@pytest.fixture
def sample_html():
    """Fixture for sample HTML."""
    return """
    <html>
        <body>
            <h1>Test Heading</h1>
            <a href="link">Click Here</a>
        </body>
    </html>
    """


def test_parser_with_fixtures(parser, sample_html):
    """Test parser using fixtures."""
    soup = parser.parse(sample_html)
    assert soup.find('h1').string == 'Test Heading'
