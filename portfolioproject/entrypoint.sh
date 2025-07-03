#!/bin/bash

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Applying database migrations..."
python manage.py migrate

echo "Starting Gunicorn server..."
gunicorn protfolioproject.wsgi:application --bind 0.0.0.0:8000
