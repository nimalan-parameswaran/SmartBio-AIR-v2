import time
from typing import Dict, Any
from llm.gemini import gemini_client

def run_recommendation_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    analytics = state.get("analytics", {})
    anomalies = state.get("anomalies", [])
    
    # Generate using Gemini Client
    recs = gemini_client.generate_recommendations(telemetry, analytics, anomalies)
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Recommendation Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 90.0,
        "latest_decision": f"Generated {len(recs)} diagnostic recommendations.",
        "reasoning": "Gemini analyzed sensor deviations, heat logs, and biological parameters."
    }
    
    return {
        "recommendations": recs,
        "agent_logs": [agent_log]
    }
