```mermaid
graph TD
    %% Define styles/classes
    classDef hardware fill:#1e271e,stroke:#4e883f,stroke-width:2px,color:#fff;
    classDef database fill:#0f172a,stroke:#2563eb,stroke-width:2px,color:#fff;
    classDef backend fill:#2e1534,stroke:#86198f,stroke-width:2px,color:#fff;
    classDef agent fill:#0f2c31,stroke:#0d9488,stroke-width:2px,color:#fff;
    classDef frontend fill:#33290f,stroke:#d97706,stroke-width:2px,color:#fff;

    subgraph Edge Layer [Hardware & Edge AI]
        esp32["ESP32 Microcontroller (MYOSA Mini Kit)"]:::hardware
        sensors["Sensors (Lux, Temp, Gas, Pressure)"]:::hardware
        tinyml["TinyML (Edge Impulse / TFlite Anomaly Model)"]:::hardware
        actuators["Actuators (PWM Motors & Relay Pumps)"]:::hardware
        
        sensors --> esp32
        esp32 --> tinyml
        esp32 --> actuators
    end

    subgraph Storage Layer [Cloud Synchronization]
        firebase["Firebase Realtime Database"]:::database
    end

    subgraph Processing Layer [FastAPI Backend]
        fastapi["FastAPI Server"]:::backend
        sse["SSE Listener (Stream events)"]:::backend
        db_fallback["Local DB JSON Fallback"]:::backend
        fastapi --> db_fallback
    end

    subgraph AI Pipeline [LangGraph Multi-Agent Reasoning]
        state["TypedDict State Accumulator"]:::agent
        supervisor["LangGraph Supervisor"]:::agent
        
        sensor_a["1. Sensor Validation Agent"]:::agent
        env_a["2. Environment Agent"]:::agent
        algae_a["3. Algae Health Agent"]:::agent
        pred_a["4. Prediction Agent"]:::agent
        anomaly_a["5. Anomaly Agent"]:::agent
        maint_a["6. Maintenance Agent"]:::agent
        rec_a["7. Recommendation Agent (Gemini)"]:::agent
        research_a["8. Research Agent (Gemini)"]:::agent
        report_a["9. Report Agent (FPDF2)"]:::agent

        state --> supervisor
        supervisor --> sensor_a --> env_a --> algae_a --> pred_a --> anomaly_a --> maint_a --> rec_a --> research_a --> report_a
        report_a --> state
    end

    subgraph Interface Layer [Frontend Command Center]
        nextjs["Next.js Web Dashboard"]:::frontend
        recharts["Recharts Trends Visuals"]:::frontend
        chat["Ask AI Chat Widget"]:::frontend
    end

    %% Data Flow Connections
    esp32 -- "HTTPS POST (REST Telemetry)" --> firebase
    firebase -- "Server-Sent Events (SSE) Stream" --> sse
    sse --> fastapi
    fastapi -- "Trigger Graph Workflow" --> supervisor
    report_a -- "Output PDF Reports" --> fastapi
    fastapi -- "Update Analytics & Reports Node" --> firebase
    firebase -- "React Hook Listeners (Real-time Sync)" --> nextjs
    nextjs -- "Fetch PDF/CSV Reports" --> fastapi
    chat --> fastapi
    nextjs -- "Manual Actuator Override Settings" --> firebase
    firebase -- "Device Command Node Pull" --> esp32
```


# Architectural Layers

#### 1. Edge & IoT Layer (ESP32 / MYOSA Mini Kit)
- **Data Collection**: The microcontroller queries environmental, gas, biological, and mechanical sensors at fixed intervals (typically every 5 seconds).
- **Edge AI (TinyML)**: Rather than pushing raw data blindly, the ESP32 passes telemetry through an **Edge Impulse TinyML model** compiled with TensorFlow Lite Micro. This model checks high-frequency fluctuations in motor vibration and current profiles locally to flag mechanical anomalies at the edge.
- **Safety Interlocks & Fail-Safes**: If communication with the cloud is lost, the local ESP32 handles core control feedback loops (e.g. shutting down pumps if water levels are depleted or activating manual flow overrides).
- **Communication Protocol**: Data is packed into JSON formats and pushed via secure REST API (HTTPS POST) calls directly into the cloud storage layer.

#### 2. Cloud Telemetry Synchronization Layer (Firebase Realtime Database)
- **Low-Latency Database**: Firebase acts as the central datastore and communication broker. It exposes real-time database paths for raw telemetry, processed analytics, agent decision logs, motor control overrides, and reports metadata.
- **Server-Sent Events (SSE)**: Raw telemetry updates in Firebase trigger instantaneous Server-Sent Events (SSE) which are streamed downstream to the FastAPI server without polling overhead.

#### 3. Processing Layer (FastAPI Backend Server)
- **Event Listeners**: A persistent asynchronous loop in the backend listens to SSE updates from Firebase.
- **Pipeline Orchestrator**: Whenever a telemetry payload is received, the backend launches the multi-agent AI pipeline.
- **API Gateways**: Hosts REST endpoints for the Next.js frontend, including:
  * `/api/telemetry`: Manual telemetry injection.
  * `/api/latest`: Fetching current metrics and consolidated reports.
  * `/api/generate-report`: Compiling daily, weekly, or scientific diagnostic reports.
  * `/api/ask-ai`: Rerouting user chat queries to Google Gemini.

#### 4. Agentic AI & Reasoning Layer (LangGraph Multi-Agent Pipeline)
Instead of processing sensor telemetry through standard conditional scripts or a single static LLM prompt, Smart BIO AIR uses a **9-agent LangGraph workflow**.
- **State Propagation**: The graph uses a centralized `GraphState` TypedDict to accumulate telemetry variables, analysis arrays, predictive trends, anomaly reports, Gemini diagnostic tips, and markdown research logs.
- **Execution Pipeline**:
  1. **Sensor Validation Agent**: Filters sensor noise and checks value bounds, assigning a **Sensor Quality Score**.
  2. **Environment Analysis Agent**: Calculates Air Quality scores, Comfort Index, stability variance, and light suitability.
  3. **Algae Health Agent**: Estimates microalgae biomass density (g/L) and calculates growth rates and biological stress metrics.
  4. **Prediction Agent**: Forecasts Green Index density, culture temperature, and water flow trends over 1-hour, 24-hour, and 7-day intervals.
  5. **Anomaly Detection Agent**: Cross-references telemetry against safety thresholds, triggering severity-based alarms.
  6. **Maintenance Agent**: Computes pump remaining useful life (RUL), projects calibration cycles, and schedules biological wash cycles.
  7. **Recommendation Agent**: Formulates context-aware troubleshooter checklists and action guides via **Google Gemini**.
  8. **Research Agent**: Drafts scientific biological logs explaining ecological relationships (e.g. photosynthesis cycles) via **Google Gemini**.
  9. **Report Agent**: Takes consolidated state variables and generates a styled PDF Diagnostic Summary using FPDF2.
- **Writeback & Sync**: Once the Report Agent finishes execution, the FastAPI backend publishes the updated analytics, warnings, and PDF reports directly back to Firebase, which synchronizes instantly with the frontend.

#### 5. Interface Layer (Next.js Dashboard Command Center)
- **Real-Time Data Display**: Next.js listens directly to Firebase paths via React hooks. The dashboard updates components dynamically—such as the biological ring (`HealthGauge.tsx`) and notifications list (`Alerts.tsx`)—whenever the database changes.
- **Interactive Controls**: Users can adjust pump speed sliders and auto/manual modes directly in the dashboard, which writes back command tokens to Firebase. These overrides are pulled instantly by the ESP32.
- **Ask AI Workspace**: Integrated Chat widgets allow operators to chat directly with Gemini regarding reactor state, sensor trends, or scientific insights.
