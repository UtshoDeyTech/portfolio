#!/bin/bash

# AWS EC2 Deployment Script for Portfolio Application
# This script sets up and deploys the portfolio application using Docker on AWS EC2

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
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
if [ "$EUID" -eq 0 ]; then
    print_error "Please do not run this script as root. It will use sudo when needed."
    exit 1
fi

print_info "Starting AWS EC2 deployment setup..."

# 1. Update system packages
print_info "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y
print_success "System packages updated"

# 2. Install Docker
if ! command -v docker &> /dev/null; then
    print_info "Installing Docker..."
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Add current user to docker group
    sudo usermod -aG docker $USER
    print_success "Docker installed"
else
    print_success "Docker already installed"
fi

# 3. Install Docker Compose (standalone)
if ! command -v docker-compose &> /dev/null; then
    print_info "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed"
else
    print_success "Docker Compose already installed"
fi

# 4. Setup environment file
if [ ! -f .env.production ]; then
    print_info "Creating production environment file..."
    cp .env.production.example .env.production

    # Get EC2 public IP
    EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || echo "UNABLE_TO_DETECT")

    if [ "$EC2_PUBLIC_IP" != "UNABLE_TO_DETECT" ]; then
        print_success "Detected EC2 Public IP: $EC2_PUBLIC_IP"

        # Update .env.production with EC2 IP
        sed -i "s/your-ec2-public-ip/$EC2_PUBLIC_IP/g" .env.production
        sed -i "s/your-domain.com/$EC2_PUBLIC_IP/g" .env.production
    else
        print_error "Unable to detect EC2 public IP automatically"
        print_info "Please manually update .env.production with your EC2 public IP or domain"
    fi

    # Generate Django secret key
    DJANGO_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')
    sed -i "s/CHANGE_THIS_TO_A_RANDOM_SECRET_KEY_IN_PRODUCTION/$DJANGO_SECRET_KEY/g" .env.production

    print_success "Environment file created at .env.production"
    print_info "Please review and update .env.production with your specific configuration"
else
    print_success "Production environment file already exists"
fi

# 5. Create necessary directories
print_info "Creating necessary directories..."
mkdir -p nginx/ssl
mkdir -p portfolio-backend/staticfiles
mkdir -p portfolio-backend/media
print_success "Directories created"

# 6. Configure firewall (if UFW is available)
if command -v ufw &> /dev/null; then
    print_info "Configuring firewall..."
    sudo ufw allow 22/tcp   # SSH
    sudo ufw allow 80/tcp   # HTTP
    sudo ufw allow 443/tcp  # HTTPS
    sudo ufw --force enable
    print_success "Firewall configured"
fi

# 7. Create systemd service for auto-start
print_info "Creating systemd service..."
sudo tee /etc/systemd/system/portfolio.service > /dev/null <<EOF
[Unit]
Description=Portfolio Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$(pwd)
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml --env-file .env.production down
User=$USER

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable portfolio.service
print_success "Systemd service created and enabled"

# 8. Build and start containers
print_info "Building Docker images (this may take a few minutes)..."
docker-compose -f docker-compose.prod.yml --env-file .env.production build

print_info "Starting containers..."
docker-compose -f docker-compose.prod.yml --env-file .env.production up -d

print_success "Containers started successfully"

# 9. Wait for services to be healthy
print_info "Waiting for services to become healthy..."
sleep 10

# 10. Create Django superuser (interactive)
print_info "Creating Django superuser..."
print_info "You will be prompted to create an admin user for the Django admin panel"
docker-compose -f docker-compose.prod.yml --env-file .env.production exec backend python manage.py createsuperuser || print_info "Skipping superuser creation (you can create it later)"

# 11. Display status
print_info "Checking container status..."
docker-compose -f docker-compose.prod.yml --env-file .env.production ps

echo ""
print_success "========================================="
print_success "Deployment completed successfully!"
print_success "========================================="
echo ""
print_info "Your portfolio is now accessible at:"

if [ "$EC2_PUBLIC_IP" != "UNABLE_TO_DETECT" ]; then
    echo -e "  ${GREEN}Frontend:${NC} http://$EC2_PUBLIC_IP"
    echo -e "  ${GREEN}Backend API:${NC} http://$EC2_PUBLIC_IP/api/"
    echo -e "  ${GREEN}Django Admin:${NC} http://$EC2_PUBLIC_IP/admin/"
else
    echo -e "  ${GREEN}Frontend:${NC} http://YOUR_EC2_PUBLIC_IP"
    echo -e "  ${GREEN}Backend API:${NC} http://YOUR_EC2_PUBLIC_IP/api/"
    echo -e "  ${GREEN}Django Admin:${NC} http://YOUR_EC2_PUBLIC_IP/admin/"
fi

echo ""
print_info "Useful commands:"
echo "  View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "  Stop services: docker-compose -f docker-compose.prod.yml down"
echo "  Restart services: docker-compose -f docker-compose.prod.yml restart"
echo "  View status: docker-compose -f docker-compose.prod.yml ps"
echo ""
print_info "The application will automatically start on system reboot"
echo ""
print_info "Next steps:"
echo "  1. Configure your domain DNS to point to this EC2 instance"
echo "  2. Set up SSL/HTTPS using the ssl_setup.sh script (optional)"
echo "  3. Review and customize .env.production as needed"
echo ""
