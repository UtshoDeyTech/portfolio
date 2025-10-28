# Docker Setup Guide

This portfolio application is dockerized with separate containers for frontend (Astro) and backend (Django).

## Prerequisites

- Docker Desktop installed
- Docker Compose installed

## Quick Start

1. **Clone the repository**
   ```bash
   cd portfolio
   ```

2. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000/api
   - Django Admin: http://localhost:8000/admin

## Development Workflow

### Start the application
```bash
docker-compose up
```

### Start in detached mode
```bash
docker-compose up -d
```

### Stop the application
```bash
docker-compose down
```

### Rebuild containers (after dependency changes)
```bash
docker-compose up --build
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Django Management Commands

### Run migrations
```bash
docker-compose exec backend python manage.py migrate
```

### Create superuser (for Django admin)
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Import data from JSON
```bash
docker-compose exec backend python manage.py import_data
```

### Access Django shell
```bash
docker-compose exec backend python manage.py shell
```

## Database

The SQLite database is stored in the `backend/` directory and is persisted across container restarts.

## Volumes

- `backend-static`: Django static files
- `backend-media`: User uploaded media files
- Source code is mounted as volumes for hot-reloading during development

## Production Deployment

For production:
1. Set `DEBUG=False` in backend settings
2. Update `ALLOWED_HOSTS` in settings.py
3. Use environment variables for sensitive data
4. Consider using PostgreSQL instead of SQLite
5. Serve static files through Nginx
6. Enable HTTPS

## Troubleshooting

### Port already in use
If ports 4321 or 8000 are already in use, modify the ports in `docker-compose.yml`:
```yaml
ports:
  - "4322:4321"  # Change 4322 to any available port
```

### Database locked error
Stop all containers and restart:
```bash
docker-compose down
docker-compose up
```

### Frontend not connecting to backend
Ensure the `API_URL` environment variable in docker-compose.yml points to the correct backend service name.
