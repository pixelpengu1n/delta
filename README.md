🛠️ Getting Started
Follow these steps after cloning or pulling the repository to set up and run the application successfully.

✅ 1. Create and activate virtual environment

🪟 On Windows (PowerShell)
    make installw
    .venv\Scripts\activate

🐧 On macOS / Linux / WSL / Git Bash
    make install
    source .venv/bin/activate

▶️ 2. Run the FastAPI program
    uvicorn src.lambda_function:app --reload
    Then open your browser:

    🔗 http://127.0.0.1:8000/docs → to interact with the API using Swagger UI.

🧪 3. Run tests
Windows:
    make testw

macOS / Linux / WSL:
    make test

🧹 4. Run auto-formatting and lint checks
Windows:
    make formatw    # auto-fix formatting with black and isort
    make lintw      # check code style using flake8

macOS / Linux / WSL:
    make format
    make lint
    
📊 5. Run coverage report
Windows:
    make coveragew

macOS / Linux / WSL:
    make coverage

🧼 6. Clean up (delete .venv)
Windows:
    make donew

macOS / Linux / WSL:
    make done