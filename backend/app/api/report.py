from fastapi import APIRouter
from fastapi.responses import Response
from app.models.analysis import ReportRequest
from app.services.pdf_service import generate_pdf

router = APIRouter()


@router.post("/generate")
async def generate_report(payload: ReportRequest) -> Response:
    pdf_bytes = generate_pdf(payload.analysisResult)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sitesight-report.pdf"},
    )
