# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy project files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point
CMD ["python", "run_game.py"]
