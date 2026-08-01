import React from "react";
import { Sparkles, ArrowRight, Lightbulb } from "lucide-react";

interface RecommendationPanelProps {
  recommendations: string[];
}

export default function RecommendationPanel({ recommendations }: RecommendationPanelProps) {
  const getFallbackRecs = () => [
    "Verify water volume; add fresh growth medium if nutrient levels are depleted.",
    "Adjust lighting schedule; decrease light intensity if stress index is high.",
    "Clean the reactor walls to clear biofilm blocks and optimize sensor readings.",
    "Maintain pump motor speed; high duty cycles over extended periods cause speed decay."
  ];

  const list = recommendations && recommendations.length > 0 ? recommendations : getFallbackRecs();

  return (
    <div className="glass-panel p-5 flex flex-col h-full min-h-[300px]">
      {/* Title */}
      <div className="flex items-center gap-2 mb-4 border-b border-[#1e3226] pb-3 justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-400 animate-pulse" />
          <h2 className="text-sm font-bold tracking-wider text-emerald-400 uppercase">AI Diagnosis & Recommendations</h2>
        </div>
        <span className="text-[9px] text-cyan-400 bg-cyan-950/40 border border-cyan-800/40 px-2 py-0.5 rounded uppercase font-semibold">
          Gemini Generated
        </span>
      </div>

      {/* List items */}
      <div className="flex-1 space-y-3 overflow-y-auto max-h-[320px] pr-1">
        {list.map((rec, idx) => (
          <div 
            key={idx} 
            className="flex items-start gap-3 bg-[#121c16]/30 border border-[#1e3226]/50 rounded-lg p-3 text-xs transition-all hover:bg-emerald-500/5 hover:translate-x-1"
          >
            <div className="w-5 h-5 rounded bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-[10px] mt-0.5 flex-shrink-0">
              {idx + 1}
            </div>
            
            <div className="space-y-1.5 flex-1">
              <p className="leading-relaxed text-[#e2f0e7]/90">{rec}</p>
              <div className="flex items-center gap-1 text-[9px] text-[#7ea18b] font-medium">
                <Lightbulb className="w-3 h-3 text-amber-500" />
                <span>Suggested Action Plan</span>
                <ArrowRight className="w-2.5 h-2.5" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
