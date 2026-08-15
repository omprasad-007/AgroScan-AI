import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  CheckCircle2, 
  AlertTriangle, 
  ShieldCheck, 
  CloudSun, 
  Sparkles, 
  Bot, 
  ArrowLeft,
  FileText
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

export const ResultPage = () => {
  const { scanId } = useParams();
  const { t } = useLanguage();
  const [scan, setScan] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const [scRes, recRes] = await Promise.all([
          api.get(`/predictions/${scanId}`),
          api.get(`/recommendations/${scanId}`)
        ]);
        setScan(scRes.data);
        setRecommendation(recRes.data);
      } catch (err) {
        setError('Diagnostic report not found.');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [scanId]);

  if (loading) {
    return (
      <div className="text-center py-20 text-slate-400 text-sm animate-pulse">
        Generating diagnostic report & calculating leaf lesion severity...
      </div>
    );
  }

  if (error || !scan) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400 text-sm mb-4">{error || 'Report not available.'}</p>
        <Link to="/scan" className="text-xs text-agri-400 hover:underline">Return to Scan Page</Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Top Header */}
      <div className="flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white transition">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Dashboard</span>
        </Link>
        <div className="flex items-center space-x-2">
          {scan.is_demo && (
            <span className="px-2.5 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-bold uppercase tracking-wider">
              Demo Inference Result
            </span>
          )}
        </div>
      </div>

      {/* Main Report Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl space-y-6">
        
        {/* Title */}
        <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-semibold text-agri-400 uppercase tracking-wider">{scan.crop_detected} Crop</span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white mt-0.5">{scan.disease_name}</h1>
          </div>
          <div className="flex items-center space-x-3">
            <SeverityBadge level={scan.severity_level} />
            <WeatherRiskBadge level={scan.weather_risk_level} />
          </div>
        </div>

        {/* Diagnostic Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.confidence')}</span>
            <span className="text-xl font-bold text-emerald-400 mt-1 block">
              {(scan.confidence_score * 100).toFixed(1)}%
            </span>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.severity')}</span>
            <span className="text-xl font-bold text-amber-400 mt-1 block">
              {scan.severity_percentage}% ({scan.severity_level})
            </span>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">Affected Leaf Area</span>
            <span className="text-xl font-bold text-white mt-1 block">
              {scan.affected_area_cm2} cm²
            </span>
          </div>

        </div>

        {/* Treatment Protocol Sections */}
        {recommendation && (
          <div className="space-y-4 pt-2">
            
            {/* Organic Treatment */}
            <div className="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
              <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>{t('result.organic_remedy')}</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.organic_treatment}</p>
            </div>

            {/* Chemical Treatment */}
            <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/20">
              <h3 className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>{t('result.chemical_remedy')}</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.chemical_treatment}</p>
            </div>

            {/* Prevention */}
            <div className="p-4 rounded-xl bg-purple-500/5 border border-purple-500/20">
              <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4" />
                <span>{t('result.prevention')}</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.prevention}</p>
            </div>

          </div>
        )}

        {/* Disclaimer Note */}
        <p className="text-[11px] text-slate-500 italic bg-slate-900/40 p-3 rounded-lg border border-slate-800">
          {recommendation?.disclaimer || t('result.disclaimer')}
        </p>

      </div>

      {/* CTA to Gemini AI Assistant */}
      <div className="glass-panel p-6 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center border border-purple-500/20 shrink-0">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-white">Have questions about this disease treatment?</h4>
            <p className="text-xs text-slate-400">Ask the Gemini AI Agronomist for dosage, organic alternatives, or prevention.</p>
          </div>
        </div>
        <Link
          to={`/assistant?predictionId=${scan.id}`}
          className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-xs transition shadow-lg shadow-purple-600/20 text-center shrink-0"
        >
          Ask AI Assistant
        </Link>
      </div>

    </div>
  );
};
