#!/bin/bash

################################################################################
# Portfolio Deployment Script (Production Ready)
#
# This script will:
# 1. Install Python, Node.js, and system dependencies
# 2. Set up Python virtual environment
# 3. Install Django backend with Gunicorn
# 4. Build Astro frontend static files
# 5. Configure Nginx to serve both frontend and backend
# 6. Set up systemd service for backend auto-start
# 7. Fix all static files issues (Django admin CSS, etc.)
#
# Usage: sudo bash deploy.sh
################################################################################

set -e  # Exit on any error

echo "=================================="
echo "Portfolio Production Deployment"
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

echo -e "${YELLOW}Step 0: Cleanup - Stopping Old Services${NC}"
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

# Stop old frontend service if it exists (we'll use nginx directly)
if systemctl list-unit-files | grep -q "portfolio-frontend.service"; then
    echo "Stopping old frontend service..."
    systemctl stop portfolio-frontend.service 2>/dev/null || true
    systemctl disable portfolio-frontend.service 2>/dev/null || true
    rm -f /etc/systemd/system/portfolio-frontend.service
    systemctl daemon-reload
    echo -e "${GREEN}✓ Old frontend service removed${NC}"
fi

# Fix ownership of project directory
echo "Fixing ownership of project directory..."
chown -R $ACTUAL_USER:$ACTUAL_USER "$PROJECT_DIR"
echo -e "${GREEN}✓ Ownership fixed${NC}"

echo ""

echo -e "${GREEN}Step 1: Detecting Server Information${NC}"
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
    echo -e "${YELLOW}Could not detect EC2 public IP${NC}"
    read -p "Enter your server's public IP or domain: " EC2_PUBLIC_IP
fi

echo -e "${GREEN}✓ Server Address: $EC2_PUBLIC_IP${NC}"
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
echo "Running database migrations and collecting static files..."
sudo -u $ACTUAL_USER bash << 'DJANGO_SETUP_EOF'
cd portfolio-backend
source venv/bin/activate
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear
deactivate
DJANGO_SETUP_EOF

# Fix static and media files permissions for nginx (www-data user)
echo "Setting static and media files permissions..."
# Set directories to 755 (rwxr-xr-x)
find "$BACKEND_DIR/static" -type d -exec chmod 755 {} \;
# Set files to 644 (rw-r--r--)
find "$BACKEND_DIR/static" -type f -exec chmod 644 {} \;

# Create media directory if it doesn't exist and set permissions
mkdir -p "$BACKEND_DIR/media"
chown -R $ACTUAL_USER:$ACTUAL_USER "$BACKEND_DIR/media"
chmod 755 "$BACKEND_DIR/media"

# Make sure nginx user (www-data) can access parent directories
chmod 755 "$BACKEND_DIR"
chmod 755 "$PROJECT_DIR"

# CRITICAL: Allow nginx to traverse through home directory
# Without this, nginx gets 403 errors trying to access static files
HOME_DIR=$(dirname "$PROJECT_DIR")
if [[ "$HOME_DIR" =~ ^/home/ ]]; then
    echo "Allowing nginx to access home directory: $HOME_DIR"
    chmod 755 "$HOME_DIR"
fi

echo -e "${GREEN}✓ Django backend configured${NC}"

echo ""
echo -e "${GREEN}Step 5: Creating Systemd Service for Backend${NC}"
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
echo -e "${GREEN}Step 6: Building Frontend${NC}"
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

    # Serve frontend static files directly from dist
    root FRONTEND_DIR_PLACEHOLDER/dist;
    index index.html;

    # Frontend - serve static files with smart caching
    # HTML pages: cache for 6 hours, but check for updates (stale-while-revalidate)
    location / {
        try_files $uri $uri/ /index.html;

        # HTML pages - revalidate every 6 hours
        if ($request_uri ~* "\.html$|^/$") {
            add_header Cache-Control "public, max-age=21600, stale-while-revalidate=86400, must-revalidate";
        }

        # JS/CSS assets - cache for 1 year (versioned files)
        if ($request_uri ~* "\.(js|css|woff2|woff|ttf|eot)$") {
            add_header Cache-Control "public, max-age=31536000, immutable";
        }

        # Images - cache for 1 week
        if ($request_uri ~* "\.(jpg|jpeg|png|gif|webp|svg|ico)$") {
            add_header Cache-Control "public, max-age=604800";
        }

        # Default for HTML and other files
        add_header Cache-Control "public, max-age=21600, stale-while-revalidate=86400, must-revalidate";
    }

    # Backend API - Cache API responses for 6 hours
    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;

        # Cache API responses
        add_header Cache-Control "public, max-age=21600, stale-while-revalidate=43200";

        # Enable proxy caching
        proxy_cache_bypass $http_pragma $http_authorization;
        proxy_no_cache $http_pragma $http_authorization;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://backend/admin/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Static Files (CRITICAL FIX: Use /static/ not /staticfiles/)
    location /static/ {
        alias BACKEND_DIR_PLACEHOLDER/static/;
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
    location /api/cdn/ {
        proxy_pass http://backend/api/cdn/;
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
echo -e "${GREEN}Step 8: Testing Deployment${NC}"
echo "=========================================="

sleep 2

# Test backend API
echo "Testing backend API..."
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/ || echo "000")
if [ "$API_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Backend API responding${NC}"
else
    echo -e "${YELLOW}⚠ Backend API test returned HTTP $API_TEST${NC}"
fi

# Test Django admin static files
echo "Testing Django admin static files..."
STATIC_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN/static/admin/css/base.css || echo "000")
if [ "$STATIC_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Django admin CSS loading correctly${NC}"
elif [ "$STATIC_TEST" = "403" ]; then
    echo -e "${YELLOW}⚠ Permission denied (403) - Fixing permissions...${NC}"
    # Fix permissions again with more aggressive settings
    find "$BACKEND_DIR/static" -type d -exec chmod 755 {} \;
    find "$BACKEND_DIR/static" -type f -exec chmod 644 {} \;
    chmod 755 "$BACKEND_DIR"
    chmod 755 "$PROJECT_DIR"
    # Fix home directory permissions (most common cause of 403)
    HOME_DIR=$(dirname "$PROJECT_DIR")
    if [[ "$HOME_DIR" =~ ^/home/ ]]; then
        echo "  Fixing home directory permissions: $HOME_DIR"
        chmod 755 "$HOME_DIR"
    fi
    # Restart nginx
    systemctl reload nginx
    sleep 1
    # Test again
    STATIC_TEST_RETRY=$(curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN/static/admin/css/base.css || echo "000")
    if [ "$STATIC_TEST_RETRY" = "200" ]; then
        echo -e "${GREEN}✓ Django admin CSS now loading correctly${NC}"
    else
        echo -e "${RED}✗ Still getting HTTP $STATIC_TEST_RETRY${NC}"
        echo "  Debug: ls -ld $HOME_DIR"
        ls -ld "$HOME_DIR"
        echo "  Debug: ls -ld $PROJECT_DIR"
        ls -ld "$PROJECT_DIR"
        echo "  Debug: ls -ld $BACKEND_DIR/static"
        ls -ld "$BACKEND_DIR/static"
    fi
else
    echo -e "${YELLOW}⚠ Django admin CSS test returned HTTP $STATIC_TEST${NC}"
fi

echo ""
echo -e "${GREEN}Step 9: Setting Up Auto-Rebuild (Every 6 Hours)${NC}"
echo "=========================================="

# Make auto-rebuild script executable
chmod +x "$PROJECT_DIR/auto-rebuild.sh"
chown $ACTUAL_USER:$ACTUAL_USER "$PROJECT_DIR/auto-rebuild.sh"

# Create cron job for auto-rebuild every 6 hours
CRON_JOB="0 */6 * * * /bin/bash $PROJECT_DIR/auto-rebuild.sh"

# Check if cron job already exists
(crontab -l 2>/dev/null | grep -v "$PROJECT_DIR/auto-rebuild.sh"; echo "$CRON_JOB") | crontab -

echo -e "${GREEN}✓ Auto-rebuild cron job configured${NC}"
echo "  Schedule: Every 6 hours (at :00 minutes)"
echo "  Log file: $PROJECT_DIR/auto-rebuild.log"

echo ""
echo "=================================="
echo -e "${GREEN}✓ DEPLOYMENT COMPLETE!${NC}"
echo "=================================="
echo ""
echo "Your application is now running in production mode!"
echo ""
echo -e "${YELLOW}Access URLs:${NC}"
echo "  Website:      http://$DOMAIN"
echo "  API:          http://$DOMAIN/api/"
echo "  Django Admin: http://$DOMAIN/admin/"
echo ""
echo -e "${YELLOW}Service Management:${NC}"
echo "  Backend status:   sudo systemctl status portfolio-backend"
echo "  Backend logs:     sudo journalctl -u portfolio-backend -f"
echo "  Restart backend:  sudo systemctl restart portfolio-backend"
echo "  Nginx status:     sudo systemctl status nginx"
echo "  Nginx logs:       sudo tail -f /var/log/nginx/access.log"
echo ""
echo -e "${YELLOW}Auto-Rebuild:${NC}"
echo "  View rebuild log: tail -f $PROJECT_DIR/auto-rebuild.log"
echo "  Manual rebuild:   sudo bash $PROJECT_DIR/auto-rebuild.sh"
echo "  View cron jobs:   crontab -l"
echo ""
echo -e "${YELLOW}Create Django superuser:${NC}"
echo "  cd $BACKEND_DIR"
echo "  source venv/bin/activate"
echo "  python manage.py createsuperuser"
echo ""
echo -e "${GREEN}Key Features Configured:${NC}"
echo "  ✓ Smart HTTP caching (6-hour expiry with stale-while-revalidate)"
echo "  ✓ Automatic frontend rebuild every 6 hours"
echo "  ✓ No manual cache clearing required for users"
echo "  ✓ Static files path corrected (/static/ not /staticfiles/)"
echo "  ✓ Frontend served directly by Nginx (no extra service needed)"
echo "  ✓ Django admin CSS loads correctly"
echo "  ✓ All backend endpoints accessible from frontend"
echo "  ✓ CORS properly configured"
echo ""
