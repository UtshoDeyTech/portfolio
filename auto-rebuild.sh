#!/bin/bash

################################################################################
# Auto-Rebuild Frontend Script
#
# This script automatically rebuilds the frontend to fetch fresh data from API
# Run this via cron every 6 hours to keep content up-to-date
#
# Usage: bash /home/ubuntu/portfolio/auto-rebuild.sh
################################################################################

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the actual user (not root if run via cron as root)
ACTUAL_USER=${SUDO_USER:-ubuntu}
PROJECT_DIR="/home/${ACTUAL_USER}/portfolio"
FRONTEND_DIR="${PROJECT_DIR}/portfolio-frontend"

# Detect server public IP
EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 --max-time 2 2>/dev/null || echo "")
if [ -z "$EC2_PUBLIC_IP" ]; then
    EC2_PUBLIC_IP="localhost"
fi
DOMAIN=$EC2_PUBLIC_IP

# Log file
LOG_FILE="${PROJECT_DIR}/auto-rebuild.log"

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting auto-rebuild" >> "$LOG_FILE"

# Change to frontend directory
cd "$FRONTEND_DIR" || exit 1

# Pull latest changes (optional - uncomment if you want to auto-deploy code changes)
# sudo -u $ACTUAL_USER git pull origin main >> "$LOG_FILE" 2>&1

# Set build-time environment variables
export PUBLIC_API_URL="http://${DOMAIN}"
export SERVER_API_URL="http://127.0.0.1:8000"

# Rebuild frontend as actual user
echo "$(date '+%Y-%m-%d %H:%M:%S') - Building frontend..." >> "$LOG_FILE"
sudo -u $ACTUAL_USER bash << 'BUILD_EOF'
export PUBLIC_API_URL="${PUBLIC_API_URL}"
export SERVER_API_URL="${SERVER_API_URL}"
npm run build >> "${LOG_FILE}" 2>&1
BUILD_EOF

if [ $? -eq 0 ]; then
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - ${GREEN}✓ Build successful${NC}" >> "$LOG_FILE"

    # Reload nginx to serve new build
    systemctl reload nginx >> "$LOG_FILE" 2>&1

    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✓ Nginx reloaded" >> "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Auto-rebuild completed successfully" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
else
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - ${RED}✗ Build failed${NC}" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
    exit 1
fi
