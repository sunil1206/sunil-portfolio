FROM python:3.10-slim

WORKDIR /fastapi_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD is defined in docker-compose
