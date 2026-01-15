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
import functools

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

def is_contour_in_zone(contour, zone, frame_shape):
    h, w = frame_shape[:2]
    x = int(zone['x'] * w)
    y = int(zone['y'] * h)
    width = int(zone['width'] * w)
    height = int(zone['height'] * h)
    zone_rect = (x, y, x + width, y + height)
    
    # Get bounding box of contour
    x1, y1, w_cont, h_cont = cv2.boundingRect(contour)
    x2, y2 = x1 + w_cont, y1 + h_cont
    contour_rect = (x1, y1, x2, y2)
    
    # Check overlap
    return not (x2 < zone_rect[0] or x1 > zone_rect[2] or y2 < zone_rect[1] or y1 > zone_rect[3])

def detect_motion(url, name, channel, config):
    zones = config.get('motion_zones', {}).get(name, [])
    if not zones:
        logger.warning(f"No motion zones defined for camera {name}")
        return
    
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        logger.error(f"Cannot open camera {name}")
        return

    ret, frame1 = cap.read()
    if not ret:
        logger.error(f"Cannot read first frame for {name}")
        cap.release()
        return
    ret, frame2 = cap.read()
    if not ret:
        logger.error(f"Cannot read second frame for {name}")
        cap.release()
        return
    
    base_threshold = 5000  # Configurable?
    
    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        detected_zones = []
        for i, zone in enumerate(zones):
            zone_threshold = base_threshold * zone.get('sensitivity', 1.0)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < zone_threshold:
                    continue
                if is_contour_in_zone(contour, zone, frame1.shape):
                    detected_zones.append(i)
                    break
        
        if detected_zones:
            message = json.dumps({'type': 'motion_detected', 'camera': name, 'zones': detected_zones, 'timestamp': time.time()})
            channel.basic_publish(exchange='events', routing_key='', body=message)
            logger.info(f"Motion detected on {name} in zones {detected_zones}")
        
        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break
        time.sleep(0.1)
    cap.release()

motion_threads = {}

def callback(ch, method, properties, body, config):
    data = json.loads(body)
    camera_name = data['camera']
    if data['type'] == 'camera_online':
        if camera_name not in motion_threads or not motion_threads[camera_name].is_alive():
            motion_threads[camera_name] = threading.Thread(target=detect_motion, args=(data['url'], camera_name, ch, config))
            motion_threads[camera_name].start()
    elif data['type'] == 'camera_offline':
        # The thread will stop naturally when stream fails
        pass

def main():
    try:
        config = load_config()
        event_bus_url = os.getenv('EVENT_BUS_URL', 'amqp://guest:guest@localhost:5672/')

        logger.info("Starting motion service...")
        logger.info(f"Event bus URL: {event_bus_url}")

        # Connect to event bus
        connection = pika.BlockingConnection(pika.URLParameters(event_bus_url))
        logger.info("Event bus connection established")
        channel = connection.channel()
        channel.exchange_declare(exchange='events', exchange_type='fanout')

        # Consume events
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='events', queue=queue_name)

        channel.basic_consume(queue=queue_name, on_message_callback=functools.partial(callback, config=config), auto_ack=True)

        logger.info("Motion service running.")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Motion service error: {e}")
    finally:
        try:
            connection.close()
        except:
            pass
        logger.info("Motion service stopped")

if __name__ == "__main__":
    main()