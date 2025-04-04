🛠️ Getting Started
Follow these steps after cloning or pulling the repository to set up and run the application successfully.

✅ 1. Create and activate virtual environment (recommended)

Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

macOS / Linux / WSL / Git Bash
python3 -m venv .venv
source .venv/bin/activate

📦 2. Install dependencies
pip install -r requirements.txt

▶️ 3. Run the FastAPI program
uvicorn src.lambda_function:app --reload

Then open your browser:
http://127.0.0.1:8000/docs → to interact with the API using Swagger UI.

🧪 4. Run tests
make test

🧹 5. Run auto-formatting and lint checks
make format     # auto-fix formatting with black and isort
make lint       # check code style using flake8

📊 6. Run coverage report
make coverage