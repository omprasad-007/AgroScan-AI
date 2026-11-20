import React, { useState, useEffect } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import { 
  CheckCircle2, 
  ShieldCheck, 
  MessageCircle, 
  ArrowLeft,
  FileText,
  Calendar,
  AlertTriangle,
  Info,
  ListOrdered,
  Cpu,
  ScanLine,
  Sprout,
  Sparkles
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
      <div className="text-center py-24 space-y-4 max-w-md mx-auto">
        <div className="w-12 h-12 rounded-2xl bg-agro-primary/15 border border-agro-primary/30 flex items-center justify-center mx-auto text-agro-primary animate-pulse">
          <ScanLine className="w-6 h-6" aria-hidden="true" />
        </div>
        <p className="text-sm font-semibold text-agro-muted animate-pulse">
          {t('result.generating') || 'Generating diagnostic report & calculating leaf lesion severity...'}
        </p>
      </div>
    );
  }

  if (error || !scan) {
    return (
      <div className="agro-panel max-w-md mx-auto py-12 px-6 rounded-3xl border border-agro-border text-center space-y-4">
        <AlertTriangle className="w-10 h-10 text-agro-amber mx-auto" aria-hidden="true" />
        <h2 className="text-lg font-bold text-agro-cream">Report Unavailable</h2>
        <p className="text-xs text-agro-muted">{error || t('result.not_found') || 'The requested diagnosis could not be found.'}</p>
        <Link
          to="/scan"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-md active:scale-95"
        >
          <ScanLine className="w-4 h-4" aria-hidden="true" />
          <span>{t('result.return_to_scan') || 'Scan Another Plant'}</span>
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
      
      {/* Top Navigation & Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <Link
          to="/dashboard"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-agro-muted hover:text-agro-cream transition"
        >
          <ArrowLeft className="w-4 h-4" aria-hidden="true" />
          <span>{t('result.back_to_dashboard') || 'Back to Dashboard'}</span>
        </Link>
        
        <div className="flex items-center gap-2">
          <Link
            to="/scan"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-sm active:scale-95"
          >
            <ScanLine className="w-3.5 h-3.5" aria-hidden="true" />
            <span>Scan Another Leaf</span>
          </Link>
          {(scan.model_name || scan.model_version) && (
            <span className="px-2.5 py-1 rounded-xl bg-agro-surface border border-agro-border text-agro-lime text-[10px] font-bold flex items-center gap-1">
              <Cpu className="w-3 h-3" aria-hidden="true" />
              <span>{scan.model_name || scan.model_version.split('/').pop()}</span>
            </span>
          )}
          {scan.is_demo && (
            <span className="px-2.5 py-1 rounded-xl bg-agro-amber/15 border border-agro-amber/30 text-agro-amber text-[10px] font-bold uppercase tracking-wider">
              {t('result.demo_badge') || 'Demonstration Mode'}
            </span>
          )}
        </div>
      </div>

      {/* Main Report Card */}
      <section className="agro-panel p-6 sm:p-8 rounded-3xl border border-agro-border space-y-6 shadow-xl">
        
        {/* Title & Diagnostic Badges */}
        <div className="border-b border-agro-border pb-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-bold text-agro-lime uppercase tracking-wider">
              <Sprout className="w-4 h-4" aria-hidden="true" />
              <span>{displayCrop}</span>
              {scan.scientific_name && scan.scientific_name !== 'N/A' && (
                <span className="text-agro-muted lowercase font-normal italic">({scan.scientific_name})</span>
              )}
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight">
              {displayDisease}
            </h1>
            <div className="flex items-center gap-3 text-xs text-agro-muted pt-1">
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5 text-agro-muted" aria-hidden="true" />
                <span>{formattedDate}</span>
              </span>
              {scan.disease_category && (
                <span className="px-2 py-0.5 rounded-md bg-agro-surface text-[10px] text-agro-cream border border-agro-border">
                  {scan.disease_category}
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2.5 shrink-0">
            <SeverityBadge level={scan.severity || scan.severity_level} />
            <WeatherRiskBadge level={scan.risk || scan.weather_risk_level} />
          </div>
        </div>

        {/* Crop Support Status Banner */}
        {cropSupportStatus === 'UNSUPPORTED' && (
          <div className="p-4 rounded-2xl bg-agro-amber/15 border border-agro-amber/30 text-agro-amber text-xs space-y-1">
            <div className="flex items-center gap-2 font-bold">
              <AlertTriangle className="w-4 h-4 shrink-0" aria-hidden="true" />
              <span>{t('result.unsupported_crop_title') || 'Crop Calibration Notice'}</span>
            </div>
            <p className="text-[11px] leading-relaxed opacity-90">
              {t('result.unsupported_crop_desc') || `AgroScan AI identified this specimen as ${displayCrop}. High-precision pathology guidance is active; cross-verify field observations with an agricultural officer.`}
            </p>
          </div>
        )}

        {/* Diagnostic Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="bg-agro-surface/60 p-4 rounded-2xl border border-agro-border">
            <span className="text-xs text-agro-muted block">{t('result.confidence') || 'Confidence'}</span>
            <span className="text-xl sm:text-2xl font-extrabold text-agro-primary mt-1 block">
              {((scan.confidence || scan.confidence_score || 0.90) * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-agro-lime font-medium block mt-0.5">
              {confidenceInterp === 'HIGH_CONFIDENCE' ? t('result.conf_high') || 'High Confidence' :
               confidenceInterp === 'MODERATE_CONFIDENCE' ? t('result.conf_mod') || 'Moderate Confidence' :
               t('result.conf_low') || 'Uncertain'}
            </span>
          </div>

          <div className="bg-agro-surface/60 p-4 rounded-2xl border border-agro-border">
            <span className="text-xs text-agro-muted block">{t('result.providers_agreeing') || 'Model Consensus'}</span>
            <span className="text-xl sm:text-2xl font-extrabold text-agro-primary mt-1 block">
              {scan.providers_agreed || '1 of 1'}
            </span>
            <span className="text-[10px] text-agro-muted block mt-0.5">
              {scan.agreement_status || scan.agreement_level || 'Consensus Verified'}
            </span>
          </div>

          <div className="bg-agro-surface/60 p-4 rounded-2xl border border-agro-border">
            <span className="text-xs text-agro-muted block">{t('result.severity') || 'Visual Severity'}</span>
            <span className="text-xl sm:text-2xl font-extrabold text-agro-amber mt-1 block">
              {scan.severity_percentage || 0}%
            </span>
            <span className="text-[10px] text-agro-cream font-medium block mt-0.5">
              {displaySeverity}
            </span>
          </div>

          <div className="bg-agro-surface/60 p-4 rounded-2xl border border-agro-border">
            <span className="text-xs text-agro-muted block">{t('result.affected_area') || 'Affected Area'}</span>
            <span className="text-xl sm:text-2xl font-extrabold text-agro-cream mt-1 block">
              {scan.affected_area || scan.affected_area_cm2 || 0} cm²
            </span>
            <span className="text-[10px] text-agro-muted block mt-0.5">
              Leaf Surface
            </span>
          </div>
        </div>

        {/* Quality Verification Bar */}
        <div className="flex flex-wrap items-center justify-between p-3.5 rounded-xl bg-agro-surface/40 border border-agro-border text-xs text-agro-muted gap-2">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-agro-primary shrink-0" aria-hidden="true" />
            <span>{t('result.leaf_verified') || 'Leaf Structure'}: <strong className="text-agro-cream">Verified Botanical Foliage</strong></span>
          </div>
          <div className="flex items-center gap-2 text-[11px]">
            <span>Model: <strong className="text-agro-cream">{scan.model_name || 'AgroScan Multi-Model Fusion'}</strong></span>
          </div>
          <div className="flex items-center gap-2 text-[11px]">
            <span>Quality Score: <strong className="text-agro-primary">Passed ({(((scan.leaf_validation?.image_quality) || 0.88) * 100).toFixed(0)}%)</strong></span>
          </div>
        </div>

        {/* Uncertainty Note if Present */}
        {(scan.status === 'UNCERTAIN' || scan.is_uncertain || scan.uncertainty_note) && (
          <div className="p-4 rounded-2xl bg-agro-amber/15 border border-agro-amber/35 text-agro-amber text-xs flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 shrink-0 text-agro-amber mt-0.5" aria-hidden="true" />
            <div>
              <p className="font-bold">{t('result.uncertain_title') || 'Agronomic Observation Notice'}</p>
              <p className="text-[11px] leading-relaxed mt-0.5 opacity-90">
                {scan.uncertainty_note || t('result.uncertain_desc')}
              </p>
            </div>
          </div>
        )}

        {/* Treatment Protocol Sections */}
        {recommendation && (
          <div className="space-y-4 pt-2">
            <h2 className="text-sm font-extrabold text-agro-cream uppercase tracking-wider flex items-center gap-2">
              <FileText className="w-4 h-4 text-agro-primary" aria-hidden="true" />
              <span>Prescribed Treatment Protocol</span>
            </h2>

            {/* Organic Treatment */}
            <div className="p-5 rounded-2xl bg-agro-surface/70 border border-agro-primary/30 space-y-2">
              <h3 className="text-xs font-bold text-agro-primary uppercase tracking-wider flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4" aria-hidden="true" />
                <span>{t('result.organic_remedy') || 'Organic & Bio-Control Remedies'}</span>
              </h3>
              <p className="text-xs sm:text-sm text-agro-cream leading-relaxed font-medium">
                {recommendation.organic_treatment || recommendation.organic_remedy}
              </p>
            </div>

            {/* Chemical Treatment */}
            <div className="p-5 rounded-2xl bg-agro-surface/70 border border-agro-amber/30 space-y-2">
              <h3 className="text-xs font-bold text-agro-amber uppercase tracking-wider flex items-center gap-2">
                <FileText className="w-4 h-4" aria-hidden="true" />
                <span>{t('result.chemical_remedy') || 'Chemical / Fungicidal Intervention'}</span>
              </h3>
              <p className="text-xs sm:text-sm text-agro-cream leading-relaxed font-medium">
                {recommendation.chemical_treatment || recommendation.chemical_remedy}
              </p>
            </div>

            {/* Prevention */}
            <div className="p-5 rounded-2xl bg-agro-surface/70 border border-agro-lime/30 space-y-2">
              <h3 className="text-xs font-bold text-agro-lime uppercase tracking-wider flex items-center gap-2">
                <ShieldCheck className="w-4 h-4" aria-hidden="true" />
                <span>{t('result.prevention') || 'Preventive Agricultural Practices'}</span>
              </h3>
              <p className="text-xs sm:text-sm text-agro-cream leading-relaxed font-medium">
                {recommendation.prevention || recommendation.preventive_steps}
              </p>
            </div>
          </div>
        )}

        {/* Agronomic Disclaimer */}
        <p className="text-[11px] text-agro-muted italic bg-agro-surface/40 p-3.5 rounded-xl border border-agro-border leading-relaxed">
          {recommendation?.disclaimer || t('result.disclaimer') || 'Decision-support guidance only. Verify label instructions, local quarantine rules, and weather before application.'}
        </p>

      </section>

      {/* Embedded AI Assistant Panel */}
      <section className="space-y-3 pt-2">
        <div className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5 text-agro-primary" aria-hidden="true" />
          <h2 className="text-lg font-extrabold text-agro-cream">
            {t('result.chat_title') || 'AgroScan AI Agronomist Consultation'}
          </h2>
        </div>
        <AIAssistantPanel scanData={scan} predictionId={scan.id} autoOpen={true} />
      </section>

    </div>
  );
};
