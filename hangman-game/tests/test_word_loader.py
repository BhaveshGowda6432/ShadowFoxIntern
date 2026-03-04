"""
Unit tests for the word loader module.
"""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from word_loader import WordLoader


class TestWordLoader:
    """Test cases for WordLoader class."""
    
    @pytest.fixture
    def test_words_file(self):
        """Create a temporary words file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("apple\n")
            f.write("banana\n")
            f.write("cherry\n")
            f.write("date\n")
            f.write("elderberry\n")
            f.write("  fig  \n")  # With whitespace
            f.write("GRAPE\n")  # Uppercase
            f.write("a\n")  # Too short, should be invalid
            f.write("\n")  # Empty line
            f.write("honeydew\n")
            temp_path = f.name
        
        yield temp_path
        
        # Cleanup
        Path(temp_path).unlink()
    
    def test_load_words(self, test_words_file):
        """Test that words are loaded and validated correctly."""
        loader = WordLoader(test_words_file)
        words = loader.words
        
        # Should have 8 valid words (excluding 'a' and empty line)
        assert len(words) == 8
        assert "apple" in words
        assert "banana" in words
        assert "fig" in words  # Whitespace normalized
        assert "grape" in words  # Lowercased
        assert "honeydew" in words
        assert "a" not in words  # Too short
    
    def test_all_words_lowercase(self, test_words_file):
        """Test that all loaded words are lowercase."""
        loader = WordLoader(test_words_file)
        for word in loader.words:
            assert word == word.lower()
    
    def test_get_random_word(self, test_words_file):
        """Test that get_random_word returns a valid word from the list."""
        loader = WordLoader(test_words_file)
        word = loader.get_random_word()
        
        assert isinstance(word, str)
        assert len(word) >= 2
        assert word in loader.words
    
    def test_get_word_count(self, test_words_file):
        """Test that word count is correct."""
        loader = WordLoader(test_words_file)
        count = loader.get_word_count()
        
        assert count == 8
        assert count == len(loader.words)
    
    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            WordLoader("/nonexistent/path/words.txt")
    
    def test_no_valid_words(self):
        """Test that ValueError is raised when no valid words exist."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write("a\n")  # Too short
            f.write("b\n")  # Too short
            f.write("\n")  # Empty
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="No valid words"):
                WordLoader(temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_words_are_strings(self, test_words_file):
        """Test that all returned words are strings."""
        loader = WordLoader(test_words_file)
        for word in loader.words:
            assert isinstance(word, str)
    
    def test_words_contain_only_letters(self, test_words_file):
        """Test that all words contain only alphabetic characters."""
        loader = WordLoader(test_words_file)
        for word in loader.words:
            assert word.isalpha()
