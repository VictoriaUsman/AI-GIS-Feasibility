"use client";

import { useState } from "react";
import { MapPin, FileText, Layers, ChevronRight } from "lucide-react";
import { useAnalysisStore } from "@/store/analysisStore";
import AnalysisPanel from "./AnalysisPanel";
import ReportPanel from "./ReportPanel";
import LayersPanel from "./LayersPanel";

type Tab = "analysis" | "report" | "layers";

interface SidebarProps {
  mapLoaded: boolean;
}

export default function Sidebar({ mapLoaded }: SidebarProps) {
  const [activeTab, setActiveTab] = useState<Tab>("analysis");
  const { geometry } = useAnalysisStore();

  const tabs: { id: Tab; label: string; icon: React.ReactNode }[] = [
    { id: "analysis", label: "Analysis", icon: <MapPin size={16} /> },
    { id: "report", label: "Report", icon: <FileText size={16} /> },
    { id: "layers", label: "Layers", icon: <Layers size={16} /> },
  ];

  return (
    <div className="w-96 h-full bg-white border-l border-gray-200 flex flex-col shadow-xl z-10">
      {/* Header */}
      <div className="px-4 py-3 bg-brand-900 text-white">
        <h1 className="text-base font-semibold tracking-tight">SiteSight PH</h1>
        <p className="text-xs text-brand-100 mt-0.5">AI + GIS Feasibility Analysis</p>
      </div>

      {/* Status bar */}
      {!geometry && (
        <div className="px-4 py-2 bg-amber-50 border-b border-amber-100 flex items-center gap-2 text-xs text-amber-700">
          <ChevronRight size={12} />
          Drop a pin or draw a polygon on the map to begin
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-medium transition-colors ${
              activeTab === tab.id
                ? "text-brand-600 border-b-2 border-brand-600 bg-brand-50"
                : "text-gray-500 hover:text-gray-700 hover:bg-gray-50"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Panel content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === "analysis" && <AnalysisPanel mapLoaded={mapLoaded} />}
        {activeTab === "report" && <ReportPanel />}
        {activeTab === "layers" && <LayersPanel />}
      </div>
    </div>
  );
}
