#!/bin/bash

echo "🔄 Running migrations and collecting static files..."

# Stop current container
docker stop $(docker ps -q --filter "ancestor=bethuel-portfolio") 2>/dev/null || true

# Build new image with updates
docker build -t bethuel-portfolio . --no-cache

# Run migrations and collect static inside container
docker run --rm bethuel-portfolio python manage.py makemigrations
docker run --rm bethuel-portfolio python manage.py migrate
docker run --rm bethuel-portfolio python manage.py collectstatic --noinput

# Start new container
docker run -d -p 8000:8000 --name bethuel-site bethuel-portfolio

echo "✅ Migrations and static files updated!"
echo "🌐 Website running at: http://localhost:8000"