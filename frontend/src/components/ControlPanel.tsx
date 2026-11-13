import React from 'react';
import {
  Film,
  SplitSquareVertical,
  Flame,
  Sparkles,
  Sliders,
  Download,
  Info,
  ShieldAlert,
  ChevronRight,
  Eye,
  EyeOff
} from 'lucide-react';
import { AppViewMode, MLStatus, RegionSummaryItem } from '../types';

interface ControlPanelProps {
  currentView: AppViewMode;
  onSelectView: (mode: AppViewMode) => void;
  opacity: number;
  onOpacityChange: (opacity: number) => void;
  hideRaster: boolean;
  onToggleHideRaster: (hide: boolean) => void;
  selectedPair: string;
  onSelectPair: (pair: string) => void;
  mlStatus: MLStatus | null;
  regionSummaries: RegionSummaryItem[];
  onExportCSV: () => void;
  onFlyToHotspot: (center: [number, number], zoom: number, name: string) => void;
  selectedCluster?: number | null;
  onSelectCluster?: (id: number | null) => void;
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  currentView,
  onSelectView,
  opacity,
  onOpacityChange,
  hideRaster,
  onToggleHideRaster,
  selectedPair,
  onSelectPair,
  mlStatus,
  regionSummaries,
  onExportCSV,
  onFlyToHotspot,
  selectedCluster,
  onSelectCluster
}) => {
  const currentSummary = regionSummaries.find(r => `${r.pol}_${r.pair}` === selectedPair);

  return (
    <div className="w-88 h-full bg-[#111827] border-r border-gray-800 flex flex-col z-10 shadow-2xl overflow-hidden">
      {/* 4 Core Modes */}
      <div className="p-2 border-b border-gray-800 grid grid-cols-4 gap-1 bg-[#0b0f19]">
        <button
          onClick={() => onSelectView('observations')}
          className={`py-2 px-1 text-[11px] font-medium rounded transition flex flex-col items-center justify-center space-y-1 ${
            currentView === 'observations'
              ? 'bg-blue-600 text-white font-bold shadow'
              : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
          title="Watch the 3-date satellite time-lapse"
        >
          <Film className="w-4 h-4" />
          <span>Dance</span>
        </button>

        <button
          onClick={() => onSelectView('swipe')}
          className={`py-2 px-1 text-[11px] font-medium rounded transition flex flex-col items-center justify-center space-y-1 ${
            currentView === 'swipe'
              ? 'bg-blue-600 text-white font-bold shadow'
              : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
          title="Side-by-side synced comparison"
        >
          <SplitSquareVertical className="w-4 h-4" />
          <span>Compare</span>
        </button>

        <button
          onClick={() => onSelectView('change')}
          className={`py-2 px-1 text-[11px] font-medium rounded transition flex flex-col items-center justify-center space-y-1 ${
            currentView === 'change'
              ? 'bg-rose-600 text-white font-bold shadow'
              : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
          title="View isolated environmental change zones"
        >
          <Flame className="w-4 h-4 text-orange-400" />
          <span>Changes</span>
        </button>

        <button
          onClick={() => onSelectView('ml')}
          className={`py-2 px-1 text-[11px] font-medium rounded transition flex flex-col items-center justify-center space-y-1 ${
            currentView === 'ml'
              ? 'bg-purple-600 text-white font-bold shadow'
              : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
          }`}
          title="AI Machine Learning classification"
        >
          <Sparkles className="w-4 h-4 text-purple-300" />
          <span>AI / ML</span>
        </button>
      </div>

      {/* Main Mode Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5">
        {/* MODE 1: TIME-LAPSE / DANCE */}
        {currentView === 'observations' && (
          <div className="space-y-4">
            <div className="p-3 bg-blue-950/40 border border-blue-800/40 rounded-lg space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-blue-400 block">SAR Time-Lapse Mode</span>
              <h3 className="text-sm font-semibold text-white">The "Dance of SARs"</h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                Use the floating player at the bottom of the map to play the animation across the 3 dates (Aug 22 → Oct 09 → Oct 21) or click <strong>"Blink Compare"</strong> to make tidal flood changes flash to your eyes!
              </p>
            </div>

            <div className="space-y-2">
              <label className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">What to Look For</label>
              <div className="space-y-1.5 text-xs text-gray-300">
                <div className="p-2.5 bg-gray-900/60 rounded border border-gray-800 flex items-start space-x-2">
                  <span className="text-base">🌊</span>
                  <div>
                    <span className="font-semibold text-cyan-300 block">Tidal Fluctuation in the Channel:</span>
                    <p className="text-[11px] text-gray-400 mt-0.5">Water darkens as high tide submerges intertidal mudflats along the river mouth.</p>
                  </div>
                </div>

                <div className="p-2.5 bg-gray-900/60 rounded border border-gray-800 flex items-start space-x-2">
                  <span className="text-base">🌿</span>
                  <div>
                    <span className="font-semibold text-emerald-300 block">Mangrove Canopy Resilience:</span>
                    <p className="text-[11px] text-gray-400 mt-0.5">The green volume scattering in the central forest stays rock solid throughout all 60 days!</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* MODE 2: DUAL SYNCED COMPARE */}
        {currentView === 'swipe' && (
          <div className="space-y-4">
            <div className="p-3 bg-indigo-950/40 border border-indigo-800/40 rounded-lg space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400 block">Side-by-Side Dual View</span>
              <h3 className="text-sm font-semibold text-white">August Baseline vs October Repeat</h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                Both maps are locked and synchronized. Pan or zoom anywhere—notice the exact riverbanks and mudflats that flooded between August and October!
              </p>
            </div>

            <div className="space-y-2">
              <label className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Direct Change Comparison</label>
              <div className="p-3 bg-gray-900/80 rounded border border-gray-800 space-y-2 text-xs">
                <div className="flex justify-between items-center text-blue-300">
                  <span className="font-bold">LEFT: August 22, 2026</span>
                  <span className="font-mono text-[10px] bg-blue-900/60 px-1.5 py-0.5 rounded">Cycle 028</span>
                </div>
                <p className="text-[11px] text-gray-400">Exposed mudflats, lower water table, dry embankments.</p>
                <div className="pt-2 border-t border-gray-800 flex justify-between items-center text-indigo-300">
                  <span className="font-bold">RIGHT: October 21, 2026</span>
                  <span className="font-mono text-[10px] bg-indigo-900/60 px-1.5 py-0.5 rounded">Cycle 033</span>
                </div>
                <p className="text-[11px] text-gray-400">Submerged tidal flats, higher water extent, damp soil.</p>
              </div>
            </div>
          </div>
        )}

        {/* MODE 3: ENVIRONMENTAL CHANGES */}
        {currentView === 'change' && (
          <div className="space-y-4">
            <div className="p-3 bg-rose-950/40 border border-rose-800/40 rounded-lg space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-rose-400 block">Environmental Change Spotlight</span>
              <h3 className="text-sm font-semibold text-white">Isolated Change Zones</h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                Speckle noise is filtered out. Only statistically coherent changes (≥ 1,500 m²) are shown as glowing polygons directly on top of the real street and river map!
              </p>
            </div>

            {/* Clean Map Toggle */}
            <div className="p-2.5 bg-gray-900/80 rounded border border-gray-800 flex items-center justify-between">
              <span className="text-xs text-gray-300 font-medium">Spotlight Clean Map Mode</span>
              <button
                onClick={() => onToggleHideRaster(!hideRaster)}
                className={`px-2.5 py-1 rounded text-xs font-bold transition flex items-center space-x-1.5 ${
                  hideRaster
                    ? 'bg-emerald-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:text-white'
                }`}
                title="Hides the square box and shows only the glowing change polygons over the real map"
              >
                {hideRaster ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                <span>{hideRaster ? 'Clean Map (ON)' : 'Clean Map (OFF)'}</span>
              </button>
            </div>

            {/* Change Metrics Summary Card */}
            {currentSummary && (
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 bg-gray-900/80 rounded border border-gray-800">
                  <span className="text-gray-500 block text-[10px]">Change Polygons</span>
                  <span className="text-base font-bold text-white">{currentSummary.total_regions}</span>
                  <span className="text-[10px] text-gray-400 block">Coherent zones</span>
                </div>
                <div className="p-2.5 bg-gray-900/80 rounded border border-gray-800">
                  <span className="text-gray-500 block text-[10px]">Total Change Area</span>
                  <span className="text-base font-bold text-rose-400">{currentSummary.total_area_ha} ha</span>
                  <span className="text-[10px] text-gray-400 block">{currentSummary.interval}</span>
                </div>
              </div>
            )}

            {/* Interval Selector */}
            <div className="space-y-1.5">
              <label className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">Select Interval</label>
              {[
                { pair: 'HH_028_033', name: 'Δ HH: Aug 22 → Oct 21 (60-day Baseline)' },
                { pair: 'HV_028_033', name: 'Δ HV: Aug 22 → Oct 21 (60-day Baseline)' },
                { pair: 'HH_028_032', name: 'Δ HH: Aug 22 → Oct 09 (48-day Interval)' },
                { pair: 'HV_028_032', name: 'Δ HV: Aug 22 → Oct 09 (48-day Interval)' },
              ].map((item) => (
                <button
                  key={item.pair}
                  onClick={() => onSelectPair(item.pair)}
                  className={`w-full py-2 px-3 text-xs rounded border text-left transition flex items-center justify-between ${
                    selectedPair === item.pair
                      ? 'border-rose-500 bg-rose-950/60 text-rose-200 font-bold'
                      : 'border-gray-800 bg-gray-900/80 text-gray-300 hover:bg-gray-800'
                  }`}
                >
                  <span>{item.name}</span>
                </button>
              ))}
            </div>

            {/* Click Inspector Hint */}
            <div className="p-2 bg-blue-950/30 border border-blue-900/40 rounded text-[11px] text-blue-300 flex items-start space-x-1.5">
              <Info className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-blue-400" />
              <span>Click any red or green polygon on the map to inspect its exact hectare size and tidal flood hypothesis!</span>
            </div>
          </div>
        )}

        {/* MODE 4: MACHINE LEARNING */}
        {currentView === 'ml' && (
          <div className="space-y-4">
            <div className="p-3 bg-purple-950/40 border border-purple-800/40 rounded-lg space-y-1">
              <span className="text-[10px] font-bold uppercase tracking-wider text-purple-400 block">NASA AI Architecture</span>
              <h3 className="text-sm font-semibold text-white">MiniBatch K-Means ($k=4$)</h3>
              <p className="text-xs text-gray-300 leading-relaxed">
                The AI grouped all 250,000 pixels across 12 temporal bands into 4 clear land/water/wetland classes:
              </p>
            </div>

            <div className="space-y-2 text-xs">
              {[
                { id: 0, name: '0: Water & Mudflats', color: 'bg-blue-500', area: '20.1% (5.0 km²)', diff: '+2.66 dB', note: 'Inundation' },
                { id: 1, name: '1: Dense Mangroves', color: 'bg-emerald-500', area: '29.9% (7.5 km²)', diff: '-1.30 dB', note: 'Stable Canopy' },
                { id: 2, name: '2: Scrub & Marsh', color: 'bg-amber-500', area: '22.2% (5.6 km²)', diff: '-2.01 dB', note: 'Drying Flats' },
                { id: 3, name: '3: Urban & Structures', color: 'bg-red-500', area: '27.8% (7.0 km²)', diff: '+0.91 dB', note: 'Reflectors' },
              ].map((c) => {
                const isSelected = selectedCluster === c.id;
                return (
                  <button
                    key={c.id}
                    onClick={() => onSelectCluster && onSelectCluster(isSelected ? null : c.id)}
                    className={`w-full p-2.5 rounded border text-left transition flex items-center justify-between ${
                      isSelected
                        ? 'border-white bg-gray-800 shadow ring-1 ring-white/40'
                        : 'border-gray-800 bg-gray-900/80 hover:bg-gray-800 hover:border-gray-700'
                    }`}
                  >
                    <div className="flex items-center space-x-2">
                      <span className={`w-3.5 h-3.5 rounded ${c.color} inline-block`} />
                      <div>
                        <span className="font-semibold text-white block">{c.name}</span>
                        <span className="text-[10px] text-gray-400 font-mono">{c.area}</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`text-[11px] font-mono font-bold block ${c.diff.startsWith('+') ? 'text-emerald-400' : 'text-amber-400'}`}>
                        {c.diff}
                      </span>
                      <span className="text-[9px] text-gray-500 block">60-day shift</span>
                    </div>
                  </button>
                );
              })}
            </div>

            <div className="p-2 bg-purple-950/30 border border-purple-900/40 rounded text-[11px] text-purple-300 flex items-start space-x-1.5">
              <Sparkles className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-purple-400" />
              <span>Click any of these 4 biomes to isolate and highlight its changes on the bottom timeline!</span>
            </div>
          </div>
        )}

        {/* OPACITY SLIDER */}
        <div className="pt-3 border-t border-gray-800 space-y-1.5">
          <div className="flex items-center justify-between text-xs text-gray-300">
            <span className="flex items-center space-x-1.5">
              <Sliders className="w-3.5 h-3.5 text-gray-400" />
              <span>Layer Opacity</span>
            </span>
            <span className="font-mono text-gray-400">{Math.round(opacity * 100)}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={opacity}
            onChange={(e) => onOpacityChange(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>

        {/* EXPORT CSV */}
        <div className="pt-2">
          <button
            onClick={onExportCSV}
            className="w-full py-2 px-3 bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-medium rounded border border-gray-700 transition flex items-center justify-center space-x-2"
          >
            <Download className="w-3.5 h-3.5 text-blue-400" />
            <span>Download Change Data (CSV)</span>
          </button>
        </div>
      </div>
    </div>
  );
};
