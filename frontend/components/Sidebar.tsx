import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { LayoutDashboard, FileText, Settings, Radio } from "lucide-react";

export default function Sidebar() {
  const router = useRouter();
  const currentPath = router.pathname;
  
  const menuItems = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "Reports & Research", path: "/reports", icon: FileText },
    { name: "Simulation & Config", path: "/settings", icon: Settings },
  ];

  return (
    <div className="w-64 border-r border-[#1e3226] bg-[#0c120e]/80 backdrop-blur-md flex flex-col justify-between h-screen fixed left-0 top-0 z-30 p-4">
      <div>
        {/* Brand Header */}
        <div className="flex items-center gap-2 px-2 py-4 mb-6">
          <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center pulse-glow-green">
            <Radio className="w-5 h-5 text-black" />
          </div>
          <div>
            <h1 className="font-bold text-md text-emerald-400 tracking-wider">SMART BIO AIR</h1>
            <p className="text-[10px] text-emerald-500/70 tracking-widest uppercase">Version 2.0.0</p>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPath === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                    : "text-[#a8c3b3] hover:bg-emerald-500/5 hover:text-white"
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? "text-emerald-400" : "text-[#7ea18b]"}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer / Status Summary */}
      <div className="p-2 border-t border-[#1e3226] pt-4">
        <div className="bg-[#121c16] rounded-lg p-3 border border-[#1e3226] text-xs">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[#7ea18b]">Agent Pipeline</span>
            <span className="flex items-center gap-1 text-emerald-400 font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
              ONLINE
            </span>
          </div>
          <p className="text-[10px] text-[#7ea18b] leading-relaxed">
            LangGraph supervisor is actively listening for Firebase telemetry changes.
          </p>
        </div>
      </div>
    </div>
  );
}
