@echo off
REM ======================================================
REM RDFS - Local Development Setup Script (Windows)
REM ======================================================

echo ==========================================
echo RDFS Local Development Setup
echo ==========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo 📝 Creating .env from .env.example...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your local settings.
    echo.
)

REM Check if virtual environment exists
if not exist venv (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created.
    echo.
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Run migrations
echo.
echo 🔄 Running database migrations...
python manage.py migrate

REM Create superuser if needed
echo.
echo 👤 Creating superuser (if not exists)...
python manage.py create_admin

REM Collect static files
echo.
echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ==========================================
echo ✅ Setup complete!
echo ==========================================
echo.
echo To start the development server:
echo   python manage.py runserver
echo.
echo To run with Daphne (for WebSockets):
echo   daphne -b 0.0.0.0 -p 8000 rdfs.asgi:application
echo.
pause
