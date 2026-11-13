import React from 'react';
import { Layers, Activity, FileText, Info } from 'lucide-react';

interface HeaderProps {
  onOpenReports: () => void;
  onOpenInfo: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenReports, onOpenInfo }) => {
  return (
    <header className="h-14 bg-[#111827] border-b border-gray-800 px-6 flex items-center justify-between z-20">
      <div className="flex items-center space-x-3">
        <div className="flex items-center justify-center w-8 h-8 rounded bg-gradient-to-tr from-blue-600 to-indigo-500 font-bold text-white tracking-widest text-sm shadow">
          SAR
        </div>
        <div>
          <h1 className="text-sm font-semibold text-white tracking-wide flex items-center space-x-2">
            <span>Dancing with SARs</span>
            <span className="text-xs font-normal px-2 py-0.5 bg-blue-900/60 text-blue-300 border border-blue-700/50 rounded-full">
              NISAR L2 GCOV
            </span>
          </h1>
          <p className="text-[11px] text-gray-400">Potengi Estuary Multi-Temporal Radar Analysis • Natal, Brazil</p>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={onOpenReports}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-medium rounded border border-gray-700 transition"
        >
          <FileText className="w-3.5 h-3.5 text-blue-400" />
          <span>Scientific Reports</span>
        </button>

        <button
          onClick={onOpenInfo}
          className="flex items-center space-x-1.5 px-3 py-1.5 bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-medium rounded border border-gray-700 transition"
        >
          <Info className="w-3.5 h-3.5 text-cyan-400" />
          <span>About Project</span>
        </button>
      </div>
    </header>
  );
};
