import time
from typing import Dict, Any
from llm.gemini import gemini_client

def run_research_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    telemetry = state.get("cleaned_telemetry", {})
    history = state.get("history", [])
    
    # Generate notes using Gemini
    notes = gemini_client.generate_research_notes(telemetry, history)
    
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Research Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 88.0,
        "latest_decision": "Completed biological growth analysis log entry.",
        "reasoning": "Gemini analyzed correlation between green index, light intensity, and indoor gas profiles."
    }
    
    return {
        "research_notes": notes,
        "agent_logs": [agent_log]
    }
