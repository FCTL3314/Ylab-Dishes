#!/bin/sh

pip install -r requirements.txt

alembic revision --autogenerate -m "Database creation"
alembic upgrade head

uvicorn app.main:app --reload --host 0.0.0.0
