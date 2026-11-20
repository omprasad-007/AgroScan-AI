import React from 'react';
import { CaptureButton } from './CaptureButton';
import { useLanguage } from '../../context/LanguageContext';

export const CameraPreview = ({
  videoRef,
  onCapture,
  onSwitchCamera,
  onClose,
  canSwitch,
  facingMode
}) => {
  const { t } = useLanguage();

  return (
    <div className="relative w-full h-[450px] sm:h-[520px] bg-black rounded-3xl overflow-hidden shadow-2xl border border-agro-border flex flex-col justify-between">
      {/* Live Video Feed */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Leaf Scanning Viewfinder Overlay */}
      <div className="absolute inset-0 pointer-events-none flex flex-col items-center justify-center p-6 bg-gradient-to-b from-black/70 via-transparent to-black/80">
        
        {/* Top Visual Guidance Banner */}
        <div className="mb-auto mt-4 px-4 py-2 rounded-full bg-agro-card/90 backdrop-blur-md border border-agro-border text-xs font-semibold text-agro-lime flex items-center space-x-2 shadow-lg">
          <span className="w-2 h-2 rounded-full bg-agro-primary animate-ping"></span>
          <span>{t('scan.camera_leaf_guide') || 'Frame one affected leaf clearly • Ensure daylight or good lighting'}</span>
        </div>

        {/* Scanning Box Viewfinder */}
        <div className="relative w-64 h-64 sm:w-72 sm:h-72 rounded-3xl border-2 border-dashed border-agro-primary/70 shadow-[0_0_30px_rgba(16,185,129,0.3)] flex items-center justify-center">
          {/* Corner Guides */}
          <div className="absolute -top-1 -left-1 w-6 h-6 border-t-4 border-l-4 border-agro-lime rounded-tl-lg"></div>
          <div className="absolute -top-1 -right-1 w-6 h-6 border-t-4 border-r-4 border-agro-lime rounded-tr-lg"></div>
          <div className="absolute -bottom-1 -left-1 w-6 h-6 border-b-4 border-l-4 border-agro-lime rounded-bl-lg"></div>
          <div className="absolute -bottom-1 -right-1 w-6 h-6 border-b-4 border-r-4 border-agro-lime rounded-br-lg"></div>

          {/* Animated Laser Scanning Line */}
          <div className="w-full h-0.5 bg-gradient-to-r from-transparent via-agro-primary to-transparent shadow-[0_0_12px_#10B981] animate-laser"></div>
        </div>

        {/* Bottom Mode Indicator */}
        <div className="mt-auto mb-20 text-[11px] text-agro-muted font-medium tracking-wide uppercase">
          Camera: {facingMode === 'environment' ? 'Rear / Main' : 'Front / Selfie'}
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
