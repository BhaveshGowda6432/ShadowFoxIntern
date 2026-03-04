"""
Utility functions for the Hangman game.

This module provides helper functions for validation and string processing.
"""

from typing import List


def is_valid_letter(letter: str) -> bool:
    """
    Check if the input is a single valid letter.
    
    Args:
        letter: The character to validate.
    
    Returns:
        True if valid letter, False otherwise.
    """
    return isinstance(letter, str) and len(letter) == 1 and letter.isalpha()


def normalize_word(word: str) -> str:
    """
    Normalize a word by converting to lowercase and stripping whitespace.
    
    Args:
        word: The word to normalize.
    
    Returns:
        Normalized word (lowercase, no leading/trailing whitespace).
    """
    return word.strip().lower()


def is_valid_word(word: str) -> bool:
    """
    Check if a word is valid for the game.
    
    A valid word contains only alphabetic characters and has at least 2 letters.
    
    Args:
        word: The word to validate.
    
    Returns:
        True if valid word, False otherwise.
    """
    normalized = normalize_word(word)
    return len(normalized) >= 2 and normalized.isalpha()


def get_word_progress(word: str, guessed_letters: set) -> str:
    """
    Generate the display format of the word with guessed letters revealed.
    
    Args:
        word: The target word (lowercase).
        guessed_letters: Set of guessed letters (lowercase).
    
    Returns:
        String representation showing blanks and revealed letters.
        Example: "h _ n g m _ n"
    """
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])


def is_word_complete(word: str, guessed_letters: set) -> bool:
    """
    Check if the word has been completely guessed.
    
    Args:
        word: The target word (lowercase).
        guessed_letters: Set of guessed letters (lowercase).
    
    Returns:
        True if all letters in the word have been guessed.
    """
    return all(letter in guessed_letters for letter in word)


def format_guessed_letters(guessed_letters: set) -> str:
    """
    Format guessed letters for display.
    
    Args:
        guessed_letters: Set of guessed letters.
    
    Returns:
        Formatted string of sorted letters.
    """
    if not guessed_letters:
        return "None"
    return " ".join(sorted(guessed_letters))
