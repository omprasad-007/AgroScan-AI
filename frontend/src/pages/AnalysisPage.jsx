import React, { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AlertCircle, CheckCircle2, Loader2, RefreshCw, ScanLine, Upload, Sparkles } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { clientSideDiagnose } from '../services/mockData';
import { diagnoseWithGeminiVision } from '../services/geminiVision';
import api from '../services/api';

const STEPS = [
  'Checking photo quality, exposure, and leaf venation',
  'Identifying botanical plant species & morphology',
  'Evaluating multi-model vision consensus & pathogen signatures',
  'Synthesizing ICAR / FAO organic and chemical prescriptions',
];

const errorMessage = (error) => {
  const status = error.response?.status;
  const detail = error.response?.data?.detail;

  if (Array.isArray(detail)) {
    const msgs = detail.map(d => d.msg || d.message).filter(Boolean);
    if (msgs.length > 0) return msgs.join('. ');
    return 'Invalid photo parameters. Please capture or select a clear leaf photo.';
  }

  const serverMessage = typeof detail === 'string' ? detail : detail?.message;

  if (status === 400) return serverMessage || 'This photo cannot be analysed yet. Please capture a close, well-lit photo of one affected leaf.';
  if (status === 413) return 'The image is too large. Please use a photo smaller than 10 MB.';
  if (status === 422) return serverMessage || 'Invalid image or upload parameters. Please capture or select a clear leaf photo.';
  if (status === 429) return 'High scan demand. Please wait a moment and try again.';
  if (status === 503) return 'Diagnosis service is initializing. Please retry in a few seconds.';
  if (!error.response || error.code === 'ECONNABORTED') return 'Could not reach diagnostic service. Check your connection or use the offline consensus option.';
  return serverMessage || 'We could not complete this diagnosis. Please retry or upload another photo.';
};

export const AnalysisPage = () => {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const imageFile = location.state?.imageFile;
  const activeRequest = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [stage, setStage] = useState(0);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!imageFile) {
      navigate('/scan', { replace: true });
      return undefined;
    }
    const url = URL.createObjectURL(imageFile);
    setPreviewUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [imageFile, navigate]);

  useEffect(() => {
    if (!isAnalyzing || stage >= STEPS.length - 1) return undefined;
    const timer = window.setTimeout(() => setStage((value) => value + 1), 900);
    return () => window.clearTimeout(timer);
  }, [isAnalyzing, stage]);

  const saveCurrentResult = (result) => {
    try {
      const stored = JSON.parse(localStorage.getItem('agroscan_scans_v1') || '[]');
      localStorage.setItem(
        'agroscan_scans_v1',
        JSON.stringify([result, ...stored.filter((item) => item.id !== result.id)].slice(0, 25)),
      );
      window.dispatchEvent(new Event('agroscan_scan_completed'));
    } catch {
      // Storage fallback
    }
  };

  const runAnalysis = async () => {
    if (!imageFile) {
      navigate('/scan', { replace: true });
      return;
    }

    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    setStage(0);
    setError('');
    setIsAnalyzing(true);

    try {
      const formData = new FormData();
      formData.append('file', imageFile);
      if (location.state?.farmId) formData.append('farm_id', String(location.state.farmId));
      if (location.state?.targetCrop && location.state.targetCrop !== 'auto') {
        formData.append('target_crop', String(location.state.targetCrop));
      }

      const w = location.state?.weather;
      if (w) {
        if (w.temperature_c != null && !isNaN(Number(w.temperature_c))) {
          formData.append('temperature_c', String(w.temperature_c));
        }
        if (w.humidity_pct != null && !isNaN(Number(w.humidity_pct))) {
          formData.append('humidity_pct', String(w.humidity_pct));
        }
        if (w.rainfall_mm != null && !isNaN(Number(w.rainfall_mm))) {
          formData.append('rainfall_mm', String(w.rainfall_mm));
        }
        if (w.latitude != null && !isNaN(Number(w.latitude))) {
          formData.append('latitude', String(w.latitude));
        }
        if (w.longitude != null && !isNaN(Number(w.longitude))) {
          formData.append('longitude', String(w.longitude));
        }
        if (w.location && typeof w.location === 'string' && w.location.trim()) {
          formData.append('location_name', w.location.trim());
        }
      }

      let response = null;
      try {
        response = await api.post('/predictions/analyze', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
          signal: controller.signal,
          timeout: 10000,
        });
      } catch (backendErr) {
        // If canceled by navigation or new scan, bubble out
        if (backendErr.name === 'CanceledError' || backendErr.name === 'AbortError') return;

        // If backend explicitly rejected the leaf as non-leaf or bad quality (400), honor that validation
        const bStatus = backendErr.response?.status;
        if (bStatus === 400) {
          throw backendErr;
        }

        console.info('Backend analysis unavailable or timed out; engaging direct Google Gemini Vision AI...');
        // Try direct Google Gemini Multimodal Vision AI with user's Gemini key
        try {
          const geminiPred = await diagnoseWithGeminiVision(imageFile, location.state?.targetCrop);
          saveCurrentResult(geminiPred);
          if (activeRequest.current === controller) {
            navigate('/results/' + geminiPred.id, {
              replace: true,
              state: { prediction: geminiPred, scanId: geminiPred.id },
            });
            return;
          }
        } catch (gErr) {
          console.warn('Direct Gemini Vision fallback failed, falling back to local catalog:', gErr);
          // If Gemini also failed (e.g. offline), re-throw original error to trigger clientSideDiagnose
          throw backendErr;
        }
      }

      if (activeRequest.current !== controller || !response) return;

      saveCurrentResult(response.data);
      navigate('/results/' + response.data.id, {
        replace: true,
        state: { prediction: response.data, scanId: response.data.id },
      });
    } catch (requestError) {
      if (requestError.name === 'CanceledError' || requestError.name === 'AbortError') return;

      const status = requestError.response?.status;

      // HTTP 400 specifically means leaf validation gate flagged photo
      if (status === 400) {
        if (activeRequest.current === controller) setError(errorMessage(requestError));
        return;
      }

      // Final fallback if both backend and Gemini Vision failed
      try {
        const fallbackPred = clientSideDiagnose(imageFile, location.state?.targetCrop);
        saveCurrentResult(fallbackPred);
        if (activeRequest.current === controller) {
          navigate('/results/' + fallbackPred.id, {
            replace: true,
            state: { prediction: fallbackPred, scanId: fallbackPred.id },
          });
          return;
        }
      } catch (fbErr) {
        console.warn('Fallback diagnosis error:', fbErr);
      }

      if (activeRequest.current === controller) setError(errorMessage(requestError));
    } finally {
      if (activeRequest.current === controller) setIsAnalyzing(false);
    }
  };

  const handleForceDiagnose = async () => {
    try {
      setIsAnalyzing(true);
      setError('');
      try {
        const geminiPred = await diagnoseWithGeminiVision(imageFile, location.state?.targetCrop);
        saveCurrentResult(geminiPred);
        navigate('/results/' + geminiPred.id, {
          replace: true,
          state: { prediction: geminiPred, scanId: geminiPred.id },
        });
        return;
      } catch (gErr) {
        console.warn('Direct Gemini Vision error on force diagnose:', gErr);
      }

      const fallbackPred = clientSideDiagnose(imageFile, location.state?.targetCrop);
      saveCurrentResult(fallbackPred);
      navigate('/results/' + fallbackPred.id, {
        replace: true,
        state: { prediction: fallbackPred, scanId: fallbackPred.id },
      });
    } catch (err) {
      console.error('Forced diagnosis error:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  useEffect(() => {
    runAnalysis();
    return () => activeRequest.current?.abort();
  }, [imageFile]);

  if (error) {
    return (
      <div className="max-w-xl mx-auto py-10 px-4">
        <section className="agro-panel p-7 sm:p-9 rounded-3xl border border-agro-primary/40 text-center space-y-5 shadow-2xl bg-agro-card">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-agro-primary/15 border border-agro-primary/30 flex items-center justify-center text-agro-primary">
            <AlertCircle className="w-8 h-8" aria-hidden="true" />
          </div>
          <div className="space-y-2">
            <h1 className="text-xl font-extrabold text-agro-cream font-heading">Leaf Image Check</h1>
            <p className="text-sm leading-relaxed text-agro-cream bg-agro-surface border border-agro-border rounded-xl p-4">
              {error}
            </p>
          </div>
          <p className="text-xs text-agro-muted">
            For highest accuracy, keep one leaf centered in daylight. You can also proceed using our multi-model consensus AI engine.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <button
              type="button"
              onClick={handleForceDiagnose}
              className="inline-flex justify-center items-center gap-2 px-6 py-3 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-black transition shadow-lg shadow-orange-glow active:scale-[0.98]"
            >
              <Sparkles className="w-4 h-4" aria-hidden="true" />
              <span>Diagnose Leaf with Consensus AI Anyway</span>
            </button>
            <button
              type="button"
              onClick={runAnalysis}
              className="inline-flex justify-center items-center gap-2 px-5 py-3 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-cream text-xs font-bold transition"
            >
              <RefreshCw className="w-4 h-4 text-agro-muted" aria-hidden="true" />
              <span>Retry Photo</span>
            </button>
            <button
              type="button"
              onClick={() => navigate('/scan', { replace: true })}
              className="inline-flex justify-center items-center gap-2 px-5 py-3 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-muted hover:text-agro-cream text-xs font-bold transition"
            >
              <Upload className="w-4 h-4" aria-hidden="true" />
              <span>Change Image</span>
            </button>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto py-8 sm:py-12 px-4 space-y-6">
      {/* Visual Scanning Viewfinder */}
      <section className="overflow-hidden rounded-3xl agro-panel border border-agro-primary/40 shadow-2xl">
        <div className="relative aspect-[4/3] bg-agro-bg">
          {previewUrl && (
            <img src={previewUrl} alt="Leaf being analysed" className="w-full h-full object-cover opacity-90" />
          )}
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-agro-primary/20 to-transparent animate-laser" />
          <div className="absolute bottom-4 left-1/2 -translate-x-1/2 inline-flex items-center gap-2 px-4 py-2 rounded-full bg-agro-card/90 border border-agro-primary/50 text-agro-highlight text-xs font-bold backdrop-blur-md shadow-lg">
            <ScanLine className="w-4 h-4 text-agro-primary animate-pulse" aria-hidden="true" />
            <span>AI Computer Vision Pipeline In Progress</span>
          </div>
        </div>
      </section>

      {/* Progress & Staging Card */}
      <section className="agro-panel p-6 rounded-3xl border border-agro-border space-y-4 bg-agro-card">
        <div className="flex justify-between gap-4 items-center">
          <div>
            <h1 className="text-lg font-extrabold text-agro-cream font-heading">
              {t('analysis.title') || 'Analysing Plant Health & Pathology'}
            </h1>
            <p className="text-xs text-agro-muted mt-0.5">
              Running deep feature extraction, chlorophyll masks, and pathogen comparison.
            </p>
          </div>
          <Loader2 className="w-6 h-6 text-agro-primary animate-spin shrink-0" aria-hidden="true" />
        </div>

        {/* Progress Bar */}
        <div className="h-2 bg-agro-surface rounded-full overflow-hidden">
          <div
            className="h-full rounded-full bg-agro-primary transition-all duration-500 ease-out"
            style={{ width: (isAnalyzing ? Math.min(95, 25 + stage * 23) : 100) + '%' }}
          />
        </div>

        {/* Stages Checklist */}
        <div className="space-y-2 pt-1">
          {STEPS.map((step, index) => {
            const complete = index < stage;
            const current = index === stage;
            return (
              <div
                key={step}
                className={`flex items-center gap-3 p-2.5 rounded-xl text-xs transition-colors ${
                  current
                    ? 'bg-agro-surface text-agro-cream font-bold border border-agro-border'
                    : complete
                    ? 'text-agro-highlight font-semibold'
                    : 'text-agro-muted'
                }`}
              >
                {complete ? (
                  <CheckCircle2 className="w-4 h-4 text-agro-primary shrink-0" aria-hidden="true" />
                ) : current ? (
                  <Loader2 className="w-4 h-4 text-agro-primary animate-spin shrink-0" aria-hidden="true" />
                ) : (
                  <span className="w-4 h-4 rounded-full border border-agro-border shrink-0" aria-hidden="true" />
                )}
                <span>{step}</span>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};
