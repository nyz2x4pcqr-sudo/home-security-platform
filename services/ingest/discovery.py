#!/usr/bin/env python3

import logging
from wsdiscovery.discovery import ThreadedWSDiscovery as WSDiscovery
from onvif2 import ONVIFCamera
import cv2

logger = logging.getLogger(__name__)

def discover_onvif_cameras():
    """Discover ONVIF cameras on the network using WS-Discovery."""
    cameras = []
    try:
        wsd = WSDiscovery()
        wsd.start()
        services = wsd.searchServices()
        wsd.stop()

        for service in services:
            if 'onvif' in service.getXAddrs()[0].lower():
                ip_port = service.getXAddrs()[0].split('//')[1].split('/')[0]
                ip, port = ip_port.split(':')
                try:
                    cam = ONVIFCamera(ip, int(port), 'admin', 'admin')  # Default creds, may need config
                    media_service = cam.create_media_service()
                    profiles = media_service.GetProfiles()
                    rtsp_url = media_service.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken': profiles[0].token}).Uri
                    camera_info = {
                        'name': f'ONVIF_{ip}',
                        'type': 'onvif',
                        'ip': ip,
                        'port': port,
                        'rtsp_url': rtsp_url,
                        'onvif_url': f'http://{ip}:{port}/onvif/device_service'
                    }
                    cameras.append(camera_info)
                except Exception as e:
                    logger.warning(f"Failed to get details from ONVIF camera at {ip}:{port}: {e}")
    except Exception as e:
        logger.error(f"ONVIF discovery error: {e}")
    return cameras

def discover_usb_cameras():
    """Discover available USB cameras by testing device indices."""
    cameras = []
    for i in range(10):  # Test first 10 devices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append({
                'name': f'USB_{i}',
                'type': 'usb',
                'device': i
            })
            cap.release()
    return cameras

def discover_cameras(auto_discover=True):
    """Discover all cameras: ONVIF and USB if auto_discover is True."""
    cameras = []
    if auto_discover:
        logger.info("Starting camera discovery...")
        cameras.extend(discover_onvif_cameras())
        cameras.extend(discover_usb_cameras())
        logger.info(f"Discovered {len(cameras)} cameras")
    return cameras