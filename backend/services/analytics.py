import numpy as np
from typing import Dict, List, Any

def calculate_photosynthesis_efficiency(temp_c: float, light_lux: float) -> float:
    # Algae photosynthesis peaks around 24C and 2000-3000 Lux.
    # High light (>8000 Lux) causes photoinhibition. Low light (<200 Lux) is insufficient.
    
    # Temperature Factor (gaussian curve around 24C)
    temp_factor = np.exp(-0.01 * (temp_c - 24.0) ** 2)
    
    # Light Factor (limiting-exponential curve)
    if light_lux <= 0:
        light_factor = 0.0
    elif light_lux <= 2500:
        light_factor = light_lux / 2500.0
    else:
        # Photoinhibition above 5000 Lux
        light_factor = max(0.1, 1.0 - 0.00005 * (light_lux - 2500))
        
    efficiency = float(temp_factor * light_factor * 100.0)
    return round(max(0.0, min(100.0, efficiency)), 1)

def calculate_biomass(green_idx: float) -> float:
    # Estimate dry biomass concentration (g/L) from green index (spectrophotometric approximation)
    # Biomass (g/L) = Green Index * Constant
    biomass = green_idx * 0.18 + 0.02
    return round(max(0.0, biomass), 3)

def calculate_stress_index(temp_c: float, light_lux: float, env_stability: float) -> float:
    # Algae stress is higher when temp is far from 24C, light is extreme, or env is unstable.
    temp_stress = min(50.0, abs(temp_c - 24.0) * 4.0)
    
    light_stress = 0.0
    if light_lux < 300:
        light_stress = 30.0 # light deprivation
    elif light_lux > 6000:
        light_stress = min(40.0, (light_lux - 6000) * 0.01) # photo-stress
        
    stability_stress = (100.0 - env_stability) * 0.3
    
    stress = temp_stress + light_stress + stability_stress
    return round(max(0.0, min(100.0, stress)), 1)

def calculate_air_purification_score(mq135: float, mq7: float) -> float:
    # MQ135: general air quality / CO2 / NH3
    # MQ7: CO (Carbon Monoxide)
    # Lower values of sensor output mean cleaner air.
    # Suppose MQ135 baseline is 100-200. Anything above 500 is poor.
    # Suppose MQ7 baseline is 20-50. Anything above 150 is poor.
    
    mq135_score = max(0, 100 - (mq135 / 6.0))
    mq7_score = max(0, 100 - (mq7 / 2.0))
    
    purification_score = 0.7 * mq135_score + 0.3 * mq7_score
    return round(max(0.0, min(100.0, purification_score)), 1)

def calculate_comfort_index(temp_c: float, pressure: float) -> float:
    # Human indoor comfort index based on temperature and atmospheric pressure
    # Comfort is highest around 22C and 1013 hPa
    temp_comfort = max(0, 100 - abs(temp_c - 22.0) * 6.0)
    press_comfort = max(0, 100 - abs(pressure - 1013.0) * 0.5)
    
    comfort = 0.6 * temp_comfort + 0.4 * press_comfort
    return round(max(0.0, min(100.0, comfort)), 1)

def analyze_all(telemetry: Dict[str, Any], history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    algae = telemetry.get("algae", {})
    env = telemetry.get("env", {})
    gas = telemetry.get("gas", {})
    motor = telemetry.get("motor", {})
    
    temp_c = algae.get("temp_c", 22.0)
    light_lux = algae.get("light_lux", 1000.0)
    green_idx = algae.get("green_idx", 0.5)
    
    pressure = env.get("pressure", 1013.0)
    
    mq135 = gas.get("mq135", 150.0)
    mq7 = gas.get("mq7", 30.0)
    
    # Base calculations
    p_eff = calculate_photosynthesis_efficiency(temp_c, light_lux)
    biomass = calculate_biomass(green_idx)
    air_pur_score = calculate_air_purification_score(mq135, mq7)
    comfort = calculate_comfort_index(temp_c, pressure)
    
    # Calculate environmental stability based on rolling variance of temperature & pressure in history
    env_stability = 95.0
    growth_rate = 0.0
    
    if history and len(history) > 1:
        temps = [h.get("algae", {}).get("temp_c", temp_c) for h in history[-10:]]
        pressures = [h.get("env", {}).get("pressure", pressure) for h in history[-10:]]
        
        t_var = np.var(temps) if len(temps) > 1 else 0.0
        p_var = np.var(pressures) if len(pressures) > 1 else 0.0
        
        env_stability = max(50.0, 100.0 - (t_var * 10.0 + p_var * 0.1))
        
        # Calculate Growth Rate (change in green index per hour)
        prev = history[-1]
        prev_algae = prev.get("algae", {})
        prev_gi = prev_algae.get("green_idx", green_idx)
        prev_time = prev.get("timestamp", telemetry.get("timestamp", 0) - 5)
        curr_time = telemetry.get("timestamp", 0)
        
        time_diff_hours = (curr_time - prev_time) / 3600.0
        if time_diff_hours > 0.001:
            growth_rate = (green_idx - prev_gi) / time_diff_hours
            
    stress = calculate_stress_index(temp_c, light_lux, env_stability)
    
    return {
        "photosynthesis_efficiency": round(p_eff, 1),
        "biomass_g_l": round(biomass, 3),
        "growth_rate_hr": round(growth_rate, 5),
        "stress_index": round(stress, 1),
        "air_purification_score": round(air_pur_score, 1),
        "comfort_index": round(comfort, 1),
        "environmental_stability": round(env_stability, 1)
    }
