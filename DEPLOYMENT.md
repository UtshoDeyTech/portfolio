# Portfolio Deployment Guide

## 🚀 Quick Deploy (One Command)

Deploy your portfolio to AWS EC2 or any Ubuntu/Debian server:

```bash
sudo bash deploy.sh
```

**That's it!** The script will:
- ✅ Install all dependencies (Python, Node.js, Nginx)
- ✅ Set up Django backend with Gunicorn
- ✅ Build and serve Astro frontend
- ✅ Configure Nginx for both frontend and backend
- ✅ **Fix all static files issues** (Django admin CSS will work!)
- ✅ Auto-detect EC2 public IP
- ✅ Set up auto-restart services

## 🔧 Prerequisites

1. **Server**: AWS EC2 instance (Ubuntu 20.04+) or any Ubuntu/Debian server
   - Instance Type: t2.small or larger
   - Storage: At least 10GB
   - Open ports: 80 (HTTP), 443 (HTTPS)

2. **Access**: SSH access with sudo privileges

## 📋 Step-by-Step Deployment

### 1. Launch EC2 Instance

1. Go to AWS EC2 Console → Launch Instance
2. Choose **Ubuntu Server 22.04 LTS**
3. Instance type: **t2.small** (minimum) or **t2.medium** (recommended)
4. Configure Security Group:
   ```
   Type       Protocol    Port    Source
   SSH        TCP         22      Your IP
   HTTP       TCP         80      0.0.0.0/0
   HTTPS      TCP         443     0.0.0.0/0
   ```
5. Launch and save your `.pem` key file

### 2. Connect to Server

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### 3. Clone Repository

```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/UtshoDeyTech/portfolio.git
cd portfolio
```

### 4. Deploy

```bash
sudo bash deploy.sh
```

The script will auto-detect your EC2 public IP and configure everything!

### 5. Create Django Admin User

```bash
cd portfolio-backend
source venv/bin/activate
python manage.py createsuperuser
deactivate
```

### 6. Access Your Site

- **Website**: `http://YOUR_EC2_IP`
- **API**: `http://YOUR_EC2_IP/api/`
- **Django Admin**: `http://YOUR_EC2_IP/admin/` (with full CSS styling!)

## ✨ What Was Fixed

### Critical Bug: Django Admin CSS Not Loading

**❌ Previous Issue:**
```nginx
# Old deployment scripts had wrong path
location /static/ {
    alias /path/to/staticfiles/;  # ❌ This directory doesn't exist!
}
```
```python
# But Django creates:
STATIC_ROOT = BASE_DIR / 'static'  # Creates /static/ not /staticfiles/
```

**✅ Fixed in deploy.sh:**
```nginx
# Correct path matching Django's STATIC_ROOT
location /static/ {
    alias /path/to/static/;  # ✅ Matches Django's actual directory
}
```

**Result:** Django admin now loads with full CSS, JavaScript, and styling!

### Other Improvements

1. **No Extra Services** - Frontend served directly by Nginx (faster, no sirv-cli needed)
2. **CORS Fixed** - Auto-configured with your domain/IP
3. **Auto-detection** - Detects EC2 IP using AWS metadata service
4. **Idempotent** - Safe to run multiple times for updates

## 🔄 Update Deployment

To update after pulling new code:

```bash
cd portfolio
git pull origin main
sudo bash deploy.sh
```

## 📊 Service Management

### Check Status
```bash
sudo systemctl status portfolio-backend
sudo systemctl status nginx
```

### View Logs
```bash
# Backend logs (live)
sudo journalctl -u portfolio-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Restart Services
```bash
sudo systemctl restart portfolio-backend
sudo systemctl reload nginx
```

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────┐
│                  Nginx :80                        │
├───────────────────────────────────────────────────┤
│                                                   │
│  Frontend (/)                                     │
│  └─> /dist/ (Astro static files)                │
│                                                   │
│  Backend (/api/, /admin/)                        │
│  └─> Gunicorn :8000 (Django)                    │
│                                                   │
│  Static Files (/static/)                         │
│  └─> portfolio-backend/static/                  │
│                                                   │
│  Media Files (/media/)                           │
│  └─> portfolio-backend/media/                   │
│                                                   │
└───────────────────────────────────────────────────┘
```

## 🌐 Custom Domain Setup

### 1. Point Domain to EC2

In your domain registrar (GoDaddy, Namecheap, etc.):

```
Type: A Record
Name: @ (or subdomain)
Value: YOUR_EC2_IP
TTL: 300
```

### 2. Re-run Deployment

The script will detect your domain:

```bash
cd portfolio
sudo bash deploy.sh
# When prompted, enter your domain instead of IP
```

### 3. Add SSL Certificate

```bash
sudo certbot --nginx -d yourdomain.com
```

Then rebuild frontend with HTTPS:

```bash
cd portfolio-frontend
PUBLIC_API_URL=https://yourdomain.com npm run build
sudo systemctl reload nginx
```

## 🐛 Troubleshooting

### Backend Not Responding

```bash
# Check if service is running
sudo systemctl status portfolio-backend

# View last 50 log lines
sudo journalctl -u portfolio-backend -n 50

# Restart service
sudo systemctl restart portfolio-backend
```

### Django Admin CSS Still Not Loading

```bash
# Verify static files exist
ls -la portfolio-backend/static/admin/css/

# Fix permissions
sudo chmod -R 755 portfolio-backend/static/

# Verify nginx config
sudo nginx -t

# Check nginx is serving static files
curl http://YOUR_IP/static/admin/css/base.css
```

### Frontend Can't Reach Backend

```bash
# Check CORS configuration
cat portfolio-backend/.env | grep CORS

# Should show: CORS_ALLOWED_ORIGINS=http://YOUR_IP,https://YOUR_IP

# Rebuild frontend with correct API URL
cd portfolio-frontend
PUBLIC_API_URL=http://YOUR_IP npm run build
sudo systemctl reload nginx
```

### Nginx Configuration Errors

```bash
# Test nginx config
sudo nginx -t

# View error logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

## 💾 Database Management

### Backup Database

```bash
cd portfolio-backend
source venv/bin/activate
python manage.py dumpdata > backup_$(date +%Y%m%d).json
deactivate
```

Or backup SQLite file directly:

```bash
cp portfolio-backend/db.sqlite3 backup_$(date +%Y%m%d).sqlite3
```

### Restore Database

```bash
cd portfolio-backend
source venv/bin/activate
python manage.py loaddata backup_20250117.json
deactivate
```

## 🔒 Security Checklist

- [x] Django `SECRET_KEY` auto-generated (random 50 characters)
- [x] `DEBUG=False` in production
- [x] `ALLOWED_HOSTS` configured with your domain/IP
- [ ] SSL certificate installed (use certbot)
- [ ] Regular database backups
- [ ] Strong admin password created
- [ ] Firewall configured (optional):
  ```bash
  sudo ufw allow 22/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  sudo ufw enable
  ```

## 📈 Performance Tips

1. **Use t2.medium or larger** for better performance
2. **Add swap space** if using t2.small:
   ```bash
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

3. **Enable gzip compression** (already configured in nginx)

## 🎯 Common Tasks

### Add New Blog Post

1. Login to admin: `http://YOUR_IP/admin/`
2. Navigate to "Blog posts" → "Add blog post"
3. Fill in details and save
4. View on frontend: `http://YOUR_IP/blog/`

### Upload Project Images

1. Login to admin: `http://YOUR_IP/admin/`
2. Navigate to "Projects" → Select project
3. Upload image in "Thumbnail" or "Image" field
4. Save

### View API Documentation

Visit: `http://YOUR_IP/api/` for API overview

Available endpoints:
- `/api/home/` - Home page data
- `/api/blog-posts/` - All blog posts
- `/api/projects/` - All projects
- `/api/experience/` - Work experience
- `/api/education/` - Education history
- `/api/research/` - Research publications

## 📞 Support

If deployment fails:

1. **Check logs**: `sudo journalctl -u portfolio-backend -n 100`
2. **Verify nginx**: `sudo nginx -t`
3. **Check disk space**: `df -h`
4. **Verify services**: `sudo systemctl status portfolio-backend nginx`

## 🎉 Success!

Your portfolio is now live with:
- ✅ Fast static frontend (Astro)
- ✅ RESTful API backend (Django)
- ✅ Fully styled admin panel
- ✅ Auto-restart on failure
- ✅ All endpoints accessible

Access your portfolio at: **http://YOUR_EC2_IP**

Enjoy! 🚀
