#!/bin/bash

# Ensure script halts on error
set -e

echo "🚀 Starting Agentic Design System Platform..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
  echo "Error: Docker is not running. Please start Docker Desktop and try again."
  exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up --build
