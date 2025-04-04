# Create venv and install requirements
install:
	if not exist .venv\Scripts\python.exe python -m venv .venv
	.venv\Scripts\python.exe -m pip install --upgrade pip
	.venv\Scripts\python.exe -m pip install -r requirements.txt

# Run formatting tools
format:
	.venv\Scripts\python.exe -m black .
	.venv\Scripts\python.exe -m isort .

# Lint using flake8
lint:
	.venv\Scripts\python.exe -m flake8 .

# Run all tests
test:
	.venv\Scripts\python.exe -m pytest --disable-warnings

# Run coverage
coverage:
	.venv\Scripts\python.exe -m pytest --cov=src tests/ --cov-report=term-missing

# Delete venv
done:
	rmdir /S /Q .venv
