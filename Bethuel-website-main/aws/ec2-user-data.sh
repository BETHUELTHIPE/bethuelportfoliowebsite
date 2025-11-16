#!/bin/bash

# EC2 User Data Script for Ubuntu
# This script runs when the EC2 instance starts

# Update system
apt-get update -y
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
apt-get install -y git

# Clone repository
cd /home/ubuntu
git clone https://github.com/BETHUELTHIPE/bethuelportfoliowebsite.git
cd bethuelportfoliowebsite/Bethuel-website-main

# Set permissions
chown -R ubuntu:ubuntu /home/ubuntu/bethuelportfoliowebsite
chmod +x /home/ubuntu/bethuelportfoliowebsite/Bethuel-website-main/deploy-production.sh

# Create environment file
cat > .env << EOF
DJANGO_SECRET_KEY=bethuel-portfolio-secret-key-2024-production
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=*
POSTGRES_DB=bethuel_portfolio
POSTGRES_USER=bethuel
POSTGRES_PASSWORD=bethuel123
POSTGRES_HOST=db
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>
DEFAULT_FROM_EMAIL=<email>
EOF

# Start services
docker-compose up -d

# Setup log rotation
cat > /etc/logrotate.d/docker-compose << EOF
/home/ubuntu/bethuelportfoliowebsite/Bethuel-website-main/logs/*.log {
    daily
    missingok
    rotate 7
    compress
    notifempty
    create 644 ubuntu ubuntu
}
EOF

echo "✅ Bethuel Portfolio deployed successfully on EC2!"
echo "🌐 Website will be available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"