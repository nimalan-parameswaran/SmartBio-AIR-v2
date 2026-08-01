import React from "react";
import { Cpu, CheckCircle2, ShieldAlert, Clock, Sparkles } from "lucide-react";
import { AgentLog } from "../services/api";

interface AgentStatusProps {
  logs: AgentLog[];
}

export default function AgentStatus({ logs }: AgentStatusProps) {
  // If backend hasn't run the agents yet, display static lists of all 10 agents
  const defaultAgents = [
    "Sensor Validation Agent",
    "Environment Analysis Agent",
    "Algae Health Agent",
    "Air Purification Agent",
    "Prediction Agent",
    "Anomaly Detection Agent",
    "Maintenance Agent",
    "Recommendation Agent",
    "Research Agent",
    "Report Agent"
  ];

  const getAgentLogs = () => {
    if (logs && logs.length > 0) return logs;
    
    // Seed default list
    return defaultAgents.map((name) => ({
      agent: name,
      status: "IDLE",
      execution_time_ms: 0,
      confidence_score: 95.0,
      latest_decision: "Waiting for telemetry trigger...",
      reasoning: "Supervisor loop standby."
    }));
  };

  const agentLogs = getAgentLogs();

  return (
    <div className="glass-panel p-5 flex flex-col h-full">
      {/* Title */}
      <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3 justify-between">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">LangGraph AI Agent Panel</h2>
        </div>
        <div className="flex items-center gap-1 text-[10px] bg-[#121c16] border border-[#1e3226] px-2 py-0.5 rounded text-[#7ea18b] font-mono">
          <Clock className="w-3 h-3 text-[#7ea18b]" />
          <span>Active Pipeline</span>
        </div>
      </div>

      {/* Grid of Agents */}
      <div className="flex-1 overflow-y-auto space-y-3 max-h-[460px] pr-1.5">
        {agentLogs.map((log, i) => {
          const isCompleted = log.status === "COMPLETED";
          const isIdle = log.status === "IDLE";
          
          return (
            <div 
              key={i} 
              className="bg-[#121c16]/30 border border-[#1e3226]/50 rounded-lg p-3 text-xs space-y-1.5 transition-colors hover:bg-emerald-500/5 hover:border-emerald-800/30"
            >
              <div className="flex justify-between items-center">
                <span className="font-bold text-[#e2f0e7] tracking-wider">{log.agent}</span>
                <span className={`px-2 py-0.5 rounded-[4px] text-[9px] border font-bold uppercase tracking-wider ${
                  isCompleted 
                    ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400" 
                    : isIdle 
                      ? "bg-[#18231c] border-[#1e3226] text-[#7ea18b]"
                      : "bg-red-500/10 border-red-500/20 text-red-400"
                }`}>
                  {log.status}
                </span>
              </div>

              <div className="flex justify-between text-[10px] text-[#7ea18b]">
                <span className="flex items-center gap-1">
                  <Clock className="w-3 h-3 text-[#7ea18b]" />
                  Runtime: <strong className="text-[#a8c3b3]">{log.execution_time_ms.toFixed(0)} ms</strong>
                </span>
                <span className="flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-[#7ea18b]" />
                  Confidence: <strong className="text-emerald-400 font-bold">{log.confidence_score}%</strong>
                </span>
              </div>

              <div className="bg-[#0e1612] p-2 rounded text-[10px] text-[#a8c3b3]/90 leading-normal border border-[#1e3226]/30">
                <div className="font-semibold text-emerald-500/80 mb-0.5">Decision Summary:</div>
                <p className="italic">{log.latest_decision}</p>
                {log.reasoning && (
                  <p className="mt-1 text-[9px] opacity-75 border-t border-[#1e3226]/30 pt-1">
                    {log.reasoning}
                  </p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
