import React, { useState } from "react";
import { Settings, Play, Square, ShieldAlert, Cpu } from "lucide-react";
import { apiService, TelemetryData } from "../services/api";

interface MotorControlProps {
  telemetry: TelemetryData;
  maintenance: any;
  onControlChange: () => void;
}

export default function MotorControl({ telemetry, maintenance, onControlChange }: MotorControlProps) {
  const { motor } = telemetry;
  const rul = maintenance?.remaining_useful_life_hours ?? 4880;
  
  const [loading, setLoading] = useState(false);
  const [speedVal, setSpeedVal] = useState(motor.speed);

  const handleStatusChange = async (newStatus: string) => {
    setLoading(true);
    try {
      await apiService.sendManualControl({
        status: newStatus,
        speed: speedVal,
        emergency_stop: false
      });
      onControlChange();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSpeedSlider = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    setSpeedVal(val);
  };

  const submitSpeed = async () => {
    setLoading(true);
    try {
      await apiService.sendManualControl({
        status: motor.status,
        speed: speedVal,
        emergency_stop: false
      });
      onControlChange();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEmergencyStop = async () => {
    setLoading(true);
    try {
      await apiService.sendManualControl({
        status: "OFF",
        speed: 0,
        emergency_stop: true
      });
      setSpeedVal(0);
      onControlChange();
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel p-5 flex flex-col justify-between h-full">
      {/* Title */}
      <div className="flex items-center gap-2 mb-4 justify-between">
        <div className="flex items-center gap-2">
          <Settings className="w-4 h-4 text-cyan-400 animate-spin" style={{ animationDuration: '6s' }} />
          <h2 className="text-sm font-bold tracking-wider text-cyan-400 uppercase">Bioreactor Motor Control</h2>
        </div>
        <div className="flex items-center gap-1.5 text-[10px] bg-[#121c16] px-2 py-0.5 rounded border border-[#1e3226] text-cyan-400 font-semibold uppercase">
          <Cpu className="w-3 h-3" />
          <span>Control: {motor.status}</span>
        </div>
      </div>

      {/* Grid of operational readouts */}
      <div className="grid grid-cols-3 gap-3 mb-5">
        <div className="bg-[#121c16]/50 p-2.5 rounded border border-[#1e3226]/50 text-center">
          <span className="text-[9px] text-[#7ea18b] uppercase tracking-wider block">Flow Rate</span>
          <span className="text-sm font-bold text-cyan-400">{motor.flow_rate.toFixed(2)} L/m</span>
        </div>
        <div className="bg-[#121c16]/50 p-2.5 rounded border border-[#1e3226]/50 text-center">
          <span className="text-[9px] text-[#7ea18b] uppercase tracking-wider block">Run Hours</span>
          <span className="text-sm font-bold text-[#e2f0e7]">{motor.operating_hours.toFixed(1)}h</span>
        </div>
        <div className="bg-[#121c16]/50 p-2.5 rounded border border-[#1e3226]/50 text-center">
          <span className="text-[9px] text-[#7ea18b] uppercase tracking-wider block">Motor Life</span>
          <span className="text-sm font-bold text-emerald-400">{rul.toFixed(0)}h RUL</span>
        </div>
      </div>

      {/* Speed Slider */}
      <div className="mb-5">
        <div className="flex justify-between text-xs mb-1.5">
          <span className="text-[#a8c3b3]">Pump Motor Speed</span>
          <span className="text-cyan-400 font-bold">{speedVal}%</span>
        </div>
        <div className="flex gap-2">
          <input
            type="range"
            min="0"
            max="100"
            value={speedVal}
            onChange={handleSpeedSlider}
            disabled={loading}
            className="flex-1 accent-cyan-500 h-1.5 bg-[#121c16] rounded-lg cursor-pointer border border-[#1e3226] self-center"
          />
          <button
            onClick={submitSpeed}
            disabled={loading}
            className="px-2.5 py-1 text-[10px] bg-cyan-950/60 border border-cyan-800/60 hover:bg-cyan-900/60 text-cyan-400 rounded-md font-semibold transition-colors"
          >
            Apply
          </button>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="flex gap-2 mb-3">
        <button
          onClick={() => handleStatusChange("ON")}
          disabled={loading || motor.status === "ON"}
          className="flex-1 py-2 text-xs font-semibold rounded-lg flex items-center justify-center gap-1.5 border transition-all bg-emerald-950/20 border-emerald-900/40 text-emerald-400 hover:bg-emerald-900/20 disabled:opacity-50"
        >
          <Play className="w-3.5 h-3.5 fill-emerald-400" />
          <span>Manual ON</span>
        </button>
        <button
          onClick={() => handleStatusChange("AUTO")}
          disabled={loading || motor.status === "AUTO"}
          className="flex-1 py-2 text-xs font-semibold rounded-lg flex items-center justify-center gap-1.5 border transition-all bg-cyan-950/20 border-cyan-900/40 text-cyan-400 hover:bg-cyan-900/20 disabled:opacity-50"
        >
          <Cpu className="w-3.5 h-3.5" />
          <span>Auto AI</span>
        </button>
        <button
          onClick={() => handleStatusChange("OFF")}
          disabled={loading || motor.status === "OFF"}
          className="flex-1 py-2 text-xs font-semibold rounded-lg flex items-center justify-center gap-1.5 border transition-all bg-[#121c16] border-[#1e3226] text-[#a8c3b3] hover:bg-emerald-500/5 disabled:opacity-50"
        >
          <Square className="w-3.5 h-3.5 fill-[#7ea18b]" />
          <span>OFF</span>
        </button>
      </div>

      {/* Emergency Stop */}
      <button
        onClick={handleEmergencyStop}
        disabled={loading}
        className="w-full py-2 bg-red-950/40 border border-red-800/40 hover:bg-red-900/40 text-red-400 rounded-lg flex items-center justify-center gap-2 text-xs font-bold transition-all shadow-md active:scale-[0.98]"
      >
        <ShieldAlert className="w-4 h-4 animate-pulse" />
        <span>EMERGENCY STOP (SHUTDOWN)</span>
      </button>
    </div>
  );
}
