@echo off
echo Building Bethuel Portfolio Docker Image...
docker build -t bethuel-portfolio:v3 .
echo Build complete!
echo Run with: docker run -p 8000:8000 bethuel-portfolio:v3