#!/bin/bash

# This script sets up and runs the portfolio project on a Linux server without Docker.
# It assumes you have Python 3, pip, Node.js, and npm installed.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Backend Setup (Django) ---
echo "--- Setting up Django Backend ---"

# Navigate to the backend directory
cd portfolio-backend

# Create a Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create a .env file for the backend
echo "Creating backend .env file..."
cat > .env << EOF
DJANGO_SECRET_KEY=your-super-secret-key-that-you-should-change
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your_ec2_public_ip
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:80,http://127.0.0.1:80,http://your_ec2_public_ip:80
EOF

echo "IMPORTANT: Update DJANGO_ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS in portfolio-backend/.env with your EC2 instance's public IP address."

# Run database migrations
echo "Running Django migrations..."
python3 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Install Gunicorn for serving the Django app
echo "Installing Gunicorn..."
pip install gunicorn

echo "--- Backend setup complete ---"
echo "To run the backend server, navigate to the portfolio-backend directory and run:"
echo "gunicorn --workers 3 --bind 0.0.0.0:8000 portfolio_backend.wsgi:application &"
echo ""

# Deactivate the virtual environment
deactivate


# --- Frontend Setup (Astro) ---
echo "--- Setting up Astro Frontend ---"

# Navigate to the frontend directory
cd ../portfolio-frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Create a .env file for the frontend
echo "Creating frontend .env file..."
cat > .env << EOF
# URL for the browser to connect to the backend
PUBLIC_API_URL=http://your_ec2_public_ip:8000
# URL for the Astro server to connect to the backend (same as public for non-Docker setup)
SERVER_API_URL=http://localhost:8000
EOF

echo "IMPORTANT: Update PUBLIC_API_URL in portfolio-frontend/.env with your EC2 instance's public IP address."

# Build the Astro project for production
echo "Building Astro project..."
npm run build

# Install pm2 to run the server in the background
echo "Installing pm2 globally..."
sudo npm install -g pm2

echo "--- Frontend setup complete ---"
echo "To run the frontend server, navigate to the portfolio-frontend directory and run:"
echo "pm2 start npm --name 'portfolio-frontend' -- run preview --port 80"
echo ""

echo "--- All Done! ---"
echo "Remember to replace 'your_ec2_public_ip' in the .env files."
echo "You can start the servers with the commands provided above."
