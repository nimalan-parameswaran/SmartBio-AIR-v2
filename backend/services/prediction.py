import time
import numpy as np
from typing import Dict, List, Any

def predict_future(history: List[Dict[str, Any]], current_telemetry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict parameters for the next 1 hour, 24 hours (1 day), and 7 days.
    Uses history trends and models circadian variations (for temp/gas) 
    and logistic growth (for algae density).
    """
    latest = current_telemetry
    algae = latest.get("algae", {})
    env = latest.get("env", {})
    gas = latest.get("gas", {})
    motor = latest.get("motor", {})
    
    curr_gi = algae.get("green_idx", 0.5)
    curr_temp = algae.get("temp_c", 22.0)
    curr_mq135 = gas.get("mq135", 150.0)
    curr_hours = motor.get("operating_hours", 0.0)
    
    # Growth rate estimate (default is positive growth unless stressed)
    p_eff = algae.get("health", 85.0) # we can use health score as a growth proxy
    stress = algae.get("stress_index", 10.0)
    
    # Calculate base growth coefficient
    growth_coefficient = max(-0.05, (p_eff * 0.002) - (stress * 0.005))
    
    # 1 Hour, 24 Hour, 7 Day offsets (in hours)
    intervals = {"1h": 1, "24h": 24, "7d": 168}
    predictions = {}
    
    for label, hours in intervals.items():
        # 1. Green Index (Logistic Algae Growth: limit max Green Index to 2.5)
        k = 2.5 # carrying capacity
        gi_pred = k / (1.0 + ((k - curr_gi) / max(0.01, curr_gi)) * np.exp(-growth_coefficient * hours))
        gi_pred = round(max(0.0, min(2.5, float(gi_pred))), 3)
        
        # 2. Temperature (Circadian cycle: +/- 2 degrees around current, plus steady target convergence)
        # We simulate diurnal cycle using current timestamp + hours
        curr_time = latest.get("timestamp", time.time())
        future_hour = (time.localtime(curr_time + hours * 3600).tm_hour)
        diurnal_offset = 2.0 * np.sin((future_hour - 6) / 24.0 * 2.0 * np.pi)
        # converge to target 24C slightly
        temp_pred = curr_temp * 0.8 + 24.0 * 0.2 + diurnal_offset * 0.5
        temp_pred = round(float(temp_pred), 1)
        
        # 3. Gas reduction (MQ135)
        # More algae (higher Green Index) means better CO2/VOC reduction (lower MQ135)
        # MQ135 baseline is 100. Algae reduces gas concentration.
        gas_reduction_factor = max(0.1, 1.0 - (gi_pred * 0.15))
        mq135_pred = max(80.0, curr_mq135 * gas_reduction_factor)
        mq135_pred = round(float(mq135_pred), 1)
        
        # 4. Motor Health / Remaining Useful Life
        # Decays proportionally to hours operated. Max lifetime = 5000 hours.
        added_hours = hours
        future_hours = curr_hours + added_hours
        motor_health_pred = max(0.0, 100.0 - (future_hours / 5000.0) * 100.0)
        motor_health_pred = round(float(motor_health_pred), 1)
        
        # 5. Air Purification Score (derived from predicted gas values)
        air_quality_pred = round(max(0.0, min(100.0, 100.0 - (mq135_pred - 80.0) * 0.15)), 1)
        
        predictions[label] = {
            "green_idx": gi_pred,
            "temp_c": temp_pred,
            "mq135": mq135_pred,
            "motor_health": motor_health_pred,
            "air_purification_score": air_quality_pred,
            "biomass_g_l": round(gi_pred * 0.18 + 0.02, 3),
            "gas_reduction_pct": round(max(0.0, (curr_mq135 - mq135_pred) / max(1.0, curr_mq135) * 100.0), 1)
        }
        
    return predictions
