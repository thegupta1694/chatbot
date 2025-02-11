FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | bash

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Set environment variables for memory constraints
ENV OLLAMA_HOST=127.0.0.1:11434
ENV OLLAMA_ORIGINS=*
ENV GOGC=20
ENV MALLOC_ARENA_MAX=2

# Expose port
EXPOSE 8000

# Start the application
CMD ["./start.sh"]
