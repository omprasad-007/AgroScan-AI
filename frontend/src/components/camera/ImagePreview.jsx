import React from 'react';
import { RotateCcw, Sparkles, CheckCircle2 } from 'lucide-react';

export const ImagePreview = ({ imageUrl, onRetake, onUsePhoto, isScanning }) => {
  return (
    <div className="space-y-6">
      <div className="agro-panel p-6 sm:p-8 rounded-3xl border border-agro-border text-center space-y-5">
        <div className="relative max-w-sm mx-auto rounded-2xl overflow-hidden shadow-2xl border border-agro-primary/40 bg-agro-bg">
          <img
            src={imageUrl}
            alt="Captured Leaf Preview"
            className="w-full h-72 object-cover"
          />
          <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-agro-card/90 backdrop-blur-md border border-agro-primary/40 text-[11px] font-bold text-agro-primary flex items-center gap-1.5 shadow">
            <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Ready for Analysis</span>
          </div>
        </div>

        <p className="text-xs text-agro-muted max-w-md mx-auto">
          Leaf photo captured successfully. Verify the leaf is in focus before proceeding to diagnosis.
        </p>

        {/* Control Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
          <button
            type="button"
            onClick={onRetake}
            disabled={isScanning}
            className="px-5 py-3 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-xs font-bold border border-agro-border flex items-center justify-center gap-2 transition disabled:opacity-50"
          >
            <RotateCcw className="w-4 h-4 text-agro-muted" aria-hidden="true" />
            <span>Retake Photo</span>
          </button>

          <button
            type="button"
            onClick={onUsePhoto}
            disabled={isScanning}
            className="px-7 py-3 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-agro-bg text-xs font-extrabold flex items-center justify-center gap-2 transition shadow-lg shadow-agro-primary/25 disabled:opacity-50 active:scale-[0.98]"
          >
            <Sparkles className="w-4 h-4" aria-hidden="true" />
            <span>{isScanning ? 'Diagnosing...' : 'Start Disease Diagnosis'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
