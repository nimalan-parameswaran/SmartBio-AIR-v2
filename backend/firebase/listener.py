import threading
import time
import json
import logging
import requests
from sseclient import SSEClient
from firebase.firebase import db_client
from config import Config

logger = logging.getLogger("smartbio_listener")

class DatabaseListener:
    def __init__(self, callback_fn):
        self.callback_fn = callback_fn
        self.db_url = Config.FIREBASE_DATABASE_URL.rstrip("/")
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info("Database listener thread started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            logger.info("Database listener thread stopped.")

    def _run_loop(self):
        while self.running:
            if db_client.mode == "firebase":
                try:
                    logger.info("Connecting to Firebase Event Stream...")
                    stream_url = f"{self.db_url}/bio_monitor.json"
                    headers = {'Accept': 'text/event-stream'}
                    # Stream updates using sseclient
                    response = requests.get(stream_url, headers=headers, stream=True, timeout=30.0)
                    client = SSEClient(response)
                    
                    for event in client.events():
                        if not self.running:
                            break
                        
                        if event.event == 'put' or event.event == 'patch':
                            try:
                                payload = json.loads(event.data)
                                if not payload:
                                    continue
                                
                                # Firebase paths in event data
                                path = payload.get("path", "/")
                                data = payload.get("data")
                                
                                logger.info(f"Stream Event received: path={path}")
                                if path == "/" and isinstance(data, dict):
                                    # Full load or multiple entries
                                    for key, val in data.items():
                                        if isinstance(val, dict):
                                            self.callback_fn(key, val)
                                elif path.startswith("/") and len(path.split("/")) == 2:
                                    # Single entry written
                                    key = path.strip("/")
                                    if isinstance(data, dict):
                                        self.callback_fn(key, data)
                                elif path == "" or data is None:
                                    continue
                            except Exception as parse_err:
                                logger.error(f"Error parsing stream event: {parse_err}")
                except Exception as conn_err:
                    logger.error(f"Firebase stream connection error: {conn_err}. Reconnecting in 10s...")
                    time.sleep(10.0)
            else:
                # Local fallback polling
                # In local mode, the REST API or simulation script writes directly to `local_db.json`.
                # We can check if any new telemetry was added.
                last_checked_id = None
                while self.running and db_client.mode == "local":
                    try:
                        latest = db_client.get_latest_telemetry()
                        if latest:
                            ts = str(int(latest.get("timestamp", 0)))
                            if ts != last_checked_id:
                                logger.info(f"Local database update detected: measurement={ts}")
                                last_checked_id = ts
                                self.callback_fn(ts, latest)
                    except Exception as e:
                        logger.error(f"Error checking local DB: {e}")
                    time.sleep(3.0)
