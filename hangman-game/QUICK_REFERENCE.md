# 🎯 Quick Reference - Hangman Game

## 🚀 Quick Start Commands

### Run the Game

```bash
python run_game.py
```

### Run Tests

```bash
pytest tests/ -v
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📋 Common Commands

### Virtual Environment

```bash
# Create
python -m venv venv

# Activate Windows
venv\Scripts\activate

# Activate macOS/Linux
source venv/bin/activate

# Deactivate
deactivate
```

### Testing

```bash
# All tests
pytest

# Verbose
pytest -v

# With coverage
pytest --cov=src tests

# HTML coverage report
pytest --cov=src --cov-report=html tests

# Specific test
pytest tests/test_game_engine.py::TestGameEngine::test_win_condition -v

# Stop on first failure
pytest -x tests

# Show print statements
pytest -s tests
```

### Docker

```bash
# Build image
docker build -t hangman-game .

# Run container
docker run -it hangman-game

# With docker-compose
docker-compose up --build
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

---

## 📂 File Organization

| File                 | Purpose         |
| -------------------- | --------------- |
| `run_game.py`        | Start game      |
| `requirements.txt`   | Dependencies    |
| `src/main.py`        | Game controller |
| `src/game_engine.py` | Core logic      |
| `tests/`             | Unit tests      |
| `data/words.txt`     | Word list       |
| `Dockerfile`         | Docker config   |

---

## 🎮 Game Commands

### During Game

| Action       | Input      |
| ------------ | ---------- |
| Guess letter | `a-z`      |
| Play again   | `y` or `n` |
| Quit         | `Ctrl+C`   |

### Difficulty Levels

| Level  | Command | Attempts |
| ------ | ------- | -------- |
| Easy   | `1`     | 12       |
| Medium | `2`     | 6        |
| Hard   | `3`     | 4        |

---

## 🐛 Troubleshooting

| Issue                | Solution                            |
| -------------------- | ----------------------------------- |
| Module not found     | `pip install -r requirements.txt`   |
| Tests fail           | `pytest tests/ -v`                  |
| Port in use (Docker) | `docker ps` then `docker stop <id>` |

---

## 📊 Project Stats

- **Lines of Code:** ~1,500
- **Test Cases:** 25+
- **Coverage:** 95%+
- **Modules:** 6
- **Classes:** 4

---

## 🔗 Key Resources

- 📖 **README.md** - Full documentation
- 🧪 **TESTING_GUIDE.md** - Testing details
- 🚀 **DEPLOYMENT_GUIDE.md** - Deployment options
- 👥 **CONTRIBUTING.md** - Development guide

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Tests passing: `pytest tests/ -v`
- [ ] Game runs: `python run_game.py`

---

**Happy Hangman! 🎮**
