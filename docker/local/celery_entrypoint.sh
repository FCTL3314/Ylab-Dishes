#!/bin/sh

poetry run celery -A app.celery:celery worker -l info -P eventlet
