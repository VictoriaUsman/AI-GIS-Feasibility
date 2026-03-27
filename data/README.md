# GIS Data Directory

Place raw GIS data files here before loading into PostGIS.

## Required Data Sources

### 1. MGB Geohazard Maps (flood + landslide)
- Source: Mines and Geosciences Bureau — https://www.mgb.gov.ph/
- Files: Geohazard shapefiles per province
- Load command:
  ```
  ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
    flood_susceptibility.shp -nln flood_susceptibility -t_srs EPSG:4326
  ```

### 2. PHIVOLCS Active Fault Lines
- Source: Philippine Institute of Volcanology and Seismology — https://www.phivolcs.dost.gov.ph/
- Files: Active Fault Line shapefile (Philippines)
- Load command:
  ```
  ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
    active_faults.shp -nln fault_lines -t_srs EPSG:4326
  ```

### 3. PSA Barangay Boundaries + Census 2020
- Source: Philippine Statistics Authority — https://psa.gov.ph/
- Files: Barangay shapefile + Census 2020 population data
- Load command:
  ```
  ogr2ogr -f "PostgreSQL" PG:"host=localhost dbname=gis_feasibility user=postgres password=postgres" \
    barangays.shp -nln barangays -t_srs EPSG:4326
  ```

### 4. OpenStreetMap Philippines
- Source: Geofabrik — https://download.geofabrik.de/asia/philippines.html
- File: philippines-latest.osm.pbf
- Load command:
  ```
  osm2pgsql -d gis_feasibility -U postgres -H localhost philippines-latest.osm.pbf
  ```

### 5. NAMRIA Land Use / Land Cover
- Source: National Mapping and Resource Information Authority — https://www.namria.gov.ph/
- Files: Land use classification shapefiles

## Directory Structure
```
data/
├── mgb/
│   ├── flood/          # MGB flood susceptibility shapefiles
│   └── landslide/      # MGB landslide susceptibility shapefiles
├── phivolcs/
│   └── faults/         # Active fault line shapefiles
├── psa/
│   ├── barangays/      # Barangay boundary shapefiles
│   └── census2020/     # PSA 2020 census CSV data
├── namria/
│   └── landuse/        # Land use/land cover shapefiles
└── osm/
    └── philippines-latest.osm.pbf
```
