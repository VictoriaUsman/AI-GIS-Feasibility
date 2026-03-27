# SiteSight PH

AI-powered site feasibility analysis for the Philippines. Drop a pin or draw a polygon on the map — get a scored GIS assessment and a downloadable PDF report in seconds.

---

## What It Does

1. User selects a location on the map (point or polygon)
2. Backend queries PostGIS layers for that location
3. Each GIS layer is scored 0–100
4. GPT-4o mini generates a professional narrative
5. User downloads a PDF feasibility report

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, MapLibre GL JS, Tailwind CSS, Zustand |
| Backend | FastAPI (Python), SQLAlchemy async |
| Database | PostgreSQL + PostGIS |
| AI | OpenAI GPT-4o mini |
| PDF | WeasyPrint + Jinja2 |
| Maps | MapLibre GL JS + OpenFreeMap tiles (no API key) |

---

## GIS Data Layers

| Layer | Score Weight | Source |
|---|---|---|
| Flood Susceptibility | 25% | MGB Philippines |
| Fault Line Proximity | 20% | PHIVOLCS |
| Landslide Susceptibility | 15% | MGB Philippines |
| Road Access | 15% | OpenStreetMap |
| Population / Demographics | 15% | PSA Census 2020 |
| POI Density | 10% | OpenStreetMap |

---

## Project Structure

```
.
├── frontend/               # Next.js app
│   ├── src/
│   │   ├── app/            # App router (layout, page)
│   │   ├── components/
│   │   │   ├── Map/        # MapLibre map + draw tools
│   │   │   └── Sidebar/    # Analysis, Report, Layers panels
│   │   ├── store/          # Zustand state
│   │   ├── lib/api.ts      # Axios API client
│   │   └── types/          # TypeScript types
│   └── .env.local
├── backend/                # FastAPI app
│   ├── app/
│   │   ├── api/            # /analysis/run, /report/generate
│   │   ├── services/
│   │   │   ├── gis_service.py   # PostGIS queries + scoring
│   │   │   ├── ai_service.py    # GPT-4o mini narrative
│   │   │   └── pdf_service.py   # WeasyPrint PDF generation
│   │   ├── templates/      # HTML report template
│   │   └── sql/init.sql    # PostGIS schema
│   └── .env
├── data/                   # GIS data files (see data/README.md)
└── docker-compose.yml
```

---

## Getting Started

### 1. Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Node.js 20+
- Python 3.11+
- OpenAI API key

### 2. Configure environment

**`backend/.env`**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gis_feasibility
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
DATA_DIR=./data
```

**`frontend/.env.local`**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the database

```bash
docker-compose up db
```

### 4. Run the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 5. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

---

## Loading GIS Data

The app runs without GIS data (layers return placeholder scores). To load real data:

### OpenStreetMap — roads + POIs (do this first, it's free and fast)
```bash
# Download Philippines OSM data
# From: https://download.geofabrik.de/asia/philippines.html

osm2pgsql -d gis_feasibility -U postgres -H localhost data/osm/philippines-latest.osm.pbf
```

### MGB Flood + Landslide Susceptibility
```bash
# Download from: https://www.mgb.gov.ph/ (Geohazard Maps section)

ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
  data/mgb/flood/flood_susceptibility.shp \
  -nln flood_susceptibility -t_srs EPSG:4326
```

### PHIVOLCS Active Fault Lines
```bash
# Download from: https://www.phivolcs.dost.gov.ph/

ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
  data/phivolcs/faults/active_faults.shp \
  -nln fault_lines -t_srs EPSG:4326
```

### PSA Barangay Boundaries + Census 2020
```bash
# Download from: https://psa.gov.ph/ (geographic boundaries section)

ogr2ogr -f "PostgreSQL" \
  PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
  data/psa/barangays/barangays.shp \
  -nln barangays -t_srs EPSG:4326
```

See `data/README.md` for full details.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analysis/run` | Run GIS analysis for a location |
| `POST` | `/api/report/generate` | Generate PDF report |
| `GET` | `/health` | Health check |

### Example: Run analysis
```json
POST /api/analysis/run
{
  "geometry": { "type": "Point", "coordinates": [121.05, 14.55] },
  "coordinates": { "lat": 14.55, "lng": 121.05 }
}
```

---

## Roadmap

- [ ] Load real MGB / PHIVOLCS / PSA data
- [ ] User authentication (Supabase)
- [ ] Save and compare multiple sites
- [ ] Address / barangay search
- [ ] Additional layers: NAMRIA land use, school zones, utilities
- [ ] Export to Excel / Word
