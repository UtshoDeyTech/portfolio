#!/bin/bash

set -e

echo "=================================="
echo "Fix Portfolio Deployment Issues"
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
echo "Step 1: Detecting Current Configuration"
echo "=========================================="

# Try to get EC2 metadata
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s --connect-timeout 2 || echo "")

if [ -n "$TOKEN" ]; then
    PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
else
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
fi

# Try to detect domain from current nginx config
if [ -f /etc/nginx/sites-available/portfolio ]; then
    DETECTED_DOMAIN=$(grep "server_name" /etc/nginx/sites-available/portfolio | head -1 | awk '{print $2}' | sed 's/;//')
    echo -e "${GREEN}Detected domain from nginx: $DETECTED_DOMAIN${NC}"
    echo "Current IP: $PUBLIC_IP"
    echo ""
    read -p "Use detected domain '$DETECTED_DOMAIN'? (y/n): " use_detected
    if [ "$use_detected" = "y" ] || [ "$use_detected" = "Y" ]; then
        DOMAIN="$DETECTED_DOMAIN"
    else
        read -p "Enter your domain or IP address: " DOMAIN
    fi
else
    read -p "Enter your domain or IP address (e.g., example.com or $PUBLIC_IP): " DOMAIN
fi

# Check if using HTTPS
if [ -d /etc/letsencrypt/live/$DOMAIN ]; then
    USE_HTTPS=true
    PROTOCOL="https"
    echo -e "${GREEN}SSL certificate detected - will use HTTPS${NC}"
else
    USE_HTTPS=false
    PROTOCOL="http"
    echo -e "${YELLOW}No SSL certificate detected - will use HTTP${NC}"
fi

echo ""
echo "Step 2: Updating Backend Configuration"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-backend"

if [ -f ".env" ]; then
    echo "Backing up existing .env file..."
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
fi

# Update CORS settings in .env
if grep -q "CORS_ALLOWED_ORIGINS" .env 2>/dev/null; then
    echo "Updating CORS_ALLOWED_ORIGINS..."
    if [ "$USE_HTTPS" = true ]; then
        sed -i "s|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321|" .env
    else
        sed -i "s|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=http://$DOMAIN,http://$PUBLIC_IP,http://localhost:4321|" .env
    fi
else
    echo "Adding CORS_ALLOWED_ORIGINS..."
    if [ "$USE_HTTPS" = true ]; then
        echo "CORS_ALLOWED_ORIGINS=http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321" >> .env
    else
        echo "CORS_ALLOWED_ORIGINS=http://$DOMAIN,http://$PUBLIC_IP,http://localhost:4321" >> .env
    fi
fi

# Update ALLOWED_HOSTS in .env
if grep -q "ALLOWED_HOSTS" .env 2>/dev/null; then
    echo "Updating ALLOWED_HOSTS..."
    sed -i "s|ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1|" .env
else
    echo "Adding ALLOWED_HOSTS..."
    echo "ALLOWED_HOSTS=$DOMAIN,$PUBLIC_IP,localhost,127.0.0.1" >> .env
fi

echo -e "${GREEN}✓ Backend configuration updated${NC}"

# Restart backend service
echo "Restarting backend service..."
sudo systemctl restart portfolio-backend

echo ""
echo "Step 3: Rebuilding Frontend"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-frontend"

# Create .env file for frontend build with correct API URL
echo "Creating frontend .env file with API URL: $PROTOCOL://$DOMAIN"
cat > .env << EOF
PUBLIC_API_URL=$PROTOCOL://$DOMAIN
EOF

echo "Rebuilding frontend..."
npm run build

# Clean up .env file
rm -f .env

echo -e "${GREEN}✓ Frontend rebuilt${NC}"

# Restart frontend service
echo "Restarting frontend service..."
sudo systemctl restart portfolio-frontend

echo ""
echo "Step 4: Verifying Services"
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

echo ""
echo "=================================="
echo -e "${GREEN}Fix Complete!${NC}"
echo "=================================="
echo ""
echo "Your portfolio should now be accessible at:"
echo "  $PROTOCOL://$DOMAIN"
echo ""
echo "Test the API directly:"
echo "  curl $PROTOCOL://$DOMAIN/api/blog-settings/"
echo ""
echo "If you still have issues, check the logs:"
echo "  Backend:  sudo journalctl -u portfolio-backend -f"
echo "  Frontend: sudo journalctl -u portfolio-frontend -f"
echo "  Nginx:    sudo tail -f /var/log/nginx/error.log"
echo ""
