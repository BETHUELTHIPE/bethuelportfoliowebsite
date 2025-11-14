#!/bin/bash

echo "🚀 Deploying Full Stack Bethuel Portfolio..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Remove old images
echo "🗑️ Cleaning up old images..."
docker system prune -f

# Build and start all services
echo "🔨 Building and starting all services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Show running containers
echo "📊 Running services:"
docker-compose ps

echo ""
echo "✅ Full stack deployment complete!"
echo ""
echo "🌐 Services available at:"
echo "   Portfolio Website: http://localhost"
echo "   pgAdmin:          http://localhost:5050"
echo "   Redis:            localhost:6379"
echo "   PostgreSQL:       localhost:5432"
echo ""
echo "🔐 Default credentials:"
echo "   pgAdmin: admin@bethuel.com / admin123"
echo "   PostgreSQL: bethuel / bethuel123"
echo ""
echo "📋 To view logs:"
echo "   docker-compose logs -f [service_name]"
echo ""
echo "🛑 To stop all services:"
echo "   docker-compose down"