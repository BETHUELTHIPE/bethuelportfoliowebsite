#!/bin/bash

echo "🔍 Testing All Production Services..."
echo "=================================="

# Test Docker services
echo "📦 Checking Docker Services:"
docker-compose ps

echo ""
echo "🌐 Testing Service Endpoints:"

# Test main website
echo -n "Website (port 80): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo "✅ ONLINE"
else
    echo "❌ OFFLINE"
fi

# Test pgAdmin
echo -n "pgAdmin (port 5050): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5050 | grep -q "200"; then
    echo "✅ ONLINE"
else
    echo "❌ OFFLINE"
fi

# Test Redis
echo -n "Redis (port 6379): "
if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
    echo "✅ ONLINE"
else
    echo "❌ OFFLINE"
fi

# Test PostgreSQL
echo -n "PostgreSQL (port 5432): "
if docker-compose exec -T db pg_isready -U bethuel | grep -q "accepting connections"; then
    echo "✅ ONLINE"
else
    echo "❌ OFFLINE"
fi

echo ""
echo "🔧 Testing Application Features:"

# Test Django admin
echo -n "Django Admin: "
if curl -s http://localhost/admin/ | grep -q "Django"; then
    echo "✅ ACCESSIBLE"
else
    echo "❌ NOT ACCESSIBLE"
fi

# Test static files
echo -n "Static Files: "
if curl -s -o /dev/null -w "%{http_code}" http://localhost/static/css/style.css | grep -q "200"; then
    echo "✅ SERVED"
else
    echo "❌ NOT SERVED"
fi

# Test Celery worker
echo -n "Celery Worker: "
if docker-compose logs celery | grep -q "ready"; then
    echo "✅ RUNNING"
else
    echo "❌ NOT RUNNING"
fi

echo ""
echo "📊 Service Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "🔍 Recent Logs (last 10 lines):"
echo "Web Service:"
docker-compose logs --tail=5 web

echo ""
echo "Nginx Service:"
docker-compose logs --tail=5 nginx

echo ""
echo "✅ Service testing complete!"
echo "Run 'python test_production.py' for detailed functionality tests."