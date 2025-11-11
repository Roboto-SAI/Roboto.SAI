#!/bin/bash
# Quick deployment validation and startup script for Roboto SAI

set -e  # Exit on error

echo "🚀 Roboto SAI - Quick Start Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed"
    exit 1
fi

# Check if .env file exists
echo ""
echo "Checking environment configuration..."
if [ -f .env ]; then
    print_success ".env file found"
    
    # Check for SESSION_SECRET
    if grep -q "SESSION_SECRET=" .env && ! grep -q "SESSION_SECRET=your_session_secret_here" .env; then
        print_success "SESSION_SECRET is configured"
    else
        print_error "SESSION_SECRET is not set or still has default value"
        print_info "Generate a secure secret with: openssl rand -hex 32"
        exit 1
    fi
else
    print_error ".env file not found"
    print_info "Copy .env.example to .env and configure your environment variables"
    echo "  cp .env.example .env"
    echo "  # Then edit .env and set SESSION_SECRET"
    exit 1
fi

# Check if virtual environment exists
echo ""
echo "Checking virtual environment..."
if [ -d ".venv" ]; then
    print_success "Virtual environment found"
else
    print_warning "Virtual environment not found, creating one..."
    python3 -m venv .venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Check if requirements are installed
echo ""
echo "Checking dependencies..."
if python3 -c "import flask" 2>/dev/null; then
    print_success "Dependencies appear to be installed"
else
    print_warning "Dependencies not installed, installing now..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
fi

# Run verification script if available
echo ""
echo "Running deployment verification..."
if [ -f verify_deployment.py ]; then
    python3 verify_deployment.py
    VERIFY_RESULT=$?
    if [ $VERIFY_RESULT -eq 0 ]; then
        print_success "All deployment checks passed!"
    else
        print_warning "Some deployment checks failed, but continuing..."
    fi
else
    print_warning "verify_deployment.py not found, skipping verification"
fi

# Ask user which mode to run
echo ""
echo "=================================="
echo "How would you like to run Roboto SAI?"
echo ""
echo "1) Development mode (python run_app.py)"
echo "2) Production mode (gunicorn)"
echo "3) Custom port development mode"
echo ""
read -p "Enter your choice (1-3): " CHOICE

case $CHOICE in
    1)
        echo ""
        print_info "Starting in development mode..."
        python3 run_app.py
        ;;
    2)
        echo ""
        print_info "Starting in production mode with gunicorn..."
        print_info "App will be available at http://localhost:5000"
        gunicorn --config gunicorn.conf.py main:app
        ;;
    3)
        echo ""
        read -p "Enter port number (default 5001): " PORT
        PORT=${PORT:-5001}
        print_info "Starting on port $PORT..."
        python3 main.py $PORT
        ;;
    *)
        print_error "Invalid choice, defaulting to development mode"
        python3 run_app.py
        ;;
esac
