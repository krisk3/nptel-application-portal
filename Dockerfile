# Use Python 3.9 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py       
ENV FLASK_DEBUG=True  

# Set working directory
WORKDIR /app

# Install system dependencies (for PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run Flask development server
CMD ["flask", "run", "--host=0.0.0.0"]