#!/bin/sh

pip install -r requirements.txt

alembic revision --autogenerate -m "Database creation"
alembic upgrade head

pytest . -W ignore::Warning
