🛠️ Getting Started
Follow these steps after cloning or pulling the repository to set up and run the application successfully.

✅ 1. Create and activate virtual environment (recommended)

Windows (PowerShell)
make install
.venv\Scripts\activate

macOS / Linux / WSL / Git Bash
make install
source .venv/bin/activate

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