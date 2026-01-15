# Home Security Platform API Documentation

The Home Security Platform provides a REST API for programmatic access to system functionality. The API is built with FastAPI and runs on port 8000 by default.

## Authentication

All API endpoints (except health check) require HTTP Basic Authentication.

- **Username/Password**: As configured in `config/default.yml` (default: admin/admin)
- **Header**: `Authorization: Basic <base64-encoded-credentials>`

## Base URL

```
http://<server-ip>:8000
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "ok"
}
```

### Cameras

#### GET /cameras

Retrieve list of configured cameras.

**Authentication:** Required

**Response:**
```json
{
  "cameras": [
    {
      "name": "Front Door",
      "url": "rtsp://...",
      "type": "rtsp"
    }
  ]
}
```

#### POST /cameras

Add a new camera.

**Authentication:** Required

**Request Body:**
```json
{
  "name": "New Camera",
  "url": "rtsp://camera-url",
  "type": "rtsp"
}
```

**Response:**
```json
{
  "message": "Camera added"
}
```

#### DELETE /cameras/{camera_name}

Delete a camera by name.

**Authentication:** Required

**Parameters:**
- `camera_name` (path): Name of the camera to delete

**Response:**
```json
{
  "message": "Camera deleted"
}
```

### Events

#### GET /events

Retrieve recent events (currently returns empty list; event storage not yet implemented).

**Authentication:** Required

**Response:**
```json
{
  "events": []
}
```

### Recordings

#### GET /recordings

List available video recordings.

**Authentication:** Required

**Response:**
```json
{
  "recordings": [
    "camera1_2023-01-01_12-00-00.avi",
    "camera2_2023-01-01_12-05-00.avi"
  ]
}
```

## Error Responses

All errors return JSON with appropriate HTTP status codes:

```json
{
  "detail": "Error description"
}
```

Common status codes:
- `401`: Invalid credentials
- `404`: Resource not found
- `500`: Internal server error

## Notes

- Configuration changes via API are not persisted yet; they apply only to the current session.
- Event system is not fully implemented; events are not stored or retrievable.
- For production use, consider enabling HTTPS and additional security measures.