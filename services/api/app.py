#!/usr/bin/env python3

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os
import yaml
import logging
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    config = load_config()
    users = config.get('users', [])
    for user in users:
        if user['username'] == credentials.username and verify_password(credentials.password, user['password_hash']):
            return user
    raise HTTPException(status_code=401, detail="Invalid credentials")

app = FastAPI(title="Home Security API")

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

@app.get("/")
def read_root():
    return {"message": "Home Security API"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Placeholder for more endpoints
@app.get("/cameras", dependencies=[Depends(authenticate)])
def get_cameras():
    config = load_config()
    return {"cameras": config.get('cameras', [])}

@app.post("/cameras", dependencies=[Depends(authenticate)])
def add_camera(camera: dict):
    # Note: In real implementation, persist to config file or database
    config = load_config()
    if 'cameras' not in config:
        config['cameras'] = []
    config['cameras'].append(camera)
    # For demo, just return success
    return {"message": "Camera added"}

@app.delete("/cameras/{camera_name}", dependencies=[Depends(authenticate)])
def delete_camera(camera_name: str):
    config = load_config()
    cameras = config.get('cameras', [])
    config['cameras'] = [c for c in cameras if c.get('name') != camera_name]
    # Persist
    return {"message": "Camera deleted"}

@app.get("/events", dependencies=[Depends(authenticate)])
def get_events():
    return {"events": []}

@app.get("/recordings", dependencies=[Depends(authenticate)])
def get_recordings():
    import os
    recordings_path = os.getenv('DATA_PATH', '/data')
    recordings_dir = os.path.join(recordings_path, 'recordings')
    if os.path.exists(recordings_dir):
        recordings = os.listdir(recordings_dir)
        return {"recordings": recordings}
    else:
        return {"recordings": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)