@echo off
REM Home Security Platform Installation Script for Windows

echo Installing Home Security Platform...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if Docker Compose is available
docker compose version >nul 2>&1
if errorlevel 1 (
    docker-compose version >nul 2>&1
    if errorlevel 1 (
        echo Docker Compose is not installed. Please install Docker Compose first.
        pause
        exit /b 1
    )
)

REM Create config directory if it doesn't exist
if not exist config mkdir config

REM Copy default config if it doesn't exist
if not exist config\default.yml (
    if exist config\default.yml.example (
        copy config\default.yml.example config\default.yml
        echo Copied config\default.yml.example to config\default.yml
        echo Please edit config\default.yml to configure your settings.
    ) else (
        echo Warning: config\default.yml.example not found.
    )
) else (
    echo Config file config\default.yml already exists.
)

REM Copy .env if it doesn't exist
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo Copied .env.example to .env
        echo Please edit .env to configure your environment variables.
    ) else (
        echo Warning: .env.example not found.
    )
) else (
    echo .env file already exists.
)

REM Build and start the services
echo Building and starting services...
docker compose version >nul 2>&1
if errorlevel 0 (
    docker compose up --build -d
) else (
    docker-compose up --build -d
)

echo Installation complete!
echo Services should be available at:
echo - Web UI: http://localhost:8080
echo - API: http://localhost:8000
echo - RabbitMQ Management: http://localhost:15672
pause