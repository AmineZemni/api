VENV_DIR := .venv

.PHONY: install start test

install:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt && pre-commit install

migrate:
	. $(VENV_DIR)/bin/activate && alembic upgrade head

downgrade:
	. $(VENV_DIR)/bin/activate && alembic downgrade -1

start:
	$(MAKE) install
	docker compose up -d
	$(MAKE) migrate
	. $(VENV_DIR)/bin/activate && uvicorn app.main:app --reload

test:
	$(MAKE) install
	$(MAKE) migrate
	. $(VENV_DIR)/bin/activate && pytest
