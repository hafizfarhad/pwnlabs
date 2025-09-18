# Simple Python-based Dockerfile for Heroku
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy lab materials
COPY . .

# Create non-root user for security
RUN useradd -m -s /bin/bash labuser && chown -R labuser:labuser /app
USER labuser

# Use Heroku's PORT environment variable
ENV PORT=8888
EXPOSE $PORT

# Heroku-compatible startup command
CMD jupyter lab --ip=0.0.0.0 --port=$PORT --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' --NotebookApp.allow_remote_access=True
