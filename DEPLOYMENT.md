# AWS EC2 Deployment Guide

This guide will help you deploy your Portfolio project on AWS EC2 with Docker and Nginx.

## 🚀 Quick Deployment

### Prerequisites

1. **AWS EC2 Instance** (Ubuntu 20.04 or later recommended)
   - Instance Type: t2.medium or larger recommended
   - Storage: At least 20GB
   - Security Group: Allow ports 80 (HTTP) and 443 (HTTPS)

2. **SSH Access** to your EC2 instance

### Step 1: Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose **Ubuntu Server 22.04 LTS**
4. Instance type: **t2.medium** (or larger)
5. Configure Security Group:
   ```
   Type            Protocol    Port Range    Source
   SSH             TCP         22            Your IP
   HTTP            TCP         80            0.0.0.0/0
   HTTPS           TCP         443           0.0.0.0/0
   Custom TCP      TCP         8000          0.0.0.0/0 (for testing)
   Custom TCP      TCP         4321          0.0.0.0/0 (for testing)
   ```
6. Launch and save your `.pem` key file

### Step 2: Connect to EC2

```bash
# Make key file secure
chmod 400 your-key.pem

# Connect to EC2
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Step 3: Clone Repository

```bash
# Update system
sudo apt update

# Install git
sudo apt install -y git

# Clone your repository
git clone https://github.com/yourusername/portfolio.git
cd portfolio
```

### Step 4: Run Deployment Script

```bash
# Make script executable
chmod +x deploy-aws.sh

# Run deployment script (as root)
sudo bash deploy-aws.sh
```

The script will:
- ✅ Detect EC2 public IP automatically
- ✅ Install Docker and Docker Compose
- ✅ Install and configure Nginx
- ✅ Create `.env` file with proper configurations
- ✅ Update Django and Astro configs
- ✅ Set up SSL (if you have a domain)
- ✅ Build and start Docker containers
- ✅ Run database migrations
- ✅ Set up auto-restart on reboot

### Step 5: Access Your Application

After deployment completes, access your app:

- **Frontend**: `http://your-ec2-public-ip`
- **Backend API**: `http://your-ec2-public-ip/api`
- **Admin Panel**: `http://your-ec2-public-ip/admin`

## 🔧 Manual Configuration (if needed)

### Update Django Settings

If you need to manually update Django settings:

```bash
nano portfolio-backend/portfolio_backend/settings.py
```

Update:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-ec2-ip', 'localhost']
```

### Update Astro Config

```bash
nano portfolio-frontend/astro.config.mjs
```

Update:
```javascript
export default defineConfig({
    site: 'http://your-ec2-public-ip',
    // ... rest of config
});
```

### Update Environment Variables

```bash
nano .env
```

Update URLs:
```env
VITE_API_URL=http://your-ec2-public-ip/api
PUBLIC_API_URL=http://your-ec2-public-ip/api
PUBLIC_SITE_URL=http://your-ec2-public-ip
```

## 🌐 Custom Domain Setup

### Step 1: Point Domain to EC2

1. Go to your domain registrar (e.g., GoDaddy, Namecheap)
2. Add an A record:
   ```
   Type: A
   Name: @ (or subdomain)
   Value: your-ec2-public-ip
   TTL: 300
   ```

### Step 2: Update Deployment

Run deployment script again and provide your domain when prompted:
```bash
sudo bash deploy-aws.sh
```

### Step 3: SSL Certificate

The script will automatically set up SSL with Let's Encrypt if you have a domain.

Manual SSL setup:
```bash
sudo certbot --nginx -d yourdomain.com
```

## 📊 Useful Commands

### Docker Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# Restart all containers
docker-compose restart

# Stop all containers
docker-compose down

# Start all containers
docker-compose up -d

# Rebuild containers
docker-compose up -d --build
```

### Django Commands

```bash
# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Run migrations
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput

# Django shell
docker-compose exec backend python manage.py shell
```

### Nginx Commands

```bash
# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

# Restart Nginx
sudo systemctl restart nginx

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log

# View Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

## 🔄 Updating Your Application

```bash
# Navigate to project directory
cd ~/portfolio

# Pull latest changes
git pull origin main

# Rebuild and restart containers
docker-compose down
docker-compose up -d --build

# Run migrations (if any)
docker-compose exec backend python manage.py migrate

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

## 💾 Database Backup

```bash
# Backup database
docker-compose exec backend python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Or backup SQLite file directly
cp portfolio-backend/db.sqlite3 db_backup_$(date +%Y%m%d_%H%M%S).sqlite3
```

## 🔒 Security Checklist

- [ ] Change Django `SECRET_KEY` in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL certificate
- [ ] Configure firewall (ufw)
- [ ] Regular database backups
- [ ] Keep system and Docker images updated
- [ ] Use strong passwords for admin accounts

## 🐛 Troubleshooting

### Containers won't start

```bash
# Check logs
docker-compose logs

# Check individual service
docker-compose logs backend
docker-compose logs frontend
```

### Can't access website

1. Check EC2 Security Group allows ports 80 and 443
2. Check Nginx is running: `sudo systemctl status nginx`
3. Check containers are running: `docker-compose ps`
4. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`

### Database issues

```bash
# Reset database
docker-compose down
rm portfolio-backend/db.sqlite3
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### SSL certificate issues

```bash
# Renew SSL certificate
sudo certbot renew

# Force renew
sudo certbot renew --force-renewal
```

## 📞 Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify EC2 Security Group settings
4. Ensure all environment variables are set correctly

## 🎉 Success!

Your portfolio is now deployed and accessible to the world!

- Frontend: `http://your-domain-or-ip`
- Admin: `http://your-domain-or-ip/admin`

Enjoy! 🚀
