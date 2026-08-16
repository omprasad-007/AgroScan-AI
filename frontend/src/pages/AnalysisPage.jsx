import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Sparkles, CheckCircle2, Loader2, AlertCircle, RefreshCw, Upload } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export const AnalysisPage = () => {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);
  const [analyzedPred, setAnalyzedPred] = useState(null);

  const steps = [
    { label: "Executing Stage 1 Image Validation...", duration: 500 },
    { label: "Normalizing image & applying OpenCV HSV color space mask...", duration: 700 },
    { label: "Executing MobileNetV2 Deep Learning inference model...", duration: 800 },
    { label: "Evaluating weather-based disease risk matrix...", duration: 600 }
  ];

  const imageFile = location.state?.imageFile;
  const previewUrl = imageFile ? URL.createObjectURL(imageFile) : "https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=600&q=80";

  useEffect(() => {
    let isMounted = true;

    const runAnalysisPipeline = async () => {
      try {
        if (!imageFile) {
          setTimeout(() => {
            if (isMounted) navigate('/results/pred_001');
          }, 2000);
          return;
        }

        const formData = new FormData();
        formData.append('file', imageFile);

        // Stage 1: Mandatory Image Validation
        const valRes = await api.post('/predictions/validate-image', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (valRes.data?.is_plant === false) {
          if (isMounted) {
            setError(valRes.data.message || "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant.");
          }
          return;
        }

        if (valRes.data?.is_plant === null) {
          if (isMounted) {
            setError(valRes.data.message || "We couldn't verify the image. Please try again.");
          }
          return;
        }

        // Stage 2: Disease Detection & Inference (Only when is_plant == true)
        const res = await api.post('/predictions/analyze', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });

        if (isMounted) {
          setAnalyzedPred(res.data);
        }
      } catch (err) {
        if (isMounted) {
          const detail = err.response?.data?.detail || err.message || "You have not scanned a leaf or plant. Please scan a clear photo of a leaf or plant.";
          setError(detail);
        }
      }
    };

    runAnalysisPipeline();

    return () => { isMounted = false; };
  }, [imageFile, navigate]);

  useEffect(() => {
    let timeoutId;
    if (!error && currentStep < steps.length) {
      timeoutId = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, steps[currentStep].duration);
    } else if (!error && currentStep >= steps.length && analyzedPred) {
      timeoutId = setTimeout(() => {
        navigate(`/results/${analyzedPred.id}`, { state: { prediction: analyzedPred } });
      }, 500);
    }
    return () => clearTimeout(timeoutId);
  }, [currentStep, analyzedPred, error, navigate]);

  if (error) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4 space-y-6 text-center">
        <div className="glass-panel p-8 rounded-3xl border border-red-500/40 space-y-5 shadow-2xl">
          <div className="w-16 h-16 rounded-2xl bg-red-500/10 text-red-400 border border-red-500/30 flex items-center justify-center mx-auto shadow-inner">
            <AlertCircle className="w-8 h-8" />
          </div>

          <h2 className="text-xl font-extrabold text-white">Validation Error</h2>
          
          <p className="text-xs sm:text-sm text-red-200/90 leading-relaxed bg-red-500/10 p-4 rounded-xl border border-red-500/20 font-medium">
            {error}
          </p>

          <p className="text-xs text-slate-400">
            Ensure your photo clearly shows a leaf, stem, fruit, or plant part with good lighting.
          </p>

          <div className="pt-4 flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              to="/scan"
              className="px-6 py-3 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-agri-500/20 inline-flex items-center justify-center space-x-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Scan Again</span>
            </Link>
            <Link
              to="/scan"
              className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs border border-slate-700 inline-flex items-center justify-center space-x-2"
            >
              <Upload className="w-4 h-4" />
              <span>Upload Another Image</span>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6 text-center py-10">
      
      {/* Title */}
      <div>
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-agri-400 text-xs font-semibold mb-3">
          <Sparkles className="w-4 h-4 text-agri-400 animate-pulse" />
          <span>AI Plant Detection & Computer Vision Pipeline</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Analyzing Plant Leaf...</h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Processing plant verification, OpenCV color masks, and disease classification.
        </p>
      </div>

      {/* Animated Radar Scanning Container */}
      <div className="relative w-64 h-64 mx-auto rounded-3xl overflow-hidden glass-panel border-2 border-agri-500/40 shadow-2xl flex items-center justify-center">
        <img 
          src={previewUrl} 
          alt="Scanning Leaf" 
          className="w-full h-full object-cover opacity-80"
        />
        {/* Animated Scan Line */}
        <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-agri-400 to-transparent shadow-[0_0_15px_#22c55e] animate-[bounce_2s_infinite]" />
        
        {/* Central Overlay Badge */}
        <div className="absolute bg-slate-950/80 backdrop-blur-md px-4 py-2 rounded-xl border border-agri-500/30 text-xs font-bold text-agri-400 flex items-center space-x-2">
          <Loader2 className="w-4 h-4 animate-spin text-agri-400" />
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
                <Loader2 className="w-4 h-4 text-agri-400 animate-spin shrink-0" />
              ) : (
                <div className="w-4 h-4 rounded-full border border-slate-700 shrink-0" />
              )}
              <span className="leading-tight">{step.label}</span>
            </div>
          );
        })}
      </div>

    </div>
  );
};
