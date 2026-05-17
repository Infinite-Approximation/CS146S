.PHONY: run test format lint seed

run:
	uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

test:
	python -m pytest -q backend/tests

format:
	python -m black .
	python -m ruff check . --fix

lint:
	python -m ruff check .

seed:
	python -c "from backend.app.db import apply_seed_if_needed; apply_seed_if_needed()"
