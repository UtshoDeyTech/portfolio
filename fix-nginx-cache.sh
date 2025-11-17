#!/bin/bash

################################################################################
# Quick Fix: Disable caching for interactive API endpoints
# This fixes the like/unlike button not updating immediately
################################################################################

set -e

echo "=================================="
echo "Fixing Nginx Cache Configuration"
echo "=================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Backup current config
echo "Creating backup..."
cp /etc/nginx/sites-available/portfolio /etc/nginx/sites-available/portfolio.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

# Get current values
DOMAIN=$(grep -oP 'server_name \K[^;]+' /etc/nginx/sites-available/portfolio | head -1)
FRONTEND_DIR=$(grep -oP 'root \K[^;]+' /etc/nginx/sites-available/portfolio | head -1 | sed 's|/dist$||')
BACKEND_DIR=$(grep -oP 'alias \K[^/]+/[^/]+/portfolio-backend' /etc/nginx/sites-available/portfolio | head -1)

echo "Detected configuration:"
echo "  Domain: $DOMAIN"
echo "  Frontend: $FRONTEND_DIR"
echo "  Backend: $BACKEND_DIR"
echo ""

# Create new Nginx config with fixed caching
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

    # Backend API - NO caching for interactive endpoints (POST/mutations)
    # Disable caching for: like, comments, view tracking
    location ~ ^/api/blog-posts/[^/]+/(toggle-like|increment-view|update-duration|comments)/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;

        # NO caching - immediate updates
        add_header Cache-Control "no-store, no-cache, must-revalidate, max-age=0";
        add_header Pragma "no-cache";
        expires -1;
    }

    # Backend API - Short cache for blog detail (admin can update anytime)
    # Cache for only 2 minutes so admin updates show quickly
    location ~ ^/api/blog-posts/[^/]+/?$ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;

        # Short cache for blog detail - 2 minutes
        # This allows admin updates to show quickly
        add_header Cache-Control "public, max-age=120, must-revalidate";
    }

    # Backend API - Cache read-only GET requests (lists, static data)
    location /api/ {
        proxy_pass http://backend/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;

        # Only cache GET requests, never POST/PUT/DELETE
        set $no_cache 0;
        if ($request_method != GET) {
            set $no_cache 1;
        }

        # Cache GET requests for 6 hours (lists, static data)
        add_header Cache-Control "public, max-age=21600, stale-while-revalidate=43200";

        # Disable caching for non-GET requests
        proxy_cache_bypass $no_cache;
        proxy_no_cache $no_cache;
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

echo "Testing Nginx configuration..."
nginx -t

if [ $? -eq 0 ]; then
    echo "✓ Configuration is valid"
    echo ""
    echo "Reloading Nginx..."
    systemctl reload nginx
    echo "✓ Nginx reloaded"
    echo ""
    echo "=================================="
    echo "✓ FIX APPLIED SUCCESSFULLY!"
    echo "=================================="
    echo ""
    echo "Changes made:"
    echo "  ✓ Disabled caching for ALL POST/PUT/DELETE requests"
    echo "  ✓ Disabled caching for like/unlike endpoints"
    echo "  ✓ Disabled caching for comment endpoints"
    echo "  ✓ Disabled caching for view tracking endpoints"
    echo "  ✓ Blog detail pages cached for only 2 minutes (admin updates visible quickly)"
    echo "  ✓ Blog lists and static data still cached for 6 hours (performance)"
    echo ""
    echo "Expected behavior:"
    echo "  ✓ Like/unlike updates immediately"
    echo "  ✓ Comments appear immediately after posting"
    echo "  ✓ Admin blog updates visible within 2 minutes"
    echo "  ✓ Fast page loads (static content still cached)"
    echo ""
    echo "Test the fix:"
    echo "  1. Clear your browser cache (Ctrl+Shift+Delete)"
    echo "  2. Visit: http://$DOMAIN/blog/docker-kubernetes-beginners-guide"
    echo "  3. Click the like button - should update immediately!"
    echo "  4. Post a comment - should appear in the list right away!"
    echo "  5. Update a blog post from admin - changes visible within 2 minutes!"
    echo ""
else
    echo "✗ Configuration test failed"
    echo "Restoring backup..."
    cp /etc/nginx/sites-available/portfolio.backup.* /etc/nginx/sites-available/portfolio
    systemctl reload nginx
    echo "✗ Backup restored"
    exit 1
fi
