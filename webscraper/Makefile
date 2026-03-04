.PHONY: help install install-dev test test-coverage lint format clean build docker-build docker-run run

help:
	@echo "Web Scraper - Available Commands"
	@echo "=================================="
	@echo "make install          - Install dependencies"
	@echo "make install-dev      - Install dev dependencies"
	@echo "make test             - Run tests"
	@echo "make test-coverage    - Run tests with coverage"
	@echo "make lint             - Run linting"
	@echo "make format           - Format code"
	@echo "make clean            - Clean generated files"
	@echo "make build            - Build package"
	@echo "make docker-build     - Build Docker image"
	@echo "make docker-run       - Run Docker container"
	@echo "make run              - Run scraper"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install flake8 black isort pytest pytest-cov

test:
	pytest tests/

test-coverage:
	pytest --cov=src tests/

lint:
	flake8 src/ tests/ run_scraper.py
	isort --check-only src/ tests/

format:
	black src/ tests/ run_scraper.py
	isort src/ tests/ run_scraper.py

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +

build:
	python setup.py sdist bdist_wheel

docker-build:
	docker build -t webscraper .

docker-run:
	docker run -v $(PWD)/output:/app/output webscraper

run:
	python run_scraper.py

run-verbose:
	python run_scraper.py --verbose

run-custom-url:
	python run_scraper.py --url $(URL) --format json csv

.DEFAULT_GOAL := help
