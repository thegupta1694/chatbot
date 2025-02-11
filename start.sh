#!/bin/bash
set -e

echo "Starting Ollama service..."
nohup ollama serve &

echo "Waiting for Ollama to initialize..."
sleep 15

echo "Checking Ollama service..."
curl -s http://localhost:11434/api/version || (echo "Ollama is not responding" && exit 1)

echo "Pulling llama3 model..."
ollama pull llama3

echo "Verifying model..."
ollama list

echo "Starting FastAPI application..."
exec uvicorn app:app --host 0.0.0.0 --port $PORT --log-level debug
