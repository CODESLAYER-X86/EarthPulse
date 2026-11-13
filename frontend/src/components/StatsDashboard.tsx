import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
  Legend
} from 'recharts';
import { BandStat, RegionSummaryItem, MLSummaryData, AppViewMode } from '../types';
import {
  TrendingUp,
  TrendingDown,
  Clock,
  Sparkles,
  Layers,
  ArrowRight,
  Droplets,
  Trees,
  Sun,
  Building2
} from 'lucide-react';

interface StatsDashboardProps {
  statistics: Record<string, BandStat>;
  regionSummaries: RegionSummaryItem[];
  mlSummary?: MLSummaryData | null;
  currentView?: AppViewMode;
  selectedCluster?: number | null;
  onSelectCluster?: (id: number | null) => void;
  onSelectCycle?: (cycle: string) => void;
}

const CLUSTERS = [
  {
    id: 0,
    name: 'Water & Mudflats',
    shortName: 'Water',
    color: '#3b82f6',
    icon: Droplets,
    area: '20.1% (5.0 km²)',
    hh: [-12.57, -11.32, -9.91],
    hv: [-20.01, -19.45, -18.77],
    diffs: {
      '028_032': { hh: +1.26, hv: +0.56, note: 'Tidal Inundation' },
      '032_033': { hh: +1.40, hv: +0.69, note: 'High Tidal Phase' },
      '028_033': { hh: +2.66, hv: +1.25, note: 'Net Inundation (+2.66 dB)' },
    }
  },
  {
    id: 1,
    name: 'Dense Mangroves',
    shortName: 'Mangroves',
    color: '#10b981',
    icon: Trees,
    area: '29.9% (7.5 km²)',
    hh: [-6.13, -7.88, -7.43],
    hv: [-12.26, -13.57, -13.17],
    diffs: {
      '028_032': { hh: -1.75, hv: -1.31, note: 'Canopy Drying' },
      '032_033': { hh: +0.45, hv: +0.40, note: 'Moisture Recovery' },
      '028_033': { hh: -1.30, hv: -0.91, note: 'Stable Canopy (-1.30 dB)' },
    }
  },
  {
    id: 2,
    name: 'Scrub & Marsh',
    shortName: 'Scrub',
    color: '#f59e0b',
    icon: Sun,
    area: '22.2% (5.6 km²)',
    hh: [-10.94, -11.72, -12.95],
    hv: [-21.12, -19.50, -20.31],
    diffs: {
      '028_032': { hh: -0.78, hv: +1.62, note: 'Vegetation Growth' },
      '032_033': { hh: -1.22, hv: -0.81, note: 'Surface Recession' },
      '028_033': { hh: -2.01, hv: +0.81, note: 'Dry Season Shift (-2.01 dB)' },
    }
  },
  {
    id: 3,
    name: 'Urban & Structures',
    shortName: 'Urban',
    color: '#ef4444',
    icon: Building2,
    area: '27.8% (7.0 km²)',
    hh: [-6.35, -4.69, -5.44],
    hv: [-13.15, -11.07, -11.44],
    diffs: {
      '028_032': { hh: +1.66, hv: +2.07, note: 'Corner Scattering' },
      '032_033': { hh: -0.74, hv: -0.37, note: 'Direct Reflection' },
      '028_033': { hh: +0.91, hv: +1.71, note: 'Stable Reflectors (+0.91 dB)' },
    }
  }
];

export const StatsDashboard: React.FC<StatsDashboardProps> = ({
  statistics,
  regionSummaries,
  mlSummary,
  currentView,
  selectedCluster,
  onSelectCluster,
  onSelectCycle
}) => {
  const [activePol, setActivePol] = useState<'HH' | 'HV'>('HH');
  const [activeInterval, setActiveInterval] = useState<'028_033' | '028_032' | '032_033'>('028_033');
  // Default to biomes timeline if in ML view, otherwise user can toggle
  const [viewTab, setViewTab] = useState<'biomes' | 'estuary'>(
    currentView === 'ml' ? 'biomes' : 'biomes'
  );

  // 1. 4-Element Biome Trajectory Data over the 3 epochs
  const biomeTrendData = [
    {
      date: 'Aug 22 (028)',
      cycle: '028',
      'Water & Mudflats': activePol === 'HH' ? CLUSTERS[0].hh[0] : CLUSTERS[0].hv[0],
      'Dense Mangroves': activePol === 'HH' ? CLUSTERS[1].hh[0] : CLUSTERS[1].hv[0],
      'Scrub & Marsh': activePol === 'HH' ? CLUSTERS[2].hh[0] : CLUSTERS[2].hv[0],
      'Urban & Structures': activePol === 'HH' ? CLUSTERS[3].hh[0] : CLUSTERS[3].hv[0],
    },
    {
      date: 'Oct 09 (032)',
      cycle: '032',
      'Water & Mudflats': activePol === 'HH' ? CLUSTERS[0].hh[1] : CLUSTERS[0].hv[1],
      'Dense Mangroves': activePol === 'HH' ? CLUSTERS[1].hh[1] : CLUSTERS[1].hv[1],
      'Scrub & Marsh': activePol === 'HH' ? CLUSTERS[2].hh[1] : CLUSTERS[2].hv[1],
      'Urban & Structures': activePol === 'HH' ? CLUSTERS[3].hh[1] : CLUSTERS[3].hv[1],
    },
    {
      date: 'Oct 21 (033)',
      cycle: '033',
      'Water & Mudflats': activePol === 'HH' ? CLUSTERS[0].hh[2] : CLUSTERS[0].hv[2],
      'Dense Mangroves': activePol === 'HH' ? CLUSTERS[1].hh[2] : CLUSTERS[1].hv[2],
      'Scrub & Marsh': activePol === 'HH' ? CLUSTERS[2].hh[2] : CLUSTERS[2].hv[2],
      'Urban & Structures': activePol === 'HH' ? CLUSTERS[3].hh[2] : CLUSTERS[3].hv[2],
    },
  ];

  // 2. Full Estuary Scene Progression
  const estuaryTrendData = [
    {
      date: 'Aug 22 (028)',
      cycle: '028',
      HH: statistics['hh_028_db']?.mean ? parseFloat(statistics['hh_028_db'].mean.toFixed(2)) : -8.55,
      HV: statistics['hv_028_db']?.mean ? parseFloat(statistics['hv_028_db'].mean.toFixed(2)) : -16.03,
    },
    {
      date: 'Oct 09 (032)',
      cycle: '032',
      HH: statistics['hh_032_db']?.mean ? parseFloat(statistics['hh_032_db'].mean.toFixed(2)) : -8.54,
      HV: statistics['hv_032_db']?.mean ? parseFloat(statistics['hv_032_db'].mean.toFixed(2)) : -15.37,
    },
    {
      date: 'Oct 21 (033)',
      cycle: '033',
      HH: statistics['hh_033_db']?.mean ? parseFloat(statistics['hh_033_db'].mean.toFixed(2)) : -8.60,
      HV: statistics['hv_033_db']?.mean ? parseFloat(statistics['hv_033_db'].mean.toFixed(2)) : -15.39,
    },
  ];

  // 3. Pairwise region area change distribution
  const changeDistData = regionSummaries.map((item) => ({
    name: `${item.pol} ${item.interval.replace(' (60-day)', '').replace(' (48-day)', '').replace(' (12-day)', '')}`,
    area_ha: item.total_area_ha,
    regions: item.total_regions,
    pol: item.pol
  })).filter(item => item.pol === activePol);

  const getIntervalLabel = () => {
    switch (activeInterval) {
      case '028_032': return 'Aug 22 → Oct 09 (48-Day Spring Transition)';
      case '032_033': return 'Oct 09 → Oct 21 (12-Day Rapid Repeat)';
      case '028_033': return 'Aug 22 → Oct 21 (Full 60-Day Baseline Shift)';
    }
  };

  return (
    <div
      className="bg-[#111827] border-t border-gray-800 px-6 py-2.5 flex items-center space-x-6 z-10 text-xs shrink-0 select-none"
      style={{ height: '220px', minHeight: '220px' }}
    >
      {/* ======================================================== */}
      {/* LEFT HALF: MULTI-TEMPORAL TRAJECTORY CHART (4 BIOMES)    */}
      {/* ======================================================== */}
      <div className="w-1/2 h-full flex flex-col justify-between">
        {/* Top Control Bar */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-white tracking-wide flex items-center space-x-1.5">
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span>4-Element Biome Timeline</span>
            </span>
            <span className="text-[10px] text-gray-500 font-mono">(NISAR Backscatter dB)</span>
          </div>

          <div className="flex items-center space-x-2">
            {/* Polarization Toggle */}
            <div className="flex items-center space-x-1 bg-gray-900 p-0.5 rounded border border-gray-800">
              <button
                onClick={() => setActivePol('HH')}
                className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                  activePol === 'HH' ? 'bg-blue-600 text-white font-bold' : 'text-gray-400 hover:text-white'
                }`}
                title="Co-polarization: sensitive to water surface, specular reflection & urban double-bounce"
              >
                HH Co-Pol
              </button>
              <button
                onClick={() => setActivePol('HV')}
                className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                  activePol === 'HV' ? 'bg-purple-600 text-white font-bold' : 'text-gray-400 hover:text-white'
                }`}
                title="Cross-polarization: sensitive to mangrove forest volume scattering & canopy structure"
              >
                HV Cross-Pol
              </button>
            </div>

            {/* View Switcher: 4 Biomes vs Overall */}
            <div className="flex items-center space-x-1 bg-gray-900 p-0.5 rounded border border-gray-800">
              <button
                onClick={() => setViewTab('biomes')}
                className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                  viewTab === 'biomes' ? 'bg-purple-600 text-white font-bold' : 'text-gray-400 hover:text-white'
                }`}
              >
                4 Biomes
              </button>
              <button
                onClick={() => setViewTab('estuary')}
                className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                  viewTab === 'estuary' ? 'bg-gray-700 text-white font-bold' : 'text-gray-400 hover:text-white'
                }`}
              >
                Full Scene
              </button>
            </div>
          </div>
        </div>

        {/* Chart Canvas with Explicit Height */}
        <div className="w-full relative" style={{ height: '125px', minHeight: '125px' }}>
          <ResponsiveContainer width="100%" height={125}>
            {viewTab === 'biomes' ? (
              <LineChart data={biomeTrendData} margin={{ top: 8, right: 12, left: -22, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                <XAxis dataKey="date" stroke="#6b7280" tick={{ fontSize: 10 }} />
                <YAxis
                  stroke="#6b7280"
                  domain={activePol === 'HH' ? [-16, -2] : [-24, -8]}
                  tick={{ fontSize: 10 }}
                  unit=" dB"
                />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', fontSize: '11px', borderRadius: '6px' }}
                  itemStyle={{ padding: '1px 0' }}
                />
                {CLUSTERS.map((c) => {
                  const isDimmed = selectedCluster !== null && selectedCluster !== undefined && selectedCluster !== c.id;
                  const isHighlighted = selectedCluster === c.id;
                  return (
                    <Line
                      key={c.id}
                      type="monotone"
                      dataKey={c.name}
                      stroke={c.color}
                      strokeWidth={isHighlighted ? 3.5 : isDimmed ? 1 : 2.5}
                      strokeOpacity={isDimmed ? 0.3 : 1}
                      dot={{ r: isHighlighted ? 5 : 3.5, fill: c.color }}
                      activeDot={{ r: 6 }}
                    />
                  );
                })}
              </LineChart>
            ) : (
              <LineChart data={estuaryTrendData} margin={{ top: 8, right: 12, left: -22, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
                <XAxis dataKey="date" stroke="#6b7280" tick={{ fontSize: 10 }} />
                <YAxis stroke="#6b7280" domain={[-20, -4]} tick={{ fontSize: 10 }} unit=" dB" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', fontSize: '11px', borderRadius: '6px' }}
                />
                <Line type="monotone" dataKey="HH" stroke="#38bdf8" strokeWidth={2.5} dot={{ r: 4 }} name="Mean Scene HH" />
                <Line type="monotone" dataKey="HV" stroke="#a855f7" strokeWidth={2.5} dot={{ r: 4 }} name="Mean Scene HV" />
              </LineChart>
            )}
          </ResponsiveContainer>
        </div>

        {/* Biome Filter Buttons / Legend */}
        <div className="flex items-center justify-between text-[10px]">
          <div className="flex items-center space-x-1.5">
            <button
              onClick={() => onSelectCluster && onSelectCluster(null)}
              className={`px-1.5 py-0.5 rounded border transition ${
                selectedCluster === null || selectedCluster === undefined
                  ? 'border-purple-500 bg-purple-950/60 text-purple-200 font-bold'
                  : 'border-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              All 4
            </button>
            {CLUSTERS.map((c) => (
              <button
                key={c.id}
                onClick={() => onSelectCluster && onSelectCluster(selectedCluster === c.id ? null : c.id)}
                className={`px-1.5 py-0.5 rounded border flex items-center space-x-1 transition ${
                  selectedCluster === c.id
                    ? 'border-white text-white font-bold shadow'
                    : 'border-gray-800 text-gray-400 hover:text-white'
                }`}
                style={{
                  backgroundColor: selectedCluster === c.id ? `${c.color}33` : 'transparent'
                }}
              >
                <span className="w-2 h-2 rounded-full inline-block" style={{ backgroundColor: c.color }} />
                <span>{c.shortName}</span>
              </button>
            ))}
          </div>

          <span className="text-gray-500 truncate text-[10px]">
            {activePol === 'HH'
              ? 'HH co-pol tracks specular water and urban double-bounce'
              : 'HV cross-pol tracks mangrove canopy volume scattering'}
          </span>
        </div>
      </div>

      <div className="w-px h-44 bg-gray-800" />

      {/* ======================================================== */}
      {/* RIGHT HALF: 4-ELEMENT TEMPORAL CHANGE TIMELINE & DELTAS  */}
      {/* ======================================================== */}
      <div className="w-1/2 h-full flex flex-col justify-between">
        {/* Timeline Top Bar with Interval Buttons */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-1.5">
            <Clock className="w-3.5 h-3.5 text-blue-400" />
            <span className="font-semibold text-white tracking-wide">Temporal Changes in 4 Biomes</span>
            <span className="text-[10px] text-gray-500 font-mono">(Δ dB Shift)</span>
          </div>

          {/* Timeline Step Selectors */}
          <div className="flex items-center space-x-1 bg-gray-900 p-0.5 rounded border border-gray-800">
            <button
              onClick={() => setActiveInterval('028_032')}
              className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                activeInterval === '028_032' ? 'bg-blue-600 text-white font-bold' : 'text-gray-400 hover:text-white'
              }`}
              title="August 22 to October 09 (48 days)"
            >
              Step 1 (48d)
            </button>
            <button
              onClick={() => setActiveInterval('032_033')}
              className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                activeInterval === '032_033' ? 'bg-blue-600 text-white font-bold' : 'text-gray-400 hover:text-white'
              }`}
              title="October 09 to October 21 (12 days repeat)"
            >
              Step 2 (12d)
            </button>
            <button
              onClick={() => setActiveInterval('028_033')}
              className={`px-2 py-0.5 text-[10px] font-medium rounded transition ${
                activeInterval === '028_033' ? 'bg-emerald-600 text-white font-bold' : 'text-gray-400 hover:text-white'
              }`}
              title="August 22 to October 21 (Full 60-day baseline)"
            >
              Full (60d)
            </button>
          </div>
        </div>

        {/* Visual Timeline Track */}
        <div className="w-full bg-gray-900/80 border border-gray-800 rounded px-3 py-1.5 flex items-center justify-between text-[11px]">
          <div
            onClick={() => onSelectCycle && onSelectCycle('028')}
            className={`flex items-center space-x-1 cursor-pointer transition ${
              activeInterval === '028_032' || activeInterval === '028_033' ? 'text-blue-400 font-bold' : 'text-gray-400'
            }`}
          >
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
            <span>Aug 22 (028)</span>
          </div>

          <div className="flex-1 mx-2 flex items-center justify-center relative">
            <div className="w-full h-0.5 bg-gray-700" />
            <span className="absolute bg-[#111827] px-2 py-0.5 border border-gray-700 rounded text-[9px] font-mono text-gray-300">
              {getIntervalLabel()}
            </span>
          </div>

          <div
            onClick={() => onSelectCycle && onSelectCycle('033')}
            className={`flex items-center space-x-1 cursor-pointer transition ${
              activeInterval === '032_033' || activeInterval === '028_033' ? 'text-emerald-400 font-bold' : 'text-gray-400'
            }`}
          >
            <span>Oct 21 (033)</span>
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
          </div>
        </div>

        {/* 4 Element Change Cards Grid */}
        <div className="grid grid-cols-4 gap-2">
          {CLUSTERS.map((c) => {
            const diffObj = c.diffs[activeInterval];
            const diffVal = activePol === 'HH' ? diffObj.hh : diffObj.hv;
            const isPositive = diffVal > 0;
            const isSelected = selectedCluster === c.id;

            return (
              <div
                key={c.id}
                onClick={() => onSelectCluster && onSelectCluster(selectedCluster === c.id ? null : c.id)}
                className={`p-2 rounded border transition cursor-pointer flex flex-col justify-between ${
                  isSelected
                    ? 'border-white bg-gray-800/90 shadow-md ring-1 ring-white/50'
                    : 'border-gray-800 bg-gray-900/70 hover:bg-gray-850 hover:border-gray-700'
                }`}
                style={{
                  borderTop: `3px solid ${c.color}`
                }}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-gray-200 truncate">{c.shortName}</span>
                  <c.icon className="w-3 h-3 text-gray-400" />
                </div>

                <div className="my-1 flex items-baseline space-x-1">
                  <span
                    className={`text-sm font-extrabold font-mono ${
                      isPositive ? 'text-emerald-400' : 'text-amber-400'
                    }`}
                  >
                    {isPositive ? `+${diffVal.toFixed(2)}` : diffVal.toFixed(2)}
                  </span>
                  <span className="text-[9px] text-gray-500 font-mono">dB</span>
                </div>

                <div className="flex items-center space-x-1 text-[9px] text-gray-400 truncate">
                  {isPositive ? (
                    <TrendingUp className="w-2.5 h-2.5 text-emerald-400 flex-shrink-0" />
                  ) : (
                    <TrendingDown className="w-2.5 h-2.5 text-amber-400 flex-shrink-0" />
                  )}
                  <span className="truncate">{diffObj.note}</span>
                </div>
              </div>
            );
          })}
        </div>

        <p className="text-[10px] text-gray-500 truncate flex items-center space-x-1.5">
          <span>Click any of the 4 elements above or in the left sidebar to isolate its timeline trajectory.</span>
        </p>
      </div>
    </div>
  );
};