#!/usr/bin/env python3

import logging
import cv2
import json
import time

logger = logging.getLogger(__name__)

class CameraMonitor:
    def __init__(self, channel):
        self.channel = channel
        self.camera_status = {}  # camera_name: bool (online True/False)

    def validate_stream(self, camera):
        """Validate camera stream using OpenCV."""
        try:
            if camera['type'] == 'usb':
                cap = cv2.VideoCapture(camera['device'])
            else:  # rtsp or onvif
                cap = cv2.VideoCapture(camera.get('url', camera.get('rtsp_url', '')))

            if not cap.isOpened():
                return False

            # Try to read a frame
            ret, frame = cap.read()
            cap.release()
            return ret and frame is not None
        except Exception as e:
            logger.error(f"Error validating stream for {camera['name']}: {e}")
            return False

    def check_camera(self, camera):
        """Check camera status and publish events if changed."""
        is_online = self.validate_stream(camera)
        last_status = self.camera_status.get(camera['name'], None)

        if last_status != is_online:
            self.camera_status[camera['name']] = is_online
            event_type = 'camera_online' if is_online else 'camera_offline'
            message = json.dumps({
                'type': event_type,
                'camera': camera['name'],
                'url': camera.get('url', camera.get('rtsp_url', '')),
                'timestamp': time.time()
            })
            self.channel.basic_publish(exchange='events', routing_key='', body=message)
            logger.info(f"Camera {camera['name']} {event_type}")
        elif not is_online:
            logger.debug(f"Camera {camera['name']} still offline")
        else:
            logger.debug(f"Camera {camera['name']} still online")