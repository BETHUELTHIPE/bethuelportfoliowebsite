# Docker Setup Guide - Bethuel Portfolio Website

## Docker Image Built Successfully ✅

**Image Name**: `bethuel-portfolio:latest`
**Size**: ~2.05GB
**Base Image**: Python 3.10-slim

## Quick Start

### Option 1: Run with Docker Compose (Recommended)

```bash
cd c:\Users\Bethuel\Downloads\Bethuel-website-main\Bethuel-website-main
docker-compose -f docker-compose.run.yml up
```

Then access: http://localhost:8000

### Option 2: Run Docker Container Directly

```bash
docker run -d \
  --name bethuel-portfolio \
  -p 8000:8000 \
  -e DJANGO_DEBUG=True \
  -e DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,* \
  bethuel-portfolio:latest
```

Then access: http://localhost:8000

### Option 3: Run with Interactive Shell

```bash
docker run -it \
  --name bethuel-portfolio \
  -p 8000:8000 \
  bethuel-portfolio:latest \
  /bin/bash
```

## Container Details

- **Port**: 8000
- **User**: app (non-root for security)
- **Working Directory**: /app
- **Entry Point**: Gunicorn WSGI server

## Available Routes

- Home: http://localhost:8000/
- About: http://localhost:8000/about/
- Projects: http://localhost:8000/projects/
- Experience: http://localhost:8000/experience/
- Contact: http://localhost:8000/contact/
- Resume: http://localhost:8000/resume/
- Admin: http://localhost:8000/admin/

## Useful Docker Commands

### View running containers
```bash
docker ps
```

### View container logs
```bash
docker logs bethuel-portfolio
```

### Stop container
```bash
docker stop bethuel-portfolio
```

### Remove container
```bash
docker rm bethuel-portfolio
```

### View image details
```bash
docker inspect bethuel-portfolio:latest
```

## Environment Variables

Configure these in docker-compose.yml or with `-e` flag:

- `DJANGO_DEBUG`: Set to True for development
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DJANGO_SECRET_KEY`: Django secret key (auto-generated if not set)
- `EMAIL_HOST_USER`: Email for contact form
- `EMAIL_HOST_PASSWORD`: Email password

## Production Deployment

For production, use:
```bash
docker run -d \
  --name bethuel-portfolio-prod \
  -p 80:8000 \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=yourdomain.com \
  -e DJANGO_SECRET_KEY=your-production-secret-key \
  bethuel-portfolio:latest
```

## Troubleshooting

### Container won't start
```bash
docker logs bethuel-portfolio
```

### Port already in use
Change port mapping: `-p 8001:8000`

### Permission denied
Ensure Docker daemon is running and you have permissions

## Image Layers

The Dockerfile uses multi-stage build:
1. **Builder Stage**: Installs Python dependencies in virtual environment
2. **Final Stage**: Copies venv and app code, runs as non-root user

This reduces final image size and improves security.
