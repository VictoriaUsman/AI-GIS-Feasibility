"""
PDF report generation using WeasyPrint + Jinja2 templates.
"""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.analysis import AnalysisResult

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def generate_pdf(result: AnalysisResult) -> bytes:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report.html")

    html_content = template.render(
        result=result,
        generated_at=datetime.now().strftime("%B %d, %Y %H:%M"),
        score_color=_score_color(result.overall_score),
        layers=[
            {**layer.model_dump(), "color": _score_color(layer.score)}
            for layer in result.layers
        ],
    )

    return HTML(string=html_content).write_pdf()


def _score_color(score: int) -> str:
    if score >= 70:
        return "#16a34a"  # green
    if score >= 40:
        return "#d97706"  # amber
    return "#dc2626"  # red
