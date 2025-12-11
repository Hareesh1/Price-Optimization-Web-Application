FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for cache efficiency
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (Dash default 8050, but Azure uses 8000 or specified)
EXPOSE 8050

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app.app:server"]
