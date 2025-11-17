#!/bin/bash

echo "Fixing Django static files permissions..."

cd ~/portfolio/portfolio-backend

# Check current permissions
echo "Current static directory permissions:"
ls -ld static/

# Fix directory permissions
echo "Setting correct permissions..."
sudo chown -R $USER:www-data static/
sudo chmod -R 755 static/
sudo find static/ -type f -exec chmod 644 {} \;
sudo find static/ -type d -exec chmod 755 {} \;

echo "New permissions:"
ls -ld static/
ls -l static/ | head -10

# Test the fix
echo ""
echo "Testing static file access..."
curl -I http://35.175.120.243/static/admin/css/base.css

echo ""
echo "Done! Check http://35.175.120.243/admin/ in your browser"
