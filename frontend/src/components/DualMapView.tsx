import React, { useEffect, useRef } from 'react';
import maplibregl from 'maplibre-gl';
import { BoundsMetadata } from '../types';

interface DualMapViewProps {
  bounds: BoundsMetadata | null;
  leftLayerId: string;
  rightLayerId: string;
  leftDateLabel: string;
  rightDateLabel: string;
  opacity: number;
}

export const DualMapView: React.FC<DualMapViewProps> = ({
  bounds,
  leftLayerId,
  rightLayerId,
  leftDateLabel,
  rightDateLabel,
  opacity,
}) => {
  const containerLeftRef = useRef<HTMLDivElement>(null);
  const containerRightRef = useRef<HTMLDivElement>(null);
  const mapLeftRef = useRef<maplibregl.Map | null>(null);
  const mapRightRef = useRef<maplibregl.Map | null>(null);
  const isSyncing = useRef<boolean>(false);

  useEffect(() => {
    if (!containerLeftRef.current || !containerRightRef.current || !bounds) return;

    const center = bounds.center as maplibregl.LngLatLike;
    const zoom = bounds.zoom || 12.3;

    const baseStyle: maplibregl.StyleSpecification = {
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
        { id: 'bg', type: 'background', paint: { 'background-color': '#0b0f19' } },
        { id: 'osm', type: 'raster', source: 'osm', paint: { 'raster-opacity': 0.65 } }
      ]
    };

    const mapLeft = new maplibregl.Map({
      container: containerLeftRef.current,
      style: baseStyle,
      center,
      zoom,
    });

    const mapRight = new maplibregl.Map({
      container: containerRightRef.current,
      style: baseStyle,
      center,
      zoom,
    });

    // Synchronize camera movement between both maps
    const syncMaps = (source: maplibregl.Map, target: maplibregl.Map) => {
      source.on('move', () => {
        if (isSyncing.current) return;
        isSyncing.current = true;
        target.jumpTo({
          center: source.getCenter(),
          zoom: source.getZoom(),
          bearing: source.getBearing(),
          pitch: source.getPitch()
        });
        isSyncing.current = false;
      });
    };

    syncMaps(mapLeft, mapRight);
    syncMaps(mapRight, mapLeft);

    // Add Raster Overlays
    const addRaster = (map: maplibregl.Map, layerId: string) => {
      const srcId = 'raster-src';
      const lyrId = 'raster-lyr';

      const setup = () => {
        if (map.getSource(srcId)) map.removeSource(srcId);
        if (map.getLayer(lyrId)) map.removeLayer(lyrId);

        map.addSource(srcId, {
          type: 'image',
          url: `/api/raster/${layerId}.png`,
          coordinates: bounds.coordinates as any
        });
        map.addLayer({
          id: lyrId,
          type: 'raster',
          source: srcId,
          paint: { 'raster-opacity': opacity }
        });
      };

      if (map.isStyleLoaded()) setup();
      else map.once('style.load', setup);
    };

    addRaster(mapLeft, leftLayerId);
    addRaster(mapRight, rightLayerId);

    mapLeftRef.current = mapLeft;
    mapRightRef.current = mapRight;

    return () => {
      mapLeft.remove();
      mapRight.remove();
      mapLeftRef.current = null;
      mapRightRef.current = null;
    };
  }, [bounds]);

  // Update layer URLs on change
  useEffect(() => {
    const updateSrc = (map: maplibregl.Map | null, layerId: string) => {
      if (!map || !map.isStyleLoaded() || !bounds) return;
      if (map.getLayer('raster-lyr')) map.removeLayer('raster-lyr');
      if (map.getSource('raster-src')) map.removeSource('raster-src');

      map.addSource('raster-src', {
        type: 'image',
        url: `/api/raster/${layerId}.png`,
        coordinates: bounds.coordinates as any
      });
      map.addLayer({
        id: 'raster-lyr',
        type: 'raster',
        source: 'raster-src',
        paint: { 'raster-opacity': opacity }
      });
    };

    updateSrc(mapLeftRef.current, leftLayerId);
    updateSrc(mapRightRef.current, rightLayerId);
  }, [leftLayerId, rightLayerId, opacity, bounds]);

  return (
    <div className="w-full h-full flex divide-x-2 divide-blue-500 relative bg-[#0b0f19]">
      {/* Left Map (Baseline) */}
      <div className="flex-1 h-full relative">
        <div ref={containerLeftRef} className="w-full h-full" />
        <div className="absolute top-4 left-4 z-20 px-3 py-1.5 bg-blue-950/90 border border-blue-500 rounded shadow-lg text-xs font-bold text-white flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-blue-400 animate-pulse" />
          <span>BASELINE: {leftDateLabel}</span>
        </div>
      </div>

      {/* Right Map (Repeat) */}
      <div className="flex-1 h-full relative">
        <div ref={containerRightRef} className="w-full h-full" />
        <div className="absolute top-4 left-4 z-20 px-3 py-1.5 bg-indigo-950/90 border border-indigo-500 rounded shadow-lg text-xs font-bold text-white flex items-center space-x-2">
          <span className="w-2.5 h-2.5 rounded-full bg-indigo-400 animate-pulse" />
          <span>REPEAT: {rightDateLabel}</span>
        </div>
      </div>

      {/* Floating Center Badge */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-30 px-3 py-1 bg-gray-900/90 border border-gray-700 rounded-full text-[11px] font-semibold text-gray-200 shadow-xl pointer-events-none">
        Synchronized Dual View (Pan & Zoom Together)
      </div>
    </div>
  );
};
