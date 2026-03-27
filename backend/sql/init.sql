-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Flood susceptibility (from MGB shapefiles)
CREATE TABLE IF NOT EXISTS flood_susceptibility (
    id SERIAL PRIMARY KEY,
    susceptibility VARCHAR(20),  -- none, low, moderate, high, very high
    geom GEOMETRY(MULTIPOLYGON, 4326)
);
CREATE INDEX IF NOT EXISTS idx_flood_geom ON flood_susceptibility USING GIST(geom);

-- Landslide susceptibility (from MGB shapefiles)
CREATE TABLE IF NOT EXISTS landslide_susceptibility (
    id SERIAL PRIMARY KEY,
    susceptibility VARCHAR(20),
    geom GEOMETRY(MULTIPOLYGON, 4326)
);
CREATE INDEX IF NOT EXISTS idx_landslide_geom ON landslide_susceptibility USING GIST(geom);

-- Active fault lines (from PHIVOLCS)
CREATE TABLE IF NOT EXISTS fault_lines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    fault_type VARCHAR(100),
    geom GEOMETRY(MULTILINESTRING, 4326)
);
CREATE INDEX IF NOT EXISTS idx_fault_geom ON fault_lines USING GIST(geom);

-- Land use / zoning (from NAMRIA)
CREATE TABLE IF NOT EXISTS land_use (
    id SERIAL PRIMARY KEY,
    classification VARCHAR(100),
    description TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)
);
CREATE INDEX IF NOT EXISTS idx_landuse_geom ON land_use USING GIST(geom);

-- Barangay boundaries + PSA demographics
CREATE TABLE IF NOT EXISTS barangays (
    id SERIAL PRIMARY KEY,
    barangay_code VARCHAR(20),
    barangay_name VARCHAR(255),
    municipality VARCHAR(255),
    province VARCHAR(255),
    region VARCHAR(100),
    population INTEGER,
    household_count INTEGER,
    geom GEOMETRY(MULTIPOLYGON, 4326)
);
CREATE INDEX IF NOT EXISTS idx_barangays_geom ON barangays USING GIST(geom);

-- OSM roads and POIs are loaded via osm2pgsql into planet_osm_line / planet_osm_point
