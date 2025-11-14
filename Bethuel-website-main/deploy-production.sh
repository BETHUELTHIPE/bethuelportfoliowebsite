#!/bin/bash

echo "🚀 Deploying Bethuel Portfolio to Production..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker stop $(docker ps -q --filter "ancestor=bethuel-portfolio") 2>/dev/null || true
docker container prune -f

# Build production image
echo "🔨 Building production image..."
docker build -t bethuel-portfolio:production . --no-cache

# Run production container
echo "🌐 Starting production container..."
docker run -d \
  -p 80:8000 \
  --name bethuel-portfolio-prod \
  --restart unless-stopped \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=* \
  bethuel-portfolio:production

echo "✅ Production deployment complete!"
echo "🌍 Website available at: http://localhost"
echo "📊 Container status:"
docker ps --filter "name=bethuel-portfolio-prod"