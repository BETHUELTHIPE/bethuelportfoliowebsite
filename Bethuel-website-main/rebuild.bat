@echo off
echo 🛑 Stopping all containers...
docker stop $(docker ps -q) 2>nul

echo 🗑️ Removing old containers...
docker container prune -f

echo 🔨 Building new image with all changes...
docker build -t bethuel-portfolio . --no-cache

echo 🚀 Starting new container...
docker run -d -p 8000:8000 --name bethuel-site bethuel-portfolio

echo ✅ Done! Visit: http://localhost:8000
echo 💡 Hard refresh browser: Ctrl+F5