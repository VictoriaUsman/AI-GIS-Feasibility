"use client";

import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";

interface Layer {
  id: string;
  name: string;
  source: string;
  color: string;
  enabled: boolean;
}

const DEFAULT_LAYERS: Layer[] = [
  { id: "flood", name: "Flood Susceptibility", source: "MGB Philippines", color: "#3b82f6", enabled: true },
  { id: "landslide", name: "Landslide Susceptibility", source: "MGB Philippines", color: "#f59e0b", enabled: true },
  { id: "faults", name: "Active Fault Lines", source: "PHIVOLCS", color: "#ef4444", enabled: true },
  { id: "landuse", name: "Land Use / Zoning", source: "NAMRIA", color: "#10b981", enabled: false },
  { id: "roads", name: "Road Network", source: "OpenStreetMap", color: "#6b7280", enabled: true },
  { id: "barangays", name: "Barangay Boundaries", source: "PSA 2020", color: "#8b5cf6", enabled: false },
  { id: "poi", name: "Points of Interest", source: "OpenStreetMap", color: "#f97316", enabled: false },
];

export default function LayersPanel() {
  const [layers, setLayers] = useState<Layer[]>(DEFAULT_LAYERS);

  const toggleLayer = (id: string) => {
    setLayers((prev) =>
      prev.map((l) => (l.id === id ? { ...l, enabled: !l.enabled } : l))
    );
  };

  return (
    <div className="p-4 flex flex-col gap-3">
      <p className="text-xs text-gray-500">
        Toggle GIS data layers displayed on the map. All layers are used in the analysis regardless of visibility.
      </p>

      <div className="flex flex-col gap-1.5">
        {layers.map((layer) => (
          <div
            key={layer.id}
            className="flex items-center justify-between p-2.5 bg-white border border-gray-200 rounded-lg"
          >
            <div className="flex items-center gap-2.5">
              <div
                className="w-3 h-3 rounded-full shrink-0"
                style={{ backgroundColor: layer.color }}
              />
              <div>
                <p className="text-xs font-medium text-gray-800">{layer.name}</p>
                <p className="text-xs text-gray-400">{layer.source}</p>
              </div>
            </div>
            <button
              onClick={() => toggleLayer(layer.id)}
              className={`p-1 rounded transition-colors ${
                layer.enabled
                  ? "text-brand-600 hover:text-brand-700"
                  : "text-gray-300 hover:text-gray-400"
              }`}
            >
              {layer.enabled ? <Eye size={15} /> : <EyeOff size={15} />}
            </button>
          </div>
        ))}
      </div>

      <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 text-xs text-amber-700">
        GIS data layers will be loaded as shapefiles are added to the backend. Placeholder layers shown above.
      </div>
    </div>
  );
}
