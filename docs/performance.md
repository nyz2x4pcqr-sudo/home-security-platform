# Performance Tuning Guide

This guide helps optimize the Home Security Platform for your hardware and use case. Performance depends on CPU, RAM, storage, and camera count.

## Hardware Recommendations

### Minimum Requirements
- **CPU**: 2 cores (Intel i3 or equivalent)
- **RAM**: 4GB
- **Storage**: 500GB SSD
- **Network**: Gigabit Ethernet
- **Cameras**: 1-2

*Example: Raspberry Pi 4 (4GB)*

### Recommended Setup
- **CPU**: 4+ cores (Intel i5 or equivalent)
- **RAM**: 8GB+
- **Storage**: 1TB+ NVMe SSD
- **Network**: Gigabit Ethernet
- **Cameras**: 4-8

*Example: Intel NUC or mini PC*

### Performance Scaling

| Hardware | Max Cameras | Notes |
|----------|-------------|--------|
| RPi 4 (4GB) | 2 | Disable continuous recording |
| Intel NUC (8GB) | 6 | Monitor CPU usage |
| Server (16GB+) | 10+ | Scale horizontally if needed |

## Monitoring Performance

### Check System Resources

```bash
# Container resource usage
docker stats

# CPU and memory
htop

# Disk I/O
iotop

# Network
iptraf
```

### Service Logs

Monitor for performance warnings:
```bash
docker-compose logs motion  # CPU usage
docker-compose logs recorder  # I/O bottlenecks
```

## Tuning Configuration

### Camera Settings

Reduce load by optimizing camera configuration:

- **Resolution**: 720p instead of 1080p
- **Frame Rate**: 15-20 FPS instead of 30
- **Bitrate**: Lower for RTSP streams
- **Motion Zones**: Limit to relevant areas

### Motion Detection

In `config/default.yml`:

```yaml
motion_zones:
  "Camera 1":
    - x: 0.1
      y: 0.1
      width: 0.8
      height: 0.8
      sensitivity: 0.7  # Lower = less sensitive, less CPU
```

- Smaller zones = less processing
- Higher sensitivity threshold = fewer false positives but more CPU

### Recording Settings

```yaml
recording:
  continuous: false  # Disable if event-only recording
  resolution: "720p"
  retention_days: 14  # Shorter retention = less storage
```

Disable continuous recording if you only need event-triggered clips.

## Storage Optimization

### SSD Required

- HDD too slow for video I/O
- SSD recommended for all storage

### Storage Layout

```
/opt/home-security/
├── data/recordings/     # Large, fast storage
├── config/              # Small, persistent
└── logs/                # Optional, can be on slower storage
```

### Cleanup

Automatic cleanup runs daily. Configure retention:

```yaml
recording:
  retention_days: 30
```

Manual cleanup:
```bash
# Find old files
find /opt/home-security/data/recordings -mtime +30 -type f

# Delete old recordings
find /opt/home-security/data/recordings -mtime +30 -type f -delete
```

## Network Optimization

### Ethernet First

- Wireless adds latency and unreliability
- Use wired cameras when possible

### Bandwidth Considerations

- 1080p/30fps: ~5-10 Mbps per camera
- 720p/15fps: ~2-5 Mbps per camera
- Total bandwidth: cameras × bitrate

### Docker Networking

Services use bridge network. For high throughput:
```yaml
networks:
  home-security:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-home-security
```

## CPU Optimization

### Disable Unneeded Features

- Auto-discovery: Set `auto_discover: false` if not needed
- Continuous recording: Disable for event-only
- Motion detection: Tune zones to minimize processing

### Container Limits

Limit CPU per service in `docker-compose.yml`:

```yaml
services:
  motion:
    deploy:
      resources:
        limits:
          cpus: '0.5'  # Limit to 50% of one core
```

### Profiling

Use Python profilers for bottlenecks:

```bash
# In container
pip install py-spy
py-spy top --pid $(pgrep -f motion)
```

## Memory Optimization

### Container Memory Limits

```yaml
services:
  motion:
    deploy:
      resources:
        limits:
          memory: 512M
```

### Swap Space

Add swap for memory spikes:
```bash
# Create 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Scaling Horizontally

For high camera counts:

1. **Separate Appliances**: Run multiple instances on different hardware
2. **Load Balancing**: Distribute cameras across appliances
3. **Shared Storage**: Use NFS for centralized recordings

## Troubleshooting Performance Issues

### High CPU

- Reduce camera resolution/FPS
- Tune motion sensitivity
- Check for background processes

### High Memory

- Monitor with `docker stats`
- Add swap or increase RAM
- Reduce concurrent streams

### Slow Recordings

- Check disk I/O: `iostat -x 1`
- Use faster SSD
- Reduce recording quality

### Network Issues

- Test bandwidth: `iperf`
- Check for network congestion
- Use QoS for camera traffic

## Benchmarking

### Test Setup

1. Add cameras incrementally
2. Monitor resources: `docker stats`
3. Test motion detection responsiveness
4. Check recording quality

### Performance Metrics

- **CPU Usage**: <70% average
- **Memory**: <80% of available
- **Disk I/O**: <50MB/s sustained
- **Network**: <70% of bandwidth

## Advanced Tuning

### Kernel Parameters

For video processing:
```bash
# Increase shared memory
echo 'kernel.shmmax=2147483648' >> /etc/sysctl.conf
sysctl -p
```

### Docker Optimization

Use overlay2 storage driver:
```json
{
  "storage-driver": "overlay2"
}
```

### GPU Acceleration (Future)

OpenCV can use GPU; planned for future releases.

For more help, see [FAQ](faq.md) or open an issue.