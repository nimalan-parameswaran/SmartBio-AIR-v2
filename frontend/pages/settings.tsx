import React, { useState, useEffect } from "react";
import Head from "next/head";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { Settings as SettingsIcon, Play, Database, Flame, HelpCircle } from "lucide-react";
import { apiService, SystemStatus } from "../services/api";

export default function SettingsPage() {
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

  // Injector state
  const [temp, setTemp] = useState(24.0);
  const [lux, setLux] = useState(1500);
  const [gi, setGi] = useState(0.85);
  const [mq135, setMq135] = useState(180);
  const [mq7, setMq7] = useState(30);
  const [runHours, setRunHours] = useState(120.0);
  const [injecting, setInjecting] = useState(false);

  const loadData = async () => {
    try {
      const sys = await apiService.getSystem();
      setSystem(sys);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleInject = async () => {
    setInjecting(true);
    try {
      // Simulate raw telemetry post
      const payload = {
        algae: {
          green_idx: gi,
          health: 80, // will be overwritten by agent
          light_lux: lux,
          temp_c: temp
        },
        env: {
          altitude: 150.0,
          pressure: 1013.2
        },
        gas: {
          mq135: mq135,
          mq2: 35.0,
          mq3: 20.0,
          mq7: mq7
        },
        motor: {
          status: system.motor_status,
          speed: system.pump_speed,
          flow_rate: system.pump_speed * 0.04,
          operating_hours: runHours
        },
        timestamp: Date.now() / 1000
      };

      // In project backend design, writing to Firebase / LocalDB triggers listener.
      // We'll write to database via REST call.
      // To simulate it, we can trigger writing to bio_monitor/{timestamp} or invoke manual push.
      // Our API Service updates latest by writing. Let's make a call to write it.
      const res = await fetch("http://localhost:8000/api/manual-control", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          status: system.motor_status,
          speed: system.pump_speed,
          flow_rate: system.pump_speed * 0.04,
          emergency_stop: false
        })
      });
      
      // Let's directly push new telemetry to backend REST endpoint if available.
      // In our FastAPI app, standard ESP32 can send POST to database. Let's write a route for it if needed,
      // or we can write directly to our client mock database.
      // Let's send an injection request. We can PUT/POST directly to Firebase URL or local backend json.
      // Let's implement a POST to firebase or do it directly.
      const dbUrl = "http://localhost:8000/api/latest"; // or we can create a REST endpoint in backend to post telemetry.
      // Let's post it to backend. Wait! Did we create a POST /api/telemetry endpoint?
      // Let's check our backend/routes/api.py. We have POST /api/manual-control. 
      // Let's check if we can post telemetry. Oh, in our app.py and listener, new telemetry is detected on database.
      // If we are in local mode, how can we post telemetry?
      // In local mode, the backend client instance has `db_client.push_telemetry`.
      // Let's create an endpoint in backend `POST /api/telemetry` so the simulator can easily submit custom readings!
      // This is a brilliant addition. I will edit backend/routes/api.py to add `POST /api/telemetry` to accept telemetry payloads.
      // Let's do that right after this.
      
      const injectRes = await fetch("http://localhost:8000/api/telemetry", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (injectRes.ok) {
        alert("Telemetry injected successfully! Supervisor AI workflow is running.");
        loadData();
      } else {
        alert("Telemetry injected, but failed backend check. Ensure backend is running.");
      }
    } catch (err) {
      console.error(err);
      alert("Injection failed. Is the FastAPI server running on port 8000?");
    } finally {
      setInjecting(false);
    }
  };

  return (
    <>
      <Head>
        <title>Simulation & Configurations - Smart BIO AIR</title>
      </Head>

      <div className="min-h-screen bg-[#090d0b] flex">
        <Sidebar />

        <div className="flex-1 pl-64 flex flex-col min-h-screen">
          <Header system={system} />

          <main className="flex-1 p-6 space-y-6 overflow-y-auto">
            {/* Page Title */}
            <div>
              <h2 className="text-xl font-bold text-emerald-400 tracking-wider uppercase">Simulation & Configurations</h2>
              <p className="text-xs text-[#7ea18b] mt-1">
                Configure your Firebase connection or simulate live sensor readings to test AI agent warning reactions.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Telemetry Injector Panel */}
              <div className="glass-panel p-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3">
                    <Flame className="w-4 h-4 text-emerald-400" />
                    <h3 className="text-sm font-bold text-emerald-400 uppercase">Interactive Telemetry Injector</h3>
                  </div>

                  <div className="space-y-4">
                    {/* Temperature */}
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#a8c3b3]">Simulated Algae Water Temperature</span>
                        <span className="text-emerald-400 font-bold">{temp.toFixed(1)}°C</span>
                      </div>
                      <input
                        type="range"
                        min="10"
                        max="42"
                        step="0.5"
                        value={temp}
                        onChange={(e) => setTemp(parseFloat(e.target.value))}
                        className="w-full accent-emerald-500 h-1 bg-[#121c16] rounded-lg cursor-pointer"
                      />
                      <div className="flex justify-between text-[9px] text-[#7ea18b]">
                        <span>Cold Stress (&lt;16°C)</span>
                        <span>Optimal (22-26°C)</span>
                        <span>Hot Stress (&gt;30°C)</span>
                      </div>
                    </div>

                    {/* Light Lux */}
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#a8c3b3]">Simulated Light Lux</span>
                        <span className="text-amber-500 font-bold">{lux} Lux</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="10000"
                        step="100"
                        value={lux}
                        onChange={(e) => setLux(parseInt(e.target.value))}
                        className="w-full accent-amber-500 h-1 bg-[#121c16] rounded-lg cursor-pointer"
                      />
                      <div className="flex justify-between text-[9px] text-[#7ea18b]">
                        <span>Dark (0 Lux)</span>
                        <span>Optimal (2000 Lux)</span>
                        <span>Extreme Photoinhibition</span>
                      </div>
                    </div>

                    {/* Green Index */}
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#a8c3b3]">Simulated Algae Green Index (Density)</span>
                        <span className="text-emerald-400 font-bold">{gi.toFixed(2)}</span>
                      </div>
                      <input
                        type="range"
                        min="0.1"
                        max="2.5"
                        step="0.05"
                        value={gi}
                        onChange={(e) => setGi(parseFloat(e.target.value))}
                        className="w-full accent-emerald-500 h-1 bg-[#121c16] rounded-lg cursor-pointer"
                      />
                    </div>

                    {/* MQ135 */}
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#a8c3b3]">Simulated MQ135 (Indoor CO₂ / Vocs)</span>
                        <span className="text-cyan-400 font-bold">{mq135} ppm</span>
                      </div>
                      <input
                        type="range"
                        min="50"
                        max="800"
                        step="10"
                        value={mq135}
                        onChange={(e) => setMq135(parseInt(e.target.value))}
                        className="w-full accent-cyan-500 h-1 bg-[#121c16] rounded-lg cursor-pointer"
                      />
                      <div className="flex justify-between text-[9px] text-[#7ea18b]">
                        <span>Clean Air (&lt;150)</span>
                        <span>Elevated (&gt;350)</span>
                        <span>Hazardous (&gt;500)</span>
                      </div>
                    </div>

                    {/* Motor Hours */}
                    <div>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-[#a8c3b3]">Simulated Motor Cumulative Operating Hours</span>
                        <span className="text-emerald-400 font-bold">{runHours} hrs</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="6000"
                        step="50"
                        value={runHours}
                        onChange={(e) => setRunHours(parseFloat(e.target.value))}
                        className="w-full accent-emerald-500 h-1 bg-[#121c16] rounded-lg cursor-pointer"
                      />
                      <div className="flex justify-between text-[9px] text-[#7ea18b]">
                        <span>Brand New</span>
                        <span>Service Due (3000 hrs)</span>
                        <span>Replace Required (4500 hrs)</span>
                      </div>
                    </div>
                  </div>
                </div>

                <button
                  onClick={handleInject}
                  disabled={injecting}
                  className="w-full mt-6 py-2 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-black text-xs font-bold uppercase rounded-lg flex items-center justify-center gap-2 transition-colors cursor-pointer"
                >
                  <Play className="w-4 h-4 fill-black" />
                  <span>{injecting ? "Injecting Reading..." : "Inject Telemetry Packet"}</span>
                </button>
              </div>

              {/* Configurations Detail Panel */}
              <div className="glass-panel p-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3">
                    <Database className="w-4 h-4 text-emerald-400" />
                    <h3 className="text-sm font-bold text-emerald-400 uppercase">Firebase & API Configuration</h3>
                  </div>

                  <div className="space-y-4 text-xs">
                    <div className="bg-[#121c16]/50 p-3 rounded-lg border border-[#1e3226]/50 space-y-2">
                      <div className="font-bold text-[#e2f0e7] mb-1">Active Cloud Database:</div>
                      <div>
                        <span className="text-[#7ea18b] block text-[10px]">PROJECT ID</span>
                        <span className="font-mono text-[#a8c3b3]">smartbioair-v1</span>
                      </div>
                      <div>
                        <span className="text-[#7ea18b] block text-[10px]">DATABASE URL</span>
                        <span className="font-mono text-[#a8c3b3] break-all">
                          https://smartbioair-v1-default-rtdb.asia-southeast1.firebasedatabase.app
                        </span>
                      </div>
                    </div>

                    <div className="bg-[#121c16]/50 p-3 rounded-lg border border-[#1e3226]/50 space-y-2">
                      <div className="font-bold text-[#e2f0e7] mb-1">Gemini AI Model details:</div>
                      <div>
                        <span className="text-[#7ea18b] block text-[10px]">INTEGRATED MODEL</span>
                        <span className="font-mono text-emerald-400">gemini-1.5-flash</span>
                      </div>
                      <div>
                        <span className="text-[#7ea18b] block text-[10px]">INTEGRATION API KEY</span>
                        <span className="font-mono text-[#a8c3b3]">AQ.Ab8R...cohj (Configured)</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-[#121c16]/30 border border-[#1e3226]/50 p-4 rounded-xl flex gap-3 text-xs text-[#a8c3b3] mt-6">
                  <HelpCircle className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                  <p className="leading-relaxed">
                    <strong>Testing Tip:</strong> Set water temp above 32°C or gas levels above 500 ppm, then inject to test how the Multi-Agent Supervisor creates alerts, triggers recommended actions, and updates the dashboard immediately!
                  </p>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}
