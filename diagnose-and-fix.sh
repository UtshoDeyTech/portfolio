#!/bin/bash

set -e

echo "=================================="
echo "Portfolio Deployment Diagnostics"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "Step 1: Checking Service Status"
echo "=========================================="

# Check if services exist
if systemctl list-unit-files | grep -q "portfolio-backend.service"; then
    BACKEND_STATUS=$(systemctl is-active portfolio-backend || echo "inactive")
    if [ "$BACKEND_STATUS" = "active" ]; then
        echo -e "${GREEN}✓ Backend service is running${NC}"
    else
        echo -e "${RED}✗ Backend service is NOT running${NC}"
        echo "  Starting backend service..."
        sudo systemctl start portfolio-backend
    fi
else
    echo -e "${RED}✗ Backend service not found${NC}"
    echo "  You need to run deploy-no-docker.sh first"
    exit 1
fi

if systemctl list-unit-files | grep -q "portfolio-frontend.service"; then
    FRONTEND_STATUS=$(systemctl is-active portfolio-frontend || echo "inactive")
    if [ "$FRONTEND_STATUS" = "active" ]; then
        echo -e "${GREEN}✓ Frontend service is running${NC}"
    else
        echo -e "${RED}✗ Frontend service is NOT running${NC}"
        echo "  Starting frontend service..."
        sudo systemctl start portfolio-frontend
    fi
else
    echo -e "${RED}✗ Frontend service not found${NC}"
    exit 1
fi

NGINX_STATUS=$(systemctl is-active nginx || echo "inactive")
if [ "$NGINX_STATUS" = "active" ]; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is NOT running${NC}"
    sudo systemctl start nginx
fi

echo ""
echo "Step 2: Detecting Configuration"
echo "=========================================="

# Auto-detect EC2 public IP
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s --connect-timeout 2 || echo "")
if [ -n "$TOKEN" ]; then
    PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
else
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --connect-timeout 2 || echo "")
fi

if [ -n "$PUBLIC_IP" ]; then
    echo -e "${GREEN}Public IP: $PUBLIC_IP${NC}"
else
    echo -e "${YELLOW}Could not detect public IP${NC}"
    PUBLIC_IP=""
fi

# Detect domain from nginx
if [ -f /etc/nginx/sites-available/portfolio ]; then
    DOMAIN=$(grep "server_name" /etc/nginx/sites-available/portfolio | head -1 | awk '{print $2}' | sed 's/;//')
    echo -e "${GREEN}Domain: $DOMAIN${NC}"
else
    echo -e "${RED}Nginx configuration not found${NC}"
    exit 1
fi

# Check if SSL is enabled
if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    PROTOCOL="https"
    echo -e "${GREEN}SSL: Enabled${NC}"
else
    PROTOCOL="http"
    echo -e "${YELLOW}SSL: Not enabled${NC}"
fi

echo ""
echo "Step 3: Testing Backend API"
echo "=========================================="

# Test backend directly on localhost
echo "Testing backend on localhost:8000..."
BACKEND_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/api/blog-settings/ || echo "000")

if [ "$BACKEND_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Backend API responding on localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend API NOT responding (HTTP $BACKEND_TEST)${NC}"
    echo "  Checking backend logs..."
    sudo journalctl -u portfolio-backend -n 20 --no-pager
    exit 1
fi

# Test backend through nginx
echo "Testing backend through nginx..."
NGINX_TEST=$(curl -s -o /dev/null -w "%{http_code}" $PROTOCOL://$DOMAIN/api/blog-settings/ || echo "000")

if [ "$NGINX_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Backend API accessible through nginx${NC}"
else
    echo -e "${RED}✗ Backend API NOT accessible through nginx (HTTP $NGINX_TEST)${NC}"
    echo "  This is likely a nginx configuration issue"
    echo "  Checking nginx logs..."
    sudo tail -20 /var/log/nginx/error.log
fi

echo ""
echo "Step 4: Testing Frontend"
echo "=========================================="

# Test frontend directly
FRONTEND_TEST=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4321/ || echo "000")

if [ "$FRONTEND_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Frontend responding on localhost:4321${NC}"
else
    echo -e "${RED}✗ Frontend NOT responding (HTTP $FRONTEND_TEST)${NC}"
    echo "  Checking frontend logs..."
    sudo journalctl -u portfolio-frontend -n 20 --no-pager
fi

echo ""
echo "Step 5: Checking Backend Configuration"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-backend"

if [ -f ".env" ]; then
    echo "Backend .env file exists"

    # Check CORS configuration
    if grep -q "CORS_ALLOWED_ORIGINS" .env; then
        CORS_ORIGINS=$(grep "CORS_ALLOWED_ORIGINS" .env | cut -d'=' -f2)
        echo -e "${BLUE}CORS Origins: $CORS_ORIGINS${NC}"

        # Check if current protocol+domain is in CORS
        if echo "$CORS_ORIGINS" | grep -q "$PROTOCOL://$DOMAIN"; then
            echo -e "${GREEN}✓ Current domain is in CORS allowed origins${NC}"
        else
            echo -e "${RED}✗ Current domain NOT in CORS origins${NC}"
            echo -e "${YELLOW}  This will cause frontend-backend communication to fail!${NC}"
        fi
    else
        echo -e "${RED}✗ CORS_ALLOWED_ORIGINS not found in .env${NC}"
    fi

    # Check ALLOWED_HOSTS
    if grep -q "ALLOWED_HOSTS" .env; then
        ALLOWED_HOSTS=$(grep "ALLOWED_HOSTS" .env | cut -d'=' -f2)
        echo -e "${BLUE}Allowed Hosts: $ALLOWED_HOSTS${NC}"
    else
        echo -e "${YELLOW}⚠ ALLOWED_HOSTS not found in .env${NC}"
    fi
else
    echo -e "${RED}✗ Backend .env file NOT found${NC}"
fi

echo ""
echo "Step 6: Checking Django Static Files"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-backend"

if [ -d "static" ]; then
    echo -e "${GREEN}✓ Static files directory exists${NC}"

    # Check if Django admin static files exist
    if [ -d "static/admin" ]; then
        echo -e "${GREEN}✓ Django admin static files found${NC}"
        ADMIN_CSS_COUNT=$(find static/admin/css -name "*.css" 2>/dev/null | wc -l)
        echo "  Found $ADMIN_CSS_COUNT CSS files"
    else
        echo -e "${RED}✗ Django admin static files NOT found${NC}"
        echo -e "${YELLOW}  Need to run: python manage.py collectstatic${NC}"
    fi

    # Check static files permissions
    STATIC_PERMS=$(stat -c %a static 2>/dev/null || echo "000")
    if [ "$STATIC_PERMS" -ge "755" ]; then
        echo -e "${GREEN}✓ Static files have correct permissions${NC}"
    else
        echo -e "${YELLOW}⚠ Static files permissions might be too restrictive: $STATIC_PERMS${NC}"
    fi
else
    echo -e "${RED}✗ Static files directory NOT found${NC}"
    echo "  Need to run: python manage.py collectstatic"
fi

# Check nginx static files configuration
echo ""
echo "Checking nginx static files configuration..."
if grep -q "location /static/" /etc/nginx/sites-available/portfolio; then
    STATIC_ALIAS=$(grep -A 1 "location /static/" /etc/nginx/sites-available/portfolio | grep "alias" | awk '{print $2}' | sed 's/;//')
    echo -e "${BLUE}Nginx static alias: $STATIC_ALIAS${NC}"

    # Check if the path exists
    if [ -d "${STATIC_ALIAS}" ]; then
        echo -e "${GREEN}✓ Nginx static path exists${NC}"
    else
        echo -e "${RED}✗ Nginx static path does NOT exist: $STATIC_ALIAS${NC}"
        echo -e "${YELLOW}  Nginx configuration needs to be updated${NC}"
    fi
else
    echo -e "${RED}✗ Nginx static location NOT configured${NC}"
fi

echo ""
echo "Step 7: Checking Frontend Build"
echo "=========================================="

cd "$SCRIPT_DIR/portfolio-frontend"

if [ -d "dist" ]; then
    echo -e "${GREEN}✓ Frontend dist folder exists${NC}"

    # Check if there are any API references in built files
    echo "Searching for API configuration in built files..."
    if grep -r "PUBLIC_API_URL" dist/ 2>/dev/null | head -5; then
        echo -e "${GREEN}✓ Found API URL configuration in build${NC}"
    else
        echo -e "${YELLOW}⚠ PUBLIC_API_URL not found in build (using runtime detection)${NC}"
    fi
else
    echo -e "${RED}✗ Frontend dist folder NOT found${NC}"
    echo "  Frontend needs to be built"
fi

echo ""
echo "=========================================="
echo "DIAGNOSIS SUMMARY"
echo "=========================================="

# Provide recommendations
cd "$SCRIPT_DIR"

echo ""
echo "Common Issues and Fixes:"
echo ""
echo "1. If backend API is NOT accessible through nginx:"
echo "   - Check nginx config: sudo nginx -t"
echo "   - Restart nginx: sudo systemctl restart nginx"
echo ""
echo "2. If CORS origins are incorrect:"
echo "   - Run: ./deploy-no-docker.sh"
echo "   - This will update CORS configuration"
echo ""
echo "3. If frontend can't fetch backend data:"
echo "   - Rebuild frontend with: cd portfolio-frontend && npm run build"
echo "   - Restart frontend: sudo systemctl restart portfolio-frontend"
echo ""
echo "4. Quick fix (updates everything):"
echo "   - Run: ./deploy-no-docker.sh"
echo ""

echo ""
echo "=========================================="
echo "APPLYING AUTOMATIC FIXES"
echo "=========================================="
echo ""
echo "The script will now automatically:"
echo "  1. Update backend configuration (CORS, ALLOWED_HOSTS)"
echo "  2. Collect Django static files"
echo "  3. Rebuild frontend with correct API URL"
echo "  4. Restart all services"
echo ""

# Update backend .env
cd "$SCRIPT_DIR/portfolio-backend"

if [ -f ".env" ]; then
    echo "Updating backend .env..."
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

    # Build CORS and ALLOWED_HOSTS with auto-detected IPs
    CORS_LIST="http://$DOMAIN,https://$DOMAIN,http://localhost:4321"
    HOSTS_LIST="$DOMAIN,localhost,127.0.0.1"

    if [ -n "$PUBLIC_IP" ] && [ "$PUBLIC_IP" != "$DOMAIN" ]; then
        CORS_LIST="$CORS_LIST,http://$PUBLIC_IP,https://$PUBLIC_IP"
        HOSTS_LIST="$HOSTS_LIST,$PUBLIC_IP"
    fi

    # Update CORS
    if grep -q "CORS_ALLOWED_ORIGINS" .env; then
        sed -i "s|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=$CORS_LIST|" .env
    else
        echo "CORS_ALLOWED_ORIGINS=$CORS_LIST" >> .env
    fi

    # Update ALLOWED_HOSTS
    if grep -q "ALLOWED_HOSTS" .env; then
        sed -i "s|ALLOWED_HOSTS=.*|ALLOWED_HOSTS=$HOSTS_LIST|" .env
    else
        echo "ALLOWED_HOSTS=$HOSTS_LIST" >> .env
    fi

    echo -e "${GREEN}✓ Backend .env updated with auto-detected IPs${NC}"
    echo "  CORS: $CORS_LIST"
    echo "  Hosts: $HOSTS_LIST"
fi

# Collect static files
echo ""
echo "Collecting static files..."
source venv/bin/activate
python manage.py collectstatic --noinput
deactivate

# Fix permissions
chmod -R 755 static
echo -e "${GREEN}✓ Static files collected${NC}"

# Restart backend
echo ""
echo "Restarting backend service..."
sudo systemctl restart portfolio-backend
echo -e "${GREEN}✓ Backend restarted${NC}"

# Rebuild frontend
cd "$SCRIPT_DIR/portfolio-frontend"
echo ""
echo "Rebuilding frontend with API URL: $PROTOCOL://$DOMAIN"

cat > .env << EOF
PUBLIC_API_URL=$PROTOCOL://$DOMAIN
EOF

npm run build
rm -f .env

echo -e "${GREEN}✓ Frontend rebuilt${NC}"

# Restart frontend
echo ""
echo "Restarting frontend service..."
sudo systemctl restart portfolio-frontend
echo -e "${GREEN}✓ Frontend restarted${NC}"

echo ""
echo "Waiting for services to start..."
sleep 3

# Test again
echo ""
echo "Testing API..."
API_TEST=$(curl -s -o /dev/null -w "%{http_code}" $PROTOCOL://$DOMAIN/api/blog-settings/ || echo "000")

if [ "$API_TEST" = "200" ]; then
    echo -e "${GREEN}✓ API is working!${NC}"
else
    echo -e "${RED}✗ API still not responding (HTTP $API_TEST)${NC}"
    echo "Check logs: sudo journalctl -u portfolio-backend -n 50"
fi

# Test static files
echo ""
echo "Testing Django admin static files..."
ADMIN_CSS_TEST=$(curl -s -o /dev/null -w "%{http_code}" $PROTOCOL://$DOMAIN/static/admin/css/base.css || echo "000")

if [ "$ADMIN_CSS_TEST" = "200" ]; then
    echo -e "${GREEN}✓ Django admin static files are loading!${NC}"
else
    echo -e "${RED}✗ Django admin static files not loading (HTTP $ADMIN_CSS_TEST)${NC}"
    echo "Check nginx config and permissions"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Fix Complete!${NC}"
echo "=================================="
echo ""
echo "Your portfolio should now be accessible at:"
echo "  $PROTOCOL://$DOMAIN"
echo ""
echo "Django admin (with styling):"
echo "  $PROTOCOL://$DOMAIN/admin/"
echo ""
echo "Test in your browser:"
echo "  1. Open: $PROTOCOL://$DOMAIN"
echo "  2. Check if frontend data loads correctly"
echo "  3. Visit admin panel to verify styling"
echo ""

echo ""
echo "For detailed logs, use:"
echo "  Backend:  sudo journalctl -u portfolio-backend -f"
echo "  Frontend: sudo journalctl -u portfolio-frontend -f"
echo "  Nginx:    sudo tail -f /var/log/nginx/error.log"
echo ""
