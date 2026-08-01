import time
from typing import Dict, Any

def run_sensor_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    raw = state.get("raw_telemetry", {})
    
    cleaned = {
        "algae": {},
        "env": {},
        "gas": {},
        "motor": {},
        "timestamp": raw.get("timestamp", time.time())
    }
    
    issues = []
    total_metrics = 0
    valid_metrics = 0
    
    # Validation constraints
    ranges = {
        "algae": {
            "green_idx": (0.0, 3.0, 0.5), # (min, max, default)
            "health": (0.0, 100.0, 85.0),
            "light_lux": (0.0, 20000.0, 1000.0),
            "temp_c": (5.0, 45.0, 22.0)
        },
        "env": {
            "altitude": (0.0, 5000.0, 100.0),
            "pressure": (800.0, 1100.0, 1013.0)
        },
        "gas": {
            "mq135": (10.0, 1000.0, 150.0),
            "mq2": (5.0, 800.0, 40.0),
            "mq3": (5.0, 800.0, 30.0),
            "mq7": (2.0, 500.0, 25.0)
        },
        "motor": {
            "status": (["ON", "OFF", "AUTO"], "OFF"),
            "speed": (0.0, 100.0, 0.0),
            "flow_rate": (0.0, 10.0, 0.0),
            "operating_hours": (0.0, 10000.0, 0.0)
        }
    }
    
    # Process numeric ranges
    for category, fields in ranges.items():
        raw_cat = raw.get(category, {})
        for field, rules in fields.items():
            total_metrics += 1
            val = raw_cat.get(field)
            
            # 1. Missing Value Check
            if val is None:
                issues.append(f"Missing {category}.{field}")
                cleaned[category][field] = rules[2] if len(rules) == 3 else rules[1]
                continue
                
            # 2. Type Check / Range Check
            if isinstance(rules[0], list): # Categorical
                if val in rules[0]:
                    cleaned[category][field] = val
                    valid_metrics += 1
                else:
                    issues.append(f"Invalid category for {category}.{field}: {val}")
                    cleaned[category][field] = rules[1]
            else: # Numerical
                try:
                    num_val = float(val)
                    if rules[0] <= num_val <= rules[1]:
                        cleaned[category][field] = num_val
                        valid_metrics += 1
                    else:
                        issues.append(f"Out of range {category}.{field}: {num_val}")
                        # clamp value
                        clamped = max(rules[0], min(rules[1], num_val))
                        cleaned[category][field] = clamped
                except ValueError:
                    issues.append(f"Invalid numeric format {category}.{field}")
                    cleaned[category][field] = rules[2]

    # Calculate Sensor Quality Score
    quality_score = (valid_metrics / max(1, total_metrics)) * 100.0
    quality_score = round(quality_score, 1)
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Sensor Validation Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": quality_score,
        "latest_decision": f"Validated {valid_metrics}/{total_metrics} sensor feeds.",
        "reasoning": f"Detected issues: {', '.join(issues)}" if issues else "All sensors passed validation checks."
    }
    
    return {
        "cleaned_telemetry": cleaned,
        "sensor_quality_score": quality_score,
        "agent_logs": [agent_log]
    }
