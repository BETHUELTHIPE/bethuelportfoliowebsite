# Manual EC2 Deployment Steps

## 1. SSH into your EC2 instance
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

## 2. Install Docker and Docker Compose
```bash
# Update system
sudo apt-get update -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for docker group to take effect
exit
```

## 3. Clone and deploy
```bash
# SSH back in
ssh -i your-key.pem ubuntu@your-ec2-ip

# Clone repository
git clone https://github.com/BETHUELTHIPE/bethuelportfoliowebsite.git
cd bethuelportfoliowebsite/Bethuel-website-main

# Deploy with production config
docker-compose -f docker-compose.prod.yml up -d --build
```

## 4. Configure Security Group
Ensure your EC2 security group allows:
- Port 22 (SSH)
- Port 80 (HTTP)
- Port 8080 (Application)

## 5. Access your application
- Website: http://your-ec2-ip:8080
- Admin: http://your-ec2-ip:8080/admin (admin/admin123)