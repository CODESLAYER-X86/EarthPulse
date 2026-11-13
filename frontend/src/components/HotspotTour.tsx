import React from 'react';
import { Compass, Waves, Trees, Building2 } from 'lucide-react';

interface Hotspot {
  id: string;
  name: string;
  icon: any;
  center: [number, number];
  zoom: number;
  highlight: string;
}

interface HotspotTourProps {
  onFlyTo: (center: [number, number], zoom: number, name: string) => void;
  activeHotspot: string;
}

export const HotspotTour: React.FC<HotspotTourProps> = ({ onFlyTo, activeHotspot }) => {
  const hotspots: Hotspot[] = [
    {
      id: 'full',
      name: 'Full Estuary (25 km²)',
      icon: Compass,
      center: [-35.218, -5.761],
      zoom: 12.3,
      highlight: 'Full Potengi basin overview'
    },
    {
      id: 'tidal',
      name: '🌊 River Tidal Flooding',
      icon: Waves,
      center: [-35.219, -5.744],
      zoom: 14.8,
      highlight: 'Water flooded over intertidal mudflats'
    },
    {
      id: 'mangrove',
      name: '🌿 Core Mangrove Forest',
      icon: Trees,
      center: [-35.212, -5.758],
      zoom: 14.6,
      highlight: 'Dense Rhizophora canopy with 99% stability'
    },
    {
      id: 'urban',
      name: '🏙️ Bridge & Port Alecrim',
      icon: Building2,
      center: [-35.198, -5.753],
      zoom: 15.0,
      highlight: 'Strong structural double-bounce reflection'
    }
  ];

  return (
    <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 flex items-center space-x-1.5 bg-[#111827]/90 backdrop-blur-md p-1 rounded-full border border-gray-700 shadow-xl">
      <span className="text-[10px] font-bold uppercase tracking-wider text-gray-400 px-2.5">
        Tour Hotspots:
      </span>
      {hotspots.map((h) => (
        <button
          key={h.id}
          onClick={() => onFlyTo(h.center, h.zoom, h.id)}
          className={`px-3 py-1 rounded-full text-xs font-semibold transition flex items-center space-x-1 ${
            activeHotspot === h.id
              ? 'bg-blue-600 text-white shadow'
              : 'text-gray-300 hover:text-white hover:bg-gray-800'
          }`}
          title={h.highlight}
        >
          <span>{h.name}</span>
        </button>
      ))}
    </div>
  );
};
