#!/usr/bin/env python3

import os
import logging
import pika
import yaml
from time import sleep
import cv2
import threading
import json
import time
from datetime import datetime

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

def record_video(url, name, recordings_path, duration=30):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        logger.error(f"Cannot open camera {name} for recording")
        return
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{recordings_path}/{name}_{timestamp}.avi"
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640,480))
    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    out.release()
    cap.release()
    logger.info(f"Recording saved: {filename}")

def record_continuous(url, name, recordings_path, segment_duration=300):
    while True:
        record_video(url, name, recordings_path, duration=segment_duration)
        sleep(1)  # Short pause between segments

def callback(ch, method, properties, body, cameras, recordings_path, recording_config):
    data = json.loads(body)
    if data['type'] == 'motion_detected':
        url = cameras.get(data['camera'])
        if url and recording_config.get('event_triggered', True):
            duration = recording_config.get('duration', 30)
            threading.Thread(target=record_video, args=(url, data['camera'], recordings_path, duration)).start()

def main():
    try:
        config = load_config()
        event_bus_url = os.getenv('EVENT_BUS_URL', 'amqp://guest:guest@localhost:5672/')
        recordings_path = os.getenv('RECORDINGS_PATH', '/data/recordings')
        os.makedirs(recordings_path, exist_ok=True)

        logger.info("Starting recorder service...")
        logger.info(f"Event bus URL: {event_bus_url}")

        # Connect to event bus
        connection = pika.BlockingConnection(pika.URLParameters(event_bus_url))
        logger.info("Event bus connection established")
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='fanout')

        cameras = {c['name']: c['url'] for c in config.get('cameras', [])}
        recording_config = config.get('recording', {})

        # Start continuous recording if enabled
        if recording_config.get('continuous', False):
            for name, url in cameras.items():
                threading.Thread(target=record_continuous, args=(url, name, recordings_path)).start()
                logger.info(f"Started continuous recording for {name}")

        # Consume events
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='events', queue=queue_name)

        channel.basic_consume(queue=queue_name, on_message_callback=lambda ch, method, properties, body: callback(ch, method, properties, body, cameras, recordings_path, recording_config), auto_ack=True)

        logger.info("Recorder service running.")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Recorder service error: {e}")
    finally:
        try:
            connection.close()
        except:
            pass
        logger.info("Recorder service stopped")

if __name__ == "__main__":
    main()