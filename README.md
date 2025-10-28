# Portfolio - Full-Stack Application

A modern portfolio website built with Django REST Framework backend and Astro frontend, containerized with Docker.

## 🏗️ Architecture

- **Backend**: Django REST Framework with SQLite database
- **Frontend**: Astro static site with API integration
- **Deployment**: Docker containers orchestrated with docker-compose

## 📁 Project Structure

```
portfolio/
├── backend/          # Django REST API
│   ├── api/         # Main API app with models, serializers, views
│   ├── portfolio_backend/  # Django settings
│   └── Dockerfile   # Backend container
├── frontend/         # Astro frontend
│   ├── src/         # Source files
│   └── Dockerfile   # Frontend container
├── docker-compose.yml  # Container orchestration
└── SETUP_GUIDE.md   # Detailed setup instructions
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Start the application**
   ```bash
   docker-compose up --build
   ```

2. **Initialize the database** (in a new terminal)
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   docker-compose exec backend python manage.py import_data
   ```

3. **Access the application**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000/api
   - Django Admin: http://localhost:8000/admin

### Manual Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed manual setup instructions.

## 📝 Managing Content

Use Django Admin at http://localhost:8000/admin to manage:
- Profile information
- Education history
- Work experience
- Projects
- Research publications
- Blog posts
- Site settings

All content is stored in SQLite database and served via REST API.

## 🛠️ Development

**Backend (Django)**
```bash
cd backend
python manage.py runserver
```

**Frontend (Astro)**
```bash
cd frontend
npm run dev
```

## 📚 API Endpoints

- `GET /api/profile/` - Profile information
- `GET /api/education/` - Education entries
- `GET /api/experience/` - Work experience
- `GET /api/projects/` - Portfolio projects
- `GET /api/research/` - Research publications
- `GET /api/blogs/` - Blog posts
- `GET /api/social-links/` - Social media links
- `GET /api/site-settings/` - Site configuration

## 📖 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup and configuration guide
- [README.Docker.md](README.Docker.md) - Docker-specific instructions
- [frontend/BLOG_SYSTEM_GUIDE.md](frontend/BLOG_SYSTEM_GUIDE.md) - Blog system documentation

## 🐛 Troubleshooting

**Reset database:**
```bash
docker-compose down
rm backend/db.sqlite3
docker-compose up
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py import_data
```

**View logs:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🤝 Contributing

This is a personal portfolio project. Feel free to fork and customize for your own use.

## 📄 License

MIT License - Feel free to use this template for your own portfolio.

---

For detailed setup instructions, please refer to [SETUP_GUIDE.md](SETUP_GUIDE.md).
