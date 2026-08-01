import React, { useState, useEffect } from "react";
import Head from "next/head";
import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import { FileText, Download, Sparkles, BookOpen, AlertCircle, FileSpreadsheet } from "lucide-react";
import { apiService, SystemStatus } from "../services/api";

export default function Reports() {
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

  const [researchNotes, setResearchNotes] = useState("");
  const [downloading, setDownloading] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [sys, latest] = await Promise.all([
        apiService.getSystem(),
        apiService.getLatest()
      ]);
      setSystem(sys);
      
      // Load research notes from the agent run
      const agentsLogs = await apiService.getAgents();
      const researchAgent = agentsLogs.find((a) => a.agent === "Research Agent");
      if (researchAgent && researchAgent.latest_decision) {
        setResearchNotes(researchAgent.latest_decision);
      } else {
        setResearchNotes(
          "No research entries compiled. Run telemetry changes or manual controls to generate new AI observations."
        );
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const triggerDownload = (blob: Blob, filename: string) => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  const handleExport = async (reportType: string, format: "pdf" | "csv") => {
    setDownloading(reportType + "_" + format);
    try {
      const blob = await apiService.generateReport(reportType, format);
      if (blob) {
        triggerDownload(blob, `${reportType}_report_${intTime()}.` + format);
      }
    } catch (err) {
      console.error(err);
      alert("Error generating report. Ensure backend server is running.");
    } finally {
      setDownloading(null);
    }
  };

  const intTime = () => Math.floor(Date.now() / 1000);

  const reportCards = [
    {
      title: "Daily Operational Report",
      description: "Aggregates day-scale telemetry readings, system validation indexes, active warning counts, and basic maintenance updates.",
      type: "daily"
    },
    {
      title: "Weekly Analytical Log",
      description: "Includes weekly biological growth statistics, carbon removal estimates, environmental stability variance maps, and motor remaining useful life.",
      type: "weekly"
    },
    {
      title: "Monthly Bioreactor Summary",
      description: "Generates long-term logistic growth models, motor maintenance schedules, and cumulative air purification scores.",
      type: "monthly"
    },
    {
      title: "Scientific Research Report",
      description: "A research-grade summary integrating biochemical growth explanations, photoinhibition stress analysis, and comparisons across cycles.",
      type: "research"
    }
  ];

  return (
    <>
      <Head>
        <title>Reports & Research - Smart BIO AIR</title>
      </Head>

      <div className="min-h-screen bg-[#090d0b] flex">
        <Sidebar />

        <div className="flex-1 pl-64 flex flex-col min-h-screen">
          <Header system={system} />

          <main className="flex-1 p-6 space-y-6 overflow-y-auto">
            {/* Header Title */}
            <div>
              <h2 className="text-xl font-bold text-emerald-400 tracking-wider uppercase">Operational Reporting & Export Hub</h2>
              <p className="text-xs text-[#7ea18b] mt-1">
                Compile and export real-time diagnostics, alerts, and AI scientific reasoning notes.
              </p>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
              {/* Export Panel */}
              <div className="xl:col-span-2 space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {reportCards.map((card, i) => (
                    <div key={i} className="glass-panel p-5 flex flex-col justify-between min-h-[180px]">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <FileText className="w-4 h-4 text-emerald-400" />
                          <h3 className="text-sm font-bold text-[#e2f0e7]">{card.title}</h3>
                        </div>
                        <p className="text-xs text-[#a8c3b3] leading-relaxed mb-4">{card.description}</p>
                      </div>

                      {/* Buttons */}
                      <div className="flex gap-2 border-t border-[#1e3226]/50 pt-3">
                        <button
                          onClick={() => handleExport(card.type, "pdf")}
                          disabled={downloading !== null}
                          className="flex-1 py-1.5 bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-black text-[11px] font-bold uppercase rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
                        >
                          <Download className="w-3.5 h-3.5" />
                          <span>
                            {downloading === card.type + "_pdf" ? "Creating PDF..." : "Export PDF"}
                          </span>
                        </button>
                        
                        <button
                          onClick={() => handleExport(card.type, "csv")}
                          disabled={downloading !== null}
                          className="px-3 py-1.5 bg-[#121c16] border border-[#1e3226] hover:bg-emerald-500/5 text-[#a8c3b3] hover:text-emerald-400 text-[11px] font-bold uppercase rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer"
                        >
                          <FileSpreadsheet className="w-3.5 h-3.5" />
                          <span>CSV</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="bg-emerald-950/10 border border-emerald-900/30 rounded-xl p-4 flex gap-3 text-xs text-[#a8c3b3]">
                  <AlertCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                  <p className="leading-relaxed">
                    <strong>Report Generation Notice:</strong> PDF exports automatically include latest calculated health formulas, motor runtime RUL projections, active warning logs, and Google Gemini natural language diagnostic explanations.
                  </p>
                </div>
              </div>

              {/* Research Notes Panel */}
              <div className="glass-panel p-5 flex flex-col h-full min-h-[300px]">
                <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3 justify-between">
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-emerald-400" />
                    <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">Scientific Research Log</h2>
                  </div>
                  <span className="text-[10px] text-cyan-400 bg-cyan-950/40 border border-cyan-800/40 px-2 py-0.5 rounded font-semibold uppercase">
                    Latest Entry
                  </span>
                </div>

                <div className="bg-[#121c16]/30 border border-[#1e3226]/50 rounded-xl p-4 flex-1 text-xs text-[#a8c3b3] leading-relaxed max-h-[360px] overflow-y-auto font-sans">
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-4 h-4 text-emerald-400" />
                    <span className="text-[10px] uppercase font-bold text-emerald-400">Gemini Lab Assistant Notes:</span>
                  </div>
                  <p className="italic text-[#e2f0e7]">{researchNotes}</p>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
}
