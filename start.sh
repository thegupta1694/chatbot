#!/bin/bash
set -e

echo "Setting up system configurations..."
ulimit -m unlimited
ulimit -v unlimited

echo "Starting Ollama service..."
nohup ollama serve &

echo "Waiting for Ollama to initialize..."
sleep 15

echo "Checking Ollama service..."
curl -s http://localhost:11434/api/version || (echo "Ollama is not responding" && exit 1)

echo "Pulling optimized model..."
ollama pull gemma:2b

echo "Verifying model..."
ollama list

echo "Starting FastAPI application..."
exec uvicorn app:app --host 0.0.0.0 --port $PORT --workers 2 --limit-concurrency 5
