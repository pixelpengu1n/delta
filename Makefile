.PHONY: format lint test coverage all

format:
	black .
	isort .

lint:
	flake8 .

test:
	pytest --disable-warnings

coverage:
	pytest --cov=src tests/ --cov-report=term-missing

all: format lint coverage
