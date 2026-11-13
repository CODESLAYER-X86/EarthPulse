import React, { useEffect, useState } from 'react';
import { Play, Pause, Zap, SkipForward, SkipBack, Clock } from 'lucide-react';

interface TimeLapsePlayerProps {
  currentCycle: string; // '028' | '032' | '033'
  onSelectCycle: (cycle: string) => void;
  isPlaying: boolean;
  onTogglePlay: () => void;
  isBlinking: boolean;
  onToggleBlink: () => void;
  pol: 'HH' | 'HV';
  onTogglePol: (pol: 'HH' | 'HV') => void;
}

export const TimeLapsePlayer: React.FC<TimeLapsePlayerProps> = ({
  currentCycle,
  onSelectCycle,
  isPlaying,
  onTogglePlay,
  isBlinking,
  onToggleBlink,
  pol,
  onTogglePol,
}) => {
  const cycles = [
    { id: '028', date: 'Aug 22, 2026', label: 'Cycle 028 (Baseline)' },
    { id: '032', date: 'Oct 09, 2026', label: 'Cycle 032 (+48 Days)' },
    { id: '033', date: 'Oct 21, 2026', label: 'Cycle 033 (+60 Days)' },
  ];

  return (
    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-30 bg-[#111827]/95 backdrop-blur-md border border-gray-700 px-4 py-2.5 rounded-full shadow-2xl flex items-center space-x-4 animate-in fade-in slide-in-from-bottom-3">
      {/* Play / Pause Time-Lapse */}
      <button
        onClick={onTogglePlay}
        className={`px-3 py-1.5 rounded-full text-xs font-bold flex items-center space-x-1.5 transition shadow ${
          isPlaying
            ? 'bg-amber-600 text-white hover:bg-amber-500'
            : 'bg-blue-600 text-white hover:bg-blue-500'
        }`}
      >
        {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
        <span>{isPlaying ? 'Pause Dance' : 'Play SAR Dance'}</span>
      </button>

      {/* A/B Blink Button */}
      <button
        onClick={onToggleBlink}
        className={`px-3 py-1.5 rounded-full text-xs font-semibold flex items-center space-x-1 transition border ${
          isBlinking
            ? 'bg-emerald-600 border-emerald-400 text-white shadow-lg animate-pulse'
            : 'bg-gray-800 border-gray-700 text-gray-300 hover:text-white hover:bg-gray-700'
        }`}
        title="Flicker rapidly between August and October so changes flash to your eyes"
      >
        <Zap className="w-3.5 h-3.5 text-yellow-400" />
        <span>{isBlinking ? 'Blinking A/B' : 'Blink Compare'}</span>
      </button>

      {/* Date Stepper Pills */}
      <div className="flex items-center space-x-1 bg-gray-900/90 p-1 rounded-full border border-gray-800">
        {cycles.map((c) => (
          <button
            key={c.id}
            onClick={() => {
              if (isPlaying) onTogglePlay();
              if (isBlinking) onToggleBlink();
              onSelectCycle(c.id);
            }}
            className={`px-3 py-1 rounded-full text-xs transition font-medium ${
              currentCycle === c.id
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold shadow'
                : 'text-gray-400 hover:text-gray-200'
            }`}
          >
            {c.date}
          </button>
        ))}
      </div>

      {/* Polarization Switcher */}
      <div className="flex items-center space-x-1 bg-gray-900/90 p-1 rounded-full border border-gray-800 text-[11px]">
        <button
          onClick={() => onTogglePol('HH')}
          className={`px-2.5 py-0.5 rounded-full font-bold transition ${
            pol === 'HH' ? 'bg-cyan-600 text-white' : 'text-gray-400 hover:text-white'
          }`}
        >
          HH
        </button>
        <button
          onClick={() => onTogglePol('HV')}
          className={`px-2.5 py-0.5 rounded-full font-bold transition ${
            pol === 'HV' ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white'
          }`}
        >
          HV
        </button>
      </div>
    </div>
  );
};
