"""
Input handler module for the Hangman game.

This module handles user input validation and processing.
"""

from typing import Optional

from utils import is_valid_letter


class InputHandler:
    """Handles user input validation and processing."""
    
    @staticmethod
    def get_letter_guess(guessed_letters: set) -> str:
        """
        Prompt user for a letter guess and validate it.
        
        Validates:
        - Only single letter
        - Only alphabetic characters
        - Not previously guessed
        
        Args:
            guessed_letters: Set of previously guessed letters.
        
        Returns:
            A valid letter guess (lowercase).
        """
        while True:
            try:
                user_input = input("\nGuess a letter: ").strip().lower()
                
                # Check if it's a valid letter
                if not is_valid_letter(user_input):
                    print("❌ Invalid input! Please enter a single letter (a-z).")
                    continue
                
                # Check if letter was already guessed
                if user_input in guessed_letters:
                    print(f"⚠️  You already guessed '{user_input}'. Try a different letter!")
                    continue
                
                return user_input
            
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("Please try again.")
    
    @staticmethod
    def get_yes_no_input(prompt: str) -> bool:
        """
        Get a yes/no response from the user.
        
        Args:
            prompt: The prompt to display to the user.
        
        Returns:
            True for 'y', False for 'n'.
        """
        while True:
            try:
                user_input = input(prompt).strip().lower()
                
                if user_input in ['y', 'yes']:
                    return True
                elif user_input in ['n', 'no']:
                    return False
                else:
                    print("❌ Invalid input! Please enter 'y' or 'n'.")
            
            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
    
    @staticmethod
    def get_difficulty_level() -> str:
        """
        Get difficulty level from user.
        
        Returns:
            Difficulty level: 'easy', 'medium', or 'hard'.
        """
        while True:
            try:
                print("\nSelect difficulty level:")
                print("1. Easy (12 attempts)")
                print("2. Medium (6 attempts)")
                print("3. Hard (4 attempts)")
                
                choice = input("\nEnter your choice (1-3): ").strip()
                
                difficulty_map = {
                    '1': 'easy',
                    '2': 'medium',
                    '3': 'hard'
                }
                
                if choice in difficulty_map:
                    return difficulty_map[choice]
                else:
                    print("❌ Invalid choice! Please enter 1, 2, or 3.")
            
            except KeyboardInterrupt:
                print("\n\nThanks for playing!")
                exit(0)
            except Exception as e:
                print(f"❌ An error occurred: {e}")
