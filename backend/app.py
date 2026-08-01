import time
import logging
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import Config
from routes.api import router
from firebase.firebase import db_client
from firebase.listener import DatabaseListener
from agents.supervisor import execute_agent_workflow

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("smartbio_app")

app = FastAPI(
    title="Smart BIO AIR v2.0 AI Backend",
    description="Multi-agent supervisor system for algae bioreactors and air purification systems.",
    version="2.0.0"
)

# Set CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow development frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# Callback invoked when a new telemetry reading is written to the database
def on_telemetry_received(measurement_id: str, telemetry_data: dict = None):
    if not telemetry_data:
        return
    
    logger.info(f"New telemetry triggering AI analysis workflow for timestamp: {measurement_id}")
    
    # Read history to compute growth rates and variations
    history = db_client.get_history(limit=20)
    
    # Run the supervisor LangGraph workflow
    try:
        final_state = execute_agent_workflow(telemetry_data, history)
        
        # Write results back to Firebase paths
        db_client.write_data(f"analysis/{measurement_id}", final_state.get("analytics"))
        db_client.write_data("predictions", final_state.get("predictions"))
        db_client.write_data("recommendations", final_state.get("recommendations"))
        db_client.write_data("alerts", final_state.get("anomalies"))
        db_client.write_data("reports", final_state.get("reports"))
        db_client.write_data("agent_logs", final_state.get("agent_logs"))
        
        logger.info("Successfully updated analysis, predictions, alerts, and recommendations.")
    except Exception as e:
        logger.error(f"Failed to run multi-agent workflow: {e}")

# Global database listener reference
listener = DatabaseListener(on_telemetry_received)

def seed_initial_data_if_empty():
    """Seeds mock telemetry data if database has no entries, so the dashboard starts with metrics."""
    latest = db_client.get_latest_telemetry()
    if not latest:
        logger.info("Database is empty. Seeding simulated historical entries...")
        now = time.time()
        # Seed 10 historical points (5-second intervals for speed)
        for i in range(10):
            ts = now - (10 - i) * 60 # 1 minute increments
            sim_telemetry = {
                "algae": {
                    "green_idx": round(0.4 + i * 0.05, 3), # increasing density
                    "health": round(80.0 + i * 1.5, 1),
                    "light_lux": round(1500.0 + 100 * (i % 3), 1),
                    "temp_c": round(21.0 + (i % 4) * 0.5, 1)
                },
                "env": {
                    "altitude": 150.0,
                    "pressure": round(1012.5 + i * 0.1, 1)
                },
                "gas": {
                    "mq135": round(180.0 - i * 5.0, 1), # declining gases as algae grows
                    "mq2": round(42.0 - i * 0.5, 1),
                    "mq3": 25.0,
                    "mq7": round(35.0 - i * 1.0, 1)
                },
                "motor": {
                    "status": "ON",
                    "speed": 60.0,
                    "flow_rate": 2.4,
                    "operating_hours": round(120.0 + i * 0.1, 1)
                },
                "timestamp": ts
            }
            # Push directly and invoke workflow on it to pre-populate analysis database
            db_client.write_data(f"bio_monitor/{int(ts)}", sim_telemetry)
            on_telemetry_received(str(int(ts)), sim_telemetry)

@app.on_event("startup")
def startup_event():
    seed_initial_data_if_empty()
    listener.start()
    
    # Start a background thread that injects simulated telemetry every 10 seconds 
    # to keep the dashboard dynamic and active if no live ESP32 is writing.
    if db_client.mode == "local" or True: # Enable simulator for high-fidelity demonstration
        threading.Thread(target=run_telemetry_simulation, daemon=True).start()

@app.on_event("shutdown")
def shutdown_event():
    listener.stop()

def run_telemetry_simulation():
    """Generates continuous bioreactor sensor telemetry every 15 seconds."""
    logger.info("Starting telemetry simulation background worker...")
    time.sleep(5.0) # wait for startup
    
    # Base configuration for simulations
    green_index = 0.8
    operating_hours = 120.5
    
    while True:
        try:
            # Let's read current motor speed from motor control
            m_ctrl = db_client.read_data("motor_control") or {}
            status = m_ctrl.get("status", "ON")
            speed = m_ctrl.get("speed", 60.0)
            
            # If emergency stop is triggered, turn speed to 0 and status to OFF
            if m_ctrl.get("emergency_stop", False):
                status = "OFF"
                speed = 0.0
                
            flow = round(speed * 0.04, 2)
            operating_hours += 0.005 # increment operating time
            
            # Algae indices fluctuate depending on light
            import random
            temp = round(22.0 + random.uniform(-1.5, 1.5), 1)
            lux = round(1200.0 + random.uniform(-400, 400), 1)
            
            # Green index grows if light is present and temp is moderate
            if lux > 500 and 18 < temp < 28:
                green_index = min(2.5, green_index + random.uniform(0.002, 0.008))
            else:
                green_index = max(0.1, green_index - random.uniform(0.001, 0.005))
                
            # Gas levels decline as biomass increases (carbon uptake)
            gi = round(green_index, 3)
            mq135 = round(max(80.0, 220.0 - (gi * 45.0) + random.uniform(-5, 5)), 1)
            mq7 = round(max(10.0, 40.0 - (gi * 8.0) + random.uniform(-2, 2)), 1)
            
            telemetry = {
                "algae": {
                    "green_idx": gi,
                    "health": 85.0, # Will be recalculated by Algae health agent
                    "light_lux": lux,
                    "temp_c": temp
                },
                "env": {
                    "altitude": 150.0,
                    "pressure": round(1013.2 + random.uniform(-0.5, 0.5), 1)
                },
                "gas": {
                    "mq135": mq135,
                    "mq2": round(35.0 + random.uniform(-2, 2), 1),
                    "mq3": round(20.0 + random.uniform(-1, 1), 1),
                    "mq7": mq7
                },
                "motor": {
                    "status": status,
                    "speed": speed,
                    "flow_rate": flow,
                    "operating_hours": round(operating_hours, 2)
                },
                "timestamp": time.time()
            }
            
            # Write to database (will trigger callback)
            db_client.push_telemetry(telemetry)
            
        except Exception as e:
            logger.error(f"Simulator loop error: {e}")
            
        time.sleep(15.0) # telemetries every 15 seconds
