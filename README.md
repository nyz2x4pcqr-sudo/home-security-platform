# Home Security Platform

An open-source, local-only home security platform designed to replace subscription-based systems like ADT, Ring, and Nest. Runs entirely on your local hardware without any cloud dependencies.

## Vision

To provide a reliable, privacy-focused alternative to cloud-based security systems, empowering users with full control over their data and hardware.

## Features

- **Camera Ingestion**: Support for RTSP streams and ONVIF camera discovery
- **Recording**: Continuous recording and event-triggered clips
- **Motion Detection**: CPU-based motion detection with configurable zones using OpenCV
- **Event System**: Notifications for motion, camera offline, and other events
- **Local Web UI**: Dashboard, live camera view, timeline playback, camera management
- **Authentication**: Local user accounts with admin and viewer roles
- **Plug-and-Play**: One-command installation, zero Docker knowledge required

## Requirements

- **OS**: Ubuntu Server LTS (22.04+) or Debian (11+)
- **Architecture**: x86_64 or ARM64 (e.g., Raspberry Pi 4+)
- **Hardware**: Minimum 4GB RAM, 2-core CPU, 500GB SSD
- **Network**: Ethernet-first, local IP cameras
- **Software**: Docker and Docker Compose (installed by script)

## Quick Start

1. Download or clone the repository.
2. Run `chmod +x install.sh && ./install.sh` (installs Docker if needed).
3. Open `http://localhost:8080` in your browser to access the web UI.
4. Log in with default credentials (admin/admin).
5. Add cameras and configure settings.

For detailed setup, see [User Guide](docs/user-guide.md).

## Prerequisites

- **Operating System**: Ubuntu Server 22.04+ or Debian 11+ (x86_64 or ARM64).
- **Hardware**: Minimum 4GB RAM, 2-core CPU, 500GB SSD for storage.
- **Network**: Ethernet connection; cameras must be on the same LAN.
- **Software**: Docker and Docker Compose (installed automatically by script).
- **Permissions**: Root access for installation.

## Installation

### Automated Installation

1. Download the repository ZIP or clone via Git:
   ```
   git clone https://github.com/your-org/home-security-platform.git
   cd home-security-platform
   ```
2. Make the install script executable and run it:
   ```
   chmod +x install.sh
   ./install.sh
   ```
   The script will:
   - Install Docker and Docker Compose if not present.
   - Pull Docker images.
   - Start all services using Docker Compose.
   - Set up initial configuration.
   - Guide you through camera discovery.

3. Access the web UI at `http://<server-ip>:8080` and complete the setup wizard.

### Manual Installation

If you prefer manual setup:

1. Install Docker and Docker Compose on your system.
2. Copy `config/default.yml.example` to `config/default.yml` and edit as needed.
3. Run `docker-compose up -d` to start services.
4. Access the web UI.

### Post-Installation

- Default login: username `admin`, password `admin` (change immediately).
- Configure cameras via the web UI.
- Enable auto-discovery for ONVIF cameras.
- Set motion detection zones.

## Usage

- **Dashboard**: Overview of system status, storage usage, recent events
- **Live View**: Real-time camera feeds
- **Timeline**: Browse and play back recordings
- **Cameras**: Add, configure, and manage cameras
- **Settings**: Adjust motion zones, recording schedules, user accounts

## Configuration

Configurations are stored locally in YAML files. Edit via the web UI or directly in `/opt/home-security/config/`.

## Troubleshooting

### Common Issues

- **Web UI not accessible**:
  - Ensure ports 8080 (web UI) and 8000 (API) are open and not blocked by firewall.
  - Check if services are running: `docker-compose ps`
  - Restart services: `docker-compose restart`

- **Cameras not detected**:
  - Verify cameras are on the same network and accessible via RTSP/ONVIF.
  - Check camera credentials and URLs.
  - Enable auto-discovery in configuration.

- **Motion detection not working**:
  - Adjust motion zones in the web UI.
  - Ensure sufficient lighting; motion detection uses basic frame differencing.
  - Check logs for errors: `docker-compose logs motion`

- **Recording failures**:
  - Verify storage space: `df -h`
  - Check permissions on data directory.
  - Ensure camera streams are stable.

### Logs and Diagnostics

- View all logs: `docker-compose logs`
- Service-specific logs: `docker-compose logs <service>` (e.g., `docker-compose logs api`)
- Event bus logs: Useful for inter-service communication issues.
- System resources: Use `htop` or `docker stats` to monitor CPU/memory.

### Factory Reset

To reset to factory defaults:
```
./install.sh --reset
```
This will stop services, remove containers and volumes, and restart fresh.

### Getting Help

- Check [FAQ](docs/faq.md) for common questions.
- Review [User Guide](docs/user-guide.md) for detailed usage.
- Open an issue on GitHub with logs and system details.

## Architecture

Detailed architecture, including service descriptions and communication, is documented in [docs/architecture.md](docs/architecture.md).

## Documentation

- [User Guide](docs/user-guide.md): Complete setup and usage instructions.
- [API Documentation](docs/api.md): REST API reference for developers.
- [Performance Tuning](docs/performance.md): Optimize for your hardware.
- [Security Best Practices](docs/security.md): Secure your installation.
- [FAQ](docs/faq.md): Frequently asked questions.
- [Unimplemented Features](docs/todo.md): Planned enhancements and known limitations.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The MIT License was chosen for its permissiveness, allowing commercial use, modification, and distribution, which aligns with the goal of enabling hardware vendors to sell preconfigured appliances while keeping the software open-source.

## Security

- No outbound network traffic by default
- Passwords hashed with bcrypt
- Token-based authentication for API
- Designed for trusted local networks only

For threat model details, see [docs/architecture.md](docs/architecture.md).