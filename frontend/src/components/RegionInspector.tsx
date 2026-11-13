import React from 'react';
import { X, ShieldAlert, ArrowUpRight, ArrowDownRight, Info, MapPin } from 'lucide-react';
import { ChangeRegionProperties } from '../types';

interface RegionInspectorProps {
  region: ChangeRegionProperties | null;
  onClose: () => void;
}

export const RegionInspector: React.FC<RegionInspectorProps> = ({ region, onClose }) => {
  if (!region) return null;

  const isDecrease = region.mean_diff_db < 0;

  return (
    <div className="absolute top-4 right-4 z-30 w-84 bg-[#111827]/95 backdrop-blur-md border border-gray-700 rounded-lg shadow-2xl p-4 text-xs text-gray-200 animate-in fade-in slide-in-from-top-2">
      <div className="flex items-center justify-between pb-2 border-b border-gray-800">
        <div className="flex items-center space-x-2">
          <MapPin className="w-4 h-4 text-blue-400" />
          <span className="font-semibold text-white tracking-wide">{region.id}</span>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-gray-800 text-gray-400 hover:text-white transition"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="mt-3 space-y-2.5">
        {/* Category & Change Magnitude */}
        <div className="flex items-center justify-between bg-gray-900/80 p-2.5 rounded border border-gray-800">
          <span className="text-gray-400 font-medium">Observed Shift</span>
          <div className="flex items-center space-x-1.5 font-mono font-bold">
            {isDecrease ? (
              <span className="text-rose-400 flex items-center">
                <ArrowDownRight className="w-4 h-4 mr-0.5" />
                {region.mean_diff_db} dB
              </span>
            ) : (
              <span className="text-emerald-400 flex items-center">
                <ArrowUpRight className="w-4 h-4 mr-0.5" />
                +{region.mean_diff_db} dB
              </span>
            )}
          </div>
        </div>

        {/* Region Attributes Grid */}
        <div className="grid grid-cols-2 gap-2 text-[11px]">
          <div className="p-2 bg-gray-900/50 rounded border border-gray-800">
            <span className="text-gray-500 block">Category</span>
            <span className="font-semibold text-gray-200">{region.category}</span>
          </div>
          <div className="p-2 bg-gray-900/50 rounded border border-gray-800">
            <span className="text-gray-500 block">Area</span>
            <span className="font-semibold text-gray-200">{region.area_ha} ha ({region.pixel_count * 100} m²)</span>
          </div>
          <div className="p-2 bg-gray-900/50 rounded border border-gray-800">
            <span className="text-gray-500 block">Interval</span>
            <span className="font-semibold text-gray-200">{region.interval}</span>
          </div>
          <div className="p-2 bg-gray-900/50 rounded border border-gray-800">
            <span className="text-gray-500 block">Confidence</span>
            <span className="font-semibold text-cyan-400">{region.confidence}</span>
          </div>
        </div>

        {/* Scientific Interpretation */}
        <div className="p-2.5 bg-blue-950/40 border border-blue-900/50 rounded">
          <span className="text-blue-300 font-semibold block mb-1 flex items-center">
            <Info className="w-3.5 h-3.5 mr-1" />
            Interpretation Hypothesis
          </span>
          <p className="text-gray-300 leading-relaxed text-[11px]">{region.interpretation}</p>
        </div>

        {/* Limitations Notice */}
        <div className="p-2 bg-amber-950/20 border border-amber-900/30 rounded text-[10px] text-amber-200/80 leading-normal flex items-start space-x-1.5">
          <ShieldAlert className="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-amber-400" />
          <span>{region.limitations}</span>
        </div>
      </div>
    </div>
  );
};
