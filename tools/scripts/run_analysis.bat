@echo off
REM ===========================================
REM SFS Database Structure Analyzer for Windows
REM ===========================================

echo 🔍 Starting SFS Database Analysis...
echo.

REM ۱. به پوشه docker-compose برو
cd /d "C:\Users\Behzad\Desktop\SFS\infrastructure\docker"

REM ۲. بررسی که docker-compose اجرا شده
docker-compose ps > nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not running!
    echo Please start your containers with: docker-compose up -d
    pause
    exit /b 1
)

REM ۳. اجرای اسکریپت SQL
echo 📊 Running database analysis...
echo.

type "C:\Users\Behzad\Desktop\SFS\tools\scripts\show_database_structure.sql" | docker-compose exec -T db psql -U sfs -d sfs

REM ۴. اگر خطا داد، با سرویس‌های دیگر امتحان کن
if errorlevel 1 (
    echo ⚠️ Trying with service name: database...
    type "C:\Users\Behzad\Desktop\SFS\tools\scripts\show_database_structure.sql" | docker-compose exec -T database psql -U sfs -d sfs
)

if errorlevel 1 (
    echo ⚠️ Trying with service name: postgres...
    type "C:\Users\Behzad\Desktop\SFS\tools\scripts\show_database_structure.sql" | docker-compose exec -T postgres psql -U sfs -d sfs
)

if errorlevel 1 (
    echo ❌ Failed to execute SQL script!
    echo.
    echo Available services:
    docker-compose ps
    echo.
    echo Please check:
    echo 1. Docker is running
    echo 2. Containers are started (docker-compose up -d)
    echo 3. Service name is correct
)

echo.
echo ✅ Analysis completed!
pause