"""
Hangman ASCII visuals for the game.

This module provides the hangman stages for visual feedback.
"""

from typing import List


class HangmanVisuals:
    """Manages ASCII hangman visuals based on incorrect guesses."""
    
    # ASCII stages of hangman
    STAGES: List[str] = [
        # 0 incorrect guesses
        """
           -----
           |   |
               |
               |
               |
               |
        --------""",
        # 1 incorrect guess
        """
           -----
           |   |
           O   |
               |
               |
               |
        --------""",
        # 2 incorrect guesses
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        --------""",
        # 3 incorrect guesses
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        --------""",
        # 4 incorrect guesses
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        --------""",
        # 5 incorrect guesses
        """
           -----
           |   |
           O   |
          /|\\  |
           /    |
               |
        --------""",
        # 6 incorrect guesses (game over)
        """
           -----
           |   |
           O   |
          /|\\  |
           / \\  |
               |
        --------"""
    ]
    
    @staticmethod
    def get_stage(incorrect_count: int) -> str:
        """
        Get the hangman stage based on incorrect guess count.
        
        Args:
            incorrect_count: Number of incorrect guesses (0-6).
        
        Returns:
            ASCII art string for the current hangman stage.
        """
        if incorrect_count < 0:
            incorrect_count = 0
        if incorrect_count >= len(HangmanVisuals.STAGES):
            incorrect_count = len(HangmanVisuals.STAGES) - 1
        
        return HangmanVisuals.STAGES[incorrect_count]
    
    @staticmethod
    def get_title() -> str:
        """
        Get the game title display.
        
        Returns:
            Formatted title string.
        """
        return """
    ╔═══════════════════════════════════╗
    ║      WELCOME TO HANGMAN GAME      ║
    ╚═══════════════════════════════════╝
        """
