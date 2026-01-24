#!/bin/bash

# ======================================================
# RDFS - Local Development Setup Script
# ======================================================

echo "=========================================="
echo "RDFS Local Development Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your local settings."
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if PostgreSQL is running
echo ""
echo "🔍 Checking PostgreSQL connection..."
python -c "
import os
import psycopg2
from urllib.parse import urlparse

try:
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/rdfs_db')
    result = urlparse(db_url)
    conn = psycopg2.connect(
        database=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    conn.close()
    print('✅ PostgreSQL connection successful!')
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
    print('⚠️  Please ensure PostgreSQL is running and DATABASE_URL is correct.')
" 2>/dev/null

# Run migrations
echo ""
echo "🔄 Running database migrations..."
python manage.py migrate

# Create superuser if needed
echo ""
echo "👤 Creating superuser (if not exists)..."
python manage.py create_admin

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "To run with Daphne (for WebSockets):"
echo "  daphne -b 0.0.0.0 -p 8000 rdfs.asgi:application"
echo ""
