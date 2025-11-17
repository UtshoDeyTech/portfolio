#!/bin/bash

echo "======================================"
echo "Frontend-Backend Connection Debugger"
echo "======================================"

cd ~/portfolio

# Detect configuration
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
DOMAIN=$(grep "server_name" /etc/nginx/sites-available/portfolio | head -1 | awk '{print $2}' | sed 's/;//')

if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    PROTOCOL="https"
else
    PROTOCOL="http"
fi

echo ""
echo "Configuration:"
echo "  Domain: $DOMAIN"
echo "  IP: $PUBLIC_IP"
echo "  Protocol: $PROTOCOL"
echo ""

echo "======================================"
echo "1. Checking Backend .env Configuration"
echo "======================================"

cd portfolio-backend

echo "Current CORS settings:"
grep "CORS_ALLOWED_ORIGINS" .env || echo "NOT FOUND"

echo ""
echo "Current ALLOWED_HOSTS:"
grep "ALLOWED_HOSTS" .env || echo "NOT FOUND"

echo ""
echo "======================================"
echo "2. Testing Backend API Endpoints"
echo "======================================"

echo ""
echo "Testing /api/blog-settings/ ..."
curl -s "$PROTOCOL://$DOMAIN/api/blog-settings/" | head -c 200
echo ""

echo ""
echo "Testing /api/home/ ..."
curl -s "$PROTOCOL://$DOMAIN/api/home/" | head -c 200
echo ""

echo ""
echo "======================================"
echo "3. Checking CORS Headers"
echo "======================================"

echo ""
echo "Testing CORS from browser perspective:"
curl -I -X OPTIONS "$PROTOCOL://$DOMAIN/api/blog-settings/" \
  -H "Origin: $PROTOCOL://$DOMAIN" \
  -H "Access-Control-Request-Method: GET" 2>&1 | grep -i "access-control"

echo ""
echo "======================================"
echo "4. Checking Frontend Build"
echo "======================================"

cd ../portfolio-frontend

if [ -d "dist" ]; then
    echo "Frontend dist exists ✓"

    echo ""
    echo "Checking for API URL in built JavaScript files..."

    # Find any hardcoded API URLs
    if grep -r "http://localhost" dist/ 2>/dev/null | head -3; then
        echo ""
        echo "⚠ WARNING: Found localhost references in build!"
        echo "This means the frontend was built incorrectly."
    fi

    # Check for the actual API URL
    if grep -r "$PROTOCOL://$DOMAIN" dist/ 2>/dev/null | head -3; then
        echo ""
        echo "✓ Found correct API URL in build"
    else
        echo ""
        echo "⚠ WARNING: Correct API URL not found in build"
        echo "The frontend needs to be rebuilt with PUBLIC_API_URL=$PROTOCOL://$DOMAIN"
    fi

    # Check build timestamp
    echo ""
    echo "Frontend build timestamp:"
    ls -la dist/ | grep -E "index.html|^d"

else
    echo "✗ Frontend dist does NOT exist"
fi

echo ""
echo "======================================"
echo "5. Checking Frontend Service"
echo "======================================"

if systemctl is-active --quiet portfolio-frontend; then
    echo "✓ Frontend service is running"

    # Check what the frontend is serving
    echo ""
    echo "Testing frontend homepage:"
    curl -s http://127.0.0.1:4321/ | grep -o "<title>.*</title>" || echo "Could not get page"

else
    echo "✗ Frontend service is NOT running"
fi

echo ""
echo "======================================"
echo "6. Real Browser Test Instructions"
echo "======================================"

echo ""
echo "To debug in your browser:"
echo ""
echo "1. Open: $PROTOCOL://$DOMAIN"
echo ""
echo "2. Press F12 to open Developer Tools"
echo ""
echo "3. Go to Console tab - look for errors like:"
echo "   - CORS errors"
echo "   - Failed to fetch"
echo "   - Network errors"
echo ""
echo "4. Go to Network tab:"
echo "   - Filter by 'XHR' or 'Fetch'"
echo "   - Look for requests to /api/"
echo "   - Check if they're failing (red)"
echo "   - Click on a failed request to see details"
echo ""
echo "5. Common issues to look for:"
echo "   - Request URL going to wrong address"
echo "   - CORS error (check Response Headers)"
echo "   - 404 Not Found (API endpoint doesn't exist)"
echo "   - 500 Internal Server Error (backend crash)"
echo ""

echo "======================================"
echo "7. Quick Fixes"
echo "======================================"

echo ""
echo "If you see CORS errors, run:"
echo "  cd ~/portfolio/portfolio-backend"
echo "  sed -i 's|CORS_ALLOWED_ORIGINS=.*|CORS_ALLOWED_ORIGINS=$PROTOCOL://$DOMAIN,http://$DOMAIN,https://$DOMAIN,http://$PUBLIC_IP,https://$PUBLIC_IP,http://localhost:4321|' .env"
echo "  sudo systemctl restart portfolio-backend"
echo ""

echo "If frontend is calling wrong API URL, run:"
echo "  cd ~/portfolio/portfolio-frontend"
echo "  echo 'PUBLIC_API_URL=$PROTOCOL://$DOMAIN' > .env"
echo "  npm run build"
echo "  rm .env"
echo "  sudo systemctl restart portfolio-frontend"
echo ""

echo "======================================"
echo "8. Backend Logs (check for errors)"
echo "======================================"
echo ""
sudo journalctl -u portfolio-backend -n 30 --no-pager | tail -20

echo ""
echo "======================================"
echo "Done! Copy any errors you see and share them."
echo "======================================"
