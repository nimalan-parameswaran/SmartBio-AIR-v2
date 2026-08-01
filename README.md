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
├── system documentation.md         # System documentation (Agents & Dashboard)
├── backend/                        # FastAPI Python backend
│   ├── app.py                      # FastAPI entrypoint (starts listeners & simulation)
│   ├── config.py                   # App configurations & ENV loading
│   ├── local_db.json               # Auto-generated JSON database fallback
│   ├── requirements.txt            # Python requirements (LangGraph, FastAPI, FPDF2, etc.)
│   ├── test_agents.py              # Tests for LangGraph multi-agent pipeline
│   ├── agents/                     # LangGraph Multi-Agent implementation
│   │   ├── algae_agent.py          # Computes photosynthesis eff., growth rates, biomass
│   │   ├── anomaly_agent.py        # Monitors safety limit bounds & triggers active alerts
│   │   ├── environment_agent.py    # Calculates environmental stability & comfort indexes
│   │   ├── maintenance_agent.py    # Calculates pump running hours & Remaining Useful Life
│   │   ├── prediction_agent.py     # Extrapolates GI, Temp & motor life (1h, 24h, 7d)
│   │   ├── recommendation_agent.py # Invokes Gemini API for diagnostics
│   │   ├── report_agent.py         # Exports PDF summaries & telemetry CSV history sheets
│   │   ├── research_agent.py       # Compiles scientific biological summary logs
│   │   ├── sensor_agent.py         # Outlier & noise cleaner; reports Sensor Quality
│   │   └── supervisor.py           # LangGraph manager compiling the agent pipeline
│   ├── firebase/                   # Firebase DB client and listeners
│   │   ├── firebase.py             # Firebase DB client (supports REST and local modes)
│   │   └── listener.py             # SSE Database event stream listener
│   ├── llm/                        # Language model integration
│   │   ├── gemini.py               # Google Gemini client wrapper
│   │   └── prompts.py              # Prompt definitions for LLM agents
│   ├── models/                     # Data models and schemas
│   │   └── schemas.py              # Pydantic schema declarations
│   ├── reports/                    # Directory for generated PDF/CSV reports
│   ├── routes/                     # API routers
│   │   └── api.py                  # API routes (/api/latest, /api/telemetry, /api/ask-ai)
│   ├── services/                   # Business logic services
│   │   ├── alerts.py               # Alert checking logic
│   │   ├── analytics.py            # Analytics computations
│   │   └── prediction.py           # Prediction and estimation logic
│   └── utils/                      # Helper utility modules
│       ├── helper.py               # Miscellaneous helpers
│       └── logger.py               # Logger settings
├── dataset/                        # Datasets, acquisition, and preprocessing
│   ├── 1. datasets-main/           # Primary raw and processed data
│   │   ├── dataset - main.csv      # Main aggregated CSV dataset
│   │   ├── processed dataset/      # Processed data outputs
│   │   │   ├── ei_fault.csv
│   │   │   └── ei_normal.csv
│   │   └── raw data/               # Raw sensor collection dumps
│   │       ├── Fault_data.csv
│   │       ├── Normal1_data.csv
│   │       └── Normal2_data.csv
│   ├── 2. data acquisition/        # Scripts for telemetry gathering
│   │   ├── DataCollection.ino      # ESP32 code for reading and transmitting sensor readings
│   │   └── logger.py               # Python serial data logging utility
│   └── 3. data preprocessing/      # Notebooks for data transformation
│       └── Data_Preprocessing_and_EDA.ipynb # Jupyter notebook for cleaning and EDA
├── frontend/                       # Next.js React frontend application
│   ├── eslint.config.mjs           # ESLint configuration
│   ├── next.config.ts              # Next.js configurations
│   ├── package.json                # Frontend package dependencies & scripts
│   ├── tsconfig.json               # TypeScript configuration
│   ├── components/                 # Reusable React components
│   │   ├── AgentStatus.tsx         # LangGraph pipeline runtime & decisions list
│   │   ├── Alerts.tsx              # Scrolling alert logging feed
│   │   ├── ChatWindow.tsx          # Floating "Ask AI Assistant" widget
│   │   ├── Header.tsx              # System connectivity status bar
│   │   ├── HealthGauge.tsx         # Radial biological health ring & stress progress bars
│   │   ├── MotorControl.tsx        # Pump manual switches, speeds, emergency stops
│   │   ├── PredictionCharts.tsx    # Recharts trend forecaster
│   │   ├── RecommendationPanel.tsx # Gemini troubleshooter tips
│   │   ├── SensorCards.tsx         # Telemetry values grids
│   │   └── Sidebar.tsx             # Navigation bar
│   ├── pages/                      # Application route views
│   │   ├── index.tsx               # Entrypoint (Redirects to /dashboard)
│   │   ├── dashboard.tsx           # Main industrial-style analytics center
│   │   ├── reports.tsx             # PDF/CSV Report compile manager
│   │   └── settings.tsx            # Live Telemetry Injector & configuration
│   ├── services/                   # Frontend API connectors
│   │   └── api.ts                  # Frontend API fetch wrappers
│   └── styles/                     # Tailwind or global styling sheets
│       └── globals.css             # Global Tailwind/CSS rules
├── myosa_sketche/                  # Microcontroller firmware files
│   └── main.ino                    # Core ESP32 sketch for sensor readout and actuators
└── TinyML/                         # Embedded machine learning models and pipelines
    ├── README.md                   # TinyML project-specific documentation
    ├── fault diagnosis and anomaly detection/ # Exported Edge Impulse Arduino libraries
    │   ├── ei-myosa-6vdmp-fault-detection-arduino-1.0.2-TFlite.zip
    │   └── ei-myosa-6vdmp-fault-detection-arduino-1.0.3-EON.zip
    ├── src/                        # TinyML pipeline documentation assets
    └── test inference/             # Embedded testing firmware
        └── test_inference.ino      # Arduino test sketch running on-device inference
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
