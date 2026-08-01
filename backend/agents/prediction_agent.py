import time
from typing import Dict, Any
from services.prediction import predict_future

def run_prediction_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    history = state.get("history", [])
    
    # Run prediction algorithm
    predictions = predict_future(history, telemetry)
    
    execution_time = time.time() - start_time
    
    # Formulate decision message
    gi_1h = predictions.get("1h", {}).get("green_idx", 0.5)
    gi_24h = predictions.get("24h", {}).get("green_idx", 0.5)
    
    agent_log = {
        "agent": "Prediction Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 85.0,
        "latest_decision": f"1h green index forecast: {gi_1h}, 24h: {gi_24h}.",
        "reasoning": f"Logistic algae growth models growth velocity. Circadian variations project temperature cycles."
    }
    
    return {
        "predictions": predictions,
        "agent_logs": [agent_log]
    }
