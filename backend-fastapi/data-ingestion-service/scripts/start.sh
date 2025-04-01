cd "$(dirname "$0")"/..

# Activate the virtual environment
# Windows (Git Bash)
source .venv/Scripts/activate

# Verify current working directory (for debugging)
echo "Current directory: $(pwd)"

# Start your FastAPI app
uvicorn src.main:app --reload --log-level info --use-colors --port 8002