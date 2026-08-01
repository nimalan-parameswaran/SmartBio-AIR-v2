import sys
import os
import json
import time

# Set up path to import backend files
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.supervisor import execute_agent_workflow

def test_workflow():
    print("Initializing LangGraph multi-agent diagnostic run test...")
    
    mock_telemetry = {
        "algae": {
            "green_idx": 1.25,
            "health": 80.0,
            "light_lux": 2500.0,
            "temp_c": 34.5  # Stressed, high temperature to test warnings
        },
        "env": {
            "altitude": 100.0,
            "pressure": 1011.5
        },
        "gas": {
            "mq135": 420.0, # Elevated gas levels
            "mq2": 35.0,
            "mq3": 20.0,
            "mq7": 95.0
        },
        "motor": {
            "status": "ON",
            "speed": 85.0,
            "flow_rate": 3.4,
            "operating_hours": 3050.0  # Nearing service hours
        },
        "timestamp": time.time()
    }
    
    history = [
        # Seed simple past records
        {
            "algae": {"green_idx": 1.20, "health": 82.0, "light_lux": 2400.0, "temp_c": 33.0},
            "env": {"altitude": 100.0, "pressure": 1012.0},
            "gas": {"mq135": 430.0, "mq2": 35.0, "mq3": 20.0, "mq7": 98.0},
            "motor": {"status": "ON", "speed": 85.0, "flow_rate": 3.4, "operating_hours": 3049.0},
            "timestamp": time.time() - 3600
        }
    ]
    
    # Run graph execution loop
    start = time.time()
    results = execute_agent_workflow(mock_telemetry, history)
    duration = time.time() - start
    
    print(f"\nExecution finished in {duration:.3f} seconds.")
    print(f"Sensor Quality Score: {results['sensor_quality_score']}%")
    print(f"Photosynthesis Efficiency: {results['analytics'].get('photosynthesis_efficiency')}%")
    print(f"Algae Health Index: {results['cleaned_telemetry']['algae'].get('health')}%")
    print(f"Air Purification Score: {results['analytics'].get('air_purification_score')}%")
    print(f"Motor health: {results['maintenance'].get('motor_health')}%")
    
    print("\nAgent Pipeline Log Summary:")
    for log in results["agent_logs"]:
        print(f" - [{log['agent']}] Status: {log['status']}, Confidence: {log['confidence_score']}%, Time: {log['execution_time_ms']}ms")
        print(f"   Decision: {log['latest_decision']}")
        
    print("\nDetected Anomalies:")
    for anomaly in results["anomalies"]:
        print(f" - [{anomaly['type'].upper()}] {anomaly['message']}")
        
    print("\nAI Recommendations:")
    for idx, rec in enumerate(results["recommendations"]):
        print(f" {idx+1}. {rec}")
        
    print(f"\nAI Research Notes length: {len(results['research_notes'])} chars")
    
    # Assert logs length (should have 9 logs, one for each agent)
    assert len(results["agent_logs"]) >= 9, "Some agents failed to execute."
    print("\nAll Multi-Agent execution test assertions passed successfully!")

if __name__ == "__main__":
    test_workflow()
