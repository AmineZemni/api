VENV_DIR := .venv

.PHONY: install start test

# Install production dependencies (using the minimal requirements.txt)
install:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt && pre-commit install

# Start the FastAPI application in development mode
start:
	$(MAKE) install
	. $(VENV_DIR)/bin/activate && uvicorn app.main:app --reload

# Run tests (if you add any, e.g., with pytest)
test:
	$(MAKE) install
	. $(VENV_DIR)/bin/activate && pytest
