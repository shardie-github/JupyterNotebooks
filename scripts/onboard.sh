#!/bin/bash
# Agent Factory Platform - Developer Onboarding Script
# One-command environment setup for new developers

set -e

echo "🚀 Agent Factory Platform - Developer Onboarding"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${YELLOW}Warning: Python 3.8+ required. Found: $python_version${NC}"
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -e ".[dev]"

# Copy environment file
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file with your configuration${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Run tests
echo -e "${BLUE}Running tests...${NC}"
if pytest tests/ -v --tb=short; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${YELLOW}⚠ Some tests failed (this is OK for first setup)${NC}"
fi

# Check code quality
echo -e "${BLUE}Checking code quality...${NC}"
if command -v ruff &> /dev/null; then
    ruff check agent_factory/ --select E,F || echo -e "${YELLOW}⚠ Some linting issues found${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}================================================"
echo "✓ Onboarding complete!"
echo "================================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run API server: uvicorn agent_factory.api.main:app --reload"
echo "4. Check health: curl http://localhost:8000/health"
echo "5. Read docs: docs/GETTING_STARTED.md"
echo ""
echo "Happy coding! 🎉"
