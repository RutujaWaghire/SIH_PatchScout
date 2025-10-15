FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for scanning tools
RUN apt-get update && apt-get install -y \
    nmap \
    nikto \
    wget \
    curl \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Nuclei
RUN wget -q https://github.com/projectdiscovery/nuclei/releases/download/v3.1.0/nuclei_3.1.0_linux_amd64.zip \
    && unzip nuclei_3.1.0_linux_amd64.zip \
    && mv nuclei /usr/local/bin/ \
    && rm nuclei_3.1.0_linux_amd64.zip \
    && chmod +x /usr/local/bin/nuclei

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /app/app
COPY ./scripts /app/scripts

# Create necessary directories
RUN mkdir -p /app/chroma_db /app/model_cache /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
