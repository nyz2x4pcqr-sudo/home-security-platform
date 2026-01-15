# Commercial Appliance Alignment

## Introduction

The Home Security Platform is designed as a commercial appliance for plug-and-play home security monitoring. This document outlines procedures for factory reset, branding guidance, and hardware integration notes, with a focus on user-controlled setup and plug-and-play functionality.

## Factory Reset Procedures

Factory reset restores the appliance to its original state, removing all user data and configurations.

### User-Controlled Reset via Web UI

1. Access the web UI at `http://<server-ip>:8080` (replace `<server-ip>` with the appliance's IP address).
2. Log in using the default admin credentials (username: `admin`, password: `admin`).
3. Navigate to **Settings** > **Maintenance**.
4. Click the **Factory Reset** button and confirm the action.

This method provides a user-friendly, controlled reset process without requiring command-line access.

### Command-Line Reset

For advanced users or when UI access is unavailable, use the installation script with the reset flag:

- On Linux/Mac: `./install.sh --reset`
- On Windows: `install.bat --reset`

This script performs the following actions:
- Stops all running services
- Removes Docker containers and volumes
- Deletes user configuration files (`config/default.yml` and `.env`)
- Recreates configuration files from example templates
- Restarts the system in a clean state

**Warning**: This process permanently deletes all recorded footage, camera configurations, and user data. Back up important data before proceeding.

## Branding Guidance

The platform adheres to open-source branding principles while allowing customization for commercial deployments.

### Customization Options

- **Logo**: Replace the default logo file (`web-ui/logo.png`) with your custom logo image.
- **Color Scheme**: Modify theme colors by editing `web-ui/style.css` with CSS variable overrides.
- **Branding Elements**: Add reseller-specific text or images without altering core application code.

### Principles for Commercial Alignment

- Maintain open-source branding integrity in the base software.
- Enable white-labeling for resellers through non-invasive customization.
- Ensure all branding changes are reversible and do not impact core functionality.
- Provide clear documentation for customization to avoid support issues.

## Hardware Integration Notes

The Home Security Platform is optimized for plug-and-play deployment on commercial hardware.

### Preconfigured Hardware Specifications

Commercial appliances are shipped with:
- Operating System: Ubuntu Server 22.04+ or Debian 11+ (x86_64 or ARM64)
- Storage: 500GB+ SSD for recordings and system data
- Network: Gigabit Ethernet port for camera connectivity
- Pre-installed Software: Docker and Docker Compose for containerized services

### Plug-and-Play Setup Process

1. Connect the appliance to power and Ethernet (DHCP for automatic IP assignment).
2. Power on the device; services start automatically within 2-3 minutes.
3. Access the web UI at the assigned IP address for initial configuration.
4. Follow the setup wizard to complete basic configuration.

No additional hardware setup is required beyond power and network connection.

### User-Controlled Configuration and Integration

- **Camera Integration**: Users add cameras via the web UI, either manually (RTSP URL) or through ONVIF auto-discovery.
- **System Settings**: Configure recording options, motion detection zones, and user management through the intuitive web interface.
- **Advanced Configuration**: Edit `config/default.yml` for fine-tuning (e.g., storage retention, network settings).
- **Monitoring**: Real-time status dashboard shows camera connectivity, storage usage, and system health.

Hardware integration focuses on minimal user intervention while providing comprehensive control options.