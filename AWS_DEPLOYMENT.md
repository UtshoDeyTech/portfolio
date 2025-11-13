# AWS EC2 Deployment Guide - Portfolio Application

Complete guide for deploying your Django + Astro portfolio application on AWS EC2.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [EC2 Instance Setup](#ec2-instance-setup)
3. [Quick Deployment](#quick-deployment)
4. [Manual Deployment Steps](#manual-deployment-steps)
5. [SSL/HTTPS Setup](#sslhttps-setup)
6. [Post-Deployment Configuration](#post-deployment-configuration)
7. [Maintenance and Management](#maintenance-and-management)
8. [Troubleshooting](#troubleshooting)
9. [Cost Optimization](#cost-optimization)

---

## Prerequisites

- AWS Account
- Basic knowledge of Linux command line
- Domain name (optional, but recommended for SSL)
- SSH client installed on your local machine

---

## EC2 Instance Setup

### 1. Create EC2 Instance

1. **Log in to AWS Console**: https://console.aws.amazon.com/
2. **Navigate to EC2**: Services → EC2
3. **Launch Instance**:
   - **Name**: `portfolio-app`
   - **AMI**: Ubuntu Server 22.04 LTS (Free Tier Eligible)
   - **Instance Type**: `t2.small` or `t3.small` (minimum recommended)
     - `t2.micro` may work but could be slow during builds
   - **Key Pair**: Create new or use existing (download and save safely)
   - **Network Settings**:
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere (0.0.0.0/0)
     - Allow HTTPS (port 443) from anywhere (0.0.0.0/0)
   - **Storage**: 20-30 GB gp3 (general purpose SSD)
4. **Launch Instance**

### 2. Connect to EC2 Instance

```bash
# Update permissions on your key file
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Replace `YOUR_EC2_PUBLIC_IP` with your instance's public IP from AWS console.

### 3. Initial Server Setup (Optional but Recommended)

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Create swap file (helps with memory on smaller instances)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## Quick Deployment

### Option 1: Using Deployment Script (Recommended)

1. **Clone your repository**:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
```

2. **Make scripts executable**:
```bash
chmod +x deploy_aws.sh ssl_setup.sh manage_deployment.sh
```

3. **Run deployment script**:
```bash
./deploy_aws.sh
```

The script will:
- Install Docker and Docker Compose
- Set up environment variables
- Build and start containers
- Configure firewall
- Set up systemd service for auto-start
- Prompt you to create Django superuser

4. **Access your application**:
- Frontend: `http://YOUR_EC2_PUBLIC_IP`
- Backend API: `http://YOUR_EC2_PUBLIC_IP/api/`
- Django Admin: `http://YOUR_EC2_PUBLIC_IP/admin/`

### Option 2: Manual Deployment

See [Manual Deployment Steps](#manual-deployment-steps) below.

---

## Manual Deployment Steps

If you prefer to deploy manually or want to understand each step:

### 1. Install Docker

```bash
# Install prerequisites
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
exit
# Then reconnect via SSH
```

### 2. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 3. Clone Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
```

### 4. Configure Environment

```bash
# Copy production environment template
cp .env.production.example .env.production

# Edit with your configuration
nano .env.production
```

**Update the following in `.env.production`**:
- `DJANGO_SECRET_KEY`: Generate a random secret key
- `DJANGO_ALLOWED_HOSTS`: Add your EC2 public IP and domain
- `CORS_ALLOWED_ORIGINS`: Add your frontend URL
- `PUBLIC_API_URL`: Set to your EC2 public IP or domain

**Generate Django Secret Key**:
```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
```

### 5. Build and Start Containers

```bash
# Build images
docker-compose -f docker-compose.prod.yml --env-file .env.production build

# Start services
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

# Check status
docker-compose -f docker-compose.prod.yml --env-file .env.production ps
```

### 6. Create Django Superuser

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.production exec backend python manage.py createsuperuser
```

### 7. Configure Firewall

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 8. Set Up Systemd Service (Auto-start on Reboot)

```bash
sudo nano /etc/systemd/system/portfolio.service
```

Add the following content (replace `/home/ubuntu/portfolio` with your actual path):

```ini
[Unit]
Description=Portfolio Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/portfolio
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml --env-file .env.production down
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable portfolio.service
sudo systemctl start portfolio.service
sudo systemctl status portfolio.service
```

---

## SSL/HTTPS Setup

### Prerequisites

- A domain name pointing to your EC2 instance's public IP
- Ports 80 and 443 open in EC2 security group

### Option 1: Using SSL Setup Script

```bash
chmod +x ssl_setup.sh
sudo ./ssl_setup.sh
```

Follow the prompts to:
1. Enter your domain name
2. Enter your email address
3. The script will obtain SSL certificate and configure nginx

After running the script:
1. Edit `nginx/nginx.conf`
2. Uncomment the HTTPS server block
3. Update `server_name` with your domain
4. Uncomment the HTTP to HTTPS redirect
5. Restart nginx:

```bash
docker-compose -f docker-compose.prod.yml --env-file .env.production restart nginx
```

### Option 2: Manual SSL Setup

1. **Install Certbot**:
```bash
sudo apt-get update
sudo apt-get install -y certbot
```

2. **Stop nginx container temporarily**:
```bash
docker-compose -f docker-compose.prod.yml stop nginx
```

3. **Obtain SSL certificate**:
```bash
sudo certbot certonly --standalone \
  --preferred-challenges http \
  --email your-email@example.com \
  --agree-tos \
  -d your-domain.com
```

4. **Copy certificates**:
```bash
sudo mkdir -p nginx/ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/
sudo chmod 644 nginx/ssl/*.pem
```

5. **Update nginx configuration**:
   - Edit `nginx/nginx.conf`
   - Uncomment HTTPS server block
   - Update `server_name` to your domain

6. **Restart nginx**:
```bash
docker-compose -f docker-compose.prod.yml up -d nginx
```

### SSL Certificate Auto-Renewal

Set up a cron job for auto-renewal:

```bash
sudo crontab -e
```

Add this line:
```
0 0 1 * * certbot renew --quiet && docker-compose -f /home/ubuntu/portfolio/docker-compose.prod.yml restart nginx
```

---

## Post-Deployment Configuration

### 1. Configure Domain DNS

Point your domain to your EC2 instance:

**In your domain registrar's DNS settings**:
- Type: `A Record`
- Name: `@` (or `www`)
- Value: Your EC2 Public IP
- TTL: `3600`

### 2. Update Environment for Domain

Edit `.env.production`:

```bash
nano .env.production
```

Update:
```env
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_EC2_IP
CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
PUBLIC_API_URL=https://your-domain.com/api
```

Restart services:
```bash
docker-compose -f docker-compose.prod.yml --env-file .env.production restart
```

### 3. Set Up Monitoring (Optional)

Install monitoring tools:

```bash
# Install htop for system monitoring
sudo apt-get install -y htop

# Install Docker stats dashboard
docker stats
```

---

## Maintenance and Management

### Using Management Script

```bash
chmod +x manage_deployment.sh
./manage_deployment.sh
```

This interactive script provides options for:
- Viewing logs
- Restarting services
- Running Django commands
- Creating backups
- Updating deployment

### Common Commands

**View logs**:
```bash
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

**Restart services**:
```bash
docker-compose -f docker-compose.prod.yml restart
docker-compose -f docker-compose.prod.yml restart backend
```

**Stop/Start services**:
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

**Update deployment**:
```bash
cd ~/portfolio
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

**Database backup**:
```bash
docker cp portfolio-backend-prod:/app/db.sqlite3 ./backup_$(date +%Y%m%d).sqlite3
```

**Django management commands**:
```bash
# Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Django shell
docker-compose -f docker-compose.prod.yml exec backend python manage.py shell

# Collect static files
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic
```

---

## Troubleshooting

### Issue: Cannot connect to application

**Check if containers are running**:
```bash
docker-compose -f docker-compose.prod.yml ps
```

**Check logs**:
```bash
docker-compose -f docker-compose.prod.yml logs
```

**Check security group**: Ensure ports 80 and 443 are open in AWS EC2 security group.

### Issue: Frontend cannot connect to backend

**Check CORS settings** in `.env.production`:
```env
CORS_ALLOWED_ORIGINS=http://your-domain.com,https://your-domain.com
```

**Check API URL** in `.env.production`:
```env
PUBLIC_API_URL=http://your-domain.com/api
```

### Issue: Out of memory

**Add swap space**:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

**Or upgrade EC2 instance type** to t3.small or larger.

### Issue: SSL certificate errors

**Check certificate files**:
```bash
ls -la nginx/ssl/
```

**Verify nginx configuration**:
```bash
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

**Check certbot logs**:
```bash
sudo cat /var/log/letsencrypt/letsencrypt.log
```

### Issue: Port already in use

**Find what's using the port**:
```bash
sudo lsof -i :80
sudo lsof -i :8000
```

**Kill the process** or change ports in `.env.production`.

---

## Cost Optimization

### EC2 Instance Sizing

- **Development/Testing**: t2.micro (Free Tier) or t3.micro
- **Low Traffic Production**: t3.small
- **Medium Traffic**: t3.medium
- **High Traffic**: t3.large or consider Auto Scaling

### Cost-Saving Tips

1. **Use Reserved Instances**: Save up to 75% for long-term commitments
2. **Enable Auto-Shutdown**: Schedule instance to stop during off-hours
3. **Monitor Usage**: Use AWS CloudWatch to track usage
4. **Clean Up Resources**: Regularly remove unused volumes, snapshots
5. **Use AWS Free Tier**: First 12 months free for t2.micro

### Backup Strategy

**Regular backups**:
```bash
# Create backup script
nano ~/backup.sh
```

Add:
```bash
#!/bin/bash
cd ~/portfolio
docker cp portfolio-backend-prod:/app/db.sqlite3 ./backups/db_$(date +%Y%m%d_%H%M%S).sqlite3
# Upload to S3 (optional)
# aws s3 cp ./backups/ s3://your-bucket/portfolio-backups/ --recursive
```

Make executable and add to crontab:
```bash
chmod +x ~/backup.sh
crontab -e
# Add: 0 2 * * * /home/ubuntu/backup.sh
```

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

## Support

For issues specific to this deployment setup, please check:
1. Application logs
2. This troubleshooting guide
3. AWS EC2 documentation
4. Docker documentation

---

## Security Best Practices

1. **Keep system updated**:
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Change default SSH port** (optional but recommended)

3. **Use strong passwords** for Django admin

4. **Enable automatic security updates**:
   ```bash
   sudo apt-get install unattended-upgrades
   sudo dpkg-reconfigure --priority=low unattended-upgrades
   ```

5. **Regular backups** of database and configuration

6. **Monitor logs** for suspicious activity

7. **Use environment variables** for sensitive data (never commit secrets)

8. **Restrict SSH access** to specific IPs in security group

---

## Next Steps

After successful deployment:

1. ✅ Test all functionality
2. ✅ Set up SSL/HTTPS
3. ✅ Configure domain DNS
4. ✅ Create database backups
5. ✅ Set up monitoring
6. ✅ Add content to your portfolio
7. ✅ Test performance and optimize
8. ✅ Set up CI/CD (optional)

---

**Congratulations! Your portfolio is now live on AWS EC2! 🎉**
