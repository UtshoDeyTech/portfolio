# Backend Dockerfile for Django application
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY api /app/api
COPY manage.py /app/
COPY portfolio_backend /app/portfolio_backend
COPY temp_blog.json /app/

# Expose port
EXPOSE 8000

# Run migrations, collect static files, and start server with gunicorn
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn portfolio_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3
