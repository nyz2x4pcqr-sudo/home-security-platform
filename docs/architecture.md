# Home Security Platform Architecture

## Overview

The Home Security Platform is a modular, local-only system designed to provide home security functionality without cloud dependencies. It runs on Linux (Ubuntu Server LTS or Debian) with support for x86_64 and ARM architectures. The system uses Docker and Docker Compose for containerization, ensuring portability and ease of deployment.

## Core Principles

- **100% Local Operation**: All data and processing occur on the local appliance; no internet connectivity required.
- **Open-Source and Auditable**: Code is inspectable and modifiable; permissive licensing.
- **Simple Setup**: One-command installation for non-technical users.
- **Reliability**: Proven technologies, explicit configurations, CPU-only processing.
- **Commercial Viability**: Monetization through hardware sales.

## Service Architecture

The platform is composed of modular microservices, each with clear responsibilities. Services communicate via HTTP REST APIs and an event-driven message bus for decoupling.

### Services

- **ingest**: Handles camera discovery and ingestion.
  - Discovers ONVIF cameras on the local network.
  - Ingests RTSP streams from configured cameras.
  - Publishes camera online/offline events to the event-bus.
  - Technologies: Python with libraries for RTSP/ONVIF.

- **recorder**: Manages video recording.
  - Receives video streams from ingest.
  - Performs continuous recording and event-triggered recording (e.g., on motion).
  - Stores footage on local SSD.
  - Technologies: Python with FFmpeg or OpenCV for processing.

- **motion**: Detects motion in video streams.
  - Processes frames from recorder or directly from ingest.
  - Uses basic motion detection algorithms with configurable zones.
  - Publishes motion events to event-bus.
  - Technologies: Python with OpenCV.

- **event-bus**: Central event management.
  - Acts as a message broker for events.
  - Decouples producers and consumers.
  - Technologies: RabbitMQ or Redis pub/sub.

## Event Types

The event bus uses JSON-formatted messages with the following types:

- **camera_online**: Published by ingest service when a camera stream becomes available.
  - Fields: `type`, `camera` (name), `url`, `timestamp` (Unix epoch time)
- **camera_offline**: Published by ingest service when a camera stream becomes unavailable.
  - Fields: `type`, `camera` (name), `url`, `timestamp` (Unix epoch time)
- **motion_detected**: Published by motion service when motion is detected in configured zones.
  - Fields: `type`, `camera` (name), `zones` (list of zone indices), `timestamp` (Unix epoch time)

- **api**: Backend API.
  - Provides REST endpoints for configuration, authentication, and data retrieval.
  - Handles user management (admin/viewer roles).
  - Technologies: FastAPI (Python) or Go.

- **web-ui**: Local web interface.
  - Serves a responsive UI for dashboard, live view, timeline, camera management.
  - Includes initial setup wizard and auto-discovery.
  - No external assets; runs locally.
  - Technologies: React (minimal) or plain HTML/JS; served via Nginx or directly from api.

### Inter-Service Communication

- **REST APIs**: Synchronous calls between services (e.g., web-ui queries api for data).
- **Event Bus**: Asynchronous events (e.g., ingest publishes to event-bus, recorder subscribes).
- **Shared Volumes**: For video storage and configuration files.

## Data Flow

1. Cameras connect via RTSP/ONVIF.
2. ingest discovers and pulls streams.
3. recorder stores continuous footage and listens for events.
4. motion analyzes frames and detects motion.
5. Events are published to event-bus.
6. api aggregates data and serves UI.
7. web-ui provides user interaction.

## Architecture Diagram

```
+----------------+     +----------------+     +----------------+
|     Cameras    | --> |     ingest     | --> |   recorder     |
+----------------+     +----------------+     +----------------+
                              |                        |
                              v                        v
                       +----------------+     +----------------+
                       |     motion     |     |   event-bus    |
                       +----------------+     +----------------+
                              |                        |
                              v                        v
                       +----------------+     +----------------+
                       |      api       | <-- |    web-ui      |
                       +----------------+     +----------------+
```

## Storage

- Local SSD mounted as Docker volumes.
- Footage stored in H.264/MP4 format for efficient storage.
- Configuration in YAML/JSON files.

## Security Model

- **No Outbound Traffic**: Firewall rules to prevent internet access by default.
- **Local Authentication**: Password hashing with bcrypt or Argon2; token-based API auth.
- **Threat Model Assumptions**:
  - Appliance is physically secure.
  - Local network is trusted.
  - No remote access unless explicitly configured via local UI.
  - TLS can be enabled for local UI access over HTTPS.
- **Roles**: Admin (full access), Viewer (read-only).

## Appliance Hardening

- Run as non-root user in containers.
- Minimal base images (e.g., Alpine Linux).
- Factory reset: Script to wipe data and reset to defaults.
- Branding: Use open-source branding; allow custom skins without modifying core.

## Commercial Alignment

- Hardware: Preconfigured with Ubuntu Server, SSD, Ethernet.
- Monetization: Sell appliance hardware; software remains free.
- Support: Community-driven or paid support contracts.