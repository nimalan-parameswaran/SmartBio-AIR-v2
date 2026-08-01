import React, { useState } from "react";
import { TrendingUp, LineChart as ChartIcon, Sparkles } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, Legend } from "recharts";
import { PredictionsData, TelemetryData } from "../services/api";

interface PredictionChartsProps {
  predictions: PredictionsData;
  history: TelemetryData[];
}

export default function PredictionCharts({ predictions, history }: PredictionChartsProps) {
  const [activeTab, setActiveTab] = useState<"growth" | "gas" | "temp">("growth");

  // Format historical data
  const chartData = history.map((item, i) => {
    const timeStr = new Date(item.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    return {
      name: timeStr,
      algae_density: item.algae.green_idx,
      temp_c: item.algae.temp_c,
      air_quality: 100 - (item.gas.mq135 / 6.0),
      type: "Historical"
    };
  });

  // Append predictions if present
  if (predictions && predictions["1h"]) {
    // Add current as a bridge point
    const latest = history[history.length - 1];
    
    // Add 1h, 24h, 7d forecast points
    const intervals: ("1h" | "24h" | "7d")[] = ["1h", "24h", "7d"];
    intervals.forEach((interval) => {
      const pred = predictions[interval];
      if (pred) {
        chartData.push({
          name: `+${interval}`,
          algae_density: pred.green_idx,
          temp_c: pred.temp_c,
          air_quality: pred.air_purification_score,
          type: "Forecast"
        });
      }
    });
  }

  const getChartConfig = () => {
    switch (activeTab) {
      case "gas":
        return {
          dataKey: "air_quality",
          color: "#06b6d4",
          label: "Air Purification Score (%)",
          glowClass: "glow-text-cyan",
          yDomain: [0, 100] as [number, number]
        };
      case "temp":
        return {
          dataKey: "temp_c",
          color: "#f59e0b",
          label: "Bioreactor Temp (°C)",
          glowClass: "glow-text-amber",
          yDomain: [10, 40] as [number, number]
        };
      default:
        return {
          dataKey: "algae_density",
          color: "#10b981",
          label: "Algae Green Index",
          glowClass: "glow-text-green",
          yDomain: [0, 3.0] as [number, number]
        };
    }
  };

  const config = getChartConfig();

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full min-h-[360px]">
      {/* Header Tabs */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-[#1e3226] pb-3 mb-4">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-emerald-400" />
          <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">AI Predictive Analytics</h2>
        </div>

        {/* Tab Buttons */}
        <div className="flex gap-1.5 bg-[#121c16] border border-[#1e3226] p-1 rounded-lg">
          <button
            onClick={() => setActiveTab("growth")}
            className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase transition-all ${
              activeTab === "growth" 
                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" 
                : "text-[#7ea18b] hover:text-white"
            }`}
          >
            Algae Growth
          </button>
          <button
            onClick={() => setActiveTab("gas")}
            className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase transition-all ${
              activeTab === "gas" 
                ? "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20" 
                : "text-[#7ea18b] hover:text-white"
            }`}
          >
            Air Quality
          </button>
          <button
            onClick={() => setActiveTab("temp")}
            className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase transition-all ${
              activeTab === "temp" 
                ? "bg-amber-500/10 text-amber-400 border border-amber-500/20" 
                : "text-[#7ea18b] hover:text-white"
            }`}
          >
            Water Temp
          </button>
        </div>
      </div>

      {/* Main chart rendering */}
      <div className="flex-1 min-h-[220px] w-full text-xs">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
            <defs>
              <linearGradient id="chartColor" cx="0" cy="0" r="1">
                <stop offset="5%" stopColor={config.color} stopOpacity={0.2}/>
                <stop offset="95%" stopColor={config.color} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <XAxis 
              dataKey="name" 
              stroke="#7ea18b" 
              fontSize={9}
              tickLine={false}
              axisLine={{ stroke: '#1e3226' }}
            />
            <YAxis 
              stroke="#7ea18b" 
              fontSize={9}
              domain={config.yDomain}
              tickLine={false}
              axisLine={{ stroke: '#1e3226' }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'rgba(12, 18, 14, 0.9)', 
                borderColor: '#1e3226',
                color: '#e2f0e7',
                fontSize: '11px',
                borderRadius: '8px'
              }} 
            />
            <Legend verticalAlign="top" height={24} iconSize={8} iconType="circle" />
            <Area 
              name={config.label}
              type="monotone" 
              dataKey={config.dataKey} 
              stroke={config.color} 
              strokeWidth={2}
              fillOpacity={1} 
              fill="url(#chartColor)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Footer */}
      {predictions && predictions["24h"] && (
        <div className="mt-3 bg-[#121c16]/50 p-2.5 rounded-lg border border-[#1e3226]/50 flex justify-between items-center text-[10px]">
          <span className="text-[#a8c3b3] flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
            24-Hour Forecast Summary:
          </span>
          <span className={`font-bold ${config.glowClass}`} style={{ color: config.color }}>
            {activeTab === "growth" && `GI will stabilize around ${predictions["24h"].green_idx.toFixed(2)}`}
            {activeTab === "gas" && `Expected Air Score of ${predictions["24h"].air_purification_score.toFixed(1)}%`}
            {activeTab === "temp" && `Temp projected to hover at ${predictions["24h"].temp_c}°C`}
          </span>
        </div>
      )}
    </div>
  );
}
