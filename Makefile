VENV_DIR := .venv

.PHONY: install start test

install:
	python3 -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install --upgrade pip
	. $(VENV_DIR)/bin/activate && pip install -r requirements.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt
	. $(VENV_DIR)/bin/activate && pip install -r requirements-dev.txt && pre-commit install

clean-install:
	rm -rf $(VENV_DIR)
	$(MAKE) install

migrate:
	. $(VENV_DIR)/bin/activate && alembic upgrade head

downgrade:
	. $(VENV_DIR)/bin/activate && alembic downgrade -1

start:
	docker compose up -d
	$(MAKE) migrate
	. $(VENV_DIR)/bin/activate && uvicorn app.main:app --reload

start-install:
	$(MAKE) install
	$(MAKE) start

start-clean-install:
	$(MAKE) clean-install
	$(MAKE) start

test:
	docker compose up -d
	$(MAKE) migrate
	. $(VENV_DIR)/bin/activate && pytest

test-install:
	$(MAKE) install
	$(MAKE) test
