"""
Flask web application for Hangman Game.

This module provides a web interface for playing Hangman with a modern,
interactive UI served through Flask.
"""

import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from game_engine import GameEngine
from word_loader import WordLoader
from hangman_visuals import HangmanVisuals

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Game instance
game = None
word_loader = None


@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')


@app.route('/api/initialize', methods=['POST'])
def initialize_game():
    """Initialize a new game with selected difficulty."""
    global game, word_loader
    
    try:
        data = request.json
        difficulty = data.get('difficulty', 'medium')
        
        # Initialize word loader if not done
        if word_loader is None:
            word_loader = WordLoader()
        
        # Difficulty settings
        difficulty_settings = {
            'easy': 12,
            'medium': 6,
            'hard': 4
        }
        
        max_attempts = difficulty_settings.get(difficulty, 6)
        word = word_loader.get_random_word()
        
        # Create new game
        game = GameEngine(word, max_attempts)
        
        return jsonify({
            'status': 'success',
            'message': f'Game started on {difficulty.upper()} difficulty',
            'max_attempts': max_attempts,
            'word_length': len(word)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/guess', methods=['POST'])
def make_guess():
    """Process a letter guess."""
    global game
    
    if game is None:
        return jsonify({'status': 'error', 'message': 'Game not initialized'}), 400
    
    try:
        data = request.json
        letter = data.get('letter', '').lower()
        
        # Validate letter
        if not letter or len(letter) != 1 or not letter.isalpha():
            return jsonify({'status': 'error', 'message': 'Please enter a single letter'}), 400
        
        # Check if already guessed
        all_guessed = game.get_guessed_letters()
        if letter in all_guessed:
            return jsonify({'status': 'error', 'message': f'Letter "{letter}" already guessed'}), 400
        
        # Make guess
        is_correct, message = game.make_guess(letter)
        
        return jsonify({
            'status': 'success',
            'is_correct': is_correct,
            'message': message,
            'game_state': get_game_state()
        })
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/game-state', methods=['GET'])
def get_game_state_endpoint():
    """Get current game state."""
    if game is None:
        return jsonify({'status': 'error', 'message': 'Game not initialized'}), 400
    
    return jsonify({'status': 'success', 'game_state': get_game_state()})


def get_game_state():
    """Get formatted game state."""
    if game is None:
        return None
    
    state = game.get_state_info()
    hangman_visual = HangmanVisuals.get_stage(state['incorrect_count'])
    
    return {
        'word_progress': game.get_word_progress(),
        'guessed_letters': sorted(game.get_guessed_letters()),
        'incorrect_count': state['incorrect_count'],
        'remaining_attempts': state['remaining_attempts'],
        'max_attempts': state['max_attempts'],
        'is_game_over': state['is_game_over'],
        'player_won': state['player_won'],
        'hangman_visual': hangman_visual,
        'word_complete': state['player_won']  # For checking win
    }


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game."""
    global game
    game = None
    return jsonify({'status': 'success', 'message': 'Game reset'})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get game statistics."""
    try:
        if word_loader is None:
            word_loader_temp = WordLoader()
            word_count = word_loader_temp.get_word_count()
        else:
            word_count = word_loader.get_word_count()
        
        return jsonify({
            'status': 'success',
            'word_count': word_count,
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'status': 'error', 'message': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500


if __name__ == '__main__':
    print("🎮 Starting Hangman Game Web Server...")
    print("📱 Open http://localhost:5000 in your browser")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, host='localhost', port=5000)
