const BASE_URL = "http://localhost:8000/api";

export interface TelemetryData {
  algae: {
    green_idx: number;
    health: number;
    light_lux: number;
    temp_c: number;
  };
  env: {
    altitude: number;
    pressure: number;
  };
  gas: {
    mq135: number;
    mq2: number;
    mq3: number;
    mq7: number;
  };
  motor: {
    status: string;
    speed: number;
    flow_rate: number;
    operating_hours: number;
  };
  timestamp: number;
}

export interface AnalyticsData {
  photosynthesis_efficiency?: number;
  biomass_g_l?: number;
  growth_rate_hr?: number;
  stress_index?: number;
  air_purification_score?: number;
  comfort_index?: number;
  environmental_stability?: number;
}

export interface LatestResponse {
  telemetry?: TelemetryData;
  analytics?: AnalyticsData;
  status?: string;
  message?: string;
}

export interface SystemStatus {
  status: string;
  database_mode: string;
  air_purification_score: number;
  algae_health: number;
  motor_status: string;
  pump_speed: number;
  emergency_stop: boolean;
  last_update: number;
}

export interface AgentLog {
  agent: string;
  status: string;
  execution_time_ms: number;
  confidence_score: number;
  latest_decision: string;
  reasoning: string;
}

export interface PredictionInterval {
  green_idx: number;
  temp_c: number;
  mq135: number;
  motor_health: number;
  air_purification_score: number;
  biomass_g_l: number;
  gas_reduction_pct: number;
}

export interface PredictionsData {
  "1h"?: PredictionInterval;
  "24h"?: PredictionInterval;
  "7d"?: PredictionInterval;
}

export const apiService = {
  async getLatest(): Promise<LatestResponse> {
    try {
      const res = await fetch(`${BASE_URL}/latest`);
      return await res.json();
    } catch (err) {
      console.warn("Backend offline. Using fallback simulation data.");
      return {};
    }
  },

  async getHistory(limit = 30): Promise<TelemetryData[]> {
    try {
      const res = await fetch(`${BASE_URL}/history?limit=${limit}`);
      return await res.json();
    } catch (err) {
      return [];
    }
  },

  async getPrediction(): Promise<PredictionsData> {
    try {
      const res = await fetch(`${BASE_URL}/prediction`);
      return await res.json();
    } catch (err) {
      return {};
    }
  },

  async getRecommendation(): Promise<string[]> {
    try {
      const res = await fetch(`${BASE_URL}/recommendation`);
      return await res.json();
    } catch (err) {
      return [];
    }
  },

  async getAgents(): Promise<AgentLog[]> {
    try {
      const res = await fetch(`${BASE_URL}/agents`);
      return await res.json();
    } catch (err) {
      return [];
    }
  },

  async getSystem(): Promise<SystemStatus> {
    try {
      const res = await fetch(`${BASE_URL}/system`);
      return await res.json();
    } catch (err) {
      return {
        status: "OFFLINE",
        database_mode: "LOCAL_FALLBACK",
        air_purification_score: 0.0,
        algae_health: 0.0,
        motor_status: "OFF",
        pump_speed: 0.0,
        emergency_stop: false,
        last_update: Date.now() / 1000
      };
    }
  },

  async sendManualControl(control: {
    status: string;
    speed?: number;
    flow_rate?: number;
    emergency_stop?: boolean;
  }) {
    const res = await fetch(`${BASE_URL}/manual-control`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(control),
    });
    return await res.json();
  },

  async askAI(question: string, history: { role: string; content: string }[]): Promise<string> {
    try {
      const res = await fetch(`${BASE_URL}/ask-ai`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history }),
      });
      const data = await res.json();
      return data.answer;
    } catch (err) {
      return "AI Service is temporarily offline. Please ensure the Python backend is running.";
    }
  },

  async generateReport(reportType: string, format = "pdf"): Promise<Blob | null> {
    try {
      const res = await fetch(`${BASE_URL}/generate-report`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ report_type: reportType, format }),
      });
      if (!res.ok) throw new Error("Failed to generate report");
      return await res.blob();
    } catch (err) {
      console.error(err);
      return null;
    }
  }
};
