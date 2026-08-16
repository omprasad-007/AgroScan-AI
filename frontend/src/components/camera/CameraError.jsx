import React from 'react';
import { CameraOff, AlertTriangle, RefreshCw, Upload } from 'lucide-react';

export const CameraError = ({ errorType, message, onRetry, onFallbackUpload }) => {
  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-4 max-w-md mx-auto">
      <div className="w-14 h-14 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center mx-auto">
        {errorType === 'NotAllowedError' || errorType === 'PermissionDenied' ? (
          <CameraOff className="w-7 h-7" />
        ) : (
          <AlertTriangle className="w-7 h-7" />
        )}
      </div>

      <div className="space-y-1">
        <h3 className="text-base font-bold text-slate-100">
          {errorType === 'NotAllowedError' || errorType === 'PermissionDenied'
            ? 'Camera Access Denied'
            : 'Camera Initialization Failed'}
        </h3>
        <p className="text-xs text-slate-400 leading-relaxed">
          {message || 'Unable to access your device camera. Please grant camera permissions in your browser settings or select a file from your device.'}
        </p>
      </div>

      <div className="flex flex-col sm:flex-row gap-2 justify-center pt-2">
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 flex items-center justify-center space-x-2 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Try Camera Again</span>
          </button>
        )}
        <button
          onClick={onFallbackUpload}
          className="px-4 py-2.5 rounded-xl bg-primary hover:bg-agri-700 text-on-primary text-xs font-semibold flex items-center justify-center space-x-2 transition shadow-lg shadow-primary/20"
        >
          <Upload className="w-3.5 h-3.5" />
          <span>Upload From Device</span>
        </button>
      </div>
    </div>
  );
};
