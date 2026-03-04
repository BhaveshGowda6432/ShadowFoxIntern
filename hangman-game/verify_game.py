#!/usr/bin/env python3
"""Quick test to verify game can be imported and initialized."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from main import HangmanGame

# Test game initialization
print("Testing game initialization...")
try:
    game = HangmanGame()
    print(f"✅ Game initialized successfully")
    print(f"✅ Loaded {game.word_loader.get_word_count()} words")
    
    # Try to get a random word and start a game
    word = game.word_loader.get_random_word()
    print(f"✅ Random word selected: {len(word)} letters")
    
    game.play_round("easy")
    print(f"\n✅ Game round played successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All verification tests passed!")
