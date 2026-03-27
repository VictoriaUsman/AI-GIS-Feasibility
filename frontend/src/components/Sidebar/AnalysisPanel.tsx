"use client";

import { useState } from "react";
import toast from "react-hot-toast";
import { Loader2, AlertTriangle, CheckCircle2 } from "lucide-react";
import { useAnalysisStore } from "@/store/analysisStore";
import { runAnalysis } from "@/lib/api";
import ScoreCard from "./ScoreCard";

interface AnalysisPanelProps {
  mapLoaded: boolean;
}

export default function AnalysisPanel({ mapLoaded }: AnalysisPanelProps) {
  const [loading, setLoading] = useState(false);
  const { geometry, coordinates, analysisResult, setAnalysisResult } = useAnalysisStore();

  const handleRunAnalysis = async () => {
    if (!geometry || !coordinates) {
      toast.error("Please select a location on the map first.");
      return;
    }

    setLoading(true);
    try {
      const result = await runAnalysis({ geometry, coordinates });
      setAnalysisResult(result);
      toast.success("Analysis complete!");
    } catch (err) {
      toast.error("Analysis failed. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 flex flex-col gap-4">
      {/* Location info */}
      {coordinates && (
        <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-600">
          <p className="font-medium text-gray-800 mb-1">Selected Location</p>
          <p>Lat: {coordinates.lat.toFixed(6)}</p>
          <p>Lng: {coordinates.lng.toFixed(6)}</p>
        </div>
      )}

      {/* Run button */}
      <button
        onClick={handleRunAnalysis}
        disabled={!geometry || loading}
        className="w-full py-2.5 px-4 bg-brand-600 text-white text-sm font-medium rounded-lg hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
      >
        {loading ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            Running Analysis...
          </>
        ) : (
          "Run Feasibility Analysis"
        )}
      </button>

      {/* Results */}
      {analysisResult && (
        <div className="flex flex-col gap-3">
          {/* Overall score */}
          <div className="bg-brand-50 border border-brand-100 rounded-lg p-4 text-center">
            <p className="text-xs text-brand-700 font-medium mb-1">Overall Feasibility Score</p>
            <p className="text-4xl font-bold text-brand-600">{analysisResult.overall_score}</p>
            <p className="text-xs text-brand-500 mt-1">/100</p>
          </div>

          {/* Layer scores */}
          <div className="flex flex-col gap-2">
            {analysisResult.layers.map((layer) => (
              <ScoreCard key={layer.name} layer={layer} />
            ))}
          </div>

          {/* Risk flags */}
          {analysisResult.risk_flags.length > 0 && (
            <div className="flex flex-col gap-1.5">
              <p className="text-xs font-medium text-gray-700">Risk Flags</p>
              {analysisResult.risk_flags.map((flag, i) => (
                <div key={i} className="flex items-start gap-2 text-xs text-amber-700 bg-amber-50 rounded-md p-2">
                  <AlertTriangle size={12} className="mt-0.5 shrink-0" />
                  {flag}
                </div>
              ))}
            </div>
          )}

          {analysisResult.risk_flags.length === 0 && (
            <div className="flex items-center gap-2 text-xs text-green-700 bg-green-50 rounded-md p-2">
              <CheckCircle2 size={12} className="shrink-0" />
              No critical risk flags detected
            </div>
          )}
        </div>
      )}
    </div>
  );
}
