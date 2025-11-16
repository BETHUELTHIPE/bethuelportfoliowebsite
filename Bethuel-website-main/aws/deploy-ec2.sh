#!/bin/bash

# Deploy to existing EC2 instance
set -e

if [ -z "$1" ]; then
    echo "Usage: ./deploy-ec2.sh <EC2_PUBLIC_IP>"
    echo "Example: ./deploy-ec2.sh 54.123.45.67"
    exit 1
fi

EC2_IP=$1
KEY_FILE="bethuel-portfolio-key.pem"

echo "🚀 Deploying to EC2 instance: $EC2_IP"

# Step 1: Copy files to EC2
echo "📁 Copying project files..."
scp -i $KEY_FILE -r . ubuntu@$EC2_IP:/home/ubuntu/bethuel-portfolio/

# Step 2: SSH and deploy
echo "🔧 Connecting to EC2 and deploying..."
ssh -i $KEY_FILE ubuntu@$EC2_IP << 'EOF'
cd /home/ubuntu/bethuel-portfolio

# Update system
sudo apt-get update -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Stop existing containers
docker-compose down || true

# Build and start services
docker-compose up --build -d

# Wait for services to start
sleep 30

# Check status
docker-compose ps

echo "✅ Deployment complete!"
echo "🌐 Website available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
EOF

echo "🎉 Deployment to EC2 completed!"
echo "🌐 Access your website at: http://$EC2_IP:8080"
echo "🔧 pgAdmin at: http://$EC2_IP:5050"