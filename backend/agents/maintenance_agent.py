import time
from typing import Dict, Any

def run_maintenance_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    quality_score = state.get("sensor_quality_score", 100.0)
    
    motor = telemetry.get("motor", {})
    operating_hours = motor.get("operating_hours", 0.0)
    
    # Motor calculations
    # Max motor lifetime is 5000 hours.
    motor_health = max(0.0, 100.0 - (operating_hours / 5000.0) * 100.0)
    motor_health = round(motor_health, 1)
    
    rul_hours = max(0.0, 5000.0 - operating_hours)
    rul_hours = round(rul_hours, 1)
    
    # Cleaning schedules
    # Recommend cleaning every 15 days or if green index gets too high and limits light lux.
    # We estimate cleaning cycle from operating hours modulo 360 (15 days)
    hours_since_clean = operating_hours % 360.0
    days_to_clean = max(0.0, (360.0 - hours_since_clean) / 24.0)
    days_to_clean = round(days_to_clean, 1)
    
    # Calibration indicator
    calibration_due = "No"
    if quality_score < 85.0:
        calibration_due = "IMMEDIATE"
    elif quality_score < 92.0:
        calibration_due = "RECOMMENDED"
        
    maintenance = {
        "motor_health": motor_health,
        "remaining_useful_life_hours": rul_hours,
        "days_until_next_cleaning": days_to_clean,
        "sensor_calibration_due": calibration_due,
        "next_pump_servicing_hours": round(max(0.0, 3000.0 - (operating_hours % 3000.0)), 1)
    }
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Maintenance Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 92.0,
        "latest_decision": f"Motor health estimated at {motor_health}%. Cleaning due in {days_to_clean} days.",
        "reasoning": f"Based on {operating_hours} total motor run-hours. Sensor quality is at {quality_score}%."
    }
    
    return {
        "maintenance": maintenance,
        "agent_logs": [agent_log]
    }
