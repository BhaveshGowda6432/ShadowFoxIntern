# 👤 Contributing Guide - Hangman Game

Thank you for your interest in contributing to the Hangman Game project! This guide will help you understand how to contribute effectively.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Report issues responsibly

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on GitHub to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/hangman-game.git
cd hangman-game
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes
git checkout -b fix/issue-description
```

### 4. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install optional dev tools
pip install black flake8 mypy
```

---

## Development Workflow

### Code Style Guidelines

We follow **PEP 8** with the following conventions:

#### 1. Format Code

```bash
# Auto-format with black
black src/ tests/

# Check style with flake8
flake8 src/ tests/
```

#### 2. Type Hints

```python
# Good - includes type hints
def make_guess(self, letter: str) -> Tuple[bool, str]:
    """Process a letter guess."""
    pass

# Bad - missing type hints
def make_guess(self, letter):
    pass
```

#### 3. Docstrings

```python
# Good - comprehensive docstring
def make_guess(self, letter: str) -> Tuple[bool, str]:
    """
    Process a letter guess.

    Args:
        letter: The letter to guess (lowercase).

    Returns:
        Tuple of (is_correct: bool, message: str)

    Raises:
        ValueError: If the letter was already guessed.
    """
    pass

# Bad - missing docstring
def make_guess(self, letter: str) -> Tuple[bool, str]:
    pass
```

#### 4. Variable Naming

```python
# Good
remaining_attempts = 6
is_correct = True
player_won = False

# Bad
ra = 6
ic = True
pw = False
```

### Testing

#### Run Tests Before Submitting

```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest --cov=src tests/

# Use pre-commit hooks
pre-commit run --all-files
```

#### Write Tests for New Features

```python
class TestNewFeature:
    """Tests for new feature."""

    def test_feature_works(self):
        """Test that feature works as expected."""
        # Arrange
        feature = NewFeature()

        # Act
        result = feature.execute()

        # Assert
        assert result is not None
```

### Running Tests Locally

```bash
# Verbose output
pytest tests/ -v

# With coverage
pytest --cov=src --cov-report=html tests/

# Specific test
pytest tests/test_game_engine.py::TestGameEngine::test_win_condition -v

# Stop on first failure
pytest -x tests/

# Show print statements
pytest -s tests/
```

---

## Commit Guidelines

### Commit Message Format

```
[TYPE] Brief description (50 chars max)

Optional detailed explanation of changes.
Can be multiple paragraphs.

References: #123
```

### Commit Types

- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring (no behavior change)
- `test:` Add or improve tests
- `docs:` Documentation updates
- `style:` Code style changes (formatting, etc.)
- `perf:` Performance improvements

### Examples

```bash
# Good commits
git commit -m "feat: Add difficulty level selection"
git commit -m "fix: Correct word progress display logic"
git commit -m "test: Add tests for word loader validation"
git commit -m "docs: Update README with new features"

# Bad commits (too vague)
git commit -m "Update code"
git commit -m "Fix stuff"
```

---

## Pull Request Process

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

- Go to GitHub and click "New Pull Request"
- Select your branch
- Fill out the PR template

### 3. PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement

## Related Issues

Closes #123

## Testing

Describe how you tested the changes

## Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
```

### 4. Review Process

The maintainers will review your PR and provide feedback. Please:

- Respond to comments respectfully
- Make requested changes
- Re-request review after updates

---

## Areas for Contribution

### 🐛 Bug Reports

Found a bug? Create an issue with:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)

### ✨ Feature Requests

Have an idea? Create an issue with:

- Clear description of the feature
- Use case and benefit
- Possible implementation
- Alternative approaches

### 📚 Documentation

Help improve docs:

- Fix typos and grammar
- Add examples
- Clarify confusing sections
- Add more guides

### 🧪 Testing

Help improve test coverage:

- Add tests for edge cases
- Improve existing tests
- Test in different environments
- Performance testing

### 🎨 Code Quality

Improve the codebase:

- Refactor for clarity
- Add type hints
- Improve error handling
- Optimize performance

---

## Project Architecture

### File Structure

```
src/
├── main.py                 # Game controller
├── game_engine.py         # Core logic
├── word_loader.py         # Word management
├── hangman_visuals.py     # ASCII art
├── input_handler.py       # User input
└── utils.py              # Helpers
```

### Adding New Features

1. **Add feature code** to appropriate module
2. **Write tests** in `tests/`
3. **Update documentation** in README
4. **Test locally** with `pytest`
5. **Format code** with `black`
6. **Commit** with clear message
7. **Create PR** with description

### Example: Adding a Hint System

```python
# src/game_engine.py
def get_hint(self) -> str:
    """Provide a hint about the word."""
    # Implementation here
    pass

# tests/test_game_engine.py
def test_hint_system(self):
    """Test hint functionality."""
    # Test here
    pass

# Update README.md
# - Add hint section to features
```

---

## Code Review Checklist

When reviewing code, check:

- [ ] Code follows PEP 8
- [ ] Type hints provided
- [ ] Docstrings complete
- [ ] Tests added/updated
- [ ] Testing passes (`pytest`)
- [ ] Coverage maintained (>90%)
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Descriptive variable names
- [ ] Error handling included

---

## Performance Considerations

### Optimization Guidelines

```python
# Good - efficient
def is_word_complete(word: str, guessed_letters: set) -> bool:
    """Check in O(n) time."""
    return all(letter in guessed_letters for letter in word)

# Avoid - inefficient
def is_word_complete_slow(word: str, guessed_letters: list) -> bool:
    for letter in word:
        if letter not in guessed_letters:  # O(n) lookup
            return False
    return True
```

### Performance Testing

```bash
# Profile code
python -m cProfile -s cumulative src/main.py

# Benchmark specific function
python -m timeit "hangman_game.make_guess('a')"
```

---

## Security Considerations

### Guidelines

- [ ] Validate all user input
- [ ] Use safe file operations
- [ ] Avoid eval/exec
- [ ] Handle exceptions properly
- [ ] Don't hardcode secrets
- [ ] Sanitize displayed output

### Example: Secure File Handling

```python
# Good - safe
from pathlib import Path

file_path = Path(__file__).parent / "data" / "words.txt"
if file_path.exists():
    content = file_path.read_text(encoding='utf-8')

# Avoid - unsafe
with open(f"data/{user_input}/words.txt") as f:
    pass
```

---

## Documentation Standards

### Docstring Format

```python
"""
One-line summary of module/function.

Longer description if needed.
"""

def function(param1: str, param2: int) -> bool:
    """
    Brief description of what function does.

    Longer description explaining behavior,
    use cases, and any important notes.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is invalid.
        TypeError: When type is wrong.

    Example:
        >>> function("hello", 42)
        True
    """
    pass
```

### README Guidelines

- Clear project overview
- Installation instructions
- Usage examples
- Feature list
- Testing information
- Deployment guide

---

## Troubleshooting

### Common Issues

#### Tests Fail Locally

```bash
# Verify environment
python --version  # Should be 3.8+
pip list | grep pytest

# Clean cache
rm -rf .pytest_cache __pycache__

# Reinstall
pip install -r requirements.txt
```

#### Code Style Issues

```bash
# Auto-fix
black src/ tests/

# Check
flake8 src/ tests/
mypy src/
```

#### Type Hints Not Working

```bash
# Install stubs
pip install types-all

# Check types
mypy src/ --strict
```

---

## Resources

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Google Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Git Documentation](https://git-scm.com/doc)

---

## Getting Help

- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues
- 📧 Email: maintainer@example.com
- 💻 Slack: community-slack

---

## Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md
- Project README
- Release notes
- GitHub contributors page

---

## License

By contributing, you agree your code will be licensed under the project's license.

---

Thank you for contributing! 🙏

_Last Updated: 2026_
