.PHONY: help install run cli test lint format clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       Install dependencies"
	@echo "  make run           Run local development web server"
	@echo "  make cli           Run interactive CLI mode"
	@echo "  make test          Run full test suite"
	@echo "  make lint          Run linter checks"
	@echo "  make format        Format code with ruff"
	@echo "  make docker-build  Build production Docker container"
	@echo "  make docker-run    Run Docker container"
	@echo "  make clean         Remove cache and temporary build files"

install:
	pip install -r requirements-dev.txt

run:
	PYTHONPATH=src python3 -m wordcount

cli:
	PYTHONPATH=src python3 -m wordcount.presentation.cli

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py" -v

lint:
	ruff check src/ tests/
	mypy src/

format:
	ruff format src/ tests/

docker-build:
	docker build -t wordcount-pro:latest .

docker-run:
	docker run -p 8000:8000 --rm wordcount-pro:latest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage dist build *.egg-info
