from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analysis, report

app = FastAPI(
    title="SiteSight PH API",
    description="AI + GIS Feasibility Analysis for the Philippines",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(report.router, prefix="/api/report", tags=["report"])


@app.get("/health")
def health():
    return {"status": "ok"}
