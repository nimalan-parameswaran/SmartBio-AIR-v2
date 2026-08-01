import os
import time
from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from fastapi.responses import FileResponse
from models.schemas import TelemetryPayload, ManualControlPayload, AskAiRequest, ReportRequest
from firebase.firebase import db_client
from llm.gemini import gemini_client
from agents.supervisor import execute_agent_workflow
from agents.report_agent import create_csv_report

router = APIRouter(prefix="/api")

@router.get("/latest")
def get_latest():
    """Returns the most recent telemetry measurement along with calculated analytics."""
    latest_telemetry = db_client.get_latest_telemetry()
    if not latest_telemetry:
        return {"status": "NO_DATA", "message": "No telemetry recorded yet."}
    
    # Get latest analysis results
    ts = str(int(latest_telemetry.get("timestamp", 0)))
    analysis = db_client.read_data(f"analysis/{ts}") or {}
    
    return {
        "telemetry": latest_telemetry,
        "analytics": analysis
    }

@router.get("/history")
def get_history(limit: int = 50):
    """Returns the telemetry history."""
    history = db_client.get_history(limit=limit)
    return history

@router.get("/prediction")
def get_prediction():
    """Returns the latest prediction forecast."""
    pred = db_client.read_data("predictions") or {}
    return pred

@router.get("/recommendation")
def get_recommendation():
    """Returns the latest Gemini recommendations."""
    recs = db_client.read_data("recommendations") or []
    return recs

@router.get("/report")
def get_report():
    """Returns lists of generated report files or metadata."""
    reps = db_client.read_data("reports") or {}
    return reps

@router.get("/agents")
def get_agents():
    """Returns the running statuses of the LangGraph agent workflow."""
    # Read the agent logs written by the supervisor
    logs = db_client.read_data("agent_logs") or []
    return logs

@router.get("/system")
def get_system():
    """Returns status dashboard metrics."""
    latest_telemetry = db_client.get_latest_telemetry()
    mode = db_client.mode
    
    system_status = "STABLE"
    algae_health = 0.0
    air_score = 0.0
    
    if latest_telemetry:
        ts = str(int(latest_telemetry.get("timestamp", 0)))
        analysis = db_client.read_data(f"analysis/{ts}") or {}
        algae_health = latest_telemetry.get("algae", {}).get("health", 85.0)
        air_score = analysis.get("air_purification_score", 90.0)
        
        # Check alerts to determine status
        alerts = db_client.read_data("alerts") or []
        criticals = [a for a in alerts if a.get("type") == "critical"]
        if criticals:
            system_status = "CRITICAL"
        elif [a for a in alerts if a.get("type") == "warning"]:
            system_status = "WARNING"
            
    motor_ctrl = db_client.read_data("motor_control") or {}
    
    return {
        "status": system_status,
        "database_mode": mode,
        "air_purification_score": air_score,
        "algae_health": algae_health,
        "motor_status": motor_ctrl.get("status", "OFF"),
        "pump_speed": motor_ctrl.get("speed", 0.0),
        "emergency_stop": motor_ctrl.get("emergency_stop", False),
        "last_update": time.time()
    }

@router.post("/manual-control")
def post_manual_control(payload: ManualControlPayload):
    """Sets manual override parameters for the ESP32 motors."""
    control_data = {
        "status": payload.status,
        "speed": payload.speed if payload.speed is not None else 0.0,
        "flow_rate": payload.flow_rate if payload.flow_rate is not None else 0.0,
        "emergency_stop": payload.emergency_stop,
        "last_update": time.time()
    }
    db_client.write_data("motor_control", control_data)
    return {"status": "SUCCESS", "control_data": control_data}

@router.post("/ask-ai")
def post_ask_ai(payload: AskAiRequest):
    """Chat with the Bioreactor AI Agent."""
    latest_telemetry = db_client.get_latest_telemetry()
    analysis = {}
    if latest_telemetry:
        ts = str(int(latest_telemetry.get("timestamp", 0)))
        analysis = db_client.read_data(f"analysis/{ts}") or {}
        
    latest_state = {
        "telemetry": latest_telemetry,
        "analytics": analysis,
        "predictions": db_client.read_data("predictions") or {},
        "alerts": db_client.read_data("alerts") or []
    }
    
    response = gemini_client.ask_gemini_about_reactor(payload.question, payload.history, latest_state)
    return {"answer": response}

@router.post("/generate-report")
def post_generate_report(payload: ReportRequest, background_tasks: BackgroundTasks):
    """Manually compiles a PDF or CSV report and returns it."""
    history = db_client.get_history(limit=50)
    
    if payload.format.lower() == "csv":
        csv_data = create_csv_report(history)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={payload.report_type}_report.csv"}
        )
        
    # For PDF, compile graph workflow to get the report path
    latest_telemetry = db_client.get_latest_telemetry()
    if not latest_telemetry:
        raise HTTPException(status_code=400, detail="No telemetry available to generate report.")
        
    # Execute workflow specifically for the report agent
    state = execute_agent_workflow(latest_telemetry, history, report_type=payload.report_type)
    reports = state.get("reports", {})
    pdf_path = reports.get("pdf_path")
    
    if not pdf_path or not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Report generation failed to produce file.")
        
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=reports.get("pdf_filename", "report.pdf")
    )

@router.post("/telemetry")
def post_telemetry(payload: TelemetryPayload):
    """Submits a telemetry packet to the database, triggering the database listener/callback."""
    db_client.push_telemetry(payload.model_dump())
    return {"status": "SUCCESS", "message": "Telemetry injected successfully."}
