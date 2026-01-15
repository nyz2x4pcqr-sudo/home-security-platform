#!/usr/bin/env python3

import os
import logging
import pika
import yaml
from time import sleep
import threading

from discovery import discover_cameras
from monitoring import CameraMonitor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    config_path = os.getenv('CONFIG_PATH', '/config/default.yml')
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.warning(f"Config file {config_path} not found, using defaults")
        return {}
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {}

def main():
    try:
        config = load_config()
        event_bus_url = os.getenv('EVENT_BUS_URL', 'amqp://guest:guest@localhost:5672/')

        logger.info("Starting ingest service...")
        logger.info(f"Event bus URL: {event_bus_url}")

        # Connect to event bus
        connection = pika.BlockingConnection(pika.URLParameters(event_bus_url))
        logger.info("Event bus connection established")
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='fanout')

        monitor = CameraMonitor(channel)

        # Load configured cameras
        cameras = config.get('cameras', [])

        # Discover additional cameras if enabled
        if config.get('auto_discover', False):
            discovered = discover_cameras()
            # Merge with configured, avoiding duplicates by name
            configured_names = {cam['name'] for cam in cameras}
            for cam in discovered:
                if cam['name'] not in configured_names:
                    cameras.append(cam)
                    logger.info(f"Auto-discovered camera: {cam['name']}")

        logger.info(f"Monitoring {len(cameras)} cameras")

        def check_all_cameras():
            for camera in cameras:
                try:
                    monitor.check_camera(camera)
                except Exception as e:
                    logger.error(f"Error checking camera {camera['name']}: {e}")

        # Initial check
        check_all_cameras()

        logger.info("Ingest service running.")

        while True:
            sleep(60)  # Check cameras periodically
            check_all_cameras()

    except Exception as e:
        logger.error(f"Ingest service error: {e}")
    finally:
        try:
            connection.close()
        except:
            pass
        logger.info("Ingest service stopped")

if __name__ == "__main__":
    main()