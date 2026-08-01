<div align="center">
  <p><a><img width="100%" src="img/SmartBio Air.png"></a></p>
</div>

PublishDate: 2026-08-01

Title: **Smart BIO AIR Version 2.0:** Agentic AI-Driven Indoor Algae Based Air Purification System Using MYOSA Mini IoT Kit

An AI-powered autonomous algae bioreactor that combines Edge AI, IoT, LangGraph multi-agent reasoning, and cloud analytics to monitor biological health, predict system behaviour, automate maintenance, and improve indoor air quality.

---

## Contributors  

- **Nimalan Parameswaran** - [@nimalan-parameswaran](https://github.com/nimalan-parameswaran)  
- **Dhakshatha M K** - [@DhakshathaMylsamy](https://github.com/DhakshathaMylsamy)
  
---

## Acknowledgement 
We express our sincere gratitude to **Dr. Dinesh Chellappan**, Centre for Research and Development, for his valuable guidance, technical direction, and continuous mentorship throughout this project.

We also extend our heartfelt thanks to the **IEEE Sensors Council** for sponsoring the **MYOSA Mini IoT Kit**, which played a crucial role in enabling the development and implementation of this work.

---

<p align="center">
  <img src="img/Img1.jpg" width="600">
</p>

---

## Overview

**Smart BIO AIR Version 2.0** is an AI-powered autonomous algae bioreactor platform designed to improve indoor air quality while serving as an intelligent research platform for biological and environmental monitoring. The system combines living microalgae, Edge AI, IoT sensing, cloud computing, and a multi-agent artificial intelligence framework to continuously monitor environmental conditions, evaluate algae health, predict future system behaviour, and assist operators with real-time decision making.

The platform was developed as the next-generation evolution of **Smart BIO AIR Version 1**, following technical feedback received from researchers, scientists, industry professionals, and academic experts during **APSCON 2026** in New Delhi. Practical deployment of the first prototype highlighted several real-world challenges, including algae decomposition, odour generation, hardware degradation, cloud communication latency, and the absence of predictive intelligence. Version 2.0 addresses these limitations through a completely redesigned software architecture centred around autonomous AI agents and predictive analytics.

At the hardware level, the system uses the **MYOSA Mini IoT Kit (ESP32)** to acquire real-time telemetry from environmental sensors, gas sensors, motor diagnostics, and the algae cultivation chamber. Safety-critical operations such as motor control and TinyML-based fault detection continue to execute locally on the edge device, allowing uninterrupted operation even during temporary network failures.

Sensor telemetry is synchronised with the cloud through **Firebase Realtime Database**, where a **FastAPI** backend orchestrates a **LangGraph Multi-Agent AI pipeline** powered by **Google Gemini**. Rather than relying on a single AI model, the platform distributes intelligence across multiple specialised agents responsible for sensor validation, environmental analysis, algae health assessment, prediction, anomaly detection, predictive maintenance, recommendations, scientific research summarisation, and automated report generation. This modular architecture enables the system to reason about biological and operational conditions in a structured and explainable manner.

A modern **Next.js** dashboard functions as the operational command centre, presenting live telemetry, biological health indicators, predictive trend visualisations, AI-generated recommendations, maintenance schedules, active alerts, and an interactive "Ask AI" assistant for researchers and operators. The platform also generates downloadable PDF diagnostic reports and CSV telemetry datasets, supporting long-term environmental studies and experimental documentation.

To improve real-world usability, Version 2.0 introduces an activated carbon filtration stage that significantly reduces odour released from the algae chamber while maintaining biological activity. The prototype was evaluated under indoor conditions in a closed 250 sq ft room in Coimbatore over five experimental trials, demonstrating an average reduction of approximately **30% in both AQI and CO₂ concentrations within two hours**, while maintaining stable autonomous operation throughout the testing period.

Smart BIO AIR Version 2.0 is more than an indoor air purification system. It is an intelligent cyber-physical platform that combines biological engineering, Edge AI, IoT, cloud computing, Large Language Models, and multi-agent artificial intelligence to create a next-generation autonomous environmental monitoring and algae bioreactor research system. The platform is intended for applications in indoor environmental management, smart buildings, sustainable biotechnology, educational laboratories, and future AI-assisted biological research.

---
## Problem Statement

Conventional indoor air purification systems mainly depend on mechanical filtration methods that remove pollutants but do not actively participate in biological carbon reduction or environmental adaptation. Algae-based purification systems have strong potential for CO₂ absorption and oxygen generation; however, practical deployment faces challenges such as algae degradation, odour generation, system instability, hardware failures, and limited intelligent monitoring.

Existing IoT-based environmental systems mainly collect sensor data without providing autonomous reasoning, predictive maintenance, or biological analysis. There is a need for an intelligent platform that can continuously monitor air quality, understand algae behaviour, predict failures, and assist operators through AI-based decision support.

Smart BIO AIR Version 2.0 addresses these challenges by combining algae-based purification, Edge AI, IoT sensing, cloud analytics, and Multi-Agent AI to create an autonomous and research-oriented indoor bioreactor platform.

---
## Solution

<p align="center">
  <img src="img/Img2.png" width="50%" /> 
</p>

Smart BIO AIR Version 2.0 addresses the limitations of conventional indoor air purifiers and first-generation algae-based purification systems by combining biological air treatment, Edge AI, IoT sensing, cloud computing, and Multi-Agent Artificial Intelligence into a unified autonomous platform.

The system employs **living microalgae (*Chlorella vulgaris*)** as the primary biological medium for capturing carbon dioxide and supporting natural oxygen generation. Unlike conventional filtration systems that only trap airborne pollutants, the algae bioreactor performs continuous biological treatment while simultaneously serving as a living research model for studying environmental changes and biomass growth.

At the edge layer, the **MYOSA Mini IoT Kit (ESP32)** continuously acquires telemetry from multiple environmental sensors, gas sensors, motor diagnostics, and the algae cultivation chamber. Safety-critical operations—including motor control, relay management, sensor monitoring, and TinyML-based fault detection—are executed locally on the microcontroller. This enables uninterrupted operation even during temporary internet outages and significantly reduces response latency for hardware protection.

Sensor telemetry is synchronised with the cloud through **Firebase Realtime Database**, where a **FastAPI** backend processes incoming data and coordinates a **LangGraph Multi-Agent AI framework** powered by **Google Gemini**. Instead of relying on a single AI model, the platform distributes analytical responsibilities across specialised agents responsible for:

- Sensor validation and data quality assessment
- Environmental condition analysis
- Algae health and biomass estimation
- Future state prediction
- Anomaly detection
- Predictive maintenance
- AI-generated operational recommendations
- Scientific research summarisation
- Automated report generation

This agent-based architecture enables the system to move beyond simple monitoring by continuously interpreting environmental conditions, predicting biological behaviour, detecting abnormal events before failures occur, and generating explainable recommendations for researchers and operators.

To overcome practical deployment challenges identified during Smart BIO AIR Version 1, Version 2.0 incorporates several engineering improvements. An **activated carbon filtration stage** has been integrated to minimise odour released from the algae chamber, while predictive maintenance algorithms estimate motor health, remaining useful life, and sensor calibration schedules. These enhancements increase long-term reliability and reduce manual maintenance requirements.

A modern **Next.js** web dashboard serves as the operational command centre, providing live telemetry visualisation, biological health indicators, AI-generated diagnostics, predictive analytics, actuator controls, maintenance schedules, and an interactive **Ask AI** assistant for real-time system interaction. Researchers can also generate PDF diagnostic reports and CSV telemetry datasets for long-term analysis and documentation.

By integrating biological air purification with Edge AI, TinyML, cloud-native multi-agent intelligence, predictive analytics, and real-time visualisation, Smart BIO AIR Version 2.0 evolves from a prototype air purifier into an intelligent autonomous bioreactor platform capable of supporting sustainable indoor air purification, scientific research, and future AI-assisted environmental monitoring applications.

---
## System Workflow

<p align="center">
  <img src="img/system workflow.png" width=auto>
</p>

---

## System Architecture

The Smart BIO AIR Version 2.0 platform utilizes a multi-layered cyber-physical architecture to enable real-time telemetry streaming, edge computations, cloud database synchronization, and complex agentic AI reasoning.

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
---
## Features

- **AI-Driven Algae Bioreactor**
  - Uses *Chlorella vulgaris* for biological CO₂ absorption and oxygen generation with continuous health monitoring.

- **Real-Time Environmental Monitoring**
  - Collects temperature, light intensity, pressure, gas concentration, algae growth indicators, and motor parameters using IoT sensors.

- **LangGraph Multi-Agent AI System**
  - Uses specialised AI agents for sensor validation, environmental analysis, algae health assessment, prediction, anomaly detection, maintenance, recommendations, and reporting.

- **Edge AI-Based Autonomous Control**
  - Performs local decision-making on ESP32 for motor protection, fault detection, and operation during network failures.

- **TinyML Motor Fault Detection**
  - Uses vibration analysis from MPU6050 sensors to identify abnormal pump conditions.

- **Predictive Analytics**
  - Forecasts algae growth trends, environmental changes, and equipment behaviour using historical telemetry.

- **AI-Based Monitoring Dashboard**
  - Provides real-time visualization of sensor data, algae health status, alerts, predictions, reports, and system controls.

- **Odour Management System**
  - Uses activated carbon filtration to reduce algae-related smell during indoor operation.

- **Automated Research Reports**
  - Generates PDF diagnostic reports and CSV datasets for experimental analysis.

- **Cloud-Connected Data Management**
  - Synchronizes telemetry through Firebase Realtime Database for low-latency monitoring and AI processing.
 
---

## Experimental Indoor Testing

Smart BIO AIR was evaluated through prototype-level indoor testing in a real semi-urban environment to study its air purification performance and autonomous operation capability.

**Note:** The experiment was conducted at prototype level and was not performed under controlled laboratory conditions.

### Testing Conditions

| Parameter | Value |
|-----------|-------|
| Location | Coimbatore |
| Environment | Semi-urban indoor environment |
| Room Size | 250 sq ft |
| Ventilation | Closed room |
| Duration | 3 hours per trial |
| Trials | 5 days |

### Results

| Trial | Initial AQI | Final AQI | AQI Reduction | Initial CO₂ (ppm) | Final CO₂ (ppm) | CO₂ Reduction |
|------:|------------:|----------:|--------------:|------------------:|----------------:|--------------:|
| 1 | 162 | 118 | 27.1% | 1180 | 860 | 27.1% |
| 2 | 176 | 121 | 31.2% | 1280 | 870 | 32.0% |
| 3 | 158 | 109 | 31.0% | 1150 | 790 | 31.3% |
| 4 | 171 | 122 | 28.6% | 1240 | 890 | 28.2% |
| 5 | 168 | 116 | 31.0% | 1210 | 845 | 30.1% |

Across five trials, Smart BIO AIR achieved an average reduction of approximately **30% in AQI and CO₂ levels within two hours**. The Edge AI architecture maintained stable operation during network interruptions, while continuous telemetry logging enabled monitoring of air quality changes and algae chamber behaviour.

---
## Novelty

Smart BIO AIR Version 2.0 introduces an intelligent cyber-physical approach for algae-based indoor air purification by combining biological systems with autonomous AI reasoning.

### Key Novel Contributions

- **First Multi-Agent AI Architecture for Algae Bioreactor Monitoring**
  - Introduces a LangGraph-based agentic framework where independent AI agents collaboratively analyse biological, environmental, and mechanical conditions.

- **Biological Digital Twin Concept**
  - Creates a data-driven representation of algae growth behaviour by correlating environmental parameters, biomass indicators, and operational conditions.

- **Hybrid Edge-Cloud Intelligence**
  - Combines ESP32-based TinyML execution for fast safety decisions with cloud-based Gemini AI reasoning for advanced analysis.

- **Autonomous Biological Decision Support**
  - Moves beyond conventional monitoring by enabling AI-assisted interpretation of algae health, stress conditions, and operational requirements.

- **Predictive Failure Prevention for Bioreactor Systems**
  - Introduces AI-assisted maintenance estimation for pumps, sensors, and critical components before system failure.

- **Research-Oriented AI Documentation Framework**
  - Automatically generates scientific summaries, diagnostic reports, and experimental records from continuous telemetry.

- **Low-Latency AI-Enabled Environmental Monitoring**
  - Combines real-time database synchronization and event-based processing for rapid system response.

- **Indoor Deployment-Oriented Algae Engineering**
  - Addresses practical limitations of algae systems through odour control, autonomous operation, and intelligent monitoring.

- **Integrated Bio-IoT-Agentic AI Platform**
  - Establishes a new platform combining biotechnology, IoT, Edge AI, Large Language Models, and autonomous agents for sustainable environmental applications.
  
---
## Scope of the Project

Smart BIO AIR Version 2.0 focuses on developing an intelligent indoor algae bioreactor platform for air quality monitoring, biological purification, and AI-assisted research.

The project scope includes:

- Indoor air quality monitoring and analysis
- Algae growth and health observation
- Autonomous IoT-based bioreactor operation
- Edge AI-based safety control
- Cloud-based AI analytics
- Predictive maintenance of hardware components
- AI-assisted environmental research documentation
- Real-time dashboard monitoring and control

Future expansion areas include:

- Long-duration laboratory validation
- Larger-scale indoor deployment
- Advanced carbon fixation measurement
- Automated algae harvesting systems
- Smart building integration
- Multiple bioreactor network management

---

## Tech Stack

### Hardware
- MYOSA Mini IoT Kit
- MQ-Series Gas Sensors (MQ-2, MQ-3, MQ-7, MQ-135)
- DC Air Pump and Motor Control System
- Relay Module
- LED Grow Light
- Activated Carbon Filter

### Embedded & Edge AI
- Arduino Framework
- Embedded C/C++
- Edge Impulse
- TinyML

### Backend
- Python
- FastAPI
- LangGraph Multi-Agent Framework
- Pydantic
- REST API
- Server-Sent Events (SSE)

### Artificial Intelligence
- Google Gemini API
- Large Language Models (LLM)
- Agentic AI Workflow
- Predictive Analytics
- Rule-Based Anomaly Detection

### Database & Cloud
- Firebase Realtime Database
- Cloud Telemetry Storage
- JSON Data Processing

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- Recharts

### Data Science
- Python
- Pandas
- NumPy
- Jupyter Notebook
- Data Visualization
- Time-Series Analysis

---

## Folder Structure

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

## Quick Start

### 1. Prerequisites
Ensure you have:
* Python 3.12+ installed
* Node.js v18+ and npm installed

### 2. Backend Setup
1. Open a terminal, navigate to `/backend`, and create a `.env` file:
   ```env
   GEMINI_API_KEY="your_gemini_api_key"
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

## REST API Documentation

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
---
## License

This project is licensed under the MIT License. Refer to the LICENSE file for details.

---

## Contribution Notes

This repository is intended for research and educational use. Contributors are encouraged to document experimental conditions, sensor calibration steps, and data collection procedures clearly when submitting updates.

