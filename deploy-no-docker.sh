#!/bin/bash

set -e

echo "=================================="
echo "Portfolio Direct Deployment (No Docker)"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "Step 0: Removing Docker (if installed)"
echo "=========================================="

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "Docker found. Removing completely..."

    # Stop and remove all containers
    sudo docker-compose down 2>/dev/null || true
    sudo docker stop $(sudo docker ps -aq) 2>/dev/null || true
    sudo docker rm $(sudo docker ps -aq) 2>/dev/null || true

    # Stop Docker service
    sudo systemctl stop docker 2>/dev/null || true
    sudo systemctl disable docker 2>/dev/null || true

    # Remove Docker packages
    sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-buildx-plugin 2>/dev/null || true
    sudo apt-get purge -y docker docker-engine docker.io containerd runc 2>/dev/null || true

    # Remove Docker directories
    sudo rm -rf /var/lib/docker
    sudo rm -rf /var/lib/containerd
    sudo rm -rf /etc/docker
    sudo rm -rf ~/.docker

    # Remove Docker apt repository
    sudo rm -f /etc/apt/sources.list.d/docker.list
    sudo rm -f /etc/apt/keyrings/docker.gpg
    sudo rm -f /usr/share/keyrings/docker-archive-keyring.gpg

    # Clean up
    sudo apt-get autoremove -y
    sudo apt-get autoclean

    echo -e "${GREEN}✓ Docker completely removed${NC}"
else
    echo "Docker not installed, skipping..."
fi

echo ""
echo "Step 1: Detecting EC2 Instance Information"
echo "=========================================="

# Check if this is an existing deployment
IS_UPDATE=false
if systemctl list-unit-files | grep -q "portfolio-backend.service"; then
    IS_UPDATE=true
    echo -e "${YELLOW}Existing deployment detected - running in UPDATE mode${NC}"
fi

# Try to get EC2 metadata using IMDSv2
echo "Attempting to detect EC2 metadata..."
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s --connect-timeout 2 || echo "")

if [ -n "$TOKEN" ]; then
    echo "Using IMDSv2 (token-based) for metadata..."
    PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
    PUBLIC_DNS=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/public-hostname --connect-timeout 2 || echo "")
else
    echo "Could not get EC2 metadata token, trying IMDSv1..."
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
    PUBLIC_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname --connect-timeout 2 || echo "")
fi

if [ -z "$PUBLIC_IP" ]; then
    echo -e "${RED}Could not detect EC2 instance IP. Please run this script on an EC2 instance.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Detected Public IP: $PUBLIC_IP${NC}"
echo -e "${GREEN}✓ Detected Public DNS: $PUBLIC_DNS${NC}"

# Try to detect existing domain from nginx config
if [ "$IS_UPDATE" = true ] && [ -f /etc/nginx/sites-available/portfolio ]; then
    DETECTED_DOMAIN=$(grep "server_name" /etc/nginx/sites-available/portfolio | head -1 | awk '{print $2}' | sed 's/;//')
    echo -e "${GREEN}Detected existing domain: $DETECTED_DOMAIN${NC}"
    echo ""
    read -p "Use detected domain '$DETECTED_DOMAIN'? (y/n): " use_detected
    if [ "$use_detected" = "y" ] || [ "$use_detected" = "Y" ]; then
        DOMAIN="$DETECTED_DOMAIN"
        SERVER_NAME="$DOMAIN"
        # Assume custom domain if it's not an IP address
        if [[ "$DOMAIN" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            use_domain="n"
        else
            use_domain="y"
        fi
    else
        read -p "Do you have a custom domain? (y/n): " use_domain
        if [ "$use_domain" = "y" ] || [ "$use_domain" = "Y" ]; then
            read -p "Enter your domain name (e.g., example.com): " DOMAIN
            SERVER_NAME="$DOMAIN"
        else
            DOMAIN="$PUBLIC_IP"
            SERVER_NAME="$PUBLIC_IP"
        fi
    fi
else
    # Ask about custom domain
    echo ""
    read -p "Do you have a custom domain? (y/n): " use_domain
    if [ "$use_domain" = "y" ] || [ "$use_domain" = "Y" ]; then
        read -p "Enter your domain name (e.g., example.com): " DOMAIN
        SERVER_NAME="$DOMAIN"
    else
        DOMAIN="$PUBLIC_IP"
        SERVER_NAME="$PUBLIC_IP"
    fi
fi

echo ""
echo "Step 2: Installing System Dependencies"
echo "=========================================="

echo "Updating system packages..."
sudo apt-get update -qq

echo "Installing required packages..."
sudo apt-get install -y curl wget git nginx certbot python3-certbot-nginx python3-pip python3-venv software-properties-common

echo -e "${GREEN}✓ System dependencies installed${NC}"

echo ""
echo "Step 3: Installing Node.js"
echo "=========================================="

if ! command -v node &> /dev/null; then
    echo "Installing Node.js 20.x..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "Node.js already installed: $(node --version)"
fi

echo ""
echo "Step 4: Setting up Backend (Django)"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create or update .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321
DATABASE_URL=sqlite:///db.sqlite3
EOF
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo "Updating existing .env file..."
    # Backup existing .env
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

    # Update CORS_ALLOWED_ORIGINS
    if grep -q "CORS_ALLOWED_ORIGINS" .env; then
        sed -i "s|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321|" .env
    else
        echo "CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321" >> .env
    fi

    # Update ALLOWED_HOSTS
    if grep -q "ALLOWED_HOSTS" .env; then
        sed -i "s|ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1|" .env
    else
        echo "ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1" >> .env
    fi

    echo -e "${GREEN}✓ .env file updated${NC}"
fi

# Run migrations
echo "Running Django migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

deactivate

cd "$SCRIPT_DIR"

echo ""
echo "Step 5: Building Frontend (Astro)"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-frontend"

echo "Installing npm dependencies..."
npm install

# Create .env file for frontend build
echo "Creating frontend .env file..."
cat > .env << EOF
PUBLIC_API_URL=http://$DOMAIN
EOF

echo "Building Astro site..."
npm run build

# Clean up .env file after build (optional, for security)
rm -f .env

echo ""
echo "Step 6: Setting up systemd services"
echo "=========================================="

# Create Django service
sudo tee /etc/systemd/system/portfolio-backend.service > /dev/null << EOF
[Unit]
Description=Portfolio Django Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR/portfolio-backend
Environment="PATH=$SCRIPT_DIR/portfolio-backend/venv/bin"
ExecStart=$SCRIPT_DIR/portfolio-backend/venv/bin/gunicorn portfolio_backend.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Install gunicorn if not already installed
cd "$SCRIPT_DIR/portfolio-backend"
source venv/bin/activate
pip install gunicorn
deactivate
cd "$SCRIPT_DIR"

# Create Astro frontend service
sudo tee /etc/systemd/system/portfolio-frontend.service > /dev/null << EOF
[Unit]
Description=Portfolio Astro Frontend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$SCRIPT_DIR/portfolio-frontend
ExecStart=/usr/bin/npx sirv-cli dist --host 127.0.0.1 --port 4321 --single
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Install sirv-cli globally if not already installed
sudo npm install -g sirv-cli

# Reload systemd and start services
sudo systemctl daemon-reload
sudo systemctl enable portfolio-backend
sudo systemctl enable portfolio-frontend
sudo systemctl restart portfolio-backend
sudo systemctl restart portfolio-frontend

echo -e "${GREEN}✓ Systemd services created and started${NC}"

echo ""
echo "Step 7: Configuring Nginx"
echo "=========================================="

sudo tee /etc/nginx/sites-available/portfolio > /dev/null << EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    # Frontend (Astro)
    location / {
        proxy_pass http://127.0.0.1:4321;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Backend API (Django)
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Django admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Django static files
    location /static/ {
        alias $SCRIPT_DIR/portfolio-backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Django media files
    location /media/ {
        alias $SCRIPT_DIR/portfolio-backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

if [ $? -eq 0 ]; then
    sudo systemctl enable nginx
    sudo systemctl restart nginx
    echo -e "${GREEN}✓ Nginx configured and running${NC}"
else
    echo -e "${RED}✗ Nginx configuration error${NC}"
    exit 1
fi

echo ""
echo "Step 8: Setting up SSL (if using domain)"
echo "=========================================="

if [ "$use_domain" = "y" ] || [ "$use_domain" = "Y" ]; then
    read -p "Enter email for SSL certificate: " EMAIL
    sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL"
    echo -e "${GREEN}✓ SSL certificate installed${NC}"

    # Rebuild frontend with HTTPS API URL
    echo ""
    echo "Rebuilding frontend with HTTPS API URL..."
    cd "$SCRIPT_DIR/portfolio-frontend"
    cat > .env << EOF
PUBLIC_API_URL=https://$DOMAIN
EOF
    npm run build
    rm -f .env

    # Restart frontend service to use new build
    sudo systemctl restart portfolio-frontend
    echo -e "${GREEN}✓ Frontend rebuilt with HTTPS${NC}"

    cd "$SCRIPT_DIR"
else
    echo "Skipping SSL setup (no custom domain)"
fi

echo ""
echo "Step 9: Verifying Deployment"
echo "=========================================="

sleep 3

# Check backend status
if systemctl is-active --quiet portfolio-backend; then
    echo -e "${GREEN}✓ Backend service is running${NC}"
else
    echo -e "${RED}✗ Backend service failed to start${NC}"
    echo "Check logs with: sudo journalctl -u portfolio-backend -n 50"
fi

# Check frontend status
if systemctl is-active --quiet portfolio-frontend; then
    echo -e "${GREEN}✓ Frontend service is running${NC}"
else
    echo -e "${RED}✗ Frontend service failed to start${NC}"
    echo "Check logs with: sudo journalctl -u portfolio-frontend -n 50"
fi

# Check nginx status
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is not running${NC}"
fi

# Determine protocol
if [ "$use_domain" = "y" ] || [ "$use_domain" = "Y" ]; then
    if [ -d /etc/letsencrypt/live/$DOMAIN ]; then
        PROTOCOL="https"
    else
        PROTOCOL="http"
    fi
else
    PROTOCOL="http"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Deployment Complete!${NC}"
echo "=================================="
echo ""
echo "Your portfolio is now running at:"
echo "  $PROTOCOL://$DOMAIN"
echo ""
echo "Test the API directly:"
echo "  curl $PROTOCOL://$DOMAIN/api/blog-settings/"
echo ""
echo "Service management:"
echo "  sudo systemctl status portfolio-backend"
echo "  sudo systemctl status portfolio-frontend"
echo "  sudo systemctl restart portfolio-backend"
echo "  sudo systemctl restart portfolio-frontend"
echo ""
echo "View logs:"
echo "  Backend:  sudo journalctl -u portfolio-backend -f"
echo "  Frontend: sudo journalctl -u portfolio-frontend -f"
echo "  Nginx:    sudo tail -f /var/log/nginx/error.log"
echo ""
echo "To update this deployment in the future, simply run this script again."
echo ""
