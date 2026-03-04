#!/usr/bin/env python3
"""
Entry point for the Hangman game.

Run this script to start playing the game.
"""

import sys
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from main import main


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
