import React from "react";
import { AlertOctagon, AlertTriangle, Info, BellRing } from "lucide-react";

interface AlertItem {
  id: string;
  type: string;
  source: string;
  message: string;
  timestamp: number;
}

interface AlertsProps {
  alerts: AlertItem[];
}

export default function Alerts({ alerts }: AlertsProps) {
  const getAlertStyle = (type: string) => {
    switch (type) {
      case "critical":
        return {
          bg: "bg-red-950/20 border-red-900/30 text-red-400",
          icon: AlertOctagon,
          badge: "bg-red-500/20 border border-red-500/30 text-red-400"
        };
      case "warning":
        return {
          bg: "bg-amber-950/20 border-amber-900/30 text-amber-400",
          icon: AlertTriangle,
          badge: "bg-amber-500/20 border border-amber-500/30 text-amber-400"
        };
      default:
        return {
          bg: "bg-[#121c16]/40 border-[#1e3226] text-emerald-400",
          icon: Info,
          badge: "bg-emerald-500/20 border border-emerald-500/30 text-emerald-400"
        };
    }
  };

  return (
    <div className="glass-panel p-5 flex flex-col h-full min-h-[300px]">
      <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3 justify-between">
        <div className="flex items-center gap-2">
          <BellRing className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">Alert Logs</h2>
        </div>
        <span className="text-[10px] text-[#7ea18b] bg-[#121c16] border border-[#1e3226] px-2 py-0.5 rounded font-mono">
          {alerts.length} Active
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-2.5 max-h-[350px] pr-1.5">
        {alerts.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-[#7ea18b] text-xs py-8">
            <Info className="w-8 h-8 opacity-30 mb-2" />
            <p>No active anomalies or warning flags reported.</p>
          </div>
        ) : (
          alerts.map((alert) => {
            const style = getAlertStyle(alert.type);
            const Icon = style.icon;
            
            return (
              <div 
                key={alert.id}
                className={`p-3 rounded-lg border text-xs flex gap-3 items-start transition-all hover:scale-[1.01] ${style.bg}`}
              >
                <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                <div className="space-y-1 flex-1">
                  <div className="flex justify-between items-center">
                    <span className="font-bold tracking-wider uppercase text-[10px] opacity-90">
                      {alert.source}
                    </span>
                    <span className="text-[9px] opacity-60">
                      {new Date(alert.timestamp * 1000).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="leading-relaxed text-[#e2f0e7]/90">{alert.message}</p>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
