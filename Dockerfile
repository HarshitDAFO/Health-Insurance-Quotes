# Use official lightweight Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxrender1 \
    libxext6 \
    libx11-6 \
    xfonts-75dpi \
    xfonts-base \
    wget \
    wkhtmltopdf \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py

# Expose the port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
