#!/bin/sh

alembic revision --autogenerate -m "Database creation"
alembic upgrade head

pytest . -W ignore::Warning
