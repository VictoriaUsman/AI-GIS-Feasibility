"use client";

import { AnalysisLayer } from "@/types/analysis";

interface ScoreCardProps {
  layer: AnalysisLayer;
}

const SCORE_COLORS = {
  high: "bg-green-500",
  medium: "bg-yellow-400",
  low: "bg-red-500",
};

function getRating(score: number): "high" | "medium" | "low" {
  if (score >= 70) return "high";
  if (score >= 40) return "medium";
  return "low";
}

export default function ScoreCard({ layer }: ScoreCardProps) {
  const rating = getRating(layer.score);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-3">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-xs font-medium text-gray-700">{layer.name}</span>
        <span className="text-xs font-bold text-gray-800">{layer.score}/100</span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-1.5">
        <div
          className={`h-1.5 rounded-full transition-all ${SCORE_COLORS[rating]}`}
          style={{ width: `${layer.score}%` }}
        />
      </div>
      {layer.summary && (
        <p className="text-xs text-gray-500 mt-1.5">{layer.summary}</p>
      )}
    </div>
  );
}
