import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  CheckCircle2, 
  ShieldCheck, 
  Bot, 
  ArrowLeft,
  FileText,
  Calendar
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import { AIAssistantPanel } from '../components/assistant/AIAssistantPanel';
import api from '../services/api';

export const ResultPage = () => {
  const { scanId } = useParams();
  const { t, translateCrop, translateDisease, translateSeverity, formatDate } = useLanguage();
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
        setError(t('result.not_found') || 'Diagnostic report not found.');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [scanId, t]);

  if (loading) {
    return (
      <div className="text-center py-20 text-slate-400 text-sm animate-pulse">
        {t('result.generating') || 'Generating diagnostic report & calculating leaf lesion severity...'}
      </div>
    );
  }

  if (error || !scan) {
    return (
      <div className="text-center py-12">
        <p className="text-red-400 text-sm mb-4">{error || t('result.not_found') || 'Report not available.'}</p>
        <Link to="/scan" className="text-xs text-agri-400 hover:underline">
          {t('result.return_to_scan') || 'Return to Scan Page'}
        </Link>
      </div>
    );
  }

  const rawCrop = scan.plant || scan.crop_detected || 'Crop';
  const rawDisease = scan.disease || scan.disease_name || 'Healthy';
  const rawSeverity = scan.severity || scan.severity_level || 'Normal';

  const displayCrop = translateCrop(rawCrop);
  const displayDisease = translateDisease(rawDisease);
  const displaySeverity = translateSeverity(rawSeverity);
  const formattedDate = formatDate(scan.created_at || new Date());

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Top Header */}
      <div className="flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white transition">
          <ArrowLeft className="w-4 h-4" />
          <span>{t('result.back_to_dashboard') || 'Back to Dashboard'}</span>
        </Link>
        <div className="flex items-center space-x-2">
          {scan.is_demo && (
            <span className="px-2.5 py-1 rounded bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-bold uppercase tracking-wider">
              {t('result.demo_badge') || 'Demo Inference Result'}
            </span>
          )}
        </div>
      </div>

      {/* Main Report Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl space-y-6">
        
        {/* Title & Metadata */}
        <div className="border-b border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-400 uppercase tracking-wider">
              <span>{displayCrop}</span>
              {scan.scientific_name && scan.scientific_name !== 'N/A' && (
                <span className="text-slate-400 italic lowercase font-normal">({scan.scientific_name})</span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white mt-0.5">{displayDisease}</h1>
            <div className="flex items-center space-x-4 text-xs text-slate-400 mt-2">
              <span className="flex items-center space-x-1">
                <Calendar className="w-3.5 h-3.5 text-slate-500" />
                <span>{t('result.date') || 'Date'}: {formattedDate}</span>
              </span>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <SeverityBadge level={scan.severity || scan.severity_level} />
            <WeatherRiskBadge level={scan.risk || scan.weather_risk_level} />
          </div>
        </div>

        {/* Real Diagnostic Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.confidence')}</span>
            <span className="text-xl font-bold text-emerald-400 mt-1 block">
              {((scan.confidence || scan.confidence_score || 0.90) * 100).toFixed(1)}%
            </span>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.severity')}</span>
            <span className="text-xl font-bold text-amber-400 mt-1 block">
              {scan.severity_percentage || 0}% ({displaySeverity})
            </span>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.affected_area')}</span>
            <span className="text-xl font-bold text-white mt-1 block">
              {scan.affected_area || scan.affected_area_cm2 || 0} cm²
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
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.organic_treatment || recommendation.organic_remedy}</p>
            </div>

            {/* Chemical Treatment */}
            <div className="p-4 rounded-xl bg-blue-500/5 border border-blue-500/20">
              <h3 className="text-xs font-bold text-blue-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>{t('result.chemical_remedy')}</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.chemical_treatment || recommendation.chemical_remedy}</p>
            </div>

            {/* Prevention */}
            <div className="p-4 rounded-xl bg-purple-500/5 border border-purple-500/20">
              <h3 className="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2 flex items-center space-x-2">
                <ShieldCheck className="w-4 h-4" />
                <span>{t('result.prevention')}</span>
              </h3>
              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.prevention || recommendation.preventive_steps}</p>
            </div>

          </div>
        )}

        {/* Disclaimer Note */}
        <p className="text-[11px] text-slate-500 italic bg-slate-900/40 p-3 rounded-lg border border-slate-800">
          {recommendation?.disclaimer || t('result.disclaimer')}
        </p>

      </div>

      {/* Auto-Embedded AI Assistant Panel */}
      <div className="space-y-3 pt-2">
        <h2 className="text-lg font-extrabold text-white flex items-center space-x-2">
          <Bot className="w-5 h-5 text-emerald-400" />
          <span>{t('result.chat_title') || 'AgroScan AI Agronomist Chat'}</span>
        </h2>
        <AIAssistantPanel scanData={scan} predictionId={scan.id} autoOpen={true} />
      </div>

    </div>
  );
};
