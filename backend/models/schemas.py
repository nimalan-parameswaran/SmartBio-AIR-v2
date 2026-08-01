from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class AlgaeTelemetry(BaseModel):
    green_idx: float = Field(..., description="Green index representation of density")
    health: float = Field(..., description="Overall health score (0-100)")
    light_lux: float = Field(..., description="Light level in lux")
    temp_c: float = Field(..., description="Algae water temperature in Celsius")

class EnvTelemetry(BaseModel):
    altitude: float = Field(..., description="Altitude in meters")
    pressure: float = Field(..., description="Atmospheric pressure in hPa")

class GasTelemetry(BaseModel):
    mq135: float = Field(..., description="Air quality / Hazardous gases")
    mq2: float = Field(..., description="Combustible gas / Smoke")
    mq3: float = Field(..., description="Alcohol / Ethanol vapor")
    mq7: float = Field(..., description="Carbon Monoxide (CO)")

class MotorTelemetry(BaseModel):
    status: str = Field("OFF", description="Motor status: ON, OFF, AUTO")
    speed: Optional[float] = Field(0.0, description="Pump speed in RPM or percentage")
    flow_rate: Optional[float] = Field(0.0, description="Water flow rate in L/min")
    operating_hours: Optional[float] = Field(0.0, description="Cumulative hours of operation")

class TelemetryPayload(BaseModel):
    algae: AlgaeTelemetry
    env: EnvTelemetry
    gas: GasTelemetry
    motor: MotorTelemetry
    timestamp: float = Field(..., description="Epoch timestamp in seconds")

class ManualControlPayload(BaseModel):
    status: str = Field(..., description="ON, OFF, or AUTO")
    speed: Optional[float] = Field(None, description="Pump speed (0-100)")
    flow_rate: Optional[float] = Field(None, description="Target water flow rate")
    emergency_stop: Optional[bool] = Field(False, description="Emergency stop signal")

class AskAiRequest(BaseModel):
    question: str = Field(..., description="Natural language question about the bioreactor")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Chat history")

class ReportRequest(BaseModel):
    report_type: str = Field(..., description="daily, weekly, monthly, or research")
    format: str = Field("pdf", description="pdf or csv")
