# Quick Start Deployment Guide

Fast track guide to deploy your portfolio on AWS EC2 in under 10 minutes.

## Prerequisites

- AWS account with EC2 instance running Ubuntu 22.04
- SSH access to your EC2 instance
- Git installed on EC2

## Step-by-Step Deployment

### 1. Connect to EC2

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### 2. Clone Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
```

### 3. Run Deployment Script

```bash
chmod +x deploy_aws.sh
./deploy_aws.sh
```

The script automatically:
- Installs Docker & Docker Compose
- Configures environment variables
- Builds and starts containers
- Sets up firewall
- Configures auto-start on reboot

### 4. Create Admin User

When prompted, create a Django superuser for the admin panel.

### 5. Access Your Site

Your portfolio is now live at:
- **Frontend**: `http://YOUR_EC2_PUBLIC_IP`
- **Backend API**: `http://YOUR_EC2_PUBLIC_IP/api/`
- **Admin Panel**: `http://YOUR_EC2_PUBLIC_IP/admin/`

## Optional: Set Up HTTPS (Recommended)

If you have a domain name:

```bash
chmod +x ssl_setup.sh
sudo ./ssl_setup.sh
```

Then follow the prompts.

## Common Management Tasks

### View Application Logs

```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Restart Application

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Update Deployment

```bash
git pull
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

### Use Management Script

For an interactive menu with all common operations:

```bash
chmod +x manage_deployment.sh
./manage_deployment.sh
```

## Troubleshooting

**Can't access the site?**
- Check AWS Security Group allows port 80 and 443
- Verify containers are running: `docker-compose -f docker-compose.prod.yml ps`

**Need to restart?**
- `docker-compose -f docker-compose.prod.yml restart`

**Want to see logs?**
- `docker-compose -f docker-compose.prod.yml logs -f`

## Full Documentation

For detailed documentation, see [AWS_DEPLOYMENT.md](./AWS_DEPLOYMENT.md)

---

**That's it! Your portfolio is live! 🚀**
