FROM python:3.10-slim

# Disable .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project into the container
COPY . .

# Run Django app via Gunicorn pointing to the correct wsgi module
CMD ["gunicorn", "portfolioproject.wsgi:application", "--bind", "0.0.0.0:8000"]
