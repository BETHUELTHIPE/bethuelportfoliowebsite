#!/bin/bash

echo "🚀 Deploying Bethuel Portfolio to EC2..."

# Update system
sudo apt-get update -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Update docker-compose for production
echo "⚙️ Configuring for production..."
export DJANGO_ALLOWED_HOSTS="*"
export DJANGO_DEBUG="False"

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check status
echo "📊 Checking service status..."
docker-compose ps

# Get public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "localhost")

echo ""
echo "✅ Deployment complete!"
echo "🌐 Website: http://$PUBLIC_IP:8080"
echo "🔧 Admin: http://$PUBLIC_IP:8080/admin (admin/admin123)"
echo "📊 pgAdmin: http://$PUBLIC_IP:5050 (admin@bethuel.com/admin123)"