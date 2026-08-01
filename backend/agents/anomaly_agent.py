import time
from typing import Dict, Any
from services.alerts import evaluate_alerts

def run_anomaly_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    analytics = state.get("analytics", {})
    quality_score = state.get("sensor_quality_score", 100.0)
    
    # Run evaluation
    alerts = evaluate_alerts(telemetry, analytics, quality_score)
    
    execution_time = time.time() - start_time
    
    criticals = [a for a in alerts if a["type"] == "critical"]
    warnings = [a for a in alerts if a["type"] == "warning"]
    
    decision = f"Detected {len(criticals)} critical issues and {len(warnings)} warnings."
    if not alerts or (len(alerts) == 1 and alerts[0]["type"] == "info"):
        decision = "No anomalies detected. System health is optimal."
        
    agent_log = {
        "agent": "Anomaly Detection Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 98.0,
        "latest_decision": decision,
        "reasoning": f"Analyzed telemetry against biological limit bounds and electrical thresholds."
    }
    
    return {
        "anomalies": alerts,
        "agent_logs": [agent_log]
    }
