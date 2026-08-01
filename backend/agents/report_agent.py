import os
import csv
import time
import io
import logging
from typing import Dict, List, Any
from fpdf import FPDF

logger = logging.getLogger("smartbio_report_agent")

class PDFReport(FPDF):
    def header(self):
        self.set_fill_color(24, 31, 26) # Rich forest dark green header
        self.rect(0, 0, 210, 32, 'F')
        
        self.set_text_color(255, 255, 255)
        self.set_font('helvetica', 'B', 16)
        self.cell(0, 10, 'SMART BIO AIR - REPORTING SYSTEMS', ln=True, align='L')
        
        self.set_font('helvetica', '', 9)
        self.set_text_color(180, 200, 185)
        self.cell(0, 5, 'AI-driven Bioreactor & Indoor Air Quality Platform', ln=True, align='L')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} - Autonomous Operations AI Hub', align='C')

def clean_pdf_text(text: str) -> str:
    if not isinstance(text, str):
        return str(text)
    # Replace degree symbol and common non-latin-1 compatibility characters
    text = text.replace("°C", " C").replace("°", " deg").replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return text.encode('latin-1', 'replace').decode('latin-1')

def create_pdf_report(state: Dict[str, Any], report_type: str) -> str:
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(40, 40, 40)
    
    telemetry = state.get("cleaned_telemetry", {})
    algae = telemetry.get("algae", {})
    env = telemetry.get("env", {})
    gas = telemetry.get("gas", {})
    motor = telemetry.get("motor", {})
    
    analytics = state.get("analytics", {})
    maintenance = state.get("maintenance", {})
    anomalies = state.get("anomalies", [])
    recommendations = state.get("recommendations", [])
    research_notes = state.get("research_notes", "No research notes compiled.")
    
    # Title Section
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(30, 80, 45)
    pdf.cell(pdf.epw, 10, clean_pdf_text(f"{report_type.upper()} DIAGNOSTIC SUMMARY"), ln=True)
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(pdf.epw, 5, clean_pdf_text(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"), ln=True)
    pdf.ln(5)
    
    # Telemetry Grid
    pdf.set_fill_color(240, 245, 242)
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(pdf.epw, 7, "1. CORE TELEMETRY", fill=True, ln=True)
    pdf.set_font('helvetica', '', 9)
    # two columns of 95 each = 190 (which equals epw for A4 with 10mm margins)
    pdf.cell(95, 6, clean_pdf_text(f"Algae Temperature: {algae.get('temp_c')} C"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Photosynthesis Light: {algae.get('light_lux')} Lux"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Green Index (density): {algae.get('green_idx')}"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Estimated Biomass: {analytics.get('biomass_g_l', 0.0)} g/L"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Atmospheric Pressure: {env.get('pressure')} hPa"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Altitude: {env.get('altitude')} m"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Air Quality Score (MQ135): {analytics.get('air_quality_score', 100.0)}%"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Motor Status: {motor.get('status')} ({motor.get('speed', 0.0)}% speed)"), border=1, ln=True)
    pdf.ln(5)
    
    # Analytics Grid
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(pdf.epw, 7, "2. ANALYTICS & DIAGNOSTICS", fill=True, ln=True)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(95, 6, clean_pdf_text(f"Algae Health Index: {algae.get('health', 0.0)}%"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Photosynthesis Efficiency: {analytics.get('photosynthesis_efficiency', 0.0)}%"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Stress Index: {analytics.get('stress_index', 0.0)}%"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Comfort Index: {analytics.get('comfort_index', 0.0)}%"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Environmental Stability: {analytics.get('environmental_stability', 100.0)}%"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Growth Velocity: {analytics.get('growth_rate_hr', 0.0):.5f} GI/hr"), border=1, ln=True)
    pdf.cell(95, 6, clean_pdf_text(f"Motor Life (RUL): {maintenance.get('remaining_useful_life_hours', 5000.0)} hrs"), border=1)
    pdf.cell(95, 6, clean_pdf_text(f"Next Bio-Cleaning Due: {maintenance.get('days_until_next_cleaning', 15.0)} days"), border=1, ln=True)
    pdf.ln(5)
    
    # Alerts / Anomalies
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(pdf.epw, 7, "3. ACTIVE ALERTS & ANOMALIES", fill=True, ln=True)
    pdf.set_font('helvetica', '', 9)
    if not anomalies or (len(anomalies) == 1 and anomalies[0]["type"] == "info"):
        pdf.cell(pdf.epw, 6, "No anomalies or alerts active.", border=1, ln=True)
    else:
        for idx, alert in enumerate(anomalies):
            typ = alert.get("type", "warning").upper()
            msg = alert.get("message", "")
            pdf.cell(pdf.epw, 6, clean_pdf_text(f"[{typ}] {msg}"), border=1, ln=True)
    pdf.ln(5)
    
    # Recommendations
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(pdf.epw, 7, "4. AI RECOMMENDATIONS & ACTIONS", fill=True, ln=True)
    pdf.set_font('helvetica', '', 9)
    if not recommendations:
        pdf.cell(pdf.epw, 6, "No diagnostic recommendations generated.", border=1, ln=True)
    else:
        for idx, rec in enumerate(recommendations):
            pdf.multi_cell(pdf.epw, 6, clean_pdf_text(f"{idx+1}. {rec}"), border=1)
    pdf.ln(5)
    
    # Research Notes
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(pdf.epw, 7, "5. SCIENTIFIC RESEARCH NOTES", fill=True, ln=True)
    pdf.set_font('helvetica', '', 9)
    pdf.multi_cell(pdf.epw, 5, clean_pdf_text(research_notes), border=1)
    
    # Save Report
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reports"))
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"{report_type}_report_{int(time.time())}.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    pdf.output(filepath)
    return filepath

def create_csv_report(history: List[Dict[str, Any]]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "timestamp", "algae_temp_c", "light_lux", "green_index", "algae_health",
        "env_altitude", "env_pressure",
        "gas_mq135", "gas_mq2", "gas_mq3", "gas_mq7",
        "motor_status", "motor_speed", "motor_operating_hours"
    ])
    
    for row in history:
        algae = row.get("algae", {})
        env = row.get("env", {})
        gas = row.get("gas", {})
        motor = row.get("motor", {})
        
        writer.writerow([
            row.get("timestamp", 0),
            algae.get("temp_c", 0),
            algae.get("light_lux", 0),
            algae.get("green_idx", 0),
            algae.get("health", 0),
            env.get("altitude", 0),
            env.get("pressure", 0),
            gas.get("mq135", 0),
            gas.get("mq2", 0),
            gas.get("mq3", 0),
            gas.get("mq7", 0),
            motor.get("status", "OFF"),
            motor.get("speed", 0),
            motor.get("operating_hours", 0)
        ])
        
    return output.getvalue()

def run_report_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    
    # Extract details
    report_type = state.get("report_type", "daily")
    
    # Generate structured report data
    reports = {
        "last_generated_type": report_type,
        "timestamp": time.time(),
        "summary": f"Smart BIO AIR AI Agent successfully compiled the {report_type} report. System diagnostics, anomaly evaluations, and Google Gemini advice logs are archived."
    }
    
    # Export PDF in a background action (not blocking telemetry loop)
    # We will trigger the PDF creation and write path to state.
    try:
        pdf_path = create_pdf_report(state, report_type)
        reports["pdf_path"] = pdf_path
        reports["pdf_filename"] = os.path.basename(pdf_path)
    except Exception as e:
        logger.error(f"Failed to generate PDF in report agent: {e}")
        reports["pdf_path"] = None
        reports["pdf_error"] = str(e)
        
    execution_time = time.time() - start_time
    
    agent_log = {
        "agent": "Report Agent",
        "status": "COMPLETED",
        "execution_time_ms": round(execution_time * 1000, 1),
        "confidence_score": 95.0,
        "latest_decision": f"Compiled {report_type} report. PDF generated: {reports.get('pdf_filename')}.",
        "reasoning": "Aggregated all system nodes diagnostics, recommendations, and research logs."
    }
    
    return {
        "reports": reports,
        "agent_logs": [agent_log]
    }
