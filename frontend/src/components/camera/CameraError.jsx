import React from 'react';
import { CameraOff, AlertTriangle, RefreshCw, Upload, Smartphone } from 'lucide-react';

export const CameraError = ({ errorType, message, onRetry, onFallbackUpload, onNativeCapture }) => {
  return (
    <div className="p-6 sm:p-8 rounded-3xl bg-agro-card border border-agro-border text-center space-y-4 max-w-md mx-auto shadow-2xl">
      <div className="w-14 h-14 rounded-2xl bg-agro-amber/15 border border-agro-amber/30 text-agro-amber flex items-center justify-center mx-auto">
        {errorType === 'NotAllowedError' || errorType === 'PermissionDenied' ? (
          <CameraOff className="w-7 h-7" aria-hidden="true" />
        ) : (
          <AlertTriangle className="w-7 h-7" aria-hidden="true" />
        )}
      </div>

      <div className="space-y-1">
        <h3 className="text-base font-bold text-agro-cream">
          {errorType === 'NotAllowedError' || errorType === 'PermissionDenied'
            ? 'Camera Permission Required'
            : 'Camera Initialization Notice'}
        </h3>
        <p className="text-xs text-agro-muted leading-relaxed">
          {message || 'Unable to open camera stream. Please check browser camera permissions or upload a leaf photo directly.'}
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-2.5 justify-center pt-2">
        {onNativeCapture && (
          <button
            type="button"
            onClick={onNativeCapture}
            className="px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-xs flex items-center justify-center gap-2 transition shadow-md shadow-agro-primary/20 active:scale-95"
          >
            <Smartphone className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Use Device Camera</span>
          </button>
        )}
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="px-4 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-xs font-semibold text-agro-cream border border-agro-border flex items-center justify-center gap-2 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Retry</span>
          </button>
        )}
        <button
          type="button"
          onClick={onFallbackUpload}
          className="px-4 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-muted hover:text-agro-cream text-xs font-semibold border border-agro-border flex items-center justify-center gap-2 transition"
        >
          <Upload className="w-3.5 h-3.5" aria-hidden="true" />
          <span>Upload Image</span>
        </button>
      </div>
    </div>
  );
};
