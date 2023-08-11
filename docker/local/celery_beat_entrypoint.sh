#!/bin/sh

poetry run celery -A app.celery:celery beat
