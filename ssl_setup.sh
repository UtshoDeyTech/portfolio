#!/bin/bash

# SSL/HTTPS Setup Script using Let's Encrypt (Certbot)
# This script helps set up SSL certificates for your portfolio application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run with sudo"
    exit 1
fi

# Prompt for domain name
print_info "SSL/HTTPS Setup for Portfolio Application"
echo ""
read -p "Enter your domain name (e.g., example.com): " DOMAIN_NAME
read -p "Enter your email address for SSL certificate notifications: " EMAIL

if [ -z "$DOMAIN_NAME" ] || [ -z "$EMAIL" ]; then
    print_error "Domain name and email are required"
    exit 1
fi

print_info "Setting up SSL for domain: $DOMAIN_NAME"
print_info "Email: $EMAIL"

# Install certbot
if ! command -v certbot &> /dev/null; then
    print_info "Installing Certbot..."
    apt-get update
    apt-get install -y certbot
    print_success "Certbot installed"
else
    print_success "Certbot already installed"
fi

# Create certbot directory
mkdir -p /var/www/certbot

# Temporarily stop nginx to get certificate
print_info "Stopping nginx container..."
cd $(dirname "$0")
docker-compose -f docker-compose.prod.yml stop nginx

# Obtain certificate
print_info "Obtaining SSL certificate from Let's Encrypt..."
certbot certonly --standalone \
    --preferred-challenges http \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN_NAME"

if [ $? -eq 0 ]; then
    print_success "SSL certificate obtained successfully"
else
    print_error "Failed to obtain SSL certificate"
    docker-compose -f docker-compose.prod.yml start nginx
    exit 1
fi

# Copy certificates to nginx ssl directory
print_info "Copying certificates to nginx directory..."
mkdir -p nginx/ssl
cp /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem nginx/ssl/
chmod 644 nginx/ssl/*.pem

print_success "Certificates copied"

# Update nginx configuration
print_info "Updating nginx configuration..."
print_info "Please manually uncomment the HTTPS server block in nginx/nginx.conf"
print_info "And update 'server_name' to: $DOMAIN_NAME"

# Update .env.production
print_info "Updating .env.production..."
sed -i "s|http://$DOMAIN_NAME|https://$DOMAIN_NAME|g" .env.production
sed -i "s|http://your-domain.com|https://$DOMAIN_NAME|g" .env.production

# Restart nginx
print_info "Restarting nginx..."
docker-compose -f docker-compose.prod.yml up -d nginx

print_success "========================================="
print_success "SSL Setup Completed!"
print_success "========================================="
echo ""
print_info "Your site should now be accessible at:"
echo -e "  ${GREEN}https://$DOMAIN_NAME${NC}"
echo ""
print_info "IMPORTANT: Don't forget to:"
echo "  1. Uncomment the HTTPS server block in nginx/nginx.conf"
echo "  2. Update the server_name directive to your domain"
echo "  3. Uncomment the HTTP to HTTPS redirect in the HTTP server block"
echo "  4. Restart nginx: docker-compose -f docker-compose.prod.yml restart nginx"
echo ""
print_info "SSL certificate will auto-renew. To manually renew:"
echo "  sudo certbot renew"
echo ""
