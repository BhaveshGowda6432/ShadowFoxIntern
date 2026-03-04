# 🌐 Hangman Web Edition - Quick Start Guide

## 🚀 Launch the Web Application

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Server

```bash
python web_app.py
```

You should see:

```
🎮 Starting Hangman Game Web Server...
📱 Open http://localhost:5000 in your browser
🛑 Press Ctrl+C to stop the server
```

### 3. Open in Browser

Open your web browser and navigate to:

```
http://localhost:5000
```

---

## 🎮 How to Play Web Version

1. **Select Difficulty**
   - 🟢 Easy (12 attempts)
   - 🟡 Medium (6 attempts)
   - 🔴 Hard (4 attempts)

2. **Guess Letters**
   - Type a letter in the input box and press Enter
   - Or click keyboard buttons below
   - Or click letters on the on-screen keyboard

3. **Game Feedback**
   - ✅ Correct guesses reveal letters
   - ❌ Wrong guesses count against you
   - ASCII hangman grows with each mistake

4. **Win/Lose**
   - **Win**: Reveal all letters before attempts run out
   - **Lose**: Hangman completes (6 incorrect guesses)

5. **Play Again**
   - Click "🔄 Play Again" to start a new game
   - Click "🏠 Back to Menu" to return to difficulty selection

---

## 🎨 Features of Web Version

✨ **Modern UI**

- Gradient backgrounds
- Smooth animations
- Responsive design
- Dark theme

🎯 **Interactive Elements**

- Real-time hangman ASCII display
- Word progress with letter spacing
- Guessed letters highlighting
- Attempt progress bar

⌨️ **Multiple Input Methods**

- Text input with keyboard
- On-screen clickable keyboard
- Keyboard shortcuts

📱 **Responsive Design**

- Works on desktop
- Works on tablet
- Works on mobile devices

---

## 🔧 API Endpoints

The web app uses REST API endpoints:

### `/api/initialize` (POST)

Initialize a new game

```json
{
  "difficulty": "medium"
}
```

### `/api/guess` (POST)

Submit a letter guess

```json
{
  "letter": "a"
}
```

### `/api/game-state` (GET)

Get current game state

### `/api/reset` (POST)

Reset the game

### `/api/stats` (GET)

Get game statistics

---

## 📁 File Structure

```
hangman-game/
├── web_app.py              ← Main Flask app
├── templates/
│   └── index.html         ← Web UI
└── static/
    ├── style.css          ← Styling
    └── script.js          ← Frontend logic
```

---

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is in use, modify `web_app.py`:

```python
app.run(debug=True, host='localhost', port=5001)  # Change port number
```

### Module Not Found

Install Flask:

```bash
pip install Flask==2.3.3
```

### Game Won't Load

- Check that Python 3.8+ is installed
- Verify all dependencies: `pip install -r requirements.txt`
- Check browser console for JavaScript errors

---

## 💡 Tips

1. **Use keyboard**: You can type letters directly without clicking
2. **Quick select**: Click letters on the on-screen keyboard for speed
3. **Better feedback**: Wrong guesses are marked in red
4. **Track progress**: Watch the attempt bar decrease
5. **Play multiple rounds**: No need to restart the app

---

## 🌟 Browser Compatibility

Works best on:

- ✅ Chrome/Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Opera

---

## 📊 Comparison: CLI vs Web Version

| Feature           | CLI            | Web            |
| ----------------- | -------------- | -------------- |
| Game Logic        | ✅             | ✅             |
| ASCII Art         | ✅             | ✅             |
| Difficulty Levels | ✅             | ✅             |
| Score Tracking    | ✅             | ✅             |
| User Interface    | Text-based     | Modern UI      |
| Interaction       | Terminal input | Web interface  |
| Visuals           | ASCII only     | Styled + ASCII |
| Speed             | Fast           | Very fast      |

---

## 🔗 Original Game

This is a web version of the CLI-based Hangman game. Both versions share:

- Same game engine (Python)
- Same word list (110+ words)
- Same game logic
- Same difficulty levels

The web version adds a modern, interactive interface without changing core functionality.

---

## 📚 Related Files

- `run_game.py` - CLI version entry point
- `src/game_engine.py` - Core game logic (used by web app)
- `src/word_loader.py` - Word management (used by web app)
- `README.md` - Main documentation

---

## 🎓 Learning Resources

The web version demonstrates:

- Flask web framework
- REST API design
- Frontend/backend separation
- HTML/CSS/JavaScript
- Async JavaScript fetch API
- Interactive UI patterns

---

**Enjoy the Web Version of Hangman! 🎮**

_Happy guessing!_
