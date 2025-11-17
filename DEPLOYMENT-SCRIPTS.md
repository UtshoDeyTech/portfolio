# Deployment Scripts Guide

This project uses **2 shell scripts** for deployment and maintenance:

## 📜 Available Scripts

### 1. `deploy.sh` - Main Production Deployment
**Purpose**: Complete production deployment on Ubuntu/AWS EC2

**What it does**:
- ✅ Installs system dependencies (Python, Node.js, Nginx)
- ✅ Sets up Python virtual environment
- ✅ Configures Django backend with Gunicorn
- ✅ Builds Astro frontend
- ✅ Configures Nginx with smart caching
- ✅ Creates systemd service for auto-start
- ✅ Sets up auto-rebuild cron job

**Usage**:
```bash
cd ~/portfolio
sudo bash deploy.sh
```

**When to use**:
- Initial deployment to new server
- Major updates or configuration changes
- After pulling significant code changes

---

### 2. `auto-rebuild.sh` - Automatic Frontend Rebuild
**Purpose**: Rebuild frontend to fetch fresh data from API

**What it does**:
- ✅ Rebuilds Astro frontend with latest API data
- ✅ Reloads Nginx to serve new build
- ✅ Logs all operations to `auto-rebuild.log`

**Usage**:
```bash
# Manual run
sudo bash auto-rebuild.sh

# View auto-rebuild logs
tail -f ~/portfolio/auto-rebuild.log

# Check cron schedule
crontab -l
```

**Automatic Schedule**:
- Runs every 6 hours via cron
- Configured automatically by `deploy.sh`
- Keeps frontend data fresh without manual intervention

---

## 🚀 Quick Deployment Workflow

### First Time Setup
```bash
# 1. Clone repository
git clone https://github.com/UtshoDeyTech/portfolio.git
cd portfolio

# 2. Run full deployment
sudo bash deploy.sh

# 3. Create Django superuser (optional)
cd portfolio-backend
source venv/bin/activate
python manage.py createsuperuser
```

### Regular Updates
```bash
# 1. Pull latest changes
cd ~/portfolio
git pull origin main

# 2. Update backend dependencies
cd portfolio-backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart portfolio-backend

# 3. Rebuild frontend
cd ../portfolio-frontend
npm ci
npm run build
sudo systemctl reload nginx
```

### Quick Frontend Update Only
```bash
cd ~/portfolio
sudo bash auto-rebuild.sh
```

---

## 📊 Caching Strategy

The deployment includes a smart caching strategy:

| Resource Type | Cache Duration | Why |
|--------------|----------------|-----|
| Interactive endpoints (like, comment) | **No cache** | Immediate updates |
| Blog detail pages | **2 minutes** | Admin updates visible quickly |
| Blog lists | **6 hours** | Rarely change, fast performance |
| Static files (JS, CSS, images) | **1 year** | Versioned, immutable |

This ensures:
- ✅ Like/unlike updates immediately
- ✅ Comments appear instantly
- ✅ Admin updates visible within 2 minutes
- ✅ Fast page loads (cached static content)

---

## 🔧 Service Management

```bash
# Backend service
sudo systemctl status portfolio-backend
sudo systemctl restart portfolio-backend
sudo journalctl -u portfolio-backend -f

# Nginx
sudo systemctl status nginx
sudo systemctl reload nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View auto-rebuild logs
tail -f ~/portfolio/auto-rebuild.log
```

---

## 📁 Project Structure

```
portfolio/
├── deploy.sh                    # Main deployment script
├── auto-rebuild.sh              # Auto-rebuild script (used by cron)
├── portfolio-backend/           # Django backend
│   ├── venv/                    # Python virtual environment
│   ├── static/                  # Collected static files
│   └── media/                   # User uploaded files
└── portfolio-frontend/          # Astro frontend
    └── dist/                    # Built static files (served by Nginx)
```

---

## 🆘 Troubleshooting

### Service not starting
```bash
# Check backend logs
sudo journalctl -u portfolio-backend -n 50 --no-pager

# Check Nginx logs
sudo tail -50 /var/log/nginx/error.log
```

### Static files 403 error
```bash
# Fix permissions
cd ~/portfolio/portfolio-backend
sudo chmod 755 ~/
sudo chmod 755 ~/portfolio
sudo chmod 755 ~/portfolio/portfolio-backend
sudo chmod -R 755 static/
sudo systemctl reload nginx
```

### Frontend not updating
```bash
# Force rebuild
cd ~/portfolio
sudo bash auto-rebuild.sh

# Clear browser cache
# Chrome: Ctrl+Shift+Delete → Clear cached images and files
```

---

## 🔐 Security Group Requirements (AWS EC2)

Make sure your EC2 security group allows:
- **Port 80** (HTTP) - 0.0.0.0/0
- **Port 443** (HTTPS) - 0.0.0.0/0
- **Port 22** (SSH) - Your IP or 0.0.0.0/0

---

## 📞 Support

For issues or questions, check:
- GitHub Issues: https://github.com/UtshoDeyTech/portfolio/issues
- Server logs: `sudo journalctl -u portfolio-backend -f`
- Auto-rebuild logs: `tail -f ~/portfolio/auto-rebuild.log`
