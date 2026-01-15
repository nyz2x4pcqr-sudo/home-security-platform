#!/bin/bash

# Home Security Platform Installation Script for Linux/Mac

set -e

echo "Installing Home Security Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    if ! docker-compose version &> /dev/null; then
        echo "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
fi

# Create config directory if it doesn't exist
mkdir -p config

# Copy default config if it doesn't exist
if [ ! -f config/default.yml ]; then
    if [ -f config/default.yml.example ]; then
        cp config/default.yml.example config/default.yml
        echo "Copied config/default.yml.example to config/default.yml"
        echo "Please edit config/default.yml to configure your settings."
    else
        echo "Warning: config/default.yml.example not found."
    fi
else
    echo "Config file config/default.yml already exists."
fi

# Copy .env if it doesn't exist
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Copied .env.example to .env"
        echo "Please edit .env to configure your environment variables."
    else
        echo "Warning: .env.example not found."
    fi
else
    echo ".env file already exists."
fi

# Build and start the services
echo "Building and starting services..."
if command -v docker compose &> /dev/null; then
    docker compose up --build -d
else
    docker-compose up --build -d
fi

echo "Installation complete!"
echo "Services should be available at:"
echo "- Web UI: http://localhost:8080"
echo "- API: http://localhost:8000"
echo "- RabbitMQ Management: http://localhost:15672"