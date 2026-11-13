import React from 'react';
import { X, Satellite, ShieldCheck, Database, Award } from 'lucide-react';

interface AboutModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-6">
      <div className="bg-[#111827] border border-gray-800 rounded-lg w-full max-w-2xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="h-14 border-b border-gray-800 px-6 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Award className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-semibold text-white">About Dancing with SARs</h2>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-gray-800 text-gray-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 overflow-y-auto space-y-5 text-xs text-gray-300 leading-relaxed">
          <div className="p-3.5 bg-blue-950/40 border border-blue-800/40 rounded-lg flex items-start space-x-3">
            <Satellite className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-200">NASA Space Apps Challenge 2026</h3>
              <p className="mt-1 text-gray-400">
                Interactive multi-temporal analysis platform utilizing NASA-ISRO Synthetic Aperture Radar (NISAR) L2 GCOV observations over the Potengi Estuary, Natal, Brazil.
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-white flex items-center space-x-1.5">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>Three-Date Repeat Observations</span>
            </h4>
            <ul className="list-disc pl-5 space-y-1 text-gray-300">
              <li><strong>Cycle 028:</strong> 2026-08-22 (Descending track, 92 km swath)</li>
              <li><strong>Cycle 032:</strong> 2026-10-09 (48 days post-baseline)</li>
              <li><strong>Cycle 033:</strong> 2026-10-21 (Exact 12-day repeat orbit)</li>
              <li><strong>Polarizations:</strong> Dual-polarization Frequency A (HH and HV backscatter power)</li>
            </ul>
          </div>

          <div className="space-y-2">
            <h4 className="text-sm font-semibold text-white flex items-center space-x-1.5">
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              <span>Scientific Integrity & Transparency</span>
            </h4>
            <p className="text-gray-400">
              Radar backscatter fluctuates with surface roughness, tidal flooding, canopy moisture, and soil conditions. This application displays verified physical decibel measurements and unsupervised ML clusters without asserting unverified ecological claims.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
