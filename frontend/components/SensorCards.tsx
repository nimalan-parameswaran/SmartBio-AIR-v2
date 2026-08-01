import React from "react";
import { Thermometer, Sun, Gauge, Eye, Wind, Mountain } from "lucide-react";
import { TelemetryData } from "../services/api";

interface SensorCardsProps {
  telemetry: TelemetryData;
}

export default function SensorCards({ telemetry }: SensorCardsProps) {
  const { algae, env, gas } = telemetry;

  const cards = [
    {
      title: "Bioreactor Temperature",
      value: `${algae.temp_c}°C`,
      subtitle: "Optimal: 22°C - 26°C",
      icon: Thermometer,
      color: "text-emerald-400",
      glow: "glow-text-green",
      status: algae.temp_c > 30 || algae.temp_c < 16 ? "STRESSED" : "OPTIMAL"
    },
    {
      title: "Photosynthetic light",
      value: `${algae.light_lux.toLocaleString()} Lux`,
      subtitle: "Optimal: 1500 - 3000 Lux",
      icon: Sun,
      color: "text-amber-400",
      glow: "glow-text-amber",
      status: algae.light_lux < 300 ? "LOW" : algae.light_lux > 6000 ? "HIGH" : "OPTIMAL"
    },
    {
      title: "Algae Green Index",
      value: algae.green_idx.toFixed(2),
      subtitle: "Density Representation",
      icon: Eye,
      color: "text-emerald-400",
      glow: "glow-text-green",
      status: algae.green_idx > 1.8 ? "MATURE" : algae.green_idx < 0.3 ? "SPARSE" : "GROWING"
    },
    {
      title: "Atmospheric Pressure",
      value: `${env.pressure.toFixed(1)} hPa`,
      subtitle: `Altitude: ${env.altitude}m`,
      icon: Mountain,
      color: "text-cyan-400",
      glow: "glow-text-cyan",
      status: "STABLE"
    },
    {
      title: "Indoor CO₂ Estimation",
      value: `${gas.mq135.toFixed(1)} ppm`,
      subtitle: "Baseline clean: ~150ppm",
      icon: Wind,
      color: "text-cyan-400",
      glow: "glow-text-cyan",
      status: gas.mq135 > 500 ? "POOR" : "CLEAN"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
      {cards.map((card, i) => {
        const Icon = card.icon;
        return (
          <div key={i} className="glass-panel p-4 flex flex-col justify-between min-h-[120px] transition-transform hover:translate-y-[-2px]">
            <div className="flex justify-between items-start">
              <span className="text-xs text-[#7ea18b] font-medium tracking-wide">{card.title}</span>
              <Icon className={`w-4 h-4 ${card.color}`} />
            </div>
            
            <div className="my-2">
              <span className={`text-2xl font-bold ${card.color} ${card.glow}`}>
                {card.value}
              </span>
            </div>
            
            <div className="flex justify-between items-center text-[10px] text-[#7ea18b] border-t border-[#1e3226]/50 pt-2">
              <span>{card.subtitle}</span>
              <span className={`font-bold uppercase ${
                card.status === "OPTIMAL" || card.status === "STABLE" || card.status === "CLEAN" || card.status === "GROWING"
                  ? "text-emerald-400"
                  : "text-amber-400"
              }`}>{card.status}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
