import React, { useState, useEffect } from "react";
import Head from "next/head";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SensorCards from "../components/SensorCards";
import HealthGauge from "../components/HealthGauge";
import MotorControl from "../components/MotorControl";
import Alerts from "../components/Alerts";
import AgentStatus from "../components/AgentStatus";
import PredictionCharts from "../components/PredictionCharts";
import RecommendationPanel from "../components/RecommendationPanel";
import ChatWindow from "../components/ChatWindow";

import { apiService, TelemetryData, AnalyticsData, SystemStatus, PredictionsData, AgentLog } from "../services/api";

export default function Dashboard() {
  const [latestData, setLatestData] = useState<{ telemetry?: TelemetryData; analytics?: AnalyticsData }>({});
  const [history, setHistory] = useState<TelemetryData[]>([]);
  const [predictions, setPredictions] = useState<PredictionsData>({});
  const [recommendations, setRecommendations] = useState<string[]>([]);
  const [agents, setAgents] = useState<AgentLog[]>([]);
  const [system, setSystem] = useState<SystemStatus>({
    status: "OFFLINE",
    database_mode: "LOCAL_FALLBACK",
    air_purification_score: 0.0,
    algae_health: 0.0,
    motor_status: "OFF",
    pump_speed: 0.0,
    emergency_stop: false,
    last_update: Date.now() / 1000
  });

  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const [latest, hist, pred, recs, ags, sys] = await Promise.all([
        apiService.getLatest(),
        apiService.getHistory(30),
        apiService.getPrediction(),
        apiService.getRecommendation(),
        apiService.getAgents(),
        apiService.getSystem()
      ]);

      if (latest && latest.telemetry) {
        setLatestData(latest);
      }
      setHistory(hist);
      setPredictions(pred);
      setRecommendations(recs);
      setAgents(ags);
      setSystem(sys);
    } catch (err) {
      console.error("Error fetching dashboard telemetry: ", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // Poll updates every 4 seconds for immediate dynamic experience
    const interval = setInterval(fetchDashboardData, 4000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#090d0b] flex items-center justify-center text-[#e2f0e7]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-semibold tracking-widest uppercase opacity-75">Loading Bioreactor Core...</p>
        </div>
      </div>
    );
  }

  // Fallback default telemetry if backend is entirely empty
  const activeTelemetry: TelemetryData = latestData.telemetry || {
    algae: { green_idx: 0.5, health: 80, light_lux: 1000, temp_c: 22.0 },
    env: { altitude: 150, pressure: 1013 },
    gas: { mq135: 150, mq2: 30, mq3: 20, mq7: 25 },
    motor: { status: "OFF", speed: 0, flow_rate: 0, operating_hours: 0 },
    timestamp: Date.now() / 1000
  };

  const activeAnalytics: AnalyticsData = latestData.analytics || {
    photosynthesis_efficiency: 75.0,
    biomass_g_l: 0.11,
    growth_rate_hr: 0.0,
    stress_index: 10.0,
    air_purification_score: 88.0,
    comfort_index: 92.0,
    environmental_stability: 95.0
  };

  // Derive alerts from telemetry warnings
  const alerts = agents.find(a => a.agent === "Anomaly Detection Agent")?.reasoning 
    ? (latestData.telemetry ? (agents.find(a => a.agent === "Anomaly Detection Agent")?.reasoning.includes("issues") ? [
        {
          id: "1",
          type: "warning",
          source: "Anomaly Agent",
          message: agents.find(a => a.agent === "Anomaly Detection Agent")?.reasoning || "",
          timestamp: Date.now() / 1000
        }
      ] : []) : [])
    : [];

  const activeAlerts = alerts.length > 0 ? alerts : (
    system.status === "CRITICAL" 
      ? [{ id: "1", type: "critical", source: "System Agent", message: "Critical parameters breached! Inspect reactor immediately.", timestamp: Date.now()/1000 }]
      : []
  );

  return (
    <>
      <Head>
        <title>Smart BIO AIR – AI Bioreactor Monitor</title>
        <meta name="description" content="Industrial AI algae bioreactor and indoor air purification monitoring hub." />
      </Head>

      <div className="min-h-screen bg-[#090d0b] flex">
        {/* Sidebar Nav */}
        <Sidebar />

        {/* Dashboard Main Contents */}
        <div className="flex-1 pl-64 flex flex-col min-h-screen">
          <Header system={system} />

          <main className="flex-1 p-6 space-y-6 overflow-y-auto">
            {/* Real-time metrics grid */}
            <SensorCards telemetry={activeTelemetry} />

            {/* Middle Section: Algae Biology & Motor Control */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <HealthGauge analytics={activeAnalytics} telemetry={activeTelemetry} />
              
              <MotorControl 
                telemetry={activeTelemetry} 
                maintenance={agents.find((a) => a.agent === "Maintenance Agent")?.latest_decision} 
                onControlChange={fetchDashboardData} 
              />
            </div>

            {/* Bottom Grid: Prediction Charts, Alerts, & Recommendations */}
            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              {/* Predictions area */}
              <div className="xl:col-span-2">
                <PredictionCharts predictions={predictions} history={history.length > 0 ? history : [activeTelemetry]} />
              </div>
              
              {/* Diagnostic alerts & Gemini recs */}
              <div className="space-y-6">
                <RecommendationPanel recommendations={recommendations} />
                <Alerts alerts={activeAlerts} />
              </div>
            </div>

            {/* Agent runtime tracker */}
            <div className="grid grid-cols-1 gap-6">
              <AgentStatus logs={agents} />
            </div>
          </main>
        </div>

        {/* Ask AI Floating Chat */}
        <ChatWindow />
      </div>
    </>
  );
}
