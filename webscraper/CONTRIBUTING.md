# Contributing to Web Scraper

Thank you for your interest in contributing to the Web Scraper project! This document provides guidelines and instructions for contributing.

## 📋 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Learn and help others learn
- Report issues responsibly

## 🐛 Reporting Bugs

1. Check if the bug has already been reported
2. Provide a clear, descriptive title
3. Include steps to reproduce
4. Describe expected vs actual behavior
5. Include relevant logs and configuration

## 💡 Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Provide a clear, descriptive title
3. Explain the motivation and use case
4. Describe the proposed solution
5. Include examples if applicable

## 🔧 Development Setup

### Prerequisites

- Python 3.8+
- Git
- pip or conda

### Setup Steps

1. **Fork the repository**

   ```bash
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Making Changes

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Write docstrings for all modules, classes, and functions
- Keep lines under 100 characters when possible

### Code Quality

- Run linting

  ```bash
  flake8 src/ tests/
  ```

- Format code

  ```bash
  black src/ tests/
  ```

- Sort imports
  ```bash
  isort src/ tests/
  ```

### Testing

- Write tests for new features
- Ensure all tests pass

  ```bash
  pytest
  ```

- Check coverage
  ```bash
  pytest --cov=src tests/
  ```

## 📝 Commit Guidelines

1. Use clear, descriptive commit messages
2. Reference issues when relevant
3. Keep commits focused and atomic

### Commit Message Format

```
[TYPE] Short description

Longer description explaining the changes.

Fixes #issue_number
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `perf`: Performance improvements
- `chore`: Maintenance tasks

### Examples

```
feat: Add proxy support for distributed scraping

This commit adds the ability to use HTTP proxies
for requests, enabling distributed scraping.

Fixes #42
```

```
fix: Handle timeout errors in scraper

Add proper exception handling for request timeouts
with exponential backoff retry strategy.
```

## 🧪 Testing

### Adding Tests

Create tests in `tests/` directory for:

- New modules
- New functions or classes
- Bug fixes (add test that fails before fix)
- Edge cases and error handling

### Test Structure

```python
import pytest
from src.module import Function

class TestMyFeature:
    def setup_method(self):
        """Set up test fixtures."""
        # Initialize test data
        pass

    def test_normal_case(self):
        """Test normal behavior."""
        # Arrange
        # Act
        # Assert
        pass

    def test_error_case(self):
        """Test error handling."""
        with pytest.raises(ExpectedException):
            # Code that should raise
            pass
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_parser.py

# Specific test
pytest tests/test_parser.py::TestHTMLParser::test_parse_valid_html

# With coverage
pytest --cov=src tests/

# Verbose output
pytest -v
```

## 📚 Documentation

### Update Documentation for:

- New features
- Changed behavior
- New configuration options
- New CLI arguments

### Update Files:

- `README.md` for user-facing features
- Docstrings in code
- Module-level documentation

### Documentation Style

```python
def my_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what the function does.

    Longer description providing more context and details
    about the function's behavior and use cases.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        CustomException: When this condition occurs
        ValueError: When parameters are invalid

    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        {'status': 'success'}
    """
    pass
```

## 🔄 Pull Request Process

1. **Update local repository**

   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push changes**

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Clear title and description
   - Reference related issues
   - Include screenshots/logs if relevant
   - List changes made

4. **PR Description Template**

   ```markdown
   ## Description

   Brief description of changes

   ## Type of Change

   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation

   ## Related Issues

   Fixes #issue_number

   ## Testing

   Description of testing performed

   ## Checklist

   - [ ] Tests added/updated
   - [ ] Documentation updated
   - [ ] Code follows style guidelines
   - [ ] No new warnings generated
   ```

5. **Address Review Comments**
   - Make requested changes
   - Respond to feedback
   - Re-request review when done

## 🎯 Project Architecture

Understanding the project structure:

- `src/scraper.py`: Core scraping logic
- `src/parser.py`: HTML parsing and extraction
- `src/storage.py`: Data export functionality
- `src/config_loader.py`: Configuration management
- `src/error_handler.py`: Error handling and logging
- `src/utils.py`: Utility functions
- `tests/`: Test suite

## 🚀 Deployment

Changes to `main` branch are automatically deployed.

## 📖 Additional Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Git Documentation](https://git-scm.com/doc)
- [Pytest Documentation](https://docs.pytest.org/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## 📞 Questions?

- Check existing issues and discussions
- Create a new discussion for questions
- Review documentation and examples

## 🙏 Thank You

Thank you for contributing to make this project better!

---

**Last Updated**: 2024
