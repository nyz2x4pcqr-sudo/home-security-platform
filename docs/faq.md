# Frequently Asked Questions

## Installation

### Can I install on Windows/Mac?

No, the platform requires Linux (Ubuntu Server or Debian). Docker containers are Linux-based, and the system is optimized for Linux appliances. For development, you can run it on Windows/Mac using Docker Desktop, but production use requires Linux.

### What if Docker isn't installed?

The install script will attempt to install Docker and Docker Compose automatically on supported systems. If it fails, install manually:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl enable docker
```

### Can I run multiple instances?

Yes, but each instance needs separate ports and storage. Modify `docker-compose.yml` and environment variables.

## Cameras

### Which cameras are supported?

- **RTSP**: Most IP cameras with RTSP support (e.g., Hikvision, Reolink).
- **ONVIF**: Cameras with ONVIF Profile S.
- **USB**: Basic USB cameras (may require driver compatibility).

Test your camera's RTSP URL first. Auto-discovery helps with ONVIF cameras.

### Why isn't my camera detected?

- Ensure camera is on the same network subnet.
- Check firewall settings; no internet required but local traffic must be allowed.
- Verify RTSP URL format: `rtsp://username:password@ip:port/stream`
- For ONVIF, ensure the camera supports discovery.

### Can I use wireless cameras?

Yes, as long as they provide RTSP streams and are on the same network. Ethernet is recommended for reliability.

## Performance

### How many cameras can it handle?

Depends on hardware:
- Raspberry Pi 4: 1-2 cameras
- Intel NUC (4GB RAM): 4-6 cameras
- Server (8GB+ RAM): 8+ cameras

Motion detection and recording are CPU-intensive.

### Why are recordings laggy?

- Check CPU usage: `docker stats`
- Reduce resolution or frame rate in camera settings.
- Disable continuous recording if not needed.

## Security

### Is it secure?

Designed for trusted local networks. No internet connectivity required. Uses bcrypt password hashing. See [Security Best Practices](security.md) for details.

### Can I access it remotely?

Not currently supported. Remote access would require VPN or secure tunnel, which is planned but not implemented.

### Are recordings encrypted?

No, stored in plain AVI/MP4. Encrypt at filesystem level if needed.

## Usage

### How do I change the password?

Log in as admin, go to Settings > Users, edit the admin user.

### Can I delete old recordings?

Manually via file system or wait for automatic cleanup (30 days by default). Configure retention in `config/default.yml`.

### Why no motion alerts?

Notifications not yet implemented. Check the dashboard or logs for events. See [TODO](todo.md) for planned features.

## Troubleshooting

### Services won't start

Check logs: `docker-compose logs`
Common issues:
- Port conflicts: Change ports in `docker-compose.yml`
- Storage permissions: Ensure Docker can write to data directories
- Configuration errors: Validate YAML syntax

### Camera stream fails

- Test RTSP URL with VLC media player
- Check network connectivity: `ping camera-ip`
- Ensure credentials are correct
- Some cameras require specific RTSP paths

### Web UI not loading

- Verify port 8080 is open: `netstat -tlnp | grep 8080`
- Check API service: `curl http://localhost:8000/health`
- Browser cache: Hard refresh (Ctrl+F5)

### High CPU usage

- Motion detection runs continuously; tune sensitivity in config
- Limit cameras or disable features
- Upgrade hardware

## Development

### How do I contribute?

See [CONTRIBUTING.md](../CONTRIBUTING.md). Fork, create feature branch, submit PR.

### Can I modify the code?

Yes, MIT licensed. The system is modular; services are independent.

### Where are logs stored?

Container logs: `docker-compose logs > logs.txt`
Application logs are written to stdout/stderr.

## Hardware

### Recommended hardware?

- **Minimum**: Raspberry Pi 4 (4GB), 500GB SSD
- **Recommended**: Intel NUC or similar with 8GB RAM, 1TB SSD
- Ethernet networking required

### Can I use a NAS for storage?

Yes, mount external storage as Docker volume. Configure in `docker-compose.yml`.

## Miscellaneous

### Is it free?

Yes, MIT licensed. Hardware may be sold commercially.

### Cloud integration?

No, and not planned. Designed for local-only operation.

### Mobile app?

Not available. Use web UI on mobile browser (basic support).

If your question isn't answered here, check [User Guide](user-guide.md) or open a GitHub issue.