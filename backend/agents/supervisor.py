import time
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END

# Import agent nodes
from agents.sensor_agent import run_sensor_agent
from agents.environment_agent import run_environment_agent
from agents.algae_agent import run_algae_agent
from agents.prediction_agent import run_prediction_agent
from agents.anomaly_agent import run_anomaly_agent
from agents.maintenance_agent import run_maintenance_agent
from agents.recommendation_agent import run_recommendation_agent
from agents.research_agent import run_research_agent
from agents.report_agent import run_report_agent

# Define LangGraph State Schema
class GraphState(TypedDict):
    raw_telemetry: Dict[str, Any]
    history: List[Dict[str, Any]]
    cleaned_telemetry: Dict[str, Any]
    sensor_quality_score: float
    analytics: Dict[str, Any]
    predictions: Dict[str, Any]
    anomalies: List[Dict[str, Any]]
    maintenance: Dict[str, Any]
    recommendations: List[str]
    research_notes: str
    reports: Dict[str, Any]
    report_type: str
    agent_logs: List[Dict[str, Any]]

# Node wrappers that combine state accumulation
def node_sensor(state: GraphState) -> Dict[str, Any]:
    return run_sensor_agent(state)

def node_env(state: GraphState) -> Dict[str, Any]:
    return run_environment_agent(state)

def node_algae(state: GraphState) -> Dict[str, Any]:
    return run_algae_agent(state)

def node_prediction(state: GraphState) -> Dict[str, Any]:
    return run_prediction_agent(state)

def node_anomaly(state: GraphState) -> Dict[str, Any]:
    return run_anomaly_agent(state)

def node_maintenance(state: GraphState) -> Dict[str, Any]:
    return run_maintenance_agent(state)

def node_recommendation(state: GraphState) -> Dict[str, Any]:
    return run_recommendation_agent(state)

def node_research(state: GraphState) -> Dict[str, Any]:
    return run_research_agent(state)

def node_report(state: GraphState) -> Dict[str, Any]:
    return run_report_agent(state)

# Constructing LangGraph Workflow
workflow = StateGraph(GraphState)

# Add Nodes
workflow.add_node("sensor_agent", node_sensor)
workflow.add_node("environment_agent", node_env)
workflow.add_node("algae_agent", node_algae)
workflow.add_node("prediction_agent", node_prediction)
workflow.add_node("anomaly_agent", node_anomaly)
workflow.add_node("maintenance_agent", node_maintenance)
workflow.add_node("recommendation_agent", node_recommendation)
workflow.add_node("research_agent", node_research)
workflow.add_node("report_agent", node_report)

# Set up sequential edges
workflow.set_entry_point("sensor_agent")
workflow.add_edge("sensor_agent", "environment_agent")
workflow.add_edge("environment_agent", "algae_agent")
workflow.add_edge("algae_agent", "prediction_agent")
workflow.add_edge("prediction_agent", "anomaly_agent")
workflow.add_edge("anomaly_agent", "maintenance_agent")
workflow.add_edge("maintenance_agent", "recommendation_agent")
workflow.add_edge("recommendation_agent", "research_agent")
workflow.add_edge("research_agent", "report_agent")
workflow.add_edge("report_agent", END)

# Compile Graph
graph_app = workflow.compile()

def execute_agent_workflow(raw_telemetry: Dict[str, Any], history: List[Dict[str, Any]], report_type: str = "daily") -> Dict[str, Any]:
    """
    Executes the multi-agent graph workflow sequentially starting from Raw Telemetry.
    Accumulates state and returns the unified final state.
    """
    # Initial State
    initial_state: GraphState = {
        "raw_telemetry": raw_telemetry,
        "history": history,
        "cleaned_telemetry": {},
        "sensor_quality_score": 100.0,
        "analytics": {},
        "predictions": {},
        "anomalies": [],
        "maintenance": {},
        "recommendations": [],
        "research_notes": "",
        "reports": {},
        "report_type": report_type,
        "agent_logs": []
    }
    
    # Run the compiled LangGraph workflow
    # LangGraph updates state automatically by merging dictionaries returned by nodes
    # For a simple TypedDict state, returned values overwrite or update the matching keys.
    # In older/newer langgraph, state is returned as the final output.
    current_state = initial_state
    
    # Executing node by node manually or via graph runner
    # To avoid runtime dependency/version complications of StateGraph execution loops, 
    # we implement a secure runner that mimics the exact sequential graph edges defined.
    # This guarantees execution under any version of LangGraph!
    steps = [
        ("sensor_agent", node_sensor),
        ("environment_agent", node_env),
        ("algae_agent", node_algae),
        ("prediction_agent", node_prediction),
        ("anomaly_agent", node_anomaly),
        ("maintenance_agent", node_maintenance),
        ("recommendation_agent", node_recommendation),
        ("research_agent", node_research),
        ("report_agent", node_report)
    ]
    
    for node_name, node_func in steps:
        try:
            update = node_func(current_state)
            # Merge updates
            for k, v in update.items():
                if k == "agent_logs":
                    current_state["agent_logs"].extend(v)
                else:
                    current_state[k] = v
        except Exception as e:
            import logging
            logging.getLogger("smartbio_supervisor").error(f"Error in node {node_name}: {e}")
            # Add error log
            current_state["agent_logs"].append({
                "agent": node_name.replace("_", " ").title(),
                "status": "FAILED",
                "execution_time_ms": 0.0,
                "confidence_score": 0.0,
                "latest_decision": "Node crashed.",
                "reasoning": f"Exception raised: {str(e)}"
            })
            
    return current_state
