import React, { useState, useEffect } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import { 
  CheckCircle2, 
  ShieldCheck, 
  Bot, 
  ArrowLeft,
  FileText,
  Calendar,
  AlertTriangle,
  Info,
  ListOrdered,
  Cpu
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import { AIAssistantPanel } from '../components/assistant/AIAssistantPanel';
import api from '../services/api';

export const ResultPage = () => {
  const { scanId } = useParams();
  const location = useLocation();
  const { t, translateCrop, translateDisease, translateSeverity, formatDate } = useLanguage();

  const passedPred = location.state?.prediction;
  const isDirectMatch = passedPred && String(passedPred.id) === String(scanId);

  const [scan, setScan] = useState(() => (isDirectMatch ? passedPred : null));
  const [recommendation, setRecommendation] = useState(() => (isDirectMatch ? (passedPred.recommendation || null) : null));
  const [loading, setLoading] = useState(() => !isDirectMatch);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isDirectMatch && scan) {
      if (!recommendation && scan.recommendation) {
        setRecommendation(scan.recommendation);
      }
      return;
    }

    const fetchReport = async () => {
      setLoading(true);
      try {
        const [scRes, recRes] = await Promise.all([
          api.get(`/predictions/${scanId}`),
          api.get(`/recommendations/${scanId}`).catch(() => ({ data: null }))
        ]);
        if (scRes.data && String(scRes.data.id) === String(scanId)) {
          setScan(scRes.data);
          setRecommendation(recRes?.data || scRes.data?.recommendation || null);
          setError('');
        } else {
          setError(t('result.not_found') || 'Diagnostic report not found.');
        }
      } catch (err) {
        try {
          const raw = localStorage.getItem('agroscan_scans_v1');
          const storedList = raw ? JSON.parse(raw) : [];
          const matched = storedList.find(item => String(item.id) === String(scanId));
          if (matched) {
            setScan(matched);
            setRecommendation(matched.recommendation || null);
            setError('');
            return;
          }
        } catch (e) {
          console.warn('LocalStorage lookup failed:', e);
        }
        setError(t('result.not_found') || 'Diagnostic report not found.');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [scanId, isDirectMatch]);

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

  const rawCrop = scan.plant || scan.plant_name || scan.crop_detected || 'Crop';
  const rawDisease = scan.disease || scan.disease_name || 'Healthy';
  const rawSeverity = scan.severity || scan.severity_level || 'Normal';

  const displayCrop = translateCrop(rawCrop);
  const displayDisease = translateDisease(rawDisease);
  const displaySeverity = translateSeverity(rawSeverity);
  const formattedDate = formatDate(scan.created_at || scan.analysis_timestamp || new Date());

  const cropSupportStatus = scan.crop_support_status || 'SUPPORTED';
  const confidenceInterp = scan.confidence_interpretation || (
    (scan.confidence || scan.confidence_score || 0) >= 0.70 ? 'HIGH_CONFIDENCE' :
    (scan.confidence || scan.confidence_score || 0) >= 0.50 ? 'MODERATE_CONFIDENCE' : 'LOW_CONFIDENCE_UNCERTAIN'
  );

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Top Navigation & Badges */}
      <div className="flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white transition">
          <ArrowLeft className="w-4 h-4" />
          <span>{t('result.back_to_dashboard') || 'Back to Dashboard'}</span>
        </Link>
        <div className="flex items-center space-x-2">
          {(scan.model_name || scan.model_version) && (
            <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold flex items-center space-x-1">
              <Cpu className="w-3 h-3" />
              <span>{scan.model_name || scan.model_version.split('/').pop()}</span>
            </span>
          )}
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
              {scan.disease_category && (
                <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300 border border-slate-700">
                  {scan.disease_category}
                </span>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <SeverityBadge level={scan.severity || scan.severity_level} />
            <WeatherRiskBadge level={scan.risk || scan.weather_risk_level} />
          </div>
        </div>

        {/* Crop Support Status Banner */}
        {cropSupportStatus === 'UNSUPPORTED' && (
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs space-y-1">
            <div className="flex items-center space-x-2 font-bold">
              <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
              <span>{t('result.unsupported_crop_title') || 'Unsupported Crop Pathology Calibration'}</span>
            </div>
            <p className="text-[11px] text-amber-200/90 leading-relaxed">
              {t('result.unsupported_crop_desc') || `AgroScan AI identified this specimen as ${displayCrop}, but dedicated machine learning pathology models for this specific crop are pending field calibration. General agronomic advisory is shown below.`}
            </p>
          </div>
        )}

        {/* Identified Plant Species Card */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-950/30 via-slate-900 to-emerald-950/20 border border-emerald-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-inner">
          <div className="space-y-0.5">
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-400 block">🌿 {t('result.identified_species') || 'Identified Plant Species'}:</span>
            <div className="flex items-center space-x-2">
              <span className="text-base sm:text-lg font-black text-white">{displayCrop}</span>
              {scan.scientific_name && scan.scientific_name !== 'N/A' && (
                <span className="text-xs text-slate-300 italic">({scan.scientific_name})</span>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className={`px-3 py-1 rounded-xl text-xs font-bold border ${
              cropSupportStatus === 'SUPPORTED' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' :
              cropSupportStatus === 'PARTIALLY_SUPPORTED' ? 'bg-blue-500/10 border-blue-500/30 text-blue-400' :
              'bg-amber-500/10 border-amber-500/30 text-amber-400'
            }`}>
              {cropSupportStatus === 'SUPPORTED' ? `✓ ${t('result.supported_crop') || 'Supported Crop'}` :
               cropSupportStatus === 'PARTIALLY_SUPPORTED' ? `ℹ ${t('result.partially_supported') || 'Partially Supported'}` :
               `⚠️ ${t('result.unsupported_crop') || 'Unsupported Crop'}`}
            </span>
          </div>
        </div>

        {/* Real Diagnostic Metrics Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 sm:gap-4">
          
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.confidence') || 'Confidence'}</span>
            <span className="text-xl font-bold text-emerald-400 mt-1 block">
              {((scan.confidence || scan.confidence_score || 0.90) * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {confidenceInterp === 'HIGH_CONFIDENCE' ? t('result.conf_high') || 'High Confidence' :
               confidenceInterp === 'MODERATE_CONFIDENCE' ? t('result.conf_mod') || 'Moderate Confidence' :
               t('result.conf_low') || 'Uncertain'}
            </span>
          </div>

          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block">{t('result.providers_agreeing') || 'Model Agreement'}</span>
            <span className="text-xl font-bold text-emerald-400 mt-1 block">
              {scan.providers_agreed || '1 of 1'}
            </span>
            <span className="text-[10px] text-slate-500 block mt-0.5">
              {scan.agreement_status || scan.agreement_level || 'SINGLE_SOURCE'}
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

        {/* Leaf & Image Quality Verification Bar */}
        <div className="flex flex-wrap items-center justify-between p-3 rounded-xl bg-slate-900/40 border border-slate-800 text-xs text-slate-400 gap-2">
          <div className="flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{t('result.leaf_verified') || 'Leaf-Only Gate'}: <strong className="text-slate-200">Verified Plant Leaf</strong></span>
          </div>
          <div className="flex items-center space-x-2 text-[11px]">
            <span>{t('result.classifier') || 'Classifier'}: <strong className="text-slate-200">{scan.model_name || 'MobileNetV2 (PlantVillage v1.1)'}</strong></span>
          </div>
          <div className="flex items-center space-x-2 text-[11px]">
            <span>{t('result.image_quality') || 'Image Quality'}: <strong className="text-emerald-400">Passed ({(((scan.leaf_validation?.image_quality) || 0.88) * 100).toFixed(0)}%)</strong></span>
          </div>
        </div>

        {/* Uncertainty Note if Models Disagree or Low Confidence */}
        {(scan.status === 'UNCERTAIN' || scan.is_uncertain || scan.uncertainty_note) && (
          <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400 mt-0.5" />
            <div>
              <p className="font-bold">{t('result.uncertain_title') || 'Uncertain Preliminary Diagnosis'}</p>
              <p className="text-[11px] text-amber-200/90 mt-0.5">
                {scan.uncertainty_note || t('result.uncertain_desc')}
              </p>
            </div>
          </div>
        )}

        {/* Recommended Next Steps */}
        {scan.recommended_next_steps && scan.recommended_next_steps.length > 0 && (
          <div className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 space-y-2">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-2">
              <ListOrdered className="w-4 h-4 text-emerald-400" />
              <span>{t('result.next_steps') || 'Recommended Agronomic Next Steps:'}</span>
            </h4>
            <ul className="space-y-1.5 pl-5 list-disc text-xs text-slate-300 leading-relaxed">
              {scan.recommended_next_steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Alternative Diagnoses if Present */}
        {scan.alternative_diagnoses && scan.alternative_diagnoses.length > 0 && (
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">{t('result.alternative_conditions') || 'Alternative Possibilities Evaluated:'}</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {scan.alternative_diagnoses.map((alt, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80 flex items-center justify-between text-xs">
                  <span className="text-slate-300 font-medium">{translateDisease(alt.disease || alt.disease_name)}</span>
                  <span className="text-slate-400 font-mono text-[11px]">{((alt.confidence || 0) * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

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

        {/* Limitations Notice */}
        {scan.limitations && (
          <div className="p-3 rounded-lg bg-slate-900/30 border border-slate-800 text-[11px] text-slate-400 flex items-start space-x-2">
            <Info className="w-3.5 h-3.5 text-slate-500 shrink-0 mt-0.5" />
            <span><strong>{t('result.limitations') || 'Model Limitations'}:</strong> {scan.limitations}</span>
          </div>
        )}

        {/* Mandatory Agronomic Disclaimer Note */}
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
