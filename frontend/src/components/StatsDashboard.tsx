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
import { BandStat, RegionSummaryItem } from '../types';
import { Info, HelpCircle } from 'lucide-react';

interface StatsDashboardProps {
  statistics: Record<string, BandStat>;
  regionSummaries: RegionSummaryItem[];
}

export const StatsDashboard: React.FC<StatsDashboardProps> = ({ statistics, regionSummaries }) => {
  const [activePol, setActivePol] = useState<'HH' | 'HV'>('HH');

  // Multi-temporal backscatter progression
  const trendData = [
    {
      date: 'Aug 22 (028)',
      HH: statistics['hh_028_db']?.mean ? parseFloat(statistics['hh_028_db'].mean.toFixed(2)) : -8.55,
      HH_std: statistics['hh_028_db']?.std ? parseFloat(statistics['hh_028_db'].std.toFixed(2)) : 4.00,
      HV: statistics['hv_028_db']?.mean ? parseFloat(statistics['hv_028_db'].mean.toFixed(2)) : -16.03,
      HV_std: statistics['hv_028_db']?.std ? parseFloat(statistics['hv_028_db'].std.toFixed(2)) : 4.97,
    },
    {
      date: 'Oct 09 (032)',
      HH: statistics['hh_032_db']?.mean ? parseFloat(statistics['hh_032_db'].mean.toFixed(2)) : -8.54,
      HH_std: statistics['hh_032_db']?.std ? parseFloat(statistics['hh_032_db'].std.toFixed(2)) : 4.01,
      HV: statistics['hv_032_db']?.mean ? parseFloat(statistics['hv_032_db'].mean.toFixed(2)) : -15.37,
      HV_std: statistics['hv_032_db']?.std ? parseFloat(statistics['hv_032_db'].std.toFixed(2)) : 4.71,
    },
    {
      date: 'Oct 21 (033)',
      HH: statistics['hh_033_db']?.mean ? parseFloat(statistics['hh_033_db'].mean.toFixed(2)) : -8.60,
      HH_std: statistics['hh_033_db']?.std ? parseFloat(statistics['hh_033_db'].std.toFixed(2)) : 4.00,
      HV: statistics['hv_033_db']?.mean ? parseFloat(statistics['hv_033_db'].mean.toFixed(2)) : -15.39,
      HV_std: statistics['hv_033_db']?.std ? parseFloat(statistics['hv_033_db'].std.toFixed(2)) : 4.78,
    },
  ];

  // Pairwise change distribution data
  const changeDistData = regionSummaries.map((item) => ({
    name: `${item.pol} ${item.interval.replace(' (60-day)', '').replace(' (48-day)', '').replace(' (12-day)', '')}`,
    area_ha: item.total_area_ha,
    regions: item.total_regions,
    decreases: item.significant_decreases,
    increases: item.significant_increases,
    pol: item.pol
  })).filter(item => item.pol === activePol);

  return (
    <div className="h-50 bg-[#111827] border-t border-gray-800 px-6 py-2.5 flex items-center space-x-6 z-10 text-xs">
      {/* Chart 1: Temporal Progression with Explanation */}
      <div className="w-1/2 h-full flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-white tracking-wide">Multi-Temporal Backscatter Trajectory</span>
            <span className="text-[10px] text-gray-500 font-mono">(Unit: dB)</span>
          </div>
          <div className="flex items-center space-x-1.5 text-[10px]">
            <span className="text-gray-400">Canopy stability:</span>
            <span className="font-mono text-emerald-400 font-bold">|Δ| &lt; 0.4 dB</span>
          </div>
        </div>

        <div className="w-full h-34">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
              <XAxis dataKey="date" stroke="#6b7280" tick={{ fontSize: 10 }} />
              <YAxis stroke="#6b7280" domain={[-22, -4]} tick={{ fontSize: 10 }} unit=" dB" />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', fontSize: '11px' }}
                itemStyle={{ color: '#f3f4f6' }}
              />
              <Line type="monotone" dataKey="HH" stroke="#38bdf8" strokeWidth={2.5} dot={{ r: 4 }} name="HH Co-Pol (Surface / Specular)" />
              <Line type="monotone" dataKey="HV" stroke="#a855f7" strokeWidth={2.5} dot={{ r: 4 }} name="HV Cross-Pol (Volume / Canopy)" />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <p className="text-[10px] text-gray-500 truncate">
          Cross-polarization (HV) tracks dense mangrove volume scattering; co-polarization (HH) responds to tidal inundation and urban structures.
        </p>
      </div>

      <div className="w-px h-38 bg-gray-800" />

      {/* Chart 2: Extracted Environmental Change Regions Area */}
      <div className="w-1/2 h-full flex flex-col justify-between">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="font-semibold text-white tracking-wide">Detected Coherent Change Area</span>
            <span className="text-[10px] text-gray-500 font-mono">(Unit: Hectares)</span>
          </div>

          {/* Polarization switch */}
          <div className="flex items-center space-x-1 bg-gray-900 p-0.5 rounded border border-gray-800">
            <button
              onClick={() => setActivePol('HH')}
              className={`px-2 py-0.5 text-[10px] font-medium rounded ${
                activePol === 'HH' ? 'bg-blue-600 text-white font-bold' : 'text-gray-400 hover:text-white'
              }`}
            >
              HH Pol
            </button>
            <button
              onClick={() => setActivePol('HV')}
              className={`px-2 py-0.5 text-[10px] font-medium rounded ${
                activePol === 'HV' ? 'bg-purple-600 text-white font-bold' : 'text-gray-400 hover:text-white'
              }`}
            >
              HV Pol
            </button>
          </div>
        </div>

        <div className="w-full h-34">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={changeDistData} margin={{ top: 5, right: 10, left: -15, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
              <XAxis dataKey="name" stroke="#6b7280" tick={{ fontSize: 9 }} />
              <YAxis stroke="#6b7280" tick={{ fontSize: 10 }} unit=" ha" />
              <Tooltip
                contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', fontSize: '11px' }}
                itemStyle={{ color: '#f3f4f6' }}
              />
              <Bar dataKey="area_ha" fill="#06b6d4" name="Change Area (ha)" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-[10px] text-gray-500 truncate">
          Spatially coherent regions (MMU ≥ 1,500 m²) with statistically significant changes (|Δ| &gt; 1.25 dB) isolated from speckle noise.
        </p>
      </div>
    </div>
  );
};
