#!/bin/bash

# Collect Django static files
python manage.py collectstatic --noinput

# Run Django migrations
python manage.py migrate

# Start Gunicorn (Django) in the background
gunicorn portfolioproject.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 &

# Start Uvicorn (FastAPI)
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001
