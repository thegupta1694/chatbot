#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
sleep 10

# Pull the llama3 model
ollama pull llama3

# Start the FastAPI application
uvicorn app:app --host 0.0.0.0 --port $PORT
