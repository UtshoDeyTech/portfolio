#!/bin/bash

################################################################################
# AWS EC2 Deployment Script for Portfolio Project
#
# This script will:
# 1. Install Docker and Docker Compose
# 2. Install and configure Nginx
# 3. Detect EC2 public URL
# 4. Create .env file with proper configurations
# 5. Update Django and Astro configs
# 6. Set up SSL (optional)
# 7. Deploy the application
#
# Usage: sudo bash deploy-aws.sh
################################################################################

set -e  # Exit on any error

echo "=================================="
echo "Portfolio AWS EC2 Deployment"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Get the actual user (not root)
ACTUAL_USER=${SUDO_USER:-$USER}
PROJECT_DIR=$(pwd)

echo -e "${GREEN}Step 1: Detecting EC2 Instance Information${NC}"
echo "=========================================="

# Detect EC2 public IP - Try IMDSv2 first (more secure), then fall back to IMDSv1
echo "Attempting to detect EC2 metadata..."

# Try IMDSv2 (with token)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" --max-time 2 2>/dev/null || echo "")
if [ -n "$TOKEN" ]; then
    echo "Using IMDSv2 (token-based) for metadata..."
    EC2_PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4 --max-time 2 2>/dev/null || echo "")
    EC2_PUBLIC_DNS=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-hostname --max-time 2 2>/dev/null || echo "")
else
    # Fall back to IMDSv1 (no token)
    echo "Trying IMDSv1 (legacy) for metadata..."
    EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --max-time 2 2>/dev/null || echo "")
    EC2_PUBLIC_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname --max-time 2 2>/dev/null || echo "")
fi

if [ -z "$EC2_PUBLIC_IP" ]; then
    echo -e "${RED}Error: Could not detect EC2 public IP. Are you running on EC2?${NC}"
    read -p "Enter your server's public IP manually: " EC2_PUBLIC_IP
fi

if [ -z "$EC2_PUBLIC_DNS" ]; then
    EC2_PUBLIC_DNS=$EC2_PUBLIC_IP
fi

echo -e "${GREEN}✓ Detected Public IP: $EC2_PUBLIC_IP${NC}"
echo -e "${GREEN}✓ Detected Public DNS: $EC2_PUBLIC_DNS${NC}"
echo ""

# Ask user for domain or use IP
read -p "Do you have a custom domain? (y/n): " HAS_DOMAIN
if [ "$HAS_DOMAIN" = "y" ] || [ "$HAS_DOMAIN" = "Y" ]; then
    read -p "Enter your domain (e.g., example.com): " DOMAIN
    FRONTEND_URL="https://$DOMAIN"
    BACKEND_URL="https://$DOMAIN/api"
    USE_SSL=true
else
    DOMAIN=$EC2_PUBLIC_IP
    FRONTEND_URL="http://$EC2_PUBLIC_IP"
    BACKEND_URL="http://$EC2_PUBLIC_IP/api"
    USE_SSL=false
fi

echo ""
echo -e "${GREEN}Step 2: Installing System Dependencies${NC}"
echo "=========================================="

# Update system
echo "Updating system packages..."
apt-get update -y
apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
apt-get install -y \
    curl \
    wget \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    software-properties-common

echo -e "${GREEN}✓ System dependencies installed${NC}"
echo ""

echo -e "${GREEN}Step 3: Installing Docker${NC}"
echo "=========================================="

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo "Docker is already installed"
else
    echo "Installing Docker..."

    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh

    # Add user to docker group
    usermod -aG docker $ACTUAL_USER

    echo -e "${GREEN}✓ Docker installed${NC}"
fi

# Start Docker service
systemctl start docker
systemctl enable docker

echo ""
echo -e "${GREEN}Step 4: Installing Docker Compose${NC}"
echo "=========================================="

# Check if Docker Compose is already installed
if command -v docker-compose &> /dev/null; then
    echo "Docker Compose is already installed"
else
    echo "Installing Docker Compose..."

    # Install Docker Compose
    DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')
    curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

    echo -e "${GREEN}✓ Docker Compose installed${NC}"
fi

echo ""
echo -e "${GREEN}Step 5: Creating Environment Configuration${NC}"
echo "=========================================="

# Generate Django secret key using Python's secrets module (no Django required)
DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print("".join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)") for i in range(50)))')

# Create .env file
cat > "$PROJECT_DIR/.env" << EOF
# Django Backend Configuration
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,$EC2_PUBLIC_IP,localhost,127.0.0.1,backend

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=/app/db.sqlite3

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$EC2_PUBLIC_IP

# API URLs
VITE_API_URL=$BACKEND_URL
PUBLIC_API_URL=$BACKEND_URL

# Astro Configuration
PUBLIC_SITE_URL=$FRONTEND_URL
EOF

echo -e "${GREEN}✓ .env file created${NC}"
echo ""

echo -e "${GREEN}Step 6: Updating Application Configuration${NC}"
echo "=========================================="

# Update Django settings for production
SETTINGS_FILE="$PROJECT_DIR/portfolio-backend/portfolio_backend/settings.py"

if [ -f "$SETTINGS_FILE" ]; then
    # Backup original settings
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"

    # Update ALLOWED_HOSTS
    sed -i "s/ALLOWED_HOSTS = \[.*\]/ALLOWED_HOSTS = ['$DOMAIN', '$EC2_PUBLIC_IP', 'localhost', '127.0.0.1', 'backend']/" "$SETTINGS_FILE"

    # Update CORS settings
    if ! grep -q "CORS_ALLOWED_ORIGINS" "$SETTINGS_FILE"; then
        cat >> "$SETTINGS_FILE" << 'EOF'

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "http://$DOMAIN",
    "https://$DOMAIN",
    "http://$EC2_PUBLIC_IP",
]
CORS_ALLOW_CREDENTIALS = True
EOF
    fi

    echo -e "${GREEN}✓ Django settings updated${NC}"
fi

# Update Astro config
ASTRO_CONFIG="$PROJECT_DIR/portfolio-frontend/astro.config.mjs"
if [ -f "$ASTRO_CONFIG" ]; then
    # Backup original config
    cp "$ASTRO_CONFIG" "$ASTRO_CONFIG.backup"
    echo -e "${GREEN}✓ Astro config backed up${NC}"
fi

echo ""
echo -e "${GREEN}Step 7: Configuring Nginx${NC}"
echo "=========================================="

# Create Nginx configuration
cat > /etc/nginx/sites-available/portfolio << EOF
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:4321;
}

server {
    listen 80;
    server_name $DOMAIN $EC2_PUBLIC_IP;

    client_max_body_size 100M;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://backend/admin/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Django Static Files
    location /static/ {
        proxy_pass http://backend/static/;
        proxy_set_header Host \$host;
    }

    # Django Media Files
    location /media/ {
        proxy_pass http://backend/media/;
        proxy_set_header Host \$host;
    }
}
EOF

# Enable the site
ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Reload Nginx
systemctl reload nginx
systemctl enable nginx

echo -e "${GREEN}✓ Nginx configured and running${NC}"
echo ""

echo -e "${GREEN}Step 8: Setting up SSL (if using domain)${NC}"
echo "=========================================="

if [ "$USE_SSL" = true ]; then
    read -p "Setup SSL with Let's Encrypt? (y/n): " SETUP_SSL
    if [ "$SETUP_SSL" = "y" ] || [ "$SETUP_SSL" = "Y" ]; then
        read -p "Enter your email for SSL certificate: " SSL_EMAIL

        certbot --nginx -d $DOMAIN --non-interactive --agree-tos -m $SSL_EMAIL

        echo -e "${GREEN}✓ SSL certificate installed${NC}"
    fi
fi

echo ""
echo -e "${GREEN}Step 9: Building and Starting Docker Containers${NC}"
echo "=========================================="

cd "$PROJECT_DIR"

# Stop any running containers
docker-compose down 2>/dev/null || true

# Build and start containers
echo "Building Docker images..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up -d

# Wait for containers to be ready
echo "Waiting for containers to be ready..."
sleep 10

# Run Django migrations
echo "Running database migrations..."
docker-compose exec -T backend python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo -e "${GREEN}✓ Docker containers are running${NC}"
echo ""

echo -e "${GREEN}Step 10: Creating Superuser${NC}"
echo "=========================================="

read -p "Create Django superuser now? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ] || [ "$CREATE_SUPERUSER" = "Y" ]; then
    docker-compose exec backend python manage.py createsuperuser
fi

echo ""
echo -e "${GREEN}Step 11: Setting up Auto-restart on Reboot${NC}"
echo "=========================================="

# Create systemd service for auto-restart
cat > /etc/systemd/system/portfolio.service << EOF
[Unit]
Description=Portfolio Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable portfolio.service

echo -e "${GREEN}✓ Auto-restart on reboot configured${NC}"
echo ""

echo "=================================="
echo -e "${GREEN}✓ DEPLOYMENT COMPLETE!${NC}"
echo "=================================="
echo ""
echo "Your application is now running!"
echo ""
echo -e "${YELLOW}Access URLs:${NC}"
echo "  Frontend: $FRONTEND_URL"
echo "  Backend API: $BACKEND_URL"
echo "  Admin Panel: $BACKEND_URL/../admin/"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  View logs:           docker-compose logs -f"
echo "  Restart containers:  docker-compose restart"
echo "  Stop containers:     docker-compose down"
echo "  Start containers:    docker-compose up -d"
echo "  View status:         docker-compose ps"
echo ""
echo -e "${YELLOW}Important:${NC}"
echo "  1. Make sure EC2 Security Group allows:"
echo "     - Port 80 (HTTP)"
echo "     - Port 443 (HTTPS)"
echo "  2. Database is stored in: portfolio-backend/db.sqlite3"
echo "  3. Backups recommended before updates"
echo ""
echo -e "${GREEN}Enjoy your deployed portfolio!${NC}"
