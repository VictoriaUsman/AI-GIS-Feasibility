"""
GIS analysis service.

Queries PostGIS layers for a given point/polygon geometry and returns
scored results per layer. Each layer scorer returns:
  - score: 0-100 (higher = more favorable)
  - summary: human-readable description
  - raw_value: raw data value for the report

Data sources (to be loaded into PostGIS):
  - flood_susceptibility     (MGB Philippines)
  - landslide_susceptibility (MGB Philippines)
  - fault_lines              (PHIVOLCS)
  - land_use                 (NAMRIA)
  - roads                    (OpenStreetMap via osm2pgsql)
  - barangays + demographics (PSA 2020)
  - poi                      (OpenStreetMap)
"""

import logging
from typing import Any
from sqlalchemy import text
from app.db import get_db_session
from app.models.analysis import AnalysisLayer

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

async def analyze_location(geometry: dict[str, Any], lat: float, lng: float) -> list[AnalysisLayer]:
    """Run all GIS layer analyses and return scored results."""
    geom_wkt = _geometry_to_wkt(geometry, lat, lng)

    layers = []
    async with get_db_session() as session:
        layers.append(await _score_flood(session, geom_wkt))
        layers.append(await _score_landslide(session, geom_wkt))
        layers.append(await _score_fault_proximity(session, geom_wkt, lng, lat))
        layers.append(await _score_road_access(session, geom_wkt, lng, lat))
        layers.append(await _score_demographics(session, geom_wkt))
        layers.append(await _score_poi_density(session, geom_wkt, lng, lat))

    return layers


# ---------------------------------------------------------------------------
# Individual layer scorers
# ---------------------------------------------------------------------------

async def _score_flood(session, geom_wkt: str) -> AnalysisLayer:
    """Score flood susceptibility. Lower susceptibility = higher score."""
    try:
        result = await session.execute(
            text("""
                SELECT susceptibility
                FROM flood_susceptibility
                WHERE ST_Intersects(geom, ST_GeomFromText(:wkt, 4326))
                ORDER BY ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, 4326))) DESC
                LIMIT 1
            """),
            {"wkt": geom_wkt},
        )
        row = result.fetchone()
        if not row:
            return AnalysisLayer(name="Flood Susceptibility", score=70, summary="No flood data available for this location.", raw_value="No data")

        level = str(row[0]).lower()
        score_map = {"none": 95, "low": 80, "moderate": 50, "high": 20, "very high": 5}
        score = score_map.get(level, 60)
        return AnalysisLayer(
            name="Flood Susceptibility",
            score=score,
            summary=f"Flood susceptibility rated as {level}.",
            raw_value=level,
        )
    except Exception as e:
        logger.error("Flood query failed: %s", e)
        return AnalysisLayer(name="Flood Susceptibility", score=70, summary="Flood layer not yet loaded.", raw_value="Pending data")


async def _score_landslide(session, geom_wkt: str) -> AnalysisLayer:
    """Score landslide susceptibility."""
    try:
        result = await session.execute(
            text("""
                SELECT susceptibility
                FROM landslide_susceptibility
                WHERE ST_Intersects(geom, ST_GeomFromText(:wkt, 4326))
                ORDER BY ST_Area(ST_Intersection(geom, ST_GeomFromText(:wkt, 4326))) DESC
                LIMIT 1
            """),
            {"wkt": geom_wkt},
        )
        row = result.fetchone()
        if not row:
            return AnalysisLayer(name="Landslide Susceptibility", score=70, summary="No landslide data available.", raw_value="No data")

        level = str(row[0]).lower()
        score_map = {"none": 95, "low": 80, "moderate": 50, "high": 20, "very high": 5}
        score = score_map.get(level, 60)
        return AnalysisLayer(
            name="Landslide Susceptibility",
            score=score,
            summary=f"Landslide susceptibility rated as {level}.",
            raw_value=level,
        )
    except Exception as e:
        logger.error("Landslide query failed: %s", e)
        return AnalysisLayer(name="Landslide Susceptibility", score=70, summary="Landslide layer not yet loaded.", raw_value="Pending data")


async def _score_fault_proximity(session, geom_wkt: str, lng: float, lat: float) -> AnalysisLayer:
    """Score distance to nearest active fault line. Further = higher score."""
    try:
        result = await session.execute(
            text("""
                SELECT
                    ST_Distance(
                        geom::geography,
                        ST_Point(:lng, :lat)::geography
                    ) / 1000 AS distance_km
                FROM fault_lines
                ORDER BY geom <-> ST_Point(:lng, :lat)::geometry
                LIMIT 1
            """),
            {"lng": lng, "lat": lat},
        )
        row = result.fetchone()
        if not row:
            return AnalysisLayer(name="Fault Line Proximity", score=75, summary="No fault line data available.", raw_value="No data")

        dist_km = float(row[0])
        # PHIVOLCS: 5km setback required from active faults
        if dist_km < 5:
            score = 5
            summary = f"CRITICAL: Only {dist_km:.1f}km from active fault. PHIVOLCS requires 5km setback."
        elif dist_km < 10:
            score = 35
            summary = f"{dist_km:.1f}km from nearest active fault. Within high-risk zone."
        elif dist_km < 25:
            score = 65
            summary = f"{dist_km:.1f}km from nearest active fault. Moderate risk."
        else:
            score = 90
            summary = f"{dist_km:.1f}km from nearest active fault. Low seismic risk."

        return AnalysisLayer(name="Fault Line Proximity", score=score, summary=summary, raw_value=f"{dist_km:.1f} km")
    except Exception as e:
        logger.error("Fault line query failed: %s", e)
        return AnalysisLayer(name="Fault Line Proximity", score=70, summary="Fault line layer not yet loaded.", raw_value="Pending data")


async def _score_road_access(session, geom_wkt: str, lng: float, lat: float) -> AnalysisLayer:
    """Score road accessibility based on distance to nearest road.
    osm2pgsql stores 'way' in EPSG:3857 — transform query point accordingly.
    """
    try:
        result = await session.execute(
            text("""
                SELECT
                    ST_Distance(
                        ST_Transform(way, 4326)::geography,
                        ST_Point(:lng, :lat, 4326)::geography
                    ) AS distance_m
                FROM planet_osm_line
                WHERE highway IS NOT NULL
                ORDER BY way <-> ST_Transform(ST_SetSRID(ST_Point(:lng, :lat), 4326), 3857)
                LIMIT 1
            """),
            {"lng": lng, "lat": lat},
        )
        row = result.fetchone()
        if not row:
            return AnalysisLayer(name="Road Access", score=60, summary="Road data not yet loaded.", raw_value="Pending data")

        dist_m = float(row[0])
        if dist_m < 50:
            score = 95
            summary = f"Directly on or adjacent to a road ({dist_m:.0f}m)."
        elif dist_m < 200:
            score = 80
            summary = f"Good road access within {dist_m:.0f}m."
        elif dist_m < 500:
            score = 60
            summary = f"Moderate road access, {dist_m:.0f}m to nearest road."
        elif dist_m < 1000:
            score = 40
            summary = f"Limited road access, {dist_m:.0f}m to nearest road."
        else:
            score = 15
            summary = f"Poor road access, nearest road is {dist_m/1000:.1f}km away."

        return AnalysisLayer(name="Road Access", score=score, summary=summary, raw_value=f"{dist_m:.0f} m")
    except Exception as e:
        logger.error("Road access query failed: %s", e)
        return AnalysisLayer(name="Road Access", score=60, summary="Road layer not yet loaded.", raw_value="Pending data")


async def _score_demographics(session, geom_wkt: str) -> AnalysisLayer:
    """Score population density / market size from PSA barangay data."""
    try:
        result = await session.execute(
            text("""
                SELECT
                    b.population,
                    b.barangay_name,
                    b.municipality,
                    b.province
                FROM barangays b
                WHERE ST_Intersects(b.geom, ST_GeomFromText(:wkt, 4326))
                LIMIT 1
            """),
            {"wkt": geom_wkt},
        )
        row = result.fetchone()
        if not row:
            return AnalysisLayer(name="Population / Demographics", score=60, summary="Demographic data not yet loaded.", raw_value="Pending data")

        pop = int(row[0]) if row[0] else 0
        location = f"{row[1]}, {row[2]}, {row[3]}"

        if pop > 50000:
            score = 90
            summary = f"High-density area ({pop:,} residents). {location}."
        elif pop > 20000:
            score = 75
            summary = f"Moderate-density area ({pop:,} residents). {location}."
        elif pop > 5000:
            score = 55
            summary = f"Low-density area ({pop:,} residents). {location}."
        else:
            score = 30
            summary = f"Very low-density area ({pop:,} residents). {location}."

        return AnalysisLayer(name="Population / Demographics", score=score, summary=summary, raw_value=f"{pop:,} residents")
    except Exception as e:
        logger.error("Demographics query failed: %s", e)
        return AnalysisLayer(name="Population / Demographics", score=60, summary="Demographic layer not yet loaded.", raw_value="Pending data")


async def _score_poi_density(session, geom_wkt: str, lng: float, lat: float) -> AnalysisLayer:
    """Score points of interest density within 1km radius.
    osm2pgsql stores 'way' in EPSG:3857 — use ST_DWithin with transformed point.
    """
    try:
        result = await session.execute(
            text("""
                SELECT COUNT(*) AS poi_count
                FROM planet_osm_point
                WHERE amenity IS NOT NULL
                AND ST_DWithin(
                    way,
                    ST_Transform(ST_SetSRID(ST_Point(:lng, :lat), 4326), 3857),
                    1000
                )
            """),
            {"lng": lng, "lat": lat},
        )
        row = result.fetchone()
        count = int(row[0]) if row else 0

        if count > 100:
            score = 90
            summary = f"Very high commercial activity ({count} amenities within 1km)."
        elif count > 50:
            score = 75
            summary = f"High commercial density ({count} amenities within 1km)."
        elif count > 20:
            score = 55
            summary = f"Moderate commercial activity ({count} amenities within 1km)."
        elif count > 5:
            score = 35
            summary = f"Low commercial density ({count} amenities within 1km)."
        else:
            score = 15
            summary = f"Minimal commercial activity ({count} amenities within 1km)."

        return AnalysisLayer(name="POI Density", score=score, summary=summary, raw_value=f"{count} POIs")
    except Exception as e:
        logger.error("POI density query failed: %s", e)
        return AnalysisLayer(name="POI Density", score=50, summary="POI data not yet loaded.", raw_value="Pending data")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _geometry_to_wkt(geometry: dict[str, Any], lat: float, lng: float) -> str:
    """Convert GeoJSON geometry to WKT string. Falls back to point if needed."""
    geom_type = geometry.get("type", "")

    if geom_type == "Point":
        coords = geometry["coordinates"]
        return f"POINT({coords[0]} {coords[1]})"

    if geom_type == "Polygon":
        rings = geometry["coordinates"]
        ring_str = ", ".join(f"{c[0]} {c[1]}" for c in rings[0])
        return f"POLYGON(({ring_str}))"

    # Fallback to point
    return f"POINT({lng} {lat})"


def compute_overall_score(layers: list[AnalysisLayer]) -> int:
    """Weighted average of layer scores."""
    weights = {
        "Flood Susceptibility": 0.25,
        "Landslide Susceptibility": 0.15,
        "Fault Line Proximity": 0.20,
        "Road Access": 0.15,
        "Population / Demographics": 0.15,
        "POI Density": 0.10,
    }
    total_weight = 0.0
    weighted_sum = 0.0
    for layer in layers:
        w = weights.get(layer.name, 0.10)
        weighted_sum += layer.score * w
        total_weight += w

    return round(weighted_sum / total_weight) if total_weight else 0


def extract_risk_flags(layers: list[AnalysisLayer]) -> list[str]:
    """Extract risk flags from low-scoring layers."""
    flags = []
    for layer in layers:
        if layer.score < 20:
            flags.append(f"{layer.name}: {layer.summary}")
        elif layer.score < 40 and "fault" in layer.name.lower():
            flags.append(f"{layer.name}: {layer.summary}")
    return flags
