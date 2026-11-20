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
        aria-label="Switch Camera (Front or Rear)"
        className="w-12 h-12 rounded-2xl bg-agro-card/90 backdrop-blur-md border border-agro-border text-agro-cream flex items-center justify-center hover:bg-agro-surface transition active:scale-95 disabled:opacity-30"
      >
        <SwitchCamera className="w-5 h-5 text-agro-lime" aria-hidden="true" />
      </button>

      {/* Main Shutter Capture Button */}
      <button
        type="button"
        onClick={onCapture}
        title="Capture Leaf Photo"
        aria-label="Capture Leaf Photo"
        className="relative group p-1.5 rounded-full bg-agro-primary/20 backdrop-blur-md border-2 border-agro-primary transition active:scale-90"
      >
        <div className="w-16 h-16 rounded-full bg-agro-primary hover:bg-agro-primaryHover text-white flex items-center justify-center shadow-lg shadow-agro-primary/40 group-hover:scale-105 transition duration-150">
          <Camera className="w-7 h-7" aria-hidden="true" />
        </div>
        <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-agro-lime opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-agro-primary"></span>
        </span>
      </button>

      {/* Close Camera Button */}
      <button
        type="button"
        onClick={onClose}
        title="Close Camera"
        aria-label="Close Camera"
        className="w-12 h-12 rounded-2xl bg-agro-card/90 backdrop-blur-md border border-agro-border text-agro-muted flex items-center justify-center hover:bg-agro-terracotta/20 hover:text-agro-terracotta hover:border-agro-terracotta/40 transition active:scale-95"
      >
        <X className="w-5 h-5" aria-hidden="true" />
      </button>
    </div>
  );
};
