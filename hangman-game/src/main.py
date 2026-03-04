"""
Main game controller for the Hangman game.

This module orchestrates the game flow and user interactions.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from game_engine import GameEngine
from word_loader import WordLoader
from hangman_visuals import HangmanVisuals
from input_handler import InputHandler
from utils import format_guessed_letters


class HangmanGame:
    """Main game controller."""
    
    def __init__(self, words_file: str = None) -> None:
        """
        Initialize the Hangman game.
        
        Args:
            words_file: Optional path to words file.
        
        Raises:
            FileNotFoundError: If words file not found.
            ValueError: If no valid words in file.
        """
        self.word_loader = WordLoader(words_file)
        self.game_engine = None
        self.score = {"wins": 0, "losses": 0}
    
    def display_game_status(self) -> None:
        """Display current game status including hangman visual and word progress."""
        print("\n" + "="*50)
        
        # Display hangman ASCII art
        hangman_visual = HangmanVisuals.get_stage(self.game_engine.get_incorrect_count())
        print(hangman_visual)
        
        print("\n" + "-"*50)
        print(f"Word:  {self.game_engine.get_word_progress()}")
        print(f"Guessed letters: {format_guessed_letters(self.game_engine.get_guessed_letters())}")
        print(f"Attempts left: {self.game_engine.get_remaining_attempts()}/{self.game_engine.state.max_attempts}")
        print("="*50)
    
    def play_round(self, difficulty: str = "medium") -> None:
        """
        Play a single round of Hangman.
        
        Args:
            difficulty: Game difficulty level ('easy', 'medium', 'hard').
        """
        # Set max attempts based on difficulty
        difficulty_settings = {
            'easy': 12,
            'medium': 6,
            'hard': 4
        }
        
        max_attempts = difficulty_settings.get(difficulty, 6)
        
        # Initialize game with random word
        word = self.word_loader.get_random_word()
        self.game_engine = GameEngine(word, max_attempts)
        
        print(f"\n🎮 Starting {difficulty.upper()} game. Word length: {len(word)} letters\n")
        
        # Game loop
        while not self.game_engine.is_game_over():
            self.display_game_status()
            
            # Get user input
            letter = InputHandler.get_letter_guess(self.game_engine.get_guessed_letters())
            
            try:
                is_correct, message = self.game_engine.make_guess(letter)
                print(message)
            except ValueError as e:
                print(f"⚠️  Error: {e}")
        
        # Display final game status
        self.display_game_status()
        
        # Show game result
        if self.game_engine.did_player_win():
            print("\n" + "🎉"*20)
            print("CONGRATULATIONS! YOU WON! 🎉")
            print("🎉"*20)
            self.score["wins"] += 1
        else:
            print("\n" + "💀"*20)
            print(f"GAME OVER! The word was: {self.game_engine.state.chosen_word}")
            print("💀"*20)
            self.score["losses"] += 1
    
    def display_score(self) -> None:
        """Display the current score."""
        print(f"\n📊 Score - Wins: {self.score['wins']}, Losses: {self.score['losses']}")
    
    def play(self) -> None:
        """Main game loop - play rounds until user quits."""
        print(HangmanVisuals.get_title())
        print(f"✅ Loaded {self.word_loader.get_word_count()} words from word list\n")
        
        while True:
            try:
                # Get difficulty selection
                difficulty = InputHandler.get_difficulty_level()
                
                # Play a round
                self.play_round(difficulty)
                
                # Display score
                self.display_score()
                
                # Ask to play again
                if not InputHandler.get_yes_no_input("\n🔄 Play again? (y/n): "):
                    print("\n" + "="*50)
                    print("Thanks for playing Hangman!")
                    print(f"📊 Final Score - Wins: {self.score['wins']}, Losses: {self.score['losses']}")
                    print("="*50 + "\n")
                    break
            
            except KeyboardInterrupt:
                print("\n\n👋 Thanks for playing!")
                break
            except Exception as e:
                print(f"\n❌ An unexpected error occurred: {e}")
                print("Restarting game...\n")


def main() -> None:
    """Entry point for the game."""
    try:
        game = HangmanGame()
        game.play()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
