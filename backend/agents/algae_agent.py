import time
from typing import Dict, Any
from services.analytics import calculate_photosynthesis_efficiency, calculate_biomass, calculate_stress_index

def run_algae_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    history = state.get("history", [])
    analytics = state.get("analytics", {})
    
    algae = telemetry.get("algae", {})
    temp_c = algae.get("temp_c", 22.0)
    light_lux = algae.get("light_lux", 1000.0)
    green_idx = algae.get("green_idx", 0.5)
    
    env_stability = analytics.get("environmental_stability", 95.0)
    
    # 1. Biological indicators
    p_eff = calculate_photosynthesis_efficiency(temp_c, light_lux)
    biomass = calculate_biomass(green_idx)
    stress = calculate_stress_index(temp_c, light_lux, env_stability)
    
    # 2. Growth Rate (from history)
    growth_rate = 0.0
    if history and len(history) > 1:
        prev = history[-1]
        prev_gi = prev.get("algae", {}).get("green_idx", green_idx)
        prev_time = prev.get("timestamp", telemetry.get("timestamp", 0) - 5)
        curr_time = telemetry.get("timestamp", 0)
        
        time_diff_hours = (curr_time - prev_time) / 3600.0
        if time_diff_hours > 0.0001:
            growth_rate = (green_idx - prev_gi) / time_diff_hours
            
    # Calculate health index (0 - 100) based on stress & photosynthesis efficiency
    health_score = round(max(0.0, min(100.0, (p_eff * 0.6) + (100.0 - stress) * 0.4)), 1)
    
    # Write details to telemetry and analytics
    algae_analysis = {
        "photosynthesis_efficiency": p_eff,
        "biomass_g_l": biomass,
        "growth_rate_hr": round(growth_rate, 5),
        "stress_index": stress,
        "health_score": health_score
    }
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Algae Health Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 90.0,
        "latest_decision": f"Algae health: {health_score}%, biomass: {biomass} g/L.",
        "reasoning": f"Stress index is at {stress}%, and photosynthesis efficiency stands at {p_eff}%."
    }
    
    # Update state
    current_analytics = state.get("analytics", {})
    current_analytics.update(algae_analysis)
    
    # Overwrite health in cleaned telemetry too (as dashboard visualizes health)
    if "algae" in telemetry:
        telemetry["algae"]["health"] = health_score
        
    return {
        "analytics": current_analytics,
        "cleaned_telemetry": telemetry,
        "agent_logs": [agent_log]
    }
