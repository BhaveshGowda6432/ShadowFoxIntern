"""
Parser module for the web scraper.
Parses HTML and extracts required information.
"""

from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from src.error_handler import ParsingError, Logger
from src.utils import DataProcessor, URLValidator


class ElementExtractor:
    """Extracts elements from parsed HTML."""
    
    def __init__(self, soup: BeautifulSoup, base_url: str = ""):
        """
        Initialize element extractor.
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
        """
        self.soup = soup
        self.base_url = base_url
        self.logger = Logger()
    
    def extract_titles(self, selector: str = "title") -> List[Dict[str, Any]]:
        """
        Extract page titles.
        
        Args:
            selector: CSS selector for titles
            
        Returns:
            List of title dictionaries
        """
        try:
            titles = []
            title_elements = self.soup.select(selector) + [self.soup.find('title')]
            
            for elem in title_elements:
                if elem:
                    text = DataProcessor.extract_text_content(elem)
                    if text:
                        titles.append({'title': text})
            
            return DataProcessor.remove_duplicates(titles)
        
        except Exception as e:
            self.logger.error(f"Error extracting titles: {str(e)}")
            raise ParsingError(f"Failed to extract titles: {str(e)}")
    
    def extract_headings(self, selector: str = "h1, h2, h3, h4, h5, h6") -> List[Dict[str, Any]]:
        """
        Extract headings.
        
        Args:
            selector: CSS selector for headings
            
        Returns:
            List of heading dictionaries
        """
        try:
            headings = []
            heading_elements = self.soup.select(selector)
            
            for elem in heading_elements:
                text = DataProcessor.extract_text_content(elem)
                if text:
                    headings.append({
                        'tag': elem.name,
                        'text': text
                    })
            
            return DataProcessor.remove_duplicates(headings)
        
        except Exception as e:
            self.logger.error(f"Error extracting headings: {str(e)}")
            raise ParsingError(f"Failed to extract headings: {str(e)}")
    
    def extract_links(self, selector: str = "a") -> List[Dict[str, Any]]:
        """
        Extract links.
        
        Args:
            selector: CSS selector for links
            
        Returns:
            List of link dictionaries
        """
        try:
            links = []
            link_elements = self.soup.select(selector)
            
            for elem in link_elements:
                href = DataProcessor.extract_attribute(elem, 'href')
                if href:
                    # Convert relative URLs to absolute if base_url provided
                    if self.base_url and not href.startswith('http'):
                        href = URLValidator.join_urls(self.base_url, href)
                    
                    text = DataProcessor.extract_text_content(elem) or 'No text'
                    links.append({
                        'text': text,
                        'href': href,
                        'title': DataProcessor.extract_attribute(elem, 'title', '')
                    })
            
            return DataProcessor.remove_duplicates(links)
        
        except Exception as e:
            self.logger.error(f"Error extracting links: {str(e)}")
            raise ParsingError(f"Failed to extract links: {str(e)}")
    
    def extract_paragraphs(self, selector: str = "p") -> List[Dict[str, Any]]:
        """
        Extract paragraphs.
        
        Args:
            selector: CSS selector for paragraphs
            
        Returns:
            List of paragraph dictionaries
        """
        try:
            paragraphs = []
            para_elements = self.soup.select(selector)
            
            for elem in para_elements:
                text = DataProcessor.extract_text_content(elem)
                if text:
                    paragraphs.append({'text': text})
            
            return DataProcessor.remove_duplicates(paragraphs)
        
        except Exception as e:
            self.logger.error(f"Error extracting paragraphs: {str(e)}")
            raise ParsingError(f"Failed to extract paragraphs: {str(e)}")
    
    def extract_tables(self, selector: str = "table") -> List[Dict[str, Any]]:
        """
        Extract tables.
        
        Args:
            selector: CSS selector for tables
            
        Returns:
            List of table dictionaries
        """
        try:
            tables = []
            table_elements = self.soup.select(selector)
            
            for idx, table in enumerate(table_elements):
                table_data = {'table_id': idx, 'rows': []}
                
                # Extract headers
                headers = []
                header_elements = table.select('thead th, thead td')
                if not header_elements:
                    header_elements = table.select('tr:first-child th, tr:first-child td')
                
                for elem in header_elements:
                    headers.append(DataProcessor.extract_text_content(elem))
                
                table_data['headers'] = headers
                
                # Extract rows
                row_elements = table.select('tbody tr') or table.select('tr')[1:]
                for row in row_elements:
                    cells = []
                    for cell in row.select('td, th'):
                        cells.append(DataProcessor.extract_text_content(cell))
                    if cells:
                        table_data['rows'].append(cells)
                
                if table_data['rows']:
                    tables.append(table_data)
            
            return tables
        
        except Exception as e:
            self.logger.error(f"Error extracting tables: {str(e)}")
            raise ParsingError(f"Failed to extract tables: {str(e)}")
    
    def extract_images(self, selector: str = "img") -> List[Dict[str, Any]]:
        """
        Extract images.
        
        Args:
            selector: CSS selector for images
            
        Returns:
            List of image dictionaries
        """
        try:
            images = []
            img_elements = self.soup.select(selector)
            
            for elem in img_elements:
                src = DataProcessor.extract_attribute(elem, 'src')
                if src:
                    # Convert relative URLs to absolute if base_url provided
                    if self.base_url and not src.startswith('http'):
                        src = URLValidator.join_urls(self.base_url, src)
                    
                    images.append({
                        'src': src,
                        'alt': DataProcessor.extract_attribute(elem, 'alt', ''),
                        'title': DataProcessor.extract_attribute(elem, 'title', '')
                    })
            
            return DataProcessor.remove_duplicates(images)
        
        except Exception as e:
            self.logger.error(f"Error extracting images: {str(e)}")
            raise ParsingError(f"Failed to extract images: {str(e)}")
    
    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extract page metadata.
        
        Returns:
            Metadata dictionary
        """
        try:
            metadata = {}
            
            # Title
            title_elem = self.soup.find('title')
            metadata['title'] = DataProcessor.extract_text_content(title_elem)
            
            # Meta tags
            meta_tags = {}
            for meta in self.soup.find_all('meta'):
                name = DataProcessor.extract_attribute(meta, 'name') or \
                       DataProcessor.extract_attribute(meta, 'property')
                content = DataProcessor.extract_attribute(meta, 'content')
                if name and content:
                    meta_tags[name] = content
            
            metadata['meta_tags'] = meta_tags
            
            # Canonical link
            canonical = self.soup.find('link', {'rel': 'canonical'})
            if canonical:
                metadata['canonical'] = DataProcessor.extract_attribute(canonical, 'href')
            
            # Open Graph tags
            og_tags = {}
            for meta in self.soup.find_all('meta', {'property': True}):
                prop = meta.get('property', '')
                if prop.startswith('og:'):
                    og_tags[prop] = DataProcessor.extract_attribute(meta, 'content')
            
            metadata['og_tags'] = og_tags
            
            return metadata
        
        except Exception as e:
            self.logger.error(f"Error extracting metadata: {str(e)}")
            raise ParsingError(f"Failed to extract metadata: {str(e)}")


class HTMLParser:
    """Main HTML parser."""
    
    def __init__(self):
        """Initialize HTML parser."""
        self.logger = Logger()
    
    def parse(self, html_content: str, base_url: str = "") -> BeautifulSoup:
        """
        Parse HTML content.
        
        Args:
            html_content: HTML content as string
            base_url: Base URL for resolving relative links
            
        Returns:
            BeautifulSoup object
            
        Raises:
            ParsingError: If parsing fails
        """
        try:
            if not html_content:
                raise ParsingError("Empty HTML content")
            
            soup = BeautifulSoup(html_content, 'html.parser')
            self.logger.debug("HTML parsed successfully")
            return soup
        
        except Exception as e:
            self.logger.error(f"HTML parsing error: {str(e)}")
            raise ParsingError(f"Failed to parse HTML: {str(e)}")
    
    def extract_data(self, html_content: str, selectors: Dict[str, Any], 
                     base_url: str = "") -> Dict[str, Any]:
        """
        Extract data from HTML based on selectors.
        
        Args:
            html_content: HTML content
            selectors: Dictionary of selectors to extract
            base_url: Base URL for resolving relative links
            
        Returns:
            Extracted data dictionary
        """
        try:
            soup = self.parse(html_content, base_url)
            extractor = ElementExtractor(soup, base_url)
            extracted_data = {}
            
            for key, selector in selectors.items():
                key_lower = key.lower()
                
                try:
                    if key_lower == 'title' or key_lower == 'titles':
                        extracted_data['titles'] = extractor.extract_titles(selector)
                    
                    elif key_lower == 'heading' or key_lower == 'headings':
                        extracted_data['headings'] = extractor.extract_headings(selector)
                    
                    elif key_lower == 'link' or key_lower == 'links':
                        extracted_data['links'] = extractor.extract_links(selector)
                    
                    elif key_lower == 'paragraph' or key_lower == 'paragraphs':
                        extracted_data['paragraphs'] = extractor.extract_paragraphs(selector)
                    
                    elif key_lower == 'table' or key_lower == 'tables':
                        extracted_data['tables'] = extractor.extract_tables(selector)
                    
                    elif key_lower == 'image' or key_lower == 'images':
                        extracted_data['images'] = extractor.extract_images(selector)
                    
                    else:
                        # Custom selector
                        elements = soup.select(selector)
                        data = []
                        for elem in elements:
                            text = DataProcessor.extract_text_content(elem)
                            if text:
                                data.append({'text': text})
                        extracted_data[key] = DataProcessor.remove_duplicates(data)
                
                except ParsingError as e:
                    self.logger.warning(f"Error extracting {key}: {str(e)}")
                    extracted_data[key] = []
            
            # Always extract metadata
            extracted_data['metadata'] = extractor.extract_metadata()
            
            return extracted_data
        
        except Exception as e:
            self.logger.error(f"Data extraction error: {str(e)}")
            raise ParsingError(f"Failed to extract data: {str(e)}")
