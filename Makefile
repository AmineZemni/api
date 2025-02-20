# Makefile

.PHONY: install start test

# Install production dependencies (using the minimal requirements.txt)
install:
	pip install -r requirements.txt

# Start the FastAPI application in development mode
start:
	uvicorn app.main:app --reload

# Run tests (if you add any, e.g., with pytest)
test:
	pytest
