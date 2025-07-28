#!/bin/bash
# FortiShell Pro Environment Bootstrapper (Mastery Edition)
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function info()    { echo -e "${YELLOW}[INFO]${NC} $1"; }
function success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
function error()   { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Python version
if ! command -v python3 &>/dev/null; then
  error "python3 is not installed."
  exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info[0], sys.version_info[1]))')
info "Detected Python $PYTHON_VERSION"
REQUIRED_VERSION="3.7"
if [[ $(python3 -c "import sys; print(sys.version_info >= (3,7))") != "True" ]]; then
  error "Python $REQUIRED_VERSION+ is required."
  exit 1
fi

# Check for venv module
if ! python3 -c "import venv" &>/dev/null; then
  error "Python venv module is missing. Please install it (e.g., 'sudo apt install python3-venv')."
  exit 1
fi

# Create virtual environment if not exists
if [ ! -d ".venv" ]; then
  info "Creating virtual environment..."
  python3 -m venv .venv
  success "Virtual environment created."
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip, wheel, setuptools
info "Upgrading pip, wheel, setuptools..."
pip install --upgrade pip wheel setuptools

# Install requirements if file exists
if [ -f "requirements.txt" ]; then
  info "Installing requirements from requirements.txt..."
  pip install -r requirements.txt
  success "Requirements installed."
else
  info "No requirements.txt found. Skipping requirements installation."
fi

# Post-setup info
success "Environment setup complete!"
echo -e "${YELLOW}To activate later: source .venv/bin/activate${NC}"
