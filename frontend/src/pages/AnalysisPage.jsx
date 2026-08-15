import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, CheckCircle2, Loader2, ArrowRight } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const AnalysisPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    { label: "Normalizing image & applying OpenCV HSV color space mask...", duration: 800 },
    { label: "Executing MobileNetV2 Deep Learning inference model...", duration: 1000 },
    { label: "Segmenting leaf lesion contours & calculating severity %...", duration: 900 },
    { label: "Evaluating weather-based disease risk matrix...", duration: 800 }
  ];

  useEffect(() => {
    let timeoutId;
    if (currentStep < steps.length) {
      timeoutId = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, steps[currentStep].duration);
    } else {
      timeoutId = setTimeout(() => {
        navigate('/results/pred_001');
      }, 600);
    }
    return () => clearTimeout(timeoutId);
  }, [currentStep, navigate]);

  return (
    <div className="max-w-2xl mx-auto space-y-6 text-center py-10">
      
      {/* Title */}
      <div>
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-primary-container/30 border border-primary/20 text-primary text-xs font-semibold mb-3">
          <Sparkles className="w-4 h-4 text-primary animate-pulse" />
          <span>AI Computer Vision Pipeline</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Analyzing Plant Leaf...</h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Processing OpenCV color masks, MobileNetV2 disease classification, and severity estimation.
        </p>
      </div>

      {/* Animated Radar Scanning Container */}
      <div className="relative w-64 h-64 mx-auto rounded-3xl overflow-hidden glass-panel border-2 border-primary/40 shadow-2xl flex items-center justify-center">
        <img 
          src="https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=600&q=80" 
          alt="Scanning Leaf" 
          className="w-full h-full object-cover opacity-80"
        />
        {/* Animated Scan Line */}
        <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-agri-400 to-transparent shadow-[0_0_15px_#22c55e] animate-[bounce_2s_infinite]" />
        
        {/* Central Overlay Badge */}
        <div className="absolute bg-slate-950/80 backdrop-blur-md px-4 py-2 rounded-xl border border-primary/30 text-xs font-bold text-agri-400 flex items-center space-x-2">
          <Loader2 className="w-4 h-4 animate-spin text-primary" />
          <span>Processing Step {Math.min(currentStep + 1, steps.length)} of {steps.length}</span>
        </div>
      </div>

      {/* Step Progress Checklist */}
      <div className="glass-panel p-6 rounded-2xl max-w-md mx-auto text-left space-y-3">
        {steps.map((step, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;
          return (
            <div 
              key={idx} 
              className={`flex items-center space-x-3 text-xs p-2.5 rounded-xl border transition-all ${
                isDone 
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
                  : isCurrent 
                  ? 'bg-primary/10 border-primary/40 text-white font-medium animate-pulse' 
                  : 'bg-slate-900/40 border-slate-800 text-slate-500'
              }`}
            >
              {isDone ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              ) : isCurrent ? (
                <Loader2 className="w-4 h-4 text-primary animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-700 shrink-0" />
              )}
              <span className="leading-tight">{step.label}</span>
            </div>
          );
        })}
      </div>

      {/* Manual Override Button */}
      <button
        onClick={() => navigate('/results/pred_001')}
        className="text-xs text-slate-400 hover:text-agri-400 inline-flex items-center space-x-1 underline pt-2"
      >
        <span>Skip animation & view diagnostic report</span>
        <ArrowRight className="w-3 h-3" />
      </button>

    </div>
  );
};
