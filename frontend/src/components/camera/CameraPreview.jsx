import React from 'react';
import { CaptureButton } from './CaptureButton';

export const CameraPreview = ({
  videoRef,
  onCapture,
  onSwitchCamera,
  onClose,
  canSwitch,
  facingMode
}) => {
  return (
    <div className="relative w-full h-[450px] sm:h-[520px] bg-black rounded-2xl overflow-hidden shadow-2xl border border-slate-800 flex flex-col justify-between">
      {/* Live Video Feed */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Leaf Scanning Viewfinder Overlay */}
      <div className="absolute inset-0 pointer-events-none flex flex-col items-center justify-center p-6 bg-gradient-to-b from-black/60 via-transparent to-black/70">
        
        {/* Top Visual Guidance Banner */}
        <div className="mb-auto mt-4 px-4 py-2 rounded-full bg-slate-900/80 backdrop-blur-md border border-slate-700/60 text-xs font-semibold text-emerald-400 flex items-center space-x-2 shadow-lg">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          <span>Place the affected leaf inside the frame</span>
        </div>

        {/* Scanning Box Viewfinder */}
        <div className="relative w-64 h-64 sm:w-72 sm:h-72 rounded-3xl border-2 border-dashed border-emerald-400/80 shadow-[0_0_30px_rgba(52,211,153,0.25)] flex items-center justify-center">
          {/* Corner Guides */}
          <div className="absolute -top-1 -left-1 w-6 h-6 border-t-4 border-l-4 border-emerald-400 rounded-tl-lg"></div>
          <div className="absolute -top-1 -right-1 w-6 h-6 border-t-4 border-r-4 border-emerald-400 rounded-tr-lg"></div>
          <div className="absolute -bottom-1 -left-1 w-6 h-6 border-b-4 border-l-4 border-emerald-400 rounded-bl-lg"></div>
          <div className="absolute -bottom-1 -right-1 w-6 h-6 border-b-4 border-r-4 border-emerald-400 rounded-br-lg"></div>

          {/* Animated Laser Scanning Line */}
          <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_12px_#34d399] animate-bounce"></div>
        </div>

        {/* Bottom Mode Indicator */}
        <div className="mt-auto mb-20 text-[11px] text-slate-300 font-medium tracking-wide uppercase">
          Camera: {facingMode === 'environment' ? 'Rear (Environment)' : 'Front (Selfie)'}
        </div>
      </div>

      {/* Camera Controls Bar */}
      <CaptureButton
        onCapture={onCapture}
        onSwitchCamera={onSwitchCamera}
        onClose={onClose}
        canSwitch={canSwitch}
      />
    </div>
  );
};
