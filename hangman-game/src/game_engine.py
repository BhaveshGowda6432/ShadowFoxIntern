"""
Game engine module for the Hangman game.

This module contains the core game logic and state management.
"""

from typing import Tuple, Optional
from dataclasses import dataclass, field

from utils import is_word_complete, get_word_progress


@dataclass
class GameState:
    """Data class to represent the state of a game."""
    
    chosen_word: str
    guessed_letters: set = field(default_factory=set)
    incorrect_guesses: set = field(default_factory=set)
    incorrect_count: int = 0
    max_attempts: int = 6
    game_over: bool = False
    player_won: bool = False
    
    def reset(self, new_word: str, max_attempts: int = 6) -> None:
        """
        Reset the game state for a new game.
        
        Args:
            new_word: The new word to guess.
            max_attempts: Maximum incorrect attempts allowed.
        """
        self.chosen_word = new_word
        self.guessed_letters = set()
        self.incorrect_guesses = set()
        self.incorrect_count = 0
        self.max_attempts = max_attempts
        self.game_over = False
        self.player_won = False


class GameEngine:
    """Core game engine for Hangman."""
    
    def __init__(self, word: str, max_attempts: int = 6) -> None:
        """
        Initialize the game engine.
        
        Args:
            word: The word to guess (should be lowercase).
            max_attempts: Maximum incorrect attempts allowed (default: 6).
        
        Raises:
            ValueError: If word is empty or max_attempts is invalid.
        """
        if not word or len(word) < 2:
            raise ValueError("Word must have at least 2 characters.")
        
        if max_attempts < 1:
            raise ValueError("Max attempts must be at least 1.")
        
        self.state = GameState(
            chosen_word=word.lower(),
            max_attempts=max_attempts
        )
    
    def make_guess(self, letter: str) -> Tuple[bool, str]:
        """
        Process a letter guess.
        
        Args:
            letter: The letter to guess (lowercase).
        
        Returns:
            Tuple of (is_correct: bool, message: str)
        
        Raises:
            ValueError: If the letter has already been guessed or is invalid.
        """
        letter = letter.lower()
        
        # Check if letter was already guessed
        if letter in self.state.guessed_letters or letter in self.state.incorrect_guesses:
            raise ValueError(f"Letter '{letter}' has already been guessed.")
        
        # Add letter to guessed letters
        self.state.guessed_letters.add(letter)
        
        # Check if letter is in the word
        if letter in self.state.chosen_word:
            message = f"✅ Good guess! '{letter}' is in the word."
            
            # Check for win condition
            if is_word_complete(self.state.chosen_word, self.state.guessed_letters):
                self.state.game_over = True
                self.state.player_won = True
                message += " You won the game! 🎉"
            
            return True, message
        else:
            # Incorrect guess
            self.state.incorrect_guesses.add(letter)
            self.state.incorrect_count += 1
            message = f"❌ Wrong! '{letter}' is not in the word."
            
            # Check for loss condition
            if self.state.incorrect_count >= self.state.max_attempts:
                self.state.game_over = True
                self.state.player_won = False
                message += f" Game Over! The word was: '{self.state.chosen_word}' 💀"
            
            return False, message
    
    def get_word_progress(self) -> str:
        """
        Get the current display of the word with revealed letters.
        
        Returns:
            String showing blanks and revealed letters.
        """
        return get_word_progress(self.state.chosen_word, self.state.guessed_letters)
    
    def get_incorrect_count(self) -> int:
        """
        Get the number of incorrect guesses.
        
        Returns:
            Number of incorrect guesses.
        """
        return self.state.incorrect_count
    
    def get_remaining_attempts(self) -> int:
        """
        Get the number of remaining attempts.
        
        Returns:
            Remaining attempts before game over.
        """
        return self.state.max_attempts - self.state.incorrect_count
    
    def get_guessed_letters(self) -> set:
        """
        Get the set of guessed letters.
        
        Returns:
            Set of all guessed letters (correct and incorrect).
        """
        return self.state.guessed_letters | self.state.incorrect_guesses
    
    def get_state_info(self) -> dict:
        """
        Get comprehensive game state information.
        
        Returns:
            Dictionary containing all game state information.
        """
        return {
            'word': self.state.chosen_word,
            'progress': self.get_word_progress(),
            'guessed_letters': sorted(self.get_guessed_letters()),
            'incorrect_count': self.get_incorrect_count(),
            'remaining_attempts': self.get_remaining_attempts(),
            'max_attempts': self.state.max_attempts,
            'is_game_over': self.state.game_over,
            'player_won': self.state.player_won
        }
    
    def is_game_over(self) -> bool:
        """
        Check if the game has ended.
        
        Returns:
            True if game is over, False otherwise.
        """
        return self.state.game_over
    
    def did_player_win(self) -> bool:
        """
        Check if the player won the game.
        
        Returns:
            True if player won, False otherwise.
        """
        return self.state.player_won
    
    def reset(self, new_word: str, max_attempts: int = 6) -> None:
        """
        Reset the game with a new word.
        
        Args:
            new_word: The new word to guess.
            max_attempts: Maximum incorrect attempts for new game.
        """
        if not new_word or len(new_word) < 2:
            raise ValueError("Word must have at least 2 characters.")
        
        self.state.reset(new_word.lower(), max_attempts)
