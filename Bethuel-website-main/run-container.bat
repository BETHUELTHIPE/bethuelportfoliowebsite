@echo off
echo Starting Bethuel Portfolio Container...
docker run -d -p 8000:8000 --name bethuel-portfolio bethuel-portfolio:v3
echo Container started at http://localhost:8000