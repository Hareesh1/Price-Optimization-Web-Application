FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for numpy/pandas compilation sometimes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 8080 (Standard for AWS App Runner / Cloud Run)
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run with Gunicorn
# 1 worker is fine for dev/demo, but for prod use more workers or threads
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "app.app:server"]
