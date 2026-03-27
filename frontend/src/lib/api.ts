import axios from "axios";
import { AnalysisRequest, AnalysisResult, ReportRequest } from "@/types/analysis";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export async function runAnalysis(payload: AnalysisRequest): Promise<AnalysisResult> {
  const { data } = await api.post<AnalysisResult>("/api/analysis/run", payload);
  return data;
}

export async function generateReport(payload: ReportRequest): Promise<Blob> {
  const response = await api.post("/api/report/generate", payload, {
    responseType: "blob",
  });
  return response.data;
}
