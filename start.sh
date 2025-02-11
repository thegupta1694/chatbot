#!/bin/bash
set -e

# Start Ollama in the background
nohup ollama serve &

# Wait for Ollama to start
sleep 15

# Pull the model
ollama pull llama3

# Start the FastAPI application
exec uvicorn app:app --host 0.0.0.0 --port $PORT
