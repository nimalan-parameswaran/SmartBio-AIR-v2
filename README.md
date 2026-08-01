# Smart BIO AIR Version 2.0 – AI Multi-Agent Bioreactor Platform

**Smart BIO AIR Version 2.0** is an AI-driven, autonomous algae cultivation and indoor air purification platform. By combining IoT telemetry (ESP32), cloud database synchronization (Firebase Realtime Database), mathematical biological models, and a **LangGraph Multi-Agent AI system** running on **Google Gemini**, the system predicts biological health, detects sensor anomalies, estimates carbon sequestration/purification efficiency, and automates motor controls.

---

## 🏗️ System Architecture

```
  [ ESP32 IoT Sensors ]
           │
           ▼ (HTTPS / REST Telemetry)
 [ Firebase Realtime Database ]
           │
           ▼ (Server-Sent Events Stream / REST listener)
   [ FastAPI AI Backend ]
           │
           ▼ (LangGraph Supervisor)
  ┌────────────────────────────────────────────────────────┐
  │ Sensor validation ──► Env Analysis ──► Algae Health    │
  │        │                                  │            │
  │        ▼                                  ▼            │
  │ Report Compile ◄── Research ◄── Recommend ◄── Forecast │
  └────────────────────────────────────────────────────────┘
           │
           ▼ (Updates Firebase Nodes & Reports Path)
  [ Next.js React Dashboard ] ◄─── (User Controls & Ask AI Chat)
```

---

## 📁 Folder Structure

```
SmartBio-AIR-v2/
├── backend/
│   ├── app.py                      # FastAPI entrypoint (starts listeners & simulation)
│   ├── config.py                   # App configurations & ENV loading
│   ├── requirements.txt            # Python requirements (LangGraph, FastAPI, FPDF2, etc.)
│   ├── local_db.json               # Auto-generated JSON database fallback
│   ├── firebase/
│   │   ├── firebase.py             # Firebase DB client (supports REST and local modes)
│   │   └── listener.py             # SSE Database event stream listener
│   ├── agents/
│   │   ├── supervisor.py           # LangGraph manager compiling the agent pipeline
│   │   ├── sensor_agent.py         # Outlier & noise cleaner; reports Sensor Quality
│   │   ├── environment_agent.py    # Calculates environmental stability & comfort indexes
│   │   ├── algae_agent.py          # Computes photosynthesis eff., growth rates, biomass
│   │   ├── prediction_agent.py     # Extrapolates GI, Temp & motor life (1h, 24h, 7d)
│   │   ├── anomaly_agent.py        # Monitors safety limit bounds & triggers active alerts
│   │   ├── maintenance_agent.py    # Calculates pump running hours & Remaining Useful Life
│   │   ├── recommendation_agent.py # Invokes Gemini API for diagnostics
│   │   ├── research_agent.py       # Compiles scientific biological summary logs
│   │   └── report_agent.py         # Exports PDF summaries & telemetry CSV history sheets
│   ├── llm/
│   │   ├── gemini.py               # Google Gemini client wrapper
│   │   └── prompts.py              # Prompt definitions for LLM agents
│   └── routes/
│       └── api.py                  # API routes (/api/latest, /api/telemetry, /api/ask-ai)
└── frontend/
    ├── pages/
    │   ├── index.tsx               # Entrypoint (Redirects to /dashboard)
    │   ├── dashboard.tsx           # Main industrial-style analytics center
    │   ├── reports.tsx             # PDF/CSV Report compile manager
    │   └── settings.tsx            # Live Telemetry Injector & configuration
    ├── components/
    │   ├── Sidebar.tsx             # Nav bar
    │   ├── Header.tsx              # System connectivity status bar
    │   ├── SensorCards.tsx         # Telemetry values grids
    │   ├── HealthGauge.tsx         # Radial biological health ring & stress progress bars
    │   ├── MotorControl.tsx        # Pump manual switches, speeds, emergency stops
    │   ├── Alerts.tsx              # Scrolling alert logging feed
    │   ├── AgentStatus.tsx         # LangGraph pipeline runtime & decisions list
    │   ├── PredictionCharts.tsx    # Recharts trend forecaster
    │   ├── RecommendationPanel.tsx # Gemini troubleshooter tips
    │   └── ChatWindow.tsx          # Floating "Ask AI Assistant" widget
    └── services/
        └── api.ts                  # Frontend API fetch wrappers
```

---

## ⚡ Quick Start

### 1. Prerequisites
Ensure you have:
* Python 3.12+ installed
* Node.js v18+ and npm installed

### 2. Backend Setup
1. Open a terminal, navigate to `/backend`, and create a `.env` file:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   FIREBASE_DATABASE_URL=https://your-project-rtdb.firebaseio.com
   FIREBASE_PROJECT_ID=your-project-id
   DATABASE_MODE=firebase # Set to 'local' to run offline without Firebase
   PORT=8000
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the FastAPI server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Navigate to `/frontend` folder.
2. Install Node packages:
   ```bash
   npm install
   ```
3. Run the Next.js development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 📡 REST API Documentation

### Telemetry & Diagnostics
* **`GET /api/latest`**: Returns the most recent telemetry packet and calculated analytics.
* **`GET /api/history`**: Returns a list of the 50 most recent telemetry events.
* **`POST /api/telemetry`**: Inject a raw telemetry packet (used by ESP32 or the simulator).
  * Payload:
    ```json
    {
      "algae": { "green_idx": 0.8, "health": 80, "light_lux": 1500, "temp_c": 23.5 },
      "env": { "altitude": 150.0, "pressure": 1013.2 },
      "gas": { "mq135": 180, "mq2": 30, "mq3": 20, "mq7": 25 },
      "motor": { "status": "ON", "speed": 60, "flow_rate": 2.4, "operating_hours": 120 },
      "timestamp": 1785511869
    }
    ```

### AI & Reporting
* **`POST /api/ask-ai`**: Send a message to the AI agent regarding the reactor state.
* **`POST /api/generate-report`**: Trigger report compilations.
  * Parameters: `{"report_type": "daily"|"weekly"|"monthly"|"research", "format": "pdf"|"csv"}`
  * Returns: A download stream of the generated document.

### Actuator Control
* **`POST /api/manual-control`**: Modify pump speeds or trigger emergency stops.
  * Payload:
    ```json
    {
      "status": "AUTO",
      "speed": 75.0,
      "emergency_stop": false
    }
    ```
