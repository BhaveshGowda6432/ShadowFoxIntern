"""
Word loader module for the Hangman game.

This module handles loading words from a file and selecting random words.
"""

import random
from pathlib import Path
from typing import List, Optional

from utils import normalize_word, is_valid_word


class WordLoader:
    """Handles word loading and random selection."""
    
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initialize the word loader.
        
        Args:
            file_path: Path to the words file. If None, uses default path.
        
        Raises:
            FileNotFoundError: If the words file doesn't exist.
        """
        if file_path is None:
            # Default path relative to the project root
            file_path = Path(__file__).parent.parent / "data" / "words.txt"
        
        self.file_path = Path(file_path)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Words file not found: {self.file_path}")
        
        self.words = self._load_words()
        
        if not self.words:
            raise ValueError("No valid words found in the words file.")
    
    def _load_words(self) -> List[str]:
        """
        Load and validate words from file.
        
        Returns:
            List of valid, lowercase words.
        
        Raises:
            IOError: If the file cannot be read.
        """
        words = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = normalize_word(line)
                    if is_valid_word(word):
                        words.append(word)
        except IOError as e:
            raise IOError(f"Failed to read words file: {e}")
        
        return words
    
    def get_random_word(self) -> str:
        """
        Select a random word from the loaded words.
        
        Returns:
            A random word from the word list.
        """
        return random.choice(self.words)
    
    def get_word_count(self) -> int:
        """
        Get the total number of valid words loaded.
        
        Returns:
            Number of words in the word list.
        """
        return len(self.words)
