import time
from typing import Dict, Any
from services.analytics import calculate_comfort_index, calculate_air_purification_score

def run_environment_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    history = state.get("history", [])
    
    env = telemetry.get("env", {})
    gas = telemetry.get("gas", {})
    algae = telemetry.get("algae", {})
    
    temp_c = algae.get("temp_c", 22.0)
    pressure = env.get("pressure", 1013.0)
    mq135 = gas.get("mq135", 150.0)
    mq7 = gas.get("mq7", 25.0)
    light = algae.get("light_lux", 1000.0)
    
    # 1. Environmental Stability calculation based on history variance
    env_stability = 95.0
    if history and len(history) > 1:
        temps = [h.get("algae", {}).get("temp_c", temp_c) for h in history[-10:]]
        pressures = [h.get("env", {}).get("pressure", pressure) for h in history[-10:]]
        t_var = sum((t - sum(temps)/len(temps))**2 for t in temps)/len(temps)
        p_var = sum((p - sum(pressures)/len(pressures))**2 for p in pressures)/len(pressures)
        env_stability = max(50.0, 100.0 - (t_var * 8.0 + p_var * 0.15))
        
    env_stability = round(env_stability, 1)
    
    # 2. Indoor Air Quality and Comfort
    comfort = calculate_comfort_index(temp_c, pressure)
    air_quality = calculate_air_purification_score(mq135, mq7)
    
    # 3. Photosynthesis suitability
    suitability = 100.0
    if temp_c < 18.0 or temp_c > 30.0:
        suitability -= abs(temp_c - 24.0) * 8.0
    if light < 400.0:
        suitability -= (400.0 - light) * 0.15
    elif light > 7000.0:
        suitability -= (light - 7000.0) * 0.005
    suitability = round(max(0.0, min(100.0, suitability)), 1)
    
    env_analysis = {
        "environmental_stability": env_stability,
        "comfort_index": comfort,
        "air_quality_score": air_quality,
        "photosynthesis_suitability": suitability
    }
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Environment Analysis Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 95.0,
        "latest_decision": f"Comfort Index: {comfort}%, Stability: {env_stability}%.",
        "reasoning": f"Bioreactor environment stability stands at {env_stability}%. Air comfort is {comfort}% based on target metrics."
    }
    
    # Update state
    current_analytics = state.get("analytics", {})
    current_analytics.update(env_analysis)
    
    return {
        "analytics": current_analytics,
        "agent_logs": [agent_log]
    }
