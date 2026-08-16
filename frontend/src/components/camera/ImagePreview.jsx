import React, { useState } from 'react';
import { RotateCcw, Sparkles, CheckCircle, ArrowRight } from 'lucide-react';

export const ImagePreview = ({ imageUrl, onRetake, onUsePhoto, isScanning }) => {
  const steps = [
    { label: "Uploading image", desc: "Transferring binary payload safely..." },
    { label: "Checking image", desc: "Evaluating resolution, lighting & blur..." },
    { label: "Identifying plant", desc: "Recognizing botanical species..." },
    { label: "Detecting disease", desc: "Scanning for leaf pathogens & lesions..." },
    { label: "Assessing severity", desc: "Estimating affected tissue percentage..." },
    { label: "Loading plant information", desc: "Fetching cultivation & care data..." },
    { label: "Checking weather", desc: "Evaluating humidity & outbreak risk..." },
    { label: "Preparing recommendations", desc: "Structuring treatment guidance..." },
    { label: "Complete", desc: "Generating final diagnostic report..." }
  ];

  const [activeStepIdx, setActiveStepIdx] = useState(0);

  const handleScanClick = () => {
    // Progress through steps visually before triggering parent handler
    let step = 0;
    const interval = setInterval(() => {
      step += 1;
      if (step < steps.length) {
        setActiveStepIdx(step);
      } else {
        clearInterval(interval);
      }
    }, 600);

    onUsePhoto();
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 text-center space-y-4">
        <div className="relative max-w-sm mx-auto rounded-xl overflow-hidden shadow-2xl border border-emerald-500/30">
          <img
            src={imageUrl}
            alt="Captured Leaf Preview"
            className="w-full h-64 object-cover"
          />
          <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-slate-900/80 backdrop-blur-md border border-emerald-400/40 text-[11px] font-bold text-emerald-400 flex items-center space-x-1.5 shadow">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Captured</span>
          </div>
        </div>

        <p className="text-xs text-slate-400">
          Leaf photo captured successfully. Confirm or retake before AI analysis.
        </p>

        {/* Step-by-Step AI Scanning Animation when scanning */}
        {isScanning && (
          <div className="py-4 space-y-3 bg-slate-900/80 rounded-xl p-4 border border-emerald-500/20 text-left">
            <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center space-x-2">
              <Sparkles className="w-4 h-4 animate-spin" />
              <span>AgroScan Multi-Stage AI Analysis</span>
            </h4>
            <div className="space-y-2">
              {steps.map((s, idx) => (
                <div key={idx} className="flex items-center space-x-3 text-xs">
                  <div
                    className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] ${
                      idx <= activeStepIdx
                        ? 'bg-emerald-500 text-slate-950 font-extrabold'
                        : 'bg-slate-800 text-slate-500'
                    }`}
                  >
                    {idx + 1}
                  </div>
                  <div className="flex-1">
                    <span className={idx <= activeStepIdx ? 'text-slate-200 font-semibold' : 'text-slate-500'}>
                      {s.label}
                    </span>
                    <span className="block text-[10px] text-slate-500">{s.desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Control Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
          <button
            type="button"
            onClick={onRetake}
            disabled={isScanning}
            className="px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 flex items-center justify-center space-x-2 transition disabled:opacity-50"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Retake Photo</span>
          </button>

          <button
            type="button"
            onClick={handleScanClick}
            disabled={isScanning}
            className="px-7 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-extrabold flex items-center justify-center space-x-2 transition shadow-lg shadow-emerald-900/40 disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isScanning ? 'Analyzing Leaf...' : 'Scan Leaf Now'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
