# 🧪 Testing Guide - Hangman Game

Complete guide for testing the Hangman Game project.

## Table of Contents

1. [Testing Overview](#testing-overview)
2. [Setup](#setup)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Test Organization](#test-organization)
6. [Writing New Tests](#writing-new-tests)
7. [Debugging Tests](#debugging-tests)
8. [CI/CD Integration](#cicd-integration)

---

## Testing Overview

### Testing Strategy

This project uses **pytest** as the testing framework with comprehensive unit tests covering:

- ✅ Core game logic
- ✅ Word loading and validation
- ✅ Input validation
- ✅ State management
- ✅ Edge cases and error handling

### Test Statistics

- **Total Test Cases:** 25+
- **Coverage:** 95%+
- **Test Files:** 2
- **Execution Time:** < 1 second

---

## Setup

### Install Testing Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Verify Setup

```bash
# Check pytest is installed
pytest --version

# Run a simple test
pytest tests/test_game_engine.py::TestGameEngine::test_initialization -v
```

---

## Running Tests

### Run All Tests

```bash
# Basic run
pytest

# Verbose output
pytest -v

# Very verbose (show print statements)
pytest -vv

# Quiet mode
pytest -q
```

### Run Specific Tests

```bash
# Specific test file
pytest tests/test_game_engine.py

# Specific test class
pytest tests/test_game_engine.py::TestGameEngine

# Specific test method
pytest tests/test_game_engine.py::TestGameEngine::test_win_condition

# Multiple specific tests
pytest tests/test_game_engine.py::TestGameEngine::test_win_condition \
        tests/test_word_loader.py::TestWordLoader::test_load_words
```

### Run with Filters

```bash
# Tests matching keyword
pytest -k "win_condition"

# Tests NOT matching keyword
pytest -k "not loss"

# Tests with specific marker
pytest -m "slow"
```

### Run with Options

```bash
# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Display print statements
pytest -s

# Show summary of fails
pytest -r f

# Full traceback
pytest --tb=long

# Short traceback
pytest --tb=short

# No traceback
pytest --tb=no
```

### Parallel Testing

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -n 4

# Auto-detect number of CPUs
pytest -n auto
```

---

## Test Coverage

### Generate Coverage Report

```bash
# Install coverage plugin
pip install pytest-cov

# Generate coverage report
pytest --cov=src tests/

# Generate HTML report
pytest --cov=src --cov-report=html tests/

# View HTML report
# Open htmlcov/index.html in browser
```

### Coverage Example Output

```
src/game_engine.py         95%
src/word_loader.py         92%
src/input_handler.py       88%
src/utils.py              100%
src/main.py                85%
src/hangman_visuals.py     90%
```

### Improve Coverage

```bash
# Identify uncovered lines
pytest --cov=src --cov-report=term-missing tests/

# Coverage threshold
pytest --cov=src --cov-fail-under=90 tests/
```

---

## Test Organization

### Test Directory Structure

```
tests/
├── __init__.py
├── test_game_engine.py      # Game logic tests
└── test_word_loader.py      # Word loading tests
```

### Test File Naming

- Files: `test_*.py` or `*_test.py`
- Classes: `Test*`
- Methods: `test_*`

### Example Test Structure

```python
import pytest
from game_engine import GameEngine

class TestGameEngine:
    """Test suite for GameEngine."""

    @pytest.fixture
    def game(self):
        """Setup fixture for each test."""
        return GameEngine("test")

    def test_win_condition(self, game):
        """Test that win condition is detected."""
        # Arrange
        game.make_guess("t")
        game.make_guess("e")

        # Act
        game.make_guess("s")

        # Assert
        assert game.did_player_win()
```

---

## Writing New Tests

### Test Structure (AAA Pattern)

```python
def test_feature(self):
    """Test description."""
    # Arrange - setup test data
    game = GameEngine("example")

    # Act - execute operation
    result = game.make_guess("e")

    # Assert - verify result
    assert result[0] is True
```

### Pytest Fixtures

```python
@pytest.fixture
def word_loader(tmp_path):
    """Fixture providing word loader with temp file."""
    words_file = tmp_path / "words.txt"
    words_file.write_text("apple\nbanana\n")
    return WordLoader(str(words_file))
```

### Parameterized Tests

```python
@pytest.mark.parametrize("letter,expected", [
    ("a", True),   # 'a' is in "banana"
    ("z", False),  # 'z' is not in "banana"
])
def test_guesses(user_input, expected):
    """Test various letter guesses."""
    game = GameEngine("banana")
    result, _ = game.make_guess(user_input)
    assert result is expected
```

### Test Exceptions

```python
def test_invalid_word_raises_error(self):
    """Test that invalid word raises ValueError."""
    with pytest.raises(ValueError, match="at least 2 characters"):
        GameEngine("a")
```

### Test Markings

```python
@pytest.mark.slow
def test_large_word_list():
    """Test with large word list."""
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    """Test for feature not yet implemented."""
    pass

@pytest.mark.xfail(reason="Known issue")
def test_known_bug():
    """Test for known bug."""
    pass
```

---

## Debugging Tests

### Print Debugging

```bash
# Show print statements during test
pytest tests/test_game_engine.py -s

# With verbose output
pytest tests/test_game_engine.py -sv
```

### Pdb Debugging

```python
def test_example(self):
    """Test with debugger."""
    game = GameEngine("test")

    # Set breakpoint
    import pdb; pdb.set_trace()

    result = game.make_guess("t")
```

### Run with Debugger

```bash
# Using built-in pdb
pytest --pdb tests/test_game_engine.py

# Drop into debugger on failure
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb
```

### Inspect Test Details

```bash
# Verbose output with full details
pytest -vv tests/test_game_engine.py

# Local variables on failure
pytest -l tests/test_game_engine.py

# Extended summary
pytest -r all tests/test_game_engine.py
```

### Capture Output

```python
def test_with_output(capsys):
    """Capture stdout/stderr."""
    print("Hello")
    captured = capsys.readouterr()
    assert "Hello" in captured.out
```

---

## Test Cases Coverage

### Game Engine Tests (15 tests)

| Test                                | Purpose                               |
| ----------------------------------- | ------------------------------------- |
| `test_initialization`               | Verify game starts correctly          |
| `test_invalid_word_too_short`       | Reject single-letter words            |
| `test_invalid_empty_word`           | Reject empty words                    |
| `test_invalid_max_attempts`         | Reject invalid attempt counts         |
| `test_correct_guess`                | Correct guess adds to guessed letters |
| `test_incorrect_guess`              | Incorrect guess counts against player |
| `test_duplicate_guess_raises_error` | Prevent duplicate guesses             |
| `test_word_progress_display`        | Display updates correctly             |
| `test_win_condition`                | Win detected when word complete       |
| `test_loss_condition`               | Loss detected at max attempts         |
| `test_get_remaining_attempts`       | Remaining attempts calculated         |
| `test_get_guessed_letters`          | All guesses returned                  |
| `test_case_insensitivity`           | Guesses work regardless of case       |
| `test_get_state_info`               | State information accurate            |
| `test_reset_game`                   | Game resets properly                  |

### Word Loader Tests (10 tests)

| Test                              | Purpose                    |
| --------------------------------- | -------------------------- |
| `test_load_words`                 | Words loaded and validated |
| `test_all_words_lowercase`        | All words lowercase        |
| `test_get_random_word`            | Random word is valid       |
| `test_get_word_count`             | Word count correct         |
| `test_file_not_found`             | Error on missing file      |
| `test_no_valid_words`             | Error when no valid words  |
| `test_words_are_strings`          | All entries are strings    |
| `test_words_contain_only_letters` | No special characters      |

---

## CI/CD Integration

### GitHub Actions

**Create `.github/workflows/tests.yml`:**

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest tests/ -v --cov=src

      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### GitLab CI

**Create `.gitlab-ci.yml`:**

```yaml
image: python:3.10

stages:
  - test

test:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest tests/ -v --cov=src
  coverage: '/TOTAL.*\s+(\d+%)$/'
```

### Pre-commit Hooks

**Create `.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        stages: [commit]
```

---

## Best Practices

### ✅ Do's

- ✅ Write one assertion per test when possible
- ✅ Use descriptive test names
- ✅ Use fixtures for setup/teardown
- ✅ Test edge cases and errors
- ✅ Keep tests independent
- ✅ Mock external dependencies

### ❌ Don'ts

- ❌ Don't use `print()` for assertions (use `assert`)
- ❌ Don't share state between tests
- ❌ Don't test implementation details
- ❌ Don't ignore test failures
- ❌ Don't write tests that are flaky

### Test Quality Checklist

```
[ ] Test name is descriptive
[ ] Test has one clear purpose
[ ] Test is independent
[ ] Test uses fixtures properly
[ ] Test validates expected behavior
[ ] Test handles edge cases
[ ] Test is maintainable
[ ] Test doesn't rely on other tests
```

---

## Troubleshooting

### Common Test Issues

#### Tests Not Running

```bash
# Ensure correct path
pytest tests/

# Check Python path
python -m pytest tests/

# Add -v for debugging
pytest tests/ -v
```

#### Import Errors

```bash
# Add src to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use pytest.ini
[pytest]
pythonpath = src
```

#### Assertion Errors

```bash
# Run with locals
pytest -l tests/

# Use pdb
pytest --pdb tests/
```

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)

---

**Happy Testing! 🧪**

_Last Updated: 2026_
