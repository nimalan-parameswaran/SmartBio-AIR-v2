import React from "react";
import { Leaf, Activity, Sparkles, Thermometer } from "lucide-react";
import { AnalyticsData, TelemetryData } from "../services/api";

interface HealthGaugeProps {
  analytics: AnalyticsData;
  telemetry: TelemetryData;
}

export default function HealthGauge({ analytics, telemetry }: HealthGaugeProps) {
  const health = telemetry.algae.health || 85;
  const pEff = analytics.photosynthesis_efficiency ?? 75;
  const stress = analytics.stress_index ?? 15;
  const biomass = analytics.biomass_g_l ?? 0.15;
  const growthRate = analytics.growth_rate_hr ?? 0.0;
  
  // Circle ring configuration
  const radius = 55;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (health / 100) * circumference;

  const getHealthColor = () => {
    if (health > 75) return "stroke-emerald-400 text-emerald-400";
    if (health > 50) return "stroke-amber-400 text-amber-400";
    return "stroke-red-400 text-red-400";
  };

  const getStressColor = () => {
    if (stress < 30) return "bg-emerald-500";
    if (stress < 60) return "bg-amber-500";
    return "bg-red-500";
  };

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      <div className="flex items-center gap-2 mb-4">
        <Leaf className="w-4 h-4 text-emerald-400" />
        <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">Algae Biological Health</h2>
      </div>

      <div className="flex flex-col sm:flex-row items-center justify-around gap-4 mb-4">
        {/* SVG Health Ring Gauge */}
        <div className="relative flex items-center justify-center">
          <svg className="w-36 h-36 transform -rotate-90">
            {/* Background circle */}
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke="rgba(30, 50, 38, 0.3)"
              strokeWidth="10"
              fill="transparent"
            />
            {/* Health circle */}
            <circle
              cx="72"
              cy="72"
              r={radius}
              stroke="currentColor"
              strokeWidth="10"
              fill="transparent"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className={`transition-all duration-1000 ease-out ${getHealthColor()}`}
            />
          </svg>
          <div className="absolute flex flex-col items-center justify-center">
            <span className="text-3xl font-extrabold tracking-tight glow-text-green text-emerald-400">{health}%</span>
            <span className="text-[9px] uppercase tracking-widest text-[#7ea18b] font-semibold">Health Score</span>
          </div>
        </div>

        {/* Derived Biological Stats */}
        <div className="flex-1 w-full space-y-3.5">
          {/* Biomass */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-[#a8c3b3] flex items-center gap-1"><Sparkles className="w-3 h-3 text-emerald-400" /> Biomass Concentration</span>
              <span className="text-emerald-400 font-bold">{biomass.toFixed(3)} g/L</span>
            </div>
            <div className="text-[10px] text-[#7ea18b]">Estimated Biomass dry weight.</div>
          </div>
          
          {/* Photosynthesis Efficiency */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-[#a8c3b3] flex items-center gap-1"><Activity className="w-3 h-3 text-cyan-400" /> Photosynthesis Eff.</span>
              <span className="text-cyan-400 font-bold">{pEff}%</span>
            </div>
            <div className="w-full bg-[#121c16] h-1.5 rounded-full overflow-hidden border border-[#1e3226]">
              <div 
                className="bg-cyan-500 h-full rounded-full transition-all duration-1000"
                style={{ width: `${pEff}%` }}
              ></div>
            </div>
          </div>

          {/* Biological Stress */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-[#a8c3b3] flex items-center gap-1"><Thermometer className="w-3 h-3 text-amber-500" /> Stress Index</span>
              <span className="text-amber-500 font-bold">{stress}%</span>
            </div>
            <div className="w-full bg-[#121c16] h-1.5 rounded-full overflow-hidden border border-[#1e3226]">
              <div 
                className={`h-full rounded-full transition-all duration-1000 ${getStressColor()}`}
                style={{ width: `${stress}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Info */}
      <div className="bg-[#121c16]/50 p-2.5 rounded-lg border border-[#1e3226]/50 flex justify-between text-[11px] text-[#a8c3b3]">
        <span>Growth Velocity:</span>
        <span className="font-mono text-emerald-400 font-semibold">
          {growthRate > 0 ? `+${growthRate.toFixed(4)}` : growthRate.toFixed(4)} GI/hr
        </span>
      </div>
    </div>
  );
}
