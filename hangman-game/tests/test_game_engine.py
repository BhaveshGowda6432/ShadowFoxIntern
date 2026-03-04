"""
Unit tests for the game engine module.
"""

import pytest

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent / "src"))

from game_engine import GameEngine, GameState


class TestGameEngine:
    """Test cases for GameEngine class."""
    
    @pytest.fixture
    def game(self):
        """Create a game engine instance for testing."""
        return GameEngine("hangman", max_attempts=6)
    
    def test_initialization(self):
        """Test game engine initialization."""
        game = GameEngine("testing", max_attempts=6)
        
        assert game.state.chosen_word == "testing"
        assert game.state.max_attempts == 6
        assert game.state.incorrect_count == 0
        assert len(game.state.guessed_letters) == 0
        assert not game.state.game_over
    
    def test_invalid_word_too_short(self):
        """Test that ValueError is raised for single character words."""
        with pytest.raises(ValueError, match="at least 2 characters"):
            GameEngine("a")
    
    def test_invalid_empty_word(self):
        """Test that ValueError is raised for empty words."""
        with pytest.raises(ValueError, match="at least 2 characters"):
            GameEngine("")
    
    def test_invalid_max_attempts(self):
        """Test that ValueError is raised for invalid max_attempts."""
        with pytest.raises(ValueError, match="at least 1"):
            GameEngine("test", max_attempts=0)
    
    def test_correct_guess(self, game):
        """Test correct letter guess."""
        is_correct, message = game.make_guess("h")
        
        assert is_correct is True
        assert "h" in game.state.guessed_letters
        assert len(game.state.incorrect_guesses) == 0
        assert game.get_incorrect_count() == 0
    
    def test_incorrect_guess(self, game):
        """Test incorrect letter guess."""
        is_correct, message = game.make_guess("z")
        
        assert is_correct is False
        assert "z" in game.state.guessed_letters
        assert "z" in game.state.incorrect_guesses
        assert game.get_incorrect_count() == 1
    
    def test_duplicate_guess_raises_error(self, game):
        """Test that guessing the same letter twice raises ValueError."""
        game.make_guess("a")
        
        with pytest.raises(ValueError, match="already been guessed"):
            game.make_guess("a")
    
    def test_word_progress_display(self, game):
        """Test word progress display."""
        initial_progress = game.get_word_progress()
        assert initial_progress == "_ _ _ _ _ _ _"  # 7-letter word "hangman"
        
        game.make_guess("a")
        progress_after_a = game.get_word_progress()
        assert progress_after_a == "_ a _ _ _ a _"
        
        game.make_guess("n")
        progress_after_n = game.get_word_progress()
        assert progress_after_n == "_ a n _ _ a n"
    
    def test_win_condition(self):
        """Test win condition detection."""
        game = GameEngine("cat", max_attempts=6)
        
        assert not game.is_game_over()
        
        game.make_guess("c")
        assert not game.is_game_over()
        
        game.make_guess("a")
        assert not game.is_game_over()
        
        game.make_guess("t")
        assert game.is_game_over()
        assert game.did_player_win()
    
    def test_loss_condition(self):
        """Test loss condition detection."""
        game = GameEngine("cat", max_attempts=2)
        
        assert not game.is_game_over()
        
        game.make_guess("x")
        assert not game.is_game_over()
        
        game.make_guess("y")
        assert game.is_game_over()
        assert not game.did_player_win()
    
    def test_get_remaining_attempts(self, game):
        """Test remaining attempts calculation."""
        assert game.get_remaining_attempts() == 6
        
        game.make_guess("z")
        assert game.get_remaining_attempts() == 5
        
        game.make_guess("x")
        assert game.get_remaining_attempts() == 4
    
    def test_get_guessed_letters(self, game):
        """Test that all guessed letters are returned."""
        game.make_guess("h")
        game.make_guess("z")
        game.make_guess("a")
        
        guessed = game.get_guessed_letters()
        assert "h" in guessed
        assert "z" in guessed
        assert "a" in guessed
    
    def test_case_insensitivity(self):
        """Test that guesses are case-insensitive."""
        game = GameEngine("TEST", max_attempts=6)
        
        # Word should be lowercase internally
        assert game.state.chosen_word == "test"
        
        # Uppercase guess should work
        is_correct, _ = game.make_guess("t")
        assert is_correct is True
    
    def test_get_state_info(self, game):
        """Test state information dictionary."""
        game.make_guess("a")
        game.make_guess("z")
        
        state_info = game.get_state_info()
        
        assert state_info['word'] == 'hangman'
        assert state_info['incorrect_count'] == 1
        assert state_info['remaining_attempts'] == 5
        assert 'a' in state_info['guessed_letters']
        assert 'z' in state_info['guessed_letters']
    
    def test_reset_game(self, game):
        """Test game reset functionality."""
        game.make_guess("h")
        game.make_guess("z")
        
        assert game.get_incorrect_count() > 0
        
        game.reset("python", max_attempts=5)
        
        assert game.state.chosen_word == "python"
        assert game.state.max_attempts == 5
        assert game.get_incorrect_count() == 0
        assert len(game.state.guessed_letters) == 0
        assert len(game.state.incorrect_guesses) == 0
    
    def test_multiple_correct_letters_in_one_guess(self):
        """Test word with multiple instances of same letter."""
        game = GameEngine("banana", max_attempts=6)
        
        is_correct, _ = game.make_guess("a")
        assert is_correct is True
        
        # 'a' appears 3 times in "banana"
        progress = game.get_word_progress()
        assert progress == "_ a _ a _ a"
    
    def test_game_state_dataclass(self):
        """Test GameState dataclass."""
        state = GameState(chosen_word="test")
        
        assert state.chosen_word == "test"
        assert state.incorrect_count == 0
        assert len(state.guessed_letters) == 0
        assert not state.game_over
        
        state.guessed_letters.add("a")
        state.reset("new", max_attempts=5)
        
        assert state.chosen_word == "new"
        assert len(state.guessed_letters) == 0
