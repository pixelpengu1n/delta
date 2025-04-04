# ---------- Linux/Mac ----------
install:
	@if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
	. .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

format:
	. .venv/bin/activate && black . && isort .

lint:
	. .venv/bin/activate && flake8 .

test:
	. .venv/bin/activate && pytest --disable-warnings

coverage:
	. .venv/bin/activate && pytest --cov=src tests/ --cov-report=term-missing

done:
	rm -rf .venv


# ---------- Windows ----------
installw:
	if not exist .venv (python -m venv .venv)
	.venv\Scripts\python.exe -m pip install --upgrade pip
	.venv\Scripts\python.exe -m pip install -r requirements.txt

formatw:
	.venv\Scripts\python.exe -m black .
	.venv\Scripts\python.exe -m isort .

lintw:
	.venv\Scripts\python.exe -m flake8 .

testw:
	.venv\Scripts\python.exe -m pytest --disable-warnings

coveragew:
	.venv\Scripts\python.exe -m pytest --cov=src tests/ --cov-report=term-missing

donew:
	rmdir /s /q .venv
