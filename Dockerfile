# Use official Python slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (optional)
RUN python manage.py collectstatic --noinput

# Apply migrations (SQLite DB will be created automatically)
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
