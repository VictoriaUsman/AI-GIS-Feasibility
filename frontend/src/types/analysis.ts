export interface AnalysisLayer {
  name: string;
  score: number;
  summary: string;
  raw_value?: string | number;
}

export interface AnalysisResult {
  overall_score: number;
  layers: AnalysisLayer[];
  risk_flags: string[];
  ai_narrative: string;
  coordinates: { lat: number; lng: number };
  analyzed_at: string;
}

export interface AnalysisRequest {
  geometry: GeoJSON.Geometry;
  coordinates: { lat: number; lng: number };
}

export interface ReportRequest {
  analysisResult: AnalysisResult;
  geometry: GeoJSON.Geometry | null;
  coordinates: { lat: number; lng: number } | null;
}
