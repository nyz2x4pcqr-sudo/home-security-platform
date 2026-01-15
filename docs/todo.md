# Unimplemented Features and Known Limitations

This document outlines features that are planned for future development, known limitations, and areas for improvement. These are not bugs but missing functionality that would enhance the platform.

## High Priority

### Event Storage and Retrieval
- **Current State**: Events are published to event-bus but not stored persistently.
- **Impact**: No historical event logs; dashboard shows limited data.
- **Planned**: Implement event database (SQLite/PostgreSQL) with retention policies.
- **Timeline**: Next major release.

### Persistent Configuration Changes
- **Current State**: API changes to cameras/users are session-only; not saved to disk.
- **Impact**: Configuration lost on restart.
- **Planned**: Modify API to write to `config/default.yml` and reload services.
- **Timeline**: Next minor release.

### Role-Based Authentication
- **Current State**: Basic auth with admin/viewer; roles not enforced in API.
- **Impact**: Viewer accounts have same access as admin via API.
- **Planned**: Implement role checks in FastAPI endpoints.
- **Timeline**: Next minor release.

## Medium Priority

### Notifications System
- **Current State**: No alerts for events (email, SMS, push).
- **Impact**: Users must check dashboard manually.
- **Planned**: Email notifications for motion/camera offline; extensible plugin system.
- **Timeline**: Future release.

### Advanced Motion Detection
- **Current State**: Basic frame differencing with zones.
- **Impact**: False positives in varying light; no person detection.
- **Planned**: ML-based detection (TensorFlow Lite) for better accuracy.
- **Timeline**: Future release.

### Remote Access
- **Current State**: Local-only; no secure remote access.
- **Impact**: Cannot monitor when away from home.
- **Planned**: Optional secure tunnel (WireGuard/Tailscale) with user consent.
- **Timeline**: Future release (security review required).

### Web UI Enhancements
- **Current State**: Basic HTML/JS interface.
- **Impact**: Limited functionality; not mobile-optimized.
- **Planned**: React-based UI with mobile support, timeline scrubbing.
- **Timeline**: Future release.

### Backup and Restore
- **Current State**: Manual backup of config and recordings.
- **Impact**: No automated backups; restore is manual.
- **Planned**: Scheduled backups to external storage; one-click restore.
- **Timeline**: Future release.

## Low Priority

### Multi-Camera Views
- **Current State**: Single camera view at a time.
- **Impact**: Cannot monitor multiple cameras simultaneously.
- **Planned**: Grid view for multiple live feeds.
- **Timeline**: Future release.

### Recording Search and Tagging
- **Current State**: Basic file listing.
- **Impact**: Hard to find specific events in recordings.
- **Planned**: Metadata tagging, search by date/time/camera.
- **Timeline**: Future release.

### API Rate Limiting
- **Current State**: No rate limiting on API endpoints.
- **Impact**: Potential DoS from local network.
- **Planned**: Implement rate limiting in FastAPI.
- **Timeline**: Future release.

### HTTPS Support
- **Current State**: HTTP only.
- **Impact**: Insecure for local access over untrusted networks.
- **Planned**: Self-signed certificates or Let's Encrypt for local domains.
- **Timeline**: Future release.

## Known Limitations

- **USB Camera Support**: Partially implemented; may not work with all devices.
- **ONVIF Discovery**: Basic discovery; some cameras may not be detected.
- **Recording Formats**: Only AVI; MP4 support pending.
- **Storage**: No deduplication or compression beyond codec.
- **Scalability**: Tested with up to 4 cameras; higher counts may require optimization.

## Contributing

If you're interested in implementing any of these features, see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines. Please open an issue first to discuss your approach.