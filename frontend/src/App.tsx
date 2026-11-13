import React, { useEffect, useState, useRef } from 'react';
import { Header } from './components/Header';
import { MapView, MapViewHandle } from './components/MapView';
import { DualMapView } from './components/DualMapView';
import { ControlPanel } from './components/ControlPanel';
import { StatsDashboard } from './components/StatsDashboard';
import { RegionInspector } from './components/RegionInspector';
import { TimeLapsePlayer } from './components/TimeLapsePlayer';
import { HotspotTour } from './components/HotspotTour';
import { ReportsModal } from './components/ReportsModal';
import { AboutModal } from './components/AboutModal';
import {
  AppViewMode,
  BoundsMetadata,
  MLStatus,
  BandStat,
  ChangeRegionProperties,
  RegionSummaryItem
} from './types';

export const App: React.FC = () => {
  const [currentView, setCurrentView] = useState<AppViewMode>('observations');
  const [bounds, setBounds] = useState<BoundsMetadata | null>(null);
  const [opacity, setOpacity] = useState<number>(0.85);

  // Time-Lapse & Animation State
  const [currentCycle, setCurrentCycle] = useState<string>('028');
  const [currentPol, setCurrentPol] = useState<'HH' | 'HV'>('HH');
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [isBlinking, setIsBlinking] = useState<boolean>(false);

  // Change Map & Spotlight State
  const [selectedPair, setSelectedPair] = useState<string>('HH_028_033');
  const [hideRaster, setHideRaster] = useState<boolean>(false);
  const [selectedRegion, setSelectedRegion] = useState<ChangeRegionProperties | null>(null);
  const [activeHotspot, setActiveHotspot] = useState<string>('full');

  // Backend Data
  const [mlStatus, setMlStatus] = useState<MLStatus | null>(null);
  const [statistics, setStatistics] = useState<Record<string, BandStat>>({});
  const [regionSummaries, setRegionSummaries] = useState<RegionSummaryItem[]>([]);

  // Modals
  const [isReportsOpen, setIsReportsOpen] = useState<boolean>(false);
  const [isAboutOpen, setIsAboutOpen] = useState<boolean>(false);

  const mapRef = useRef<MapViewHandle>(null);

  // Derive active layer ID based on mode
  const getActiveLayerId = () => {
    if (currentView === 'ml') {
      return 'ml_clusters';
    }
    if (currentView === 'change') {
      return hideRaster ? 'none' : `cls_${selectedPair.toLowerCase()}`;
    }
    // Time-lapse / observation mode
    return `cycle_${currentCycle}_${currentPol.toLowerCase()}_filtered_db`;
  };

  const activeLayerId = getActiveLayerId();

  // Time-Lapse Loop
  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setCurrentCycle((prev) => {
        if (prev === '028') return '032';
        if (prev === '032') return '033';
        return '028';
      });
    }, 900);
    return () => clearInterval(interval);
  }, [isPlaying]);

  // A/B Blink Loop (Toggles 028 and 033 rapidly to make differences jump out)
  useEffect(() => {
    if (!isBlinking) return;
    const interval = setInterval(() => {
      setCurrentCycle((prev) => (prev === '028' ? '033' : '028'));
    }, 550);
    return () => clearInterval(interval);
  }, [isBlinking]);

  // Fetch Metadata & Statistics
  useEffect(() => {
    fetch('/api/metadata')
      .then((res) => res.json())
      .then((data) => setBounds(data.bounds))
      .catch(console.error);

    fetch('/api/statistics')
      .then((res) => res.json())
      .then((data) => setStatistics(data))
      .catch(console.error);

    fetch('/api/ml/status')
      .then((res) => res.json())
      .then((data: MLStatus) => setMlStatus(data))
      .catch(console.error);

    fetch('/api/regions/summary')
      .then((res) => res.json())
      .then((data: RegionSummaryItem[]) => setRegionSummaries(data))
      .catch(console.error);
  }, []);

  // When switching to Change view, default to Clean Map so glowing polygons stand out
  const handleSelectView = (view: AppViewMode) => {
    setCurrentView(view);
    if (isPlaying) setIsPlaying(false);
    if (isBlinking) setIsBlinking(false);
    if (view === 'change') {
      setHideRaster(true); // Hide opaque square, show only polygons on city map!
    } else {
      setHideRaster(false);
    }
  };

  const handleFlyTo = (center: [number, number], zoom: number, id: string) => {
    setActiveHotspot(id);
    if (mapRef.current) {
      mapRef.current.flyTo(center, zoom);
    }
  };

  const handleExportCSV = () => {
    window.open('/api/export/summary.csv', '_blank');
  };

  return (
    <div className="flex flex-col w-screen h-screen bg-[#0b0f19] text-gray-100 select-none">
      {/* Header */}
      <Header
        onOpenReports={() => setIsReportsOpen(true)}
        onOpenInfo={() => setIsAboutOpen(true)}
      />

      {/* Main Workspace */}
      <div className="flex-1 flex overflow-hidden relative">
        {/* Left Control Panel */}
        <ControlPanel
          currentView={currentView}
          onSelectView={handleSelectView}
          opacity={opacity}
          onOpacityChange={setOpacity}
          hideRaster={hideRaster}
          onToggleHideRaster={setHideRaster}
          selectedPair={selectedPair}
          onSelectPair={setSelectedPair}
          mlStatus={mlStatus}
          regionSummaries={regionSummaries}
          onExportCSV={handleExportCSV}
          onFlyToHotspot={handleFlyTo}
        />

        {/* Central Map Canvas */}
        <main className="flex-1 h-full relative">
          {/* Top Hotspot Tour Navigation */}
          {currentView !== 'swipe' && (
            <HotspotTour
              onFlyTo={handleFlyTo}
              activeHotspot={activeHotspot}
            />
          )}

          {/* DUAL VIEW OR SINGLE VIEW */}
          {currentView === 'swipe' ? (
            <DualMapView
              bounds={bounds}
              leftLayerId={`cycle_028_${currentPol.toLowerCase()}_filtered_db`}
              rightLayerId={`cycle_033_${currentPol.toLowerCase()}_filtered_db`}
              leftDateLabel="August 22, 2026 (Cycle 028)"
              rightDateLabel="October 21, 2026 (Cycle 033)"
              opacity={opacity}
            />
          ) : (
            <MapView
              ref={mapRef}
              bounds={bounds}
              activeLayerId={activeLayerId}
              opacity={opacity}
              showVectorRegions={currentView === 'change'}
              selectedPair={selectedPair}
              onSelectRegion={setSelectedRegion}
              hideRaster={hideRaster && currentView === 'change'}
            />
          )}

          {/* Time-Lapse Player (In Observation Mode) */}
          {currentView === 'observations' && (
            <TimeLapsePlayer
              currentCycle={currentCycle}
              onSelectCycle={setCurrentCycle}
              isPlaying={isPlaying}
              onTogglePlay={() => {
                if (isBlinking) setIsBlinking(false);
                setIsPlaying(!isPlaying);
              }}
              isBlinking={isBlinking}
              onToggleBlink={() => {
                if (isPlaying) setIsPlaying(false);
                setIsBlinking(!isBlinking);
              }}
              pol={currentPol}
              onTogglePol={setCurrentPol}
            />
          )}

          {/* Region Inspector Popup */}
          <RegionInspector
            region={selectedRegion}
            onClose={() => setSelectedRegion(null)}
          />
        </main>
      </div>

      {/* Bottom Recharts Statistics Bar */}
      <StatsDashboard
        statistics={statistics}
        regionSummaries={regionSummaries}
      />

      {/* Reports & About Modals */}
      <ReportsModal
        isOpen={isReportsOpen}
        onClose={() => setIsReportsOpen(false)}
      />

      <AboutModal
        isOpen={isAboutOpen}
        onClose={() => setIsAboutOpen(false)}
      />
    </div>
  );
};
