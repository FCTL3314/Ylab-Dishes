#!/bin/sh

poetry run alembic revision --autogenerate -m "Database creation"
poetry run alembic upgrade head

poetry run pytest . -W ignore::Warning -s
