"""
AI narrative generation using OpenAI GPT-4o mini.
Produces a professional feasibility summary from GIS analysis results.
"""

from openai import AsyncOpenAI
from app.config import settings
from app.models.analysis import AnalysisLayer

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def generate_narrative(
    layers: list[AnalysisLayer],
    overall_score: int,
    risk_flags: list[str],
    lat: float,
    lng: float,
) -> str:
    layer_summary = "\n".join(
        f"- {l.name}: {l.score}/100 — {l.summary}" for l in layers
    )
    flags_text = "\n".join(f"- {f}" for f in risk_flags) if risk_flags else "None"

    prompt = f"""You are a professional real estate and land use feasibility analyst in the Philippines.

Based on the GIS analysis results below, write a concise executive summary (3-4 paragraphs)
for a site feasibility report. Be specific, professional, and actionable.
Reference Philippine regulations where relevant (PHIVOLCS fault setbacks, MGB geohazard
clearances, HLURB/DHSUD zoning requirements).

Location: {lat:.6f}°N, {lng:.6f}°E
Overall Feasibility Score: {overall_score}/100

GIS Layer Results:
{layer_summary}

Risk Flags:
{flags_text}

Write the executive summary now:"""

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=600,
    )
    return response.choices[0].message.content or ""
