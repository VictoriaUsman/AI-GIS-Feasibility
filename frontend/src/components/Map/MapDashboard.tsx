"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import maplibregl from "maplibre-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import Sidebar from "@/components/Sidebar/Sidebar";
import { useAnalysisStore } from "@/store/analysisStore";

export default function MapDashboard() {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const draw = useRef<MapboxDraw | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  const { setGeometry, setCoordinates } = useAnalysisStore();

  const handleDrawCreate = useCallback(
    (e: { features: GeoJSON.Feature[] }) => {
      const feature = e.features[0];
      setGeometry(feature.geometry);

      if (feature.geometry.type === "Point") {
        const [lng, lat] = (feature.geometry as GeoJSON.Point).coordinates;
        setCoordinates({ lng, lat });
      } else if (feature.geometry.type === "Polygon") {
        const coords = (feature.geometry as GeoJSON.Polygon).coordinates[0];
        const lngs = coords.map((c) => c[0]);
        const lats = coords.map((c) => c[1]);
        setCoordinates({
          lng: (Math.min(...lngs) + Math.max(...lngs)) / 2,
          lat: (Math.min(...lats) + Math.max(...lats)) / 2,
        });
      }
    },
    [setGeometry, setCoordinates]
  );

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://tiles.openfreemap.org/styles/liberty",
      center: [121.774, 12.8797], // Philippines center
      zoom: 6,
    });

    draw.current = new MapboxDraw({
      displayControlsDefault: false,
      controls: {
        point: true,
        polygon: true,
        trash: true,
      },
    });

    map.current.addControl(new maplibregl.NavigationControl(), "top-right");
    map.current.addControl(draw.current);

    map.current.on("load", () => setMapLoaded(true));
    map.current.on("draw.create", handleDrawCreate);
    map.current.on("draw.update", handleDrawCreate);

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, [handleDrawCreate]);

  return (
    <div className="flex w-full h-full">
      {/* Map */}
      <div ref={mapContainer} className="flex-1 h-full" />

      {/* Sidebar */}
      <Sidebar mapLoaded={mapLoaded} />
    </div>
  );
}
