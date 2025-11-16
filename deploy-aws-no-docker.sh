#!/bin/bash

################################################################################
# AWS EC2 Deployment Script (NO DOCKER) for Portfolio Project
#
# This script will:
# 1. Stop Docker containers if running
# 2. Install Python, Node.js, and system dependencies
# 3. Set up Python virtual environment
# 4. Install Django backend with Gunicorn
# 5. Build Astro frontend static files
# 6. Configure Nginx to serve both
# 7. Set up systemd services for auto-start
#
# Usage: sudo bash deploy-aws-no-docker.sh
################################################################################

set -e  # Exit on any error

echo "=================================="
echo "Portfolio AWS EC2 Deployment (No Docker)"
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
BACKEND_DIR="$PROJECT_DIR/portfolio-backend"
FRONTEND_DIR="$PROJECT_DIR/portfolio-frontend"

echo -e "${YELLOW}Step 0: Cleanup - Stopping Docker Containers${NC}"
echo "=========================================="

# Stop Docker containers if running (ignore errors)
if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo "Stopping any running Docker containers..."
    cd "$PROJECT_DIR"
    docker-compose down 2>/dev/null || true
    docker stop $(docker ps -aq) 2>/dev/null || true
    echo -e "${GREEN}✓ Docker containers stopped${NC}"
else
    echo "Docker not found, skipping..."
fi

# Fix ownership of project directory
echo "Fixing ownership of project directory..."
chown -R $ACTUAL_USER:$ACTUAL_USER "$PROJECT_DIR"
echo -e "${GREEN}✓ Ownership fixed${NC}"

echo ""

echo -e "${GREEN}Step 1: Detecting EC2 Instance Information${NC}"
echo "=========================================="

# Detect EC2 public IP - Try IMDSv2 first
echo "Attempting to detect EC2 metadata..."
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" --max-time 2 2>/dev/null || echo "")
if [ -n "$TOKEN" ]; then
    echo "Using IMDSv2 (token-based) for metadata..."
    EC2_PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4 --max-time 2 2>/dev/null || echo "")
else
    echo "Trying IMDSv1 (legacy) for metadata..."
    EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --max-time 2 2>/dev/null || echo "")
fi

if [ -z "$EC2_PUBLIC_IP" ]; then
    echo -e "${RED}Error: Could not detect EC2 public IP. Are you running on EC2?${NC}"
    read -p "Enter your server's public IP manually: " EC2_PUBLIC_IP
fi

echo -e "${GREEN}✓ Detected Public IP: $EC2_PUBLIC_IP${NC}"
DOMAIN=$EC2_PUBLIC_IP

echo ""
echo -e "${GREEN}Step 2: Installing System Dependencies${NC}"
echo "=========================================="

apt-get update -y
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    curl \
    wget \
    git

# Install Node.js 20
if ! command -v node &> /dev/null; then
    echo "Installing Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

echo -e "${GREEN}✓ System dependencies installed${NC}"

echo ""
echo -e "${GREEN}Step 3: Setting Up Python Virtual Environment${NC}"
echo "=========================================="

# Create virtual environment as actual user
cd "$BACKEND_DIR"
sudo -u $ACTUAL_USER python3 -m venv venv

# Install Python dependencies as actual user
echo "Installing Python packages..."
sudo -u $ACTUAL_USER bash << 'BACKEND_EOF'
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
deactivate
BACKEND_EOF

echo -e "${GREEN}✓ Python environment ready${NC}"

echo ""
echo -e "${GREEN}Step 4: Configuring Django Backend${NC}"
echo "=========================================="

# Generate Django secret key
DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print("".join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)") for i in range(50)))')

# Create .env file
cat > "$BACKEND_DIR/.env" << EOF
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=$DOMAIN,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN
EOF

# Fix ownership of .env
chown $ACTUAL_USER:$ACTUAL_USER "$BACKEND_DIR/.env"

# Run Django setup as actual user
echo "Running database migrations..."
sudo -u $ACTUAL_USER bash << 'DJANGO_SETUP_EOF'
cd portfolio-backend
source venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
deactivate
DJANGO_SETUP_EOF

echo -e "${GREEN}✓ Django backend configured${NC}"

echo ""
echo -e "${GREEN}Step 5: Building Frontend${NC}"
echo "=========================================="

# Build frontend as actual user
echo "Installing Node.js dependencies and building..."
sudo -u $ACTUAL_USER bash << FRONTEND_EOF
cd "$FRONTEND_DIR"

# Set build-time environment variables
export PUBLIC_API_URL="http://$DOMAIN"
export SERVER_API_URL="http://127.0.0.1:8000"

# Install dependencies and build
npm ci
npm run build
FRONTEND_EOF

echo -e "${GREEN}✓ Frontend built successfully${NC}"

echo ""
echo -e "${GREEN}Step 6: Creating Systemd Service for Backend${NC}"
echo "=========================================="

# Create systemd service for Gunicorn
cat > /etc/systemd/system/portfolio-backend.service << EOF
[Unit]
Description=Portfolio Django Backend (Gunicorn)
After=network.target

[Service]
Type=notify
User=$ACTUAL_USER
Group=$ACTUAL_USER
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
EnvironmentFile=$BACKEND_DIR/.env
ExecStart=$BACKEND_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind 127.0.0.1:8000 \\
    --timeout 120 \\
    --access-logfile - \\
    --error-logfile - \\
    portfolio_backend.wsgi:application

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Stop service if already running
systemctl stop portfolio-backend.service 2>/dev/null || true

# Enable and start the service
systemctl daemon-reload
systemctl enable portfolio-backend.service
systemctl start portfolio-backend.service

# Wait for service to start
sleep 3

# Check if service started successfully
if systemctl is-active --quiet portfolio-backend.service; then
    echo -e "${GREEN}✓ Backend service created and started${NC}"
else
    echo -e "${RED}✗ Backend service failed to start${NC}"
    echo "Checking logs..."
    journalctl -u portfolio-backend -n 20 --no-pager
    exit 1
fi

echo ""
echo -e "${GREEN}Step 7: Configuring Nginx${NC}"
echo "=========================================="

# Create Nginx configuration
cat > /etc/nginx/sites-available/portfolio << 'NGINX_EOF'
upstream backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name SERVER_NAME_PLACEHOLDER;

    client_max_body_size 100M;

    # Serve frontend static files
    root FRONTEND_DIR_PLACEHOLDER/dist;
    index index.html;

    # Frontend - serve static files directly
    location / {
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "public, max-age=3600";
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://backend/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Static Files
    location /static/ {
        alias BACKEND_DIR_PLACEHOLDER/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Django Media Files
    location /media/ {
        alias BACKEND_DIR_PLACEHOLDER/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    # CDN endpoint
    location /cdn/ {
        proxy_pass http://backend/cdn/;
        proxy_set_header Host $host;
    }
}
NGINX_EOF

# Replace placeholders
sed -i "s|SERVER_NAME_PLACEHOLDER|$DOMAIN|g" /etc/nginx/sites-available/portfolio
sed -i "s|FRONTEND_DIR_PLACEHOLDER|$FRONTEND_DIR|g" /etc/nginx/sites-available/portfolio
sed -i "s|BACKEND_DIR_PLACEHOLDER|$BACKEND_DIR|g" /etc/nginx/sites-available/portfolio

# Enable the site
ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx
systemctl enable nginx

echo -e "${GREEN}✓ Nginx configured and running${NC}"

echo ""
echo "=================================="
echo -e "${GREEN}✓ DEPLOYMENT COMPLETE!${NC}"
echo "=================================="
echo ""
echo "Your application is now running WITHOUT Docker!"
echo ""
echo -e "${YELLOW}Access URLs:${NC}"
echo "  Website: http://$DOMAIN"
echo "  API: http://$DOMAIN/api"
echo "  Admin: http://$DOMAIN/admin"
echo ""
echo -e "${YELLOW}Service Management:${NC}"
echo "  Backend status:   sudo systemctl status portfolio-backend"
echo "  Backend logs:     sudo journalctl -u portfolio-backend -f"
echo "  Restart backend:  sudo systemctl restart portfolio-backend"
echo "  Nginx status:     sudo systemctl status nginx"
echo "  Nginx logs:       sudo tail -f /var/log/nginx/access.log"
echo ""
echo -e "${YELLOW}Create Django superuser:${NC}"
echo "  cd $BACKEND_DIR"
echo "  source venv/bin/activate"
echo "  python manage.py createsuperuser"
echo ""
echo -e "${GREEN}Performance: Running natively is faster than Docker!${NC}"
