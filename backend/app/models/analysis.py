from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class Coordinates(BaseModel):
    lat: float
    lng: float


class AnalysisLayer(BaseModel):
    name: str
    score: int
    summary: str
    raw_value: Optional[str | float] = None


class AnalysisRequest(BaseModel):
    geometry: dict[str, Any]  # GeoJSON geometry
    coordinates: Coordinates


class AnalysisResult(BaseModel):
    overall_score: int
    layers: list[AnalysisLayer]
    risk_flags: list[str]
    ai_narrative: str
    coordinates: Coordinates
    analyzed_at: str


class ReportRequest(BaseModel):
    analysisResult: AnalysisResult
    geometry: Optional[dict[str, Any]] = None
    coordinates: Optional[Coordinates] = None
