#!/bin/bash

# Deployment Management Script
# Provides common operations for managing the deployed portfolio application

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

show_menu() {
    echo ""
    echo "========================================="
    echo "Portfolio Deployment Management"
    echo "========================================="
    echo "1. View logs (all services)"
    echo "2. View backend logs"
    echo "3. View frontend logs"
    echo "4. View nginx logs"
    echo "5. Restart all services"
    echo "6. Restart backend"
    echo "7. Restart frontend"
    echo "8. Restart nginx"
    echo "9. Stop all services"
    echo "10. Start all services"
    echo "11. View service status"
    echo "12. Rebuild and restart all"
    echo "13. Create Django superuser"
    echo "14. Run Django migrations"
    echo "15. Collect static files"
    echo "16. View Django shell"
    echo "17. Pull latest code and redeploy"
    echo "18. Backup database"
    echo "19. Clean up Docker resources"
    echo "0. Exit"
    echo "========================================="
    read -p "Select an option: " choice
    echo ""
}

case_handler() {
    case $1 in
        1)
            print_info "Showing logs (Ctrl+C to exit)..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f
            ;;
        2)
            print_info "Showing backend logs (Ctrl+C to exit)..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f backend
            ;;
        3)
            print_info "Showing frontend logs (Ctrl+C to exit)..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f frontend
            ;;
        4)
            print_info "Showing nginx logs (Ctrl+C to exit)..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE logs -f nginx
            ;;
        5)
            print_info "Restarting all services..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE restart
            print_success "All services restarted"
            ;;
        6)
            print_info "Restarting backend..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE restart backend
            print_success "Backend restarted"
            ;;
        7)
            print_info "Restarting frontend..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE restart frontend
            print_success "Frontend restarted"
            ;;
        8)
            print_info "Restarting nginx..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE restart nginx
            print_success "Nginx restarted"
            ;;
        9)
            print_info "Stopping all services..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE down
            print_success "All services stopped"
            ;;
        10)
            print_info "Starting all services..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
            print_success "All services started"
            ;;
        11)
            print_info "Service status:"
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE ps
            ;;
        12)
            print_info "Rebuilding and restarting all services..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE down
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE build --no-cache
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
            print_success "All services rebuilt and restarted"
            ;;
        13)
            print_info "Creating Django superuser..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec backend python manage.py createsuperuser
            ;;
        14)
            print_info "Running Django migrations..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec backend python manage.py migrate
            print_success "Migrations completed"
            ;;
        15)
            print_info "Collecting static files..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec backend python manage.py collectstatic --noinput
            print_success "Static files collected"
            ;;
        16)
            print_info "Opening Django shell..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec backend python manage.py shell
            ;;
        17)
            print_info "Pulling latest code..."
            git pull
            print_info "Rebuilding and redeploying..."
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE down
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE build
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE up -d
            print_success "Redeployment completed"
            ;;
        18)
            BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sqlite3"
            print_info "Creating database backup: $BACKUP_FILE"
            docker-compose -f $COMPOSE_FILE --env-file $ENV_FILE exec backend cp /app/db.sqlite3 /app/$BACKUP_FILE
            docker cp portfolio-backend-prod:/app/$BACKUP_FILE ./backups/
            print_success "Backup created at ./backups/$BACKUP_FILE"
            ;;
        19)
            print_info "Cleaning up Docker resources..."
            docker system prune -a -f
            print_success "Docker cleanup completed"
            ;;
        0)
            print_info "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
}

# Create backups directory
mkdir -p backups

# Main loop
while true; do
    show_menu
    case_handler $choice
    read -p "Press Enter to continue..."
done
