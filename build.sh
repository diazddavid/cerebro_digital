#!/usr/bin/env bash
poetry install
python manage.py collectstatic --no-input
python manage.py migrate
