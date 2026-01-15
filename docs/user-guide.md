# Home Security Platform User Guide

This guide provides detailed instructions for setting up, configuring, and using the Home Security Platform.

## Initial Setup

### System Requirements

- **Hardware**: At least 4GB RAM, 2 CPU cores, 500GB SSD
- **OS**: Ubuntu Server 22.04+ or Debian 11+ (x86_64 or ARM64)
- **Network**: Ethernet connection to cameras
- **Software**: Docker and Docker Compose

### Installation

Follow the [Quick Start](../README.md#quick-start) in the main README.

After installation, access the web UI at `http://<server-ip>:8080`.

### First Login

- Default username: `admin`
- Default password: `admin`
- **Important**: Change the password immediately in Settings > Users.

## Adding Cameras

1. Navigate to **Management** > **Add Camera**.
2. Enter camera details:
   - **Name**: Unique identifier (e.g., "Front Door")
   - **URL**: RTSP stream URL (e.g., `rtsp://username:password@camera-ip:554/stream`)
   - **Type**: RTSP or USB
3. Click **Add Camera**.

### Auto-Discovery

Enable auto-discovery for ONVIF cameras:
1. Go to Settings > General.
2. Check "Enable Camera Auto-Discovery".
3. The system will scan your network for compatible cameras.

## Configuring Motion Detection

1. Select a camera from the **Live** view.
2. Click **Configure Motion Zones**.
3. Draw rectangles on the video feed to define detection areas.
4. Set sensitivity (0.0-1.0) for each zone.
5. Save changes.

Motion events will trigger recordings and appear in the dashboard.

## Recording Settings

### Continuous Recording

- Enabled by default.
- Records 5-minute segments continuously.
- Configurable in `config/default.yml`.

### Event-Triggered Recording

- Records for 30 seconds when motion is detected.
- Can be disabled in settings.

### Storage Management

- Recordings are stored in `/opt/home-security/data/recordings/`.
- Automatic cleanup after 30 days (configurable).
- Monitor storage usage on the Dashboard.

## User Management

### Adding Users

1. Go to Settings > Users.
2. Click **Add User**.
3. Enter username, password, and role (admin or viewer).
4. Viewer role has read-only access.

### Roles

- **Admin**: Full access to configuration and management.
- **Viewer**: Read-only access to live views, recordings, and events.

## Monitoring and Alerts

### Dashboard

- View system status, storage usage, recent events.
- See online/offline camera status.

### Event Log

- Currently basic; full event storage planned.
- Events include camera online/offline, motion detected.

### Alerts

- Not yet implemented: Email/SMS notifications for events.

## Viewing Live Feeds

1. Navigate to **Live Views**.
2. Select a camera to view real-time stream.
3. Adjust playback if needed.

## Browsing Recordings

1. Go to **Recordings**.
2. Click on a recording to play.
3. Use timeline to scrub through footage.

## Settings and Configuration

### General Settings

- Auto-discovery toggle
- Recording options
- Network settings

### Advanced Configuration

Edit `config/default.yml` directly for advanced options:
- Motion sensitivity
- Recording resolution
- Retention policies

Restart services after changes: `docker-compose restart`

## Troubleshooting

See [Troubleshooting](../README.md#troubleshooting) in the main README.

### Common Issues

- **No video feed**: Check camera URL and network connectivity.
- **Motion not detected**: Adjust zones and lighting; ensure good contrast.
- **Storage full**: Delete old recordings or increase storage.

## Maintenance

### Backups

- Configuration: Backup `config/default.yml`
- Recordings: Backup `/opt/home-security/data/` directory

### Updates

- Pull latest images: `docker-compose pull`
- Restart: `docker-compose up -d`

### Factory Reset

Run `./install.sh --reset` to reset everything.

## Security Considerations

- Change default passwords.
- Run on trusted network only.
- No outbound internet required.
- Firewall rules prevent external access by default.

For more security tips, see [Security Best Practices](security.md).

## Performance Tuning

See [Performance Tuning](performance.md) for optimization tips.

## API Usage

For programmatic access, see [API Documentation](api.md).

## Support

- Check [FAQ](faq.md)
- Open GitHub issues with logs and details.