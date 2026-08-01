import os
import json
import time
import logging
import requests
from typing import Dict, List, Any, Optional
from config import Config

logger = logging.getLogger("smartbio_firebase")
logging.basicConfig(level=logging.INFO)

class FirebaseClient:
    def __init__(self):
        self.db_url = Config.FIREBASE_DATABASE_URL.rstrip("/")
        self.mode = Config.DATABASE_MODE.lower()
        self.local_db_path = Config.LOCAL_DB_PATH
        
        # Test connection if in Firebase mode
        if self.mode == "firebase":
            try:
                # Attempt a quick light check
                res = requests.get(f"{self.db_url}/.json?shallow=true", timeout=3.0)
                if res.status_code == 200:
                    logger.info("Successfully connected to Firebase Realtime Database.")
                else:
                    logger.warning(f"Firebase connection returned status {res.status_code}. Falling back to local mode.")
                    self.mode = "local"
            except Exception as e:
                logger.warning(f"Failed to connect to Firebase ({e}). Falling back to local mode.")
                self.mode = "local"
        
        if self.mode == "local":
            logger.info(f"Operating in LOCAL DATABASE MODE. Data path: {self.local_db_path}")
            self._init_local_db()

    def _init_local_db(self):
        if not os.path.exists(self.local_db_path):
            # Seed with default initial structures
            initial_data = {
                "bio_monitor": {},
                "analysis": {},
                "predictions": {},
                "recommendations": {},
                "alerts": {},
                "reports": {},
                "motor_control": {
                    "status": "OFF",
                    "speed": 0.0,
                    "flow_rate": 0.0,
                    "emergency_stop": False,
                    "last_update": time.time()
                }
            }
            with open(self.local_db_path, "w") as f:
                json.dump(initial_data, f, indent=4)

    def _read_local(self) -> Dict[str, Any]:
        try:
            with open(self.local_db_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading local DB file: {e}")
            return {}

    def _write_local(self, data: Dict[str, Any]):
        try:
            with open(self.local_db_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error writing local DB file: {e}")

    def write_data(self, path: str, data: Any) -> bool:
        """Writes data to a path. E.g. path='analysis/measurement_1'"""
        if self.mode == "firebase":
            try:
                res = requests.put(f"{self.db_url}/{path}.json", json=data, timeout=5.0)
                if res.status_code in (200, 201):
                    return True
                logger.error(f"Firebase PUT error to {path}: {res.text}")
            except Exception as e:
                logger.error(f"Firebase PUT failed: {e}")
        
        # Local fallback/mode
        parts = path.strip("/").split("/")
        db = self._read_local()
        current = db
        for part in parts[:-1]:
            if part not in current or not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
        current[parts[-1]] = data
        self._write_local(db)
        return True

    def read_data(self, path: str) -> Any:
        """Reads data from a path."""
        if self.mode == "firebase":
            try:
                res = requests.get(f"{self.db_url}/{path}.json", timeout=5.0)
                if res.status_code == 200:
                    return res.json()
                logger.error(f"Firebase GET error from {path}: {res.text}")
            except Exception as e:
                logger.error(f"Firebase GET failed: {e}")
                
        # Local fallback/mode
        parts = path.strip("/").split("/")
        db = self._read_local()
        current = db
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current

    def push_telemetry(self, telemetry: Dict[str, Any]) -> str:
        """Pushes new telemetry to bio_monitor and returns the ID."""
        measurement_id = str(int(telemetry.get("timestamp", time.time())))
        self.write_data(f"bio_monitor/{measurement_id}", telemetry)
        return measurement_id

    def get_latest_telemetry(self) -> Optional[Dict[str, Any]]:
        """Returns the most recent telemetry measurement."""
        data = self.read_data("bio_monitor")
        if not data:
            return None
        
        # Sort by key (timestamp)
        try:
            sorted_keys = sorted(data.keys(), key=lambda x: float(x))
            return data[sorted_keys[-1]]
        except Exception as e:
            logger.error(f"Failed to parse latest telemetry keys: {e}")
            # Try to return any values
            if isinstance(data, dict):
                return list(data.values())[-1]
            return None

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns a list of recent telemetry entries sorted by timestamp."""
        data = self.read_data("bio_monitor")
        if not data or not isinstance(data, dict):
            return []
        
        try:
            sorted_keys = sorted(data.keys(), key=lambda x: float(x))
            recent_keys = sorted_keys[-limit:]
            return [data[k] for k in recent_keys]
        except Exception as e:
            logger.error(f"Failed to sort telemetry history: {e}")
            return list(data.values())[-limit:]

# Singleton client instance
db_client = FirebaseClient()
