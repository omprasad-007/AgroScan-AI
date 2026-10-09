import React from 'react';
import { CameraOff, AlertTriangle, RefreshCw, Upload, Camera } from 'lucide-react';

export const CameraError = ({ errorType, message, onRetry, onFallbackUpload, onNativeCapture }) => {
  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-4 max-w-md mx-auto shadow-2xl">
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

      <div className="flex flex-col sm:flex-row gap-2.5 justify-center pt-2">
        {onNativeCapture && (
          <button
            type="button"
            onClick={onNativeCapture}
            className="px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs flex items-center justify-center space-x-2 transition shadow-lg shadow-emerald-500/20"
          >
            <Camera className="w-3.5 h-3.5" />
            <span>Use Phone Camera</span>
          </button>
        )}
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 flex items-center justify-center space-x-2 transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Try Again</span>
          </button>
        )}
        <button
          type="button"
          onClick={onFallbackUpload}
          className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 flex items-center justify-center space-x-2 transition"
        >
          <Upload className="w-3.5 h-3.5" />
          <span>Upload Image</span>
        </button>
      </div>
    </div>
  );
};
