#!/bin/bash
# Stop system nginx
sudo systemctl stop nginx
sudo systemctl disable nginx

# Restart containers with new port mapping
docker-compose down
docker-compose up -d

echo "Port mapping fixed. Your site should now be accessible on port 80."