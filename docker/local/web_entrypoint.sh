#!/bin/sh

poetry run alembic revision --autogenerate -m "Database creation"
poetry run alembic upgrade head

poetry run uvicorn app.main:app --reload --host 0.0.0.0
