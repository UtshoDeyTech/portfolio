# Portfolio Setup Guide

This portfolio has been restructured into a full-stack application with:
- **Backend**: Django REST Framework API with SQLite database
- **Frontend**: Astro static site that calls the backend API
- **Docker**: Containerized setup with docker-compose

## Project Structure

```
portfolio/
├── backend/                 # Django REST API
│   ├── api/                # Main API app
│   │   ├── models.py       # Database models
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API viewsets
│   │   ├── urls.py         # API URL routing
│   │   ├── admin.py        # Django admin configuration
│   │   └── management/     # Custom management commands
│   ├── portfolio_backend/  # Django project settings
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container config
│   └── manage.py           # Django management script
│
├── frontend/               # Astro frontend
│   ├── src/
│   │   ├── lib/
│   │   │   └── api.ts     # API client utilities
│   │   ├── components/    # UI components
│   │   ├── layouts/       # Page layouts
│   │   └── pages/         # Route pages
│   ├── Dockerfile         # Frontend container config
│   └── package.json       # Node dependencies
│
└── docker-compose.yml     # Container orchestration
```

## Quick Start

### Option 1: Using Docker (Recommended)

1. **Start the application**
   ```bash
   docker-compose up --build
   ```

2. **Initialize the database**
   In a new terminal:
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   docker-compose exec backend python manage.py import_data
   ```

3. **Access the application**
   - Frontend: http://localhost:4321
   - Backend API: http://localhost:8000/api
   - Django Admin: http://localhost:8000/admin

### Option 2: Manual Setup (Development)

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Import sample data**
   ```bash
   python manage.py import_data
   ```

7. **Start backend server**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at http://localhost:8000

#### Frontend Setup

1. **Open a new terminal and navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   Ensure PUBLIC_API_URL=http://localhost:8000/api

4. **Start development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at http://localhost:4321

## API Endpoints

All API endpoints are available at `/api/`:

- `GET /api/profile/` - Get profile information
- `GET /api/social-links/` - Get social media links
- `GET /api/site-settings/` - Get site configuration
- `GET /api/education/` - List all education entries
- `GET /api/experience/` - List all work experiences
- `GET /api/projects/` - List all projects
- `GET /api/research/` - List all research publications
- `GET /api/blogs/` - List all blog posts
- `GET /api/blogs/{slug}/` - Get blog post by slug
- `GET /api/home-section/` - Get home page hero section

## Managing Content

### Using Django Admin

1. Access http://localhost:8000/admin
2. Login with your superuser credentials
3. Edit any content (Education, Experience, Projects, Research, Blog posts, etc.)
4. Changes will be immediately reflected via the API

### Database Models

All models are defined in `backend/api/models.py`:
- **Profile**: Personal information and bio
- **SocialLinks**: Social media and contact links
- **SiteSettings**: Website configuration and SEO
- **Education**: Education history
- **Experience**: Work experience
- **Project**: Portfolio projects
- **Research**: Research publications
- **Blog**: Blog posts
- **HomeSection**: Home page hero content

## Frontend API Integration

The frontend uses the API client located at `frontend/src/lib/api.ts`.

Example usage:
```typescript
import { getProjects, getEducation } from '@/lib/api';

// Fetch projects
const projects = await getProjects();

// Fetch education
const education = await getEducation();
```

To update a page to use API data instead of hardcoded data:
1. Import the appropriate API function from `@/lib/api`
2. Call the function to fetch data
3. Use the returned data in your component

## Development Workflow

1. **Make backend changes**
   - Edit models, serializers, or views in `backend/api/`
   - Run migrations if models changed: `python manage.py makemigrations && python manage.py migrate`
   - Django will auto-reload on file changes

2. **Make frontend changes**
   - Edit components, pages, or styles in `frontend/src/`
   - Astro will hot-reload changes automatically

3. **Manage content**
   - Use Django Admin at http://localhost:8000/admin
   - All changes are stored in SQLite database
   - Database file: `backend/db.sqlite3`

## Troubleshooting

### Database Issues
```bash
# Reset database
docker-compose down
rm backend/db.sqlite3
docker-compose up
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py import_data
```

### Port Conflicts
Edit `docker-compose.yml` and change port mappings:
```yaml
ports:
  - "8001:8000"  # Backend
  - "4322:4321"  # Frontend
```

### API Connection Issues
- Ensure backend is running
- Check `PUBLIC_API_URL` in frontend/.env
- Check browser console for CORS errors

### Docker Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Next Steps

1. **Customize the data**: Use Django Admin to update your portfolio content
2. **Update styling**: Modify Tailwind classes in frontend components
3. **Add features**: Extend models and API endpoints as needed
4. **Deploy**: Consider deploying backend to Railway/Heroku and frontend to Vercel/Netlify

## Production Considerations

- Set `DEBUG=False` in Django settings
- Use PostgreSQL instead of SQLite
- Configure proper ALLOWED_HOSTS
- Set up static file serving (Whitenoise or Nginx)
- Enable HTTPS
- Use environment variables for secrets
- Set up monitoring and logging

## Support

For issues or questions:
- Check the README.Docker.md for Docker-specific help
- Review Django logs: `docker-compose logs backend`
- Review Astro logs: `docker-compose logs frontend`
