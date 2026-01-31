# Docker Deployment Guide

## Container Basics

Docker containers provide consistent environments across development and production.

### Creating a Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

## Docker Compose

Orchestrate multiple services with `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
    depends_on:
      - db
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Deployment Tips

- Use multi-stage builds to reduce image size
- Never store secrets in images
- Tag images with version numbers, not just `latest`

Happy containerizing!
