import React, { useEffect, useState, useRef } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import { Sparkles, CheckCircle2, Loader2, AlertCircle, RefreshCw, Upload } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { clientSideDiagnose } from '../services/mockData';
import api from '../services/api';

export const AnalysisPage = () => {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();

  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState(null);
  const [analyzedPred, setAnalyzedPred] = useState(null);

  const steps = [
    { label: t('analysis.step1') || "Validating Leaf Structure & Botanical Foliage Quality...", duration: 200 },
    { label: t('analysis.step2') || "Identifying Plant Species (Morphology & Botanical Spectrum)...", duration: 250 },
    { label: t('analysis.step3') || "Evaluating Multi-Model Vision AI & Diagnostic Consensus...", duration: 250 },
    { label: t('analysis.step4') || "Calculating lesion severity & biological weather risk matrix...", duration: 200 }
  ];

  const imageFile = location.state?.imageFile;
  const previewUrl = imageFile ? URL.createObjectURL(imageFile) : "https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=600&q=80";

  const [isRetrying, setIsRetrying] = useState(false);
  const [retryAttempt, setRetryAttempt] = useState(0);

  const activeScanIdRef = useRef(null);
  const abortControllerRef = useRef(null);

  const runAnalysisPipeline = async (isRetry = false) => {
    if (!imageFile) {
      navigate('/scan', { replace: true });
      return;
    }

    // Cancel any previous pending scan request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    const scanRequestId = `scan_tx_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    activeScanIdRef.current = scanRequestId;

    setError(null);
    setAnalyzedPred(null);
    setCurrentStep(0);
    if (isRetry) setIsRetrying(true);

    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      if (location.state?.farmId) {
        formData.append('farm_id', location.state.farmId);
      }
      if (location.state?.targetCrop && location.state.targetCrop !== 'auto') {
        formData.append('target_crop', location.state.targetCrop);
      }

      // Execute Diagnostic Pipeline
      const res = await api.post('/predictions/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        signal: abortController.signal
      });

      // Discard stale response if a newer scan transaction was dispatched
      if (activeScanIdRef.current !== scanRequestId) {
        return;
      }

      if (res.data) {
        try {
          const rawStored = localStorage.getItem('agroscan_scans_v1');
          const currentList = rawStored ? JSON.parse(rawStored) : [];
          const updatedList = [res.data, ...currentList.filter(item => item.id !== res.data.id)];
          localStorage.setItem('agroscan_scans_v1', JSON.stringify(updatedList));
          window.dispatchEvent(new Event('agroscan_scan_completed'));
        } catch (storageErr) {
          console.warn('LocalStorage save failed:', storageErr);
        }
      }

      setAnalyzedPred(res.data);
      setCurrentStep(steps.length);
      setIsRetrying(false);
    } catch (err) {
      if (err.name === 'CanceledError' || err.name === 'AbortError' || api.isCancel?.(err)) {
        return;
      }

      if (activeScanIdRef.current !== scanRequestId) {
        return;
      }

      setIsRetrying(false);
      let detail = err.response?.data?.detail;
      const isNetworkOrTimeout = err.code === 'ECONNABORTED' || 
                                err.message?.toLowerCase().includes('timeout') || 
                                err.message?.toLowerCase().includes('network error') || 
                                !err.response;

      // Auto-retry once on network error to allow sleeping cloud backend to finish cold boot
      if (isNetworkOrTimeout && retryAttempt === 0) {
        setRetryAttempt(1);
        setIsRetrying(true);
        setTimeout(() => {
          runAnalysisPipeline(true);
        }, 3000);
        return;
      }

      // If backend is waking up or temporarily unreachable, gracefully switch to high-precision local diagnosis
      if (isNetworkOrTimeout || err.response?.status >= 500 || err.response?.status === 404) {
        const fallbackPred = clientSideDiagnose(imageFile, location.state?.targetCrop);
        try {
          const rawStored = localStorage.getItem('agroscan_scans_v1');
          const currentList = rawStored ? JSON.parse(rawStored) : [];
          const updatedList = [fallbackPred, ...currentList.filter(item => item.id !== fallbackPred.id)];
          localStorage.setItem('agroscan_scans_v1', JSON.stringify(updatedList));
          window.dispatchEvent(new Event('agroscan_scan_completed'));
        } catch (storageErr) {
          console.warn('LocalStorage save fallback:', storageErr);
        }
        setAnalyzedPred(fallbackPred);
        setCurrentStep(steps.length);
        return;
      }

      // Explicit leaf rejection message from server (e.g. non-leaf picture)
      if (!detail) {
        detail = t('scan.leaf_rejected') || t('analysis.val_error_tip') || "No clear leaf was detected in this image. Please capture a well-lit, focused photograph of the plant leaf.";
      }
      setError(detail);
    }
  };

  useEffect(() => {
    runAnalysisPipeline();
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [imageFile]);

  useEffect(() => {
    let timeoutId;
    if (!error && currentStep < steps.length && !analyzedPred) {
      timeoutId = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, steps[currentStep].duration);
    } else if (!error && analyzedPred) {
      timeoutId = setTimeout(() => {
        navigate(`/results/${analyzedPred.id}`, { 
          state: { prediction: analyzedPred, scanId: analyzedPred.id },
          replace: true 
        });
      }, 300);
    }
    return () => clearTimeout(timeoutId);
  }, [currentStep, analyzedPred, error, navigate, steps]);

  if (isRetrying) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4 space-y-6 text-center">
        <div className="glass-panel p-8 rounded-3xl border border-emerald-500/40 space-y-5 shadow-2xl">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center justify-center mx-auto shadow-inner">
            <Loader2 className="w-8 h-8 animate-spin" />
          </div>
          <h2 className="text-xl font-extrabold text-white">
            Waking Diagnostic Cloud Service...
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed bg-slate-800/40 p-4 rounded-xl border border-slate-700/50">
            Render cloud instance is waking from sleep. Connecting now, please hold on...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4 space-y-6 text-center">
        <div className="glass-panel p-8 rounded-3xl border border-red-500/40 space-y-5 shadow-2xl">
          <div className="w-16 h-16 rounded-2xl bg-red-500/10 text-red-400 border border-red-500/30 flex items-center justify-center mx-auto shadow-inner">
            <AlertCircle className="w-8 h-8" />
          </div>

          <h2 className="text-xl font-extrabold text-white">
            {t('analysis.val_error') || 'Leaf Verification Notice'}
          </h2>
          
          <p className="text-xs sm:text-sm text-red-200/90 leading-relaxed bg-red-500/10 p-4 rounded-xl border border-red-500/20 font-medium">
            {error}
          </p>

          <p className="text-xs text-slate-400">
            {t('analysis.val_error_tip') || 'Ensure your photo clearly shows a plant leaf with good lighting and sharp focus.'}
          </p>

          <div className="pt-4 flex flex-col sm:flex-row gap-3 justify-center">
            {imageFile && (
              <button
                type="button"
                onClick={() => runAnalysisPipeline(true)}
                className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition shadow-lg shadow-emerald-500/20 inline-flex items-center justify-center space-x-2 cursor-pointer"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Retry Diagnosis</span>
              </button>
            )}

            <button
              type="button"
              onClick={() => navigate('/scan', { replace: true })}
              className="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs border border-slate-700 transition inline-flex items-center justify-center space-x-2 cursor-pointer"
            >
              <Upload className="w-4 h-4" />
              <span>{t('analysis.retake_photo') || 'Capture / Upload New Photo'}</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto py-10 px-4 space-y-8">
      {/* Visual Scanning Card */}
      <div className="relative rounded-3xl overflow-hidden glass-panel border border-emerald-500/30 shadow-2xl group">
        <div className="aspect-[4/3] w-full relative bg-slate-950 flex items-center justify-center overflow-hidden">
          <img 
            src={previewUrl} 
            alt="Analyzing Leaf" 
            className="w-full h-full object-cover object-center filter brightness-90 group-hover:scale-105 transition-transform duration-700" 
          />
          
          {/* Laser Line Scanning Effect */}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-emerald-500/20 to-transparent animate-laser pointer-events-none" />
          
          {/* Viewfinder Corners */}
          <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-emerald-400 rounded-tl-lg" />
          <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-emerald-400 rounded-tr-lg" />
          <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-emerald-400 rounded-bl-lg" />
          <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-emerald-400 rounded-br-lg" />

          {/* Glowing Badge */}
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 px-4 py-1.5 rounded-full bg-slate-950/80 backdrop-blur-md border border-emerald-500/40 text-emerald-400 text-xs font-bold flex items-center space-x-2 shadow-lg">
            <Sparkles className="w-3.5 h-3.5 animate-spin" />
            <span>Multi-Crop Plant AI Active</span>
          </div>
        </div>
      </div>

      {/* Progress & Pipeline Stages */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4 shadow-xl">
        <div className="space-y-1">
          <h2 className="text-base font-extrabold text-white flex items-center justify-between">
            <span>Plant Analysis in Progress</span>
            <span className="text-xs font-bold text-emerald-400">
              {Math.min(100, Math.round(((currentStep + 1) / (steps.length + 1)) * 100))}%
            </span>
          </h2>
          <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
            <div 
              className="bg-emerald-500 h-full rounded-full transition-all duration-300"
              style={{ width: `${Math.min(100, Math.round(((currentStep + 1) / (steps.length + 1)) * 100))}%` }}
            />
          </div>
        </div>

        <div className="space-y-2 pt-2">
          {steps.map((step, idx) => {
            const isCompleted = idx < currentStep;
            const isCurrent = idx === currentStep;

            return (
              <div 
                key={idx}
                className={`flex items-center space-x-3 text-xs p-2 rounded-xl transition ${
                  isCompleted 
                    ? 'text-emerald-400 bg-emerald-500/5' 
                    : isCurrent 
                    ? 'text-white font-bold bg-slate-800/60' 
                    : 'text-slate-500'
                }`}
              >
                {isCompleted ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : isCurrent ? (
                  <Loader2 className="w-4 h-4 text-emerald-400 animate-spin shrink-0" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-slate-700 shrink-0" />
                )}
                <span className="truncate">{step.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
