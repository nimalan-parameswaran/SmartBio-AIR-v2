import time
from typing import Dict, List, Any

def evaluate_alerts(telemetry: Dict[str, Any], analytics: Dict[str, Any], quality_score: float) -> List[Dict[str, Any]]:
    alerts = []
    
    algae = telemetry.get("algae", {})
    gas = telemetry.get("gas", {})
    motor = telemetry.get("motor", {})
    
    temp_c = algae.get("temp_c", 22.0)
    health = algae.get("health", 100.0)
    light = algae.get("light_lux", 1000.0)
    
    mq135 = gas.get("mq135", 150.0)
    mq7 = gas.get("mq7", 30.0)
    
    motor_status = motor.get("status", "OFF")
    motor_speed = motor.get("speed", 0.0)
    motor_hours = motor.get("operating_hours", 0.0)
    
    now = time.time()
    
    # 1. Temperature Alerts
    if temp_c > 32.0:
        alerts.append({
            "id": f"temp_crit_{int(now)}",
            "type": "critical",
            "source": "Algae Temp Sensor",
            "message": f"Critical Overheating! Bioreactor water temperature at {temp_c}°C. Immediate cooling required.",
            "timestamp": now
        })
    elif temp_c > 28.0:
        alerts.append({
            "id": f"temp_warn_{int(now)}",
            "type": "warning",
            "source": "Algae Temp Sensor",
            "message": f"Algae heat stress detected. Temp is {temp_c}°C. Cooling recommended.",
            "timestamp": now
        })
    elif temp_c < 16.0:
        alerts.append({
            "id": f"temp_cold_{int(now)}",
            "type": "warning",
            "source": "Algae Temp Sensor",
            "message": f"Algae cold stress detected. Temp is {temp_c}°C. Heating recommended.",
            "timestamp": now
        })

    # 2. Algae Biological Health Alerts
    if health < 50.0:
        alerts.append({
            "id": f"algae_crit_{int(now)}",
            "type": "critical",
            "source": "Algae Health Agent",
            "message": f"Algae culture crash warning! Bio-health score has dropped to {health}%. Check parameters.",
            "timestamp": now
        })
    elif health < 75.0:
        alerts.append({
            "id": f"algae_warn_{int(now)}",
            "type": "warning",
            "source": "Algae Health Agent",
            "message": f"Algae stress warning. Health index decreased to {health}%. Inspect nutrients.",
            "timestamp": now
        })

    # 3. Gas / Air Quality Alerts
    if mq135 > 500.0:
        alerts.append({
            "id": f"gas_mq135_crit_{int(now)}",
            "type": "critical",
            "source": "Gas Sensor MQ135",
            "message": f"High CO2/Hazardous gas spike detected ({mq135} ppm). Ventilate room.",
            "timestamp": now
        })
    elif mq135 > 350.0:
        alerts.append({
            "id": f"gas_mq135_warn_{int(now)}",
            "type": "warning",
            "source": "Gas Sensor MQ135",
            "message": f"Moderate air quality index elevation ({mq135} ppm).",
            "timestamp": now
        })

    if mq7 > 120.0:
        alerts.append({
            "id": f"gas_mq7_crit_{int(now)}",
            "type": "critical",
            "source": "Gas Sensor MQ7",
            "message": f"DANGEROUS Carbon Monoxide level detected ({mq7} ppm)! Active alert.",
            "timestamp": now
        })

    # 4. Motor / Pump Alerts
    if motor_status == "ON" and motor_speed > 95.0:
        alerts.append({
            "id": f"motor_load_{int(now)}",
            "type": "warning",
            "source": "Pump Controller",
            "message": f"Pump motor operating at maximum speed ({motor_speed}%). Check for blockages.",
            "timestamp": now
        })
    
    if motor_hours > 4500.0:
        alerts.append({
            "id": f"motor_service_crit_{int(now)}",
            "type": "critical",
            "source": "Maintenance Agent",
            "message": f"Pump motor has exceeded service lifetime ({motor_hours:.1f} hrs). Replacement required.",
            "timestamp": now
        })
    elif motor_hours > 3000.0:
        alerts.append({
            "id": f"motor_service_warn_{int(now)}",
            "type": "warning",
            "source": "Maintenance Agent",
            "message": f"Pump motor nearing scheduled maintenance interval ({motor_hours:.1f} hrs).",
            "timestamp": now
        })

    # 5. Sensor Validation Quality Alerts
    if quality_score < 60.0:
        alerts.append({
            "id": f"sensor_fail_crit_{int(now)}",
            "type": "critical",
            "source": "Sensor Validation Agent",
            "message": f"Critical sensor drift or noise detected! Sensor Quality is {quality_score}%. Re-calibration required.",
            "timestamp": now
        })
    elif quality_score < 85.0:
        alerts.append({
            "id": f"sensor_fail_warn_{int(now)}",
            "type": "warning",
            "source": "Sensor Validation Agent",
            "message": f"Minor sensor noise / calibration drift detected ({quality_score}% accuracy).",
            "timestamp": now
        })

    # Add Info alert if everything is perfectly normal
    if not alerts:
        alerts.append({
            "id": f"system_info_{int(now)}",
            "type": "info",
            "source": "Supervisor Agent",
            "message": "System operating normal. Environment stability is high. Algae growth rate is stable.",
            "timestamp": now
        })

    return alerts
