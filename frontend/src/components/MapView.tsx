import React, { useEffect, useRef, useState, useImperativeHandle, forwardRef } from 'react';
import maplibregl from 'maplibre-gl';
import { BoundsMetadata, ChangeRegionProperties } from '../types';

export interface MapViewHandle {
  flyTo: (center: [number, number], zoom: number) => void;
}

interface MapViewProps {
  bounds: BoundsMetadata | null;
  activeLayerId: string;
  opacity: number;
  showVectorRegions: boolean;
  selectedPair: string; // e.g. "HH_028_033"
  onSelectRegion: (props: ChangeRegionProperties | null) => void;
  hideRaster?: boolean;
}

export const MapView = forwardRef<MapViewHandle, MapViewProps>(({
  bounds,
  activeLayerId,
  opacity,
  showVectorRegions,
  selectedPair,
  onSelectRegion,
  hideRaster = false,
}, ref) => {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const [cursorCoords, setCursorCoords] = useState<{ lon: number; lat: number } | null>(null);

  useImperativeHandle(ref, () => ({
    flyTo: (center: [number, number], zoom: number) => {
      if (mapRef.current) {
        mapRef.current.flyTo({
          center,
          zoom,
          duration: 1400,
          essential: true
        });
      }
    }
  }));

  // Initialize MapLibre
  useEffect(() => {
    if (!mapContainer.current || mapRef.current) return;

    const initialCenter = (bounds ? bounds.center : [-35.218, -5.761]) as maplibregl.LngLatLike;
    const initialZoom = bounds ? bounds.zoom : 12.3;

    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: 'raster',
            tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap'
          }
        },
        layers: [
          { id: 'background', type: 'background', paint: { 'background-color': '#0f172a' } },
          { id: 'osm-tiles', type: 'raster', source: 'osm', paint: { 'raster-opacity': 0.70 } }
        ]
      },
      center: initialCenter,
      zoom: initialZoom,
      maxPitch: 60
    });

    map.addControl(new maplibregl.NavigationControl({ showCompass: true }), 'top-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-left');

    map.on('mousemove', (e) => {
      setCursorCoords({
        lon: parseFloat(e.lngLat.lng.toFixed(5)),
        lat: parseFloat(e.lngLat.lat.toFixed(5))
      });
    });

    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, [bounds]);

  // Update Raster Layer Source
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !bounds) return;

    const updateRaster = () => {
      const sourceId = 'nisar-raster-single';
      const layerId = 'nisar-raster-layer';
      const borderSourceId = 'nisar-aoi-border';
      const borderLayerId = 'nisar-aoi-border-layer';

      // 1. AOI Bounding Box
      if (!map.getSource(borderSourceId)) {
        const polyCoords = [
          bounds.coordinates[0],
          bounds.coordinates[1],
          bounds.coordinates[2],
          bounds.coordinates[3],
          bounds.coordinates[0]
        ];
        map.addSource(borderSourceId, {
          type: 'geojson',
          data: {
            type: 'Feature',
            geometry: { type: 'Polygon', coordinates: [polyCoords] },
            properties: {}
          }
        });
        map.addLayer({
          id: borderLayerId,
          type: 'line',
          source: borderSourceId,
          paint: {
            'line-color': '#38bdf8',
            'line-width': 1.5,
            'line-dasharray': [3, 2]
          }
        });
      }

      // 2. Remove previous raster
      if (map.getLayer(layerId)) map.removeLayer(layerId);
      if (map.getSource(sourceId)) map.removeSource(sourceId);

      // 3. Add fresh raster if not hidden
      if (!hideRaster && activeLayerId !== 'none') {
        const rasterUrl = `/api/raster/${activeLayerId}.png`;
        map.addSource(sourceId, {
          type: 'image',
          url: rasterUrl,
          coordinates: bounds.coordinates as any
        });
        map.addLayer({
          id: layerId,
          type: 'raster',
          source: sourceId,
          paint: {
            'raster-opacity': opacity,
            'raster-fade-duration': 80
          }
        });
      }
    };

    if (map.isStyleLoaded()) updateRaster();
    else map.once('style.load', updateRaster);
  }, [bounds, activeLayerId, opacity, hideRaster]);

  // Update Vector Change Regions Layer
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    const sourceId = 'vector-change-regions';
    const fillLayerId = 'vector-change-fill';
    const lineLayerId = 'vector-change-line';

    const updateVectorRegions = () => {
      if (map.getLayer(lineLayerId)) map.removeLayer(lineLayerId);
      if (map.getLayer(fillLayerId)) map.removeLayer(fillLayerId);
      if (map.getSource(sourceId)) map.removeSource(sourceId);

      if (!showVectorRegions) return;

      const geojsonUrl = `/api/geojson/change-regions/${selectedPair}`;

      map.addSource(sourceId, {
        type: 'geojson',
        data: geojsonUrl
      });

      // Fill Layer
      map.addLayer({
        id: fillLayerId,
        type: 'fill',
        source: sourceId,
        paint: {
          'fill-color': [
            'match',
            ['get', 'category'],
            'Significant Decrease', '#ef4444',
            'Moderate Decrease', '#f97316',
            'Moderate Increase', '#06b6d4',
            'Significant Increase', '#10b981',
            '#9ca3af'
          ],
          'fill-opacity': 0.75
        }
      });

      // Outline Layer
      map.addLayer({
        id: lineLayerId,
        type: 'line',
        source: sourceId,
        paint: {
          'line-color': [
            'match',
            ['get', 'category'],
            'Significant Decrease', '#7f1d1d',
            'Moderate Decrease', '#7c2d12',
            'Moderate Increase', '#164e63',
            'Significant Increase', '#064e3b',
            '#ffffff'
          ],
          'line-width': 2
        }
      });

      // Click inspector
      map.on('click', fillLayerId, (e) => {
        if (e.features && e.features[0]) {
          onSelectRegion(e.features[0].properties as any);
        }
      });

      map.on('mouseenter', fillLayerId, () => {
        map.getCanvas().style.cursor = 'pointer';
      });
      map.on('mouseleave', fillLayerId, () => {
        map.getCanvas().style.cursor = '';
      });
    };

    if (map.isStyleLoaded()) updateVectorRegions();
    else map.once('style.load', updateVectorRegions);
  }, [showVectorRegions, selectedPair]);

  return (
    <div className="relative w-full h-full select-none">
      <div ref={mapContainer} className="w-full h-full" />

      {/* Coordinate HUD */}
      <div className="absolute bottom-3 right-3 bg-gray-900/90 backdrop-blur-sm border border-gray-800 text-[11px] text-gray-300 px-3 py-1.5 rounded shadow pointer-events-none flex items-center space-x-3 font-mono z-10">
        <div>
          <span className="text-gray-500">CRS: </span>
          <span>{bounds?.epsg || 'EPSG:32725'}</span>
        </div>
        {cursorCoords && (
          <div>
            <span className="text-gray-500">Lon/Lat: </span>
            <span>{cursorCoords.lon}, {cursorCoords.lat}</span>
          </div>
        )}
      </div>
    </div>
  );
});
