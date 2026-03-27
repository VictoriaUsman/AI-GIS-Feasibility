"use client";

import { useState } from "react";
import toast from "react-hot-toast";
import { FileDown, Loader2 } from "lucide-react";
import { useAnalysisStore } from "@/store/analysisStore";
import { generateReport } from "@/lib/api";

export default function ReportPanel() {
  const [loading, setLoading] = useState(false);
  const { analysisResult, geometry, coordinates } = useAnalysisStore();

  const handleGenerateReport = async () => {
    if (!analysisResult) {
      toast.error("Run an analysis first before generating a report.");
      return;
    }

    setLoading(true);
    try {
      const blob = await generateReport({ analysisResult, geometry, coordinates });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `sitesight-report-${Date.now()}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success("Report downloaded!");
    } catch (err) {
      toast.error("Report generation failed.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 flex flex-col gap-4">
      <div className="text-xs text-gray-500">
        Generate a professional PDF feasibility report based on your analysis results. The report includes AI-generated narrative, risk assessment, and GIS data summary.
      </div>

      {!analysisResult && (
        <div className="bg-gray-50 border border-dashed border-gray-200 rounded-lg p-6 text-center text-xs text-gray-400">
          Run an analysis first to enable report generation.
        </div>
      )}

      {analysisResult && (
        <div className="flex flex-col gap-3">
          {/* Preview summary */}
          <div className="bg-gray-50 rounded-lg p-3 flex flex-col gap-1.5">
            <p className="text-xs font-medium text-gray-700">Report will include:</p>
            <ul className="text-xs text-gray-500 list-disc list-inside space-y-1">
              <li>Executive summary (AI-generated)</li>
              <li>Overall feasibility score: {analysisResult.overall_score}/100</li>
              <li>{analysisResult.layers.length} GIS data layer assessments</li>
              <li>{analysisResult.risk_flags.length} risk flag(s)</li>
              <li>Recommendations</li>
            </ul>
          </div>

          {/* AI narrative preview */}
          {analysisResult.ai_narrative && (
            <div className="bg-white border border-gray-200 rounded-lg p-3">
              <p className="text-xs font-medium text-gray-700 mb-1.5">AI Summary Preview</p>
              <p className="text-xs text-gray-600 leading-relaxed line-clamp-4">
                {analysisResult.ai_narrative}
              </p>
            </div>
          )}

          <button
            onClick={handleGenerateReport}
            disabled={loading}
            className="w-full py-2.5 px-4 bg-brand-600 text-white text-sm font-medium rounded-lg hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {loading ? (
              <>
                <Loader2 size={16} className="animate-spin" />
                Generating PDF...
              </>
            ) : (
              <>
                <FileDown size={16} />
                Download PDF Report
              </>
            )}
          </button>
        </div>
      )}
    </div>
  );
}
