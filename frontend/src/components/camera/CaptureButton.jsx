import React from 'react';
import { Camera, SwitchCamera, X } from 'lucide-react';

export const CaptureButton = ({ onCapture, onSwitchCamera, onClose, canSwitch }) => {
  return (
    <div className="absolute bottom-6 left-0 right-0 px-6 flex items-center justify-between z-20 pointer-events-auto">
      {/* Switch Camera Button */}
      <button
        type="button"
        onClick={onSwitchCamera}
        disabled={!canSwitch}
        title="Switch Camera (Front/Rear)"
        className="w-12 h-12 rounded-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-slate-200 flex items-center justify-center hover:bg-slate-800 transition active:scale-95 disabled:opacity-40"
      >
        <SwitchCamera className="w-5 h-5" />
      </button>

      {/* Main Shutter Capture Button */}
      <button
        type="button"
        onClick={onCapture}
        title="Capture Leaf Photo"
        className="relative group p-1.5 rounded-full bg-white/20 backdrop-blur-md border-2 border-white/80 transition active:scale-90"
      >
        <div className="w-16 h-16 rounded-full bg-emerald-500 hover:bg-emerald-400 text-white flex items-center justify-center shadow-lg shadow-emerald-500/40 group-hover:scale-105 transition duration-200">
          <Camera className="w-7 h-7" />
        </div>
        <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500"></span>
        </span>
      </button>

      {/* Close Camera Button */}
      <button
        type="button"
        onClick={onClose}
        title="Close Camera"
        className="w-12 h-12 rounded-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-slate-200 flex items-center justify-center hover:bg-red-500/20 hover:text-red-400 hover:border-red-500/40 transition active:scale-95"
      >
        <X className="w-5 h-5" />
      </button>
    </div>
  );
};
