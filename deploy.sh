#!/bin/bash

echo "🚀 Building Backend..."
docker build -t erenisci/rag-implementation:backend ./backend

echo "🚀 Building Frontend..."
docker build -t erenisci/rag-implementation:frontend ./frontend

echo "📤 Pushing Backend to Docker Hub..."
docker push erenisci/rag-implementation:backend

echo "📤 Pushing Frontend to Docker Hub..."
docker push erenisci/rag-implementation:frontend

echo "✅ Done!"
