from datetime import datetime
from fastapi import APIRouter
from app.models.analysis import AnalysisRequest, AnalysisResult
from app.services.gis_service import analyze_location, compute_overall_score, extract_risk_flags
from app.services.ai_service import generate_narrative

router = APIRouter()


@router.post("/run", response_model=AnalysisResult)
async def run_analysis(payload: AnalysisRequest) -> AnalysisResult:
    lat = payload.coordinates.lat
    lng = payload.coordinates.lng

    layers = await analyze_location(payload.geometry, lat, lng)
    overall_score = compute_overall_score(layers)
    risk_flags = extract_risk_flags(layers)
    ai_narrative = await generate_narrative(layers, overall_score, risk_flags, lat, lng)

    return AnalysisResult(
        overall_score=overall_score,
        layers=layers,
        risk_flags=risk_flags,
        ai_narrative=ai_narrative,
        coordinates=payload.coordinates,
        analyzed_at=datetime.utcnow().isoformat(),
    )
