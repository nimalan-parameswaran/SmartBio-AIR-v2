import React, { useState, useEffect } from "react";
import { ShieldCheck, ShieldAlert, ShieldWarning, Wifi, Database } from "lucide-react";
import { SystemStatus } from "../services/api";

interface HeaderProps {
  system: SystemStatus;
}

export default function Header({ system }: HeaderProps) {
  const [timeStr, setTimeStr] = useState("");

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeStr(new Date().toLocaleTimeString());
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getStatusDetails = () => {
    switch (system.status) {
      case "CRITICAL":
        return {
          color: "text-red-400 bg-red-950/40 border-red-800/40",
          icon: ShieldAlert,
          label: "CRITICAL ALERT"
        };
      case "WARNING":
        return {
          color: "text-amber-400 bg-amber-950/40 border-amber-800/40",
          icon: ShieldWarning,
          label: "WARNING DEVIATION"
        };
      default:
        return {
          color: "text-emerald-400 bg-emerald-950/40 border-emerald-800/40",
          icon: ShieldCheck,
          label: "SYSTEM STABLE"
        };
    }
  };

  const status = getStatusDetails();
  const StatusIcon = status.icon;

  return (
    <header className="border-b border-[#1e3226] bg-[#0c120e]/80 backdrop-blur-md h-16 flex items-center justify-between px-6 sticky top-0 z-20">
      {/* System Status Indicators */}
      <div className="flex items-center gap-4">
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full border text-xs font-semibold ${status.color}`}>
          <StatusIcon className="w-3.5 h-3.5" />
          <span>{status.label}</span>
        </div>
        
        <div className="flex items-center gap-2 text-xs text-[#a8c3b3]">
          <Database className="w-3.5 h-3.5 text-cyan-400" />
          <span>DB Mode: <span className="text-cyan-400 font-semibold uppercase">{system.database_mode}</span></span>
        </div>
      </div>

      {/* Center stats overview */}
      <div className="hidden md:flex items-center gap-6 text-xs border-x border-[#1e3226] px-6">
        <div>
          <span className="text-[#7ea18b] block text-[9px] uppercase tracking-wider">Air Purification Score</span>
          <span className="text-emerald-400 font-bold text-sm glow-text-green">{system.air_purification_score}%</span>
        </div>
        <div>
          <span className="text-[#7ea18b] block text-[9px] uppercase tracking-wider">Algae Bio-Health</span>
          <span className="text-emerald-400 font-bold text-sm glow-text-green">{system.algae_health}%</span>
        </div>
        <div>
          <span className="text-[#7ea18b] block text-[9px] uppercase tracking-wider">Pump Load</span>
          <span className="text-cyan-400 font-bold text-sm glow-text-cyan">{system.pump_speed}%</span>
        </div>
      </div>

      {/* Clock & Telemetry Connection */}
      <div className="flex items-center gap-4 text-xs font-medium text-[#a8c3b3]">
        <div className="flex items-center gap-1.5 bg-[#121c16] px-2.5 py-1 rounded border border-[#1e3226] text-[11px]">
          <Wifi className="w-3 h-3 text-emerald-400 animate-pulse" />
          <span>ESP32 Connected</span>
        </div>
        <span className="font-mono text-emerald-500/80">{timeStr}</span>
      </div>
    </header>
  );
}
