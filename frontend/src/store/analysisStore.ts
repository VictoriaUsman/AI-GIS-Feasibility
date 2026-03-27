import { create } from "zustand";
import { AnalysisResult } from "@/types/analysis";

interface AnalysisState {
  geometry: GeoJSON.Geometry | null;
  coordinates: { lat: number; lng: number } | null;
  analysisResult: AnalysisResult | null;
  setGeometry: (geometry: GeoJSON.Geometry) => void;
  setCoordinates: (coords: { lat: number; lng: number }) => void;
  setAnalysisResult: (result: AnalysisResult) => void;
  reset: () => void;
}

export const useAnalysisStore = create<AnalysisState>((set) => ({
  geometry: null,
  coordinates: null,
  analysisResult: null,
  setGeometry: (geometry) => set({ geometry }),
  setCoordinates: (coordinates) => set({ coordinates }),
  setAnalysisResult: (analysisResult) => set({ analysisResult }),
  reset: () => set({ geometry: null, coordinates: null, analysisResult: null }),
}));
