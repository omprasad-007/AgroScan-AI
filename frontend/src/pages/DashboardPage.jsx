import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { 
  ScanLine, 
  CheckCircle2, 
  AlertTriangle, 
  CloudSun, 
  TrendingUp, 
  ArrowRight,
  Activity,
  RotateCcw,
  Sparkles,
  Leaf,
  ShieldCheck,
  MapPin
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import { detectLocalWeather } from '../services/weather';
import api from '../services/api';

const STORAGE_KEY = 'agroscan_scans_v1';

export const DashboardPage = () => {
  const { user } = useAuth();
  const { t, translateCrop, translateDisease, lang } = useLanguage();
  const [localWeather, setLocalWeather] = useState(null);
  const [analytics, setAnalytics] = useState({
    total_predictions: 0,
    healthy_count: 0,
    diseased_count: 0,
    average_confidence: 0,
    weather_risk_summary: {
      overall_risk_level: 'None',
      current_temp: 26.5,
      current_humidity: 65.0,
      alert: ''
    }
  });
  const [recentScans, setRecentScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showResetModal, setShowResetModal] = useState(false);

  // Compute stats and merge localStorage with backend
  const refreshDashboardData = useCallback(async () => {
    try {
      // 1. Read from localStorage
      let localScans = [];
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) localScans = JSON.parse(raw);
        if (!Array.isArray(localScans)) localScans = [];
      } catch (e) {
        console.warn('Failed to parse localStorage scans:', e);
        localScans = [];
      }

      // 2. Fetch from backend API
      let backendScans = [];
      try {
        const [anRes, scRes] = await Promise.all([
          api.get('/analytics/dashboard').catch(() => ({ data: null })),
          api.get('/predictions/history?limit=20').catch(() => ({ data: [] }))
        ]);
        backendScans = Array.isArray(scRes?.data) ? scRes.data : [];
      } catch (err) {
        console.warn('Backend dashboard fetch notice:', err);
      }

      // 3. Deduplicate and merge scans
      const mergedMap = new Map();
      localScans.forEach(s => { if (s && s.id) mergedMap.set(s.id, s); });
      backendScans.forEach(s => { if (s && s.id && !mergedMap.has(s.id)) mergedMap.set(s.id, s); });

      const allScans = Array.from(mergedMap.values()).sort((a, b) => {
        const dateA = new Date(a.created_at || a.timestamp || 0).getTime();
        const dateB = new Date(b.created_at || b.timestamp || 0).getTime();
        return dateB - dateA;
      });

      // Keep localStorage in sync with the clean merged list
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allScans));
      } catch (e) {
        console.warn('Sync to localStorage failed:', e);
      }

      // 4. Compute analytics dynamically
      const total = allScans.length;
      if (total === 0) {
        setAnalytics({
          total_predictions: 0,
          healthy_count: 0,
          diseased_count: 0,
          average_confidence: 0,
          weather_risk_summary: {
            overall_risk_level: 'None',
            current_temp: 26.5,
            current_humidity: 65.0,
            alert: t('dashboard.blank_desc') || 'Your dashboard is currently blank. Upload or capture a plant leaf photo to generate live diagnostics.'
          }
        });
        setRecentScans([]);
      } else {
        const healthy = allScans.filter(s => {
          const disease = (s.disease_name || s.disease || '').toLowerCase();
          const sev = (s.severity_level || s.severity || '').toLowerCase();
          return disease.includes('healthy') || sev === 'healthy';
        }).length;
        const diseased = total - healthy;
        
        const confSum = allScans.reduce((sum, s) => {
          const c = Number(s.confidence_score ?? s.confidence ?? 0.9);
          return sum + (isNaN(c) ? 0.9 : c);
        }, 0);
        const avgConf = total > 0 ? (confSum / total) : 0;

        const risks = allScans.map(s => s.weather_risk_level || s.risk || 'Low');
        let topRisk = 'Low';
        if (risks.some(r => String(r).toLowerCase().includes('high') || String(r).toLowerCase().includes('critical'))) {
          topRisk = 'High';
        } else if (risks.some(r => String(r).toLowerCase().includes('med') || String(r).toLowerCase().includes('mod'))) {
          topRisk = 'Moderate';
        }

        const latest = allScans[0];
        setAnalytics({
          total_predictions: total,
          healthy_count: healthy,
          diseased_count: diseased,
          average_confidence: avgConf,
          weather_risk_summary: {
            overall_risk_level: topRisk,
            current_temp: latest.ambient_temp_c || 26.5,
            current_humidity: latest.humidity_pct || 65.0,
            alert: `Active monitoring for ${latest.crop_detected || latest.plant || 'Crops'} (${latest.disease_name || latest.disease || 'General Health'}).`
          }
        });
        setRecentScans(allScans.slice(0, 5));
      }
    } catch (err) {
      console.error('Failed to compute dashboard metrics:', err);
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    refreshDashboardData();

    const handleScanEvent = () => refreshDashboardData();
    window.addEventListener('agroscan_scan_completed', handleScanEvent);
    window.addEventListener('storage', handleScanEvent);

    return () => {
      window.removeEventListener('agroscan_scan_completed', handleScanEvent);
      window.removeEventListener('storage', handleScanEvent);
    };
  }, [refreshDashboardData]);

  useEffect(() => {
    detectLocalWeather(lang)
      .then(w => {
        if (w) setLocalWeather(w);
      })
      .catch(() => {});
  }, [lang]);

  const handleResetData = async () => {
    try {
      setShowResetModal(false);
      localStorage.removeItem(STORAGE_KEY);
      localStorage.setItem(STORAGE_KEY, '[]');
      setRecentScans([]);
      setAnalytics({
        total_predictions: 0,
        healthy_count: 0,
        diseased_count: 0,
        average_confidence: 0,
        weather_risk_summary: {
          overall_risk_level: 'None',
          current_temp: 26.5,
          current_humidity: 65.0,
          alert: t('dashboard.blank_desc') || 'Your dashboard is currently blank. Upload or capture a plant leaf photo to generate live diagnostics.'
        }
      });
      try {
        await api.delete('/predictions/history');
      } catch (e) {
        console.warn('Backend reset call notice:', e);
      }
      window.dispatchEvent(new Event('agroscan_scan_completed'));
    } catch (e) {
      console.error('Failed to reset dashboard data:', e);
    }
  };

  const isBlank = (analytics.total_predictions === 0);

  return (
    <div className="space-y-6">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight font-heading">
            {t('dashboard.title')} — {user?.full_name || user?.email?.split('@')[0] || t('header.role_farmer')}
          </h1>
          <p className="text-xs sm:text-sm text-agro-muted flex items-center gap-2">
            <span className="text-agro-primary font-semibold">{user?.email || 'farmer@agroscan.ai'}</span>
            <span>•</span>
            <span>{t('dashboard.subtitle')}</span>
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {!isBlank && (
            <button
              type="button"
              onClick={() => setShowResetModal(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-primary/10 text-agro-muted hover:text-agro-primary border border-agro-border hover:border-agro-primary/30 text-xs font-semibold transition"
              title={t('dashboard.reset_data')}
            >
              <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
              <span>{t('dashboard.reset_data')}</span>
            </button>
          )}

          {/* Strong Primary CTA: Start New Scan */}
          <Link
            to="/scan"
            className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-extrabold text-sm transition shadow-lg shadow-orange-glow active:scale-[0.98] shrink-0"
          >
            <ScanLine className="w-4 h-4 shrink-0" aria-hidden="true" />
            <span>{t('nav.scan') || 'Start New Scan'}</span>
          </Link>
        </div>
      </div>

      {/* Summary Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Scans Card */}
        <div className="agro-panel bg-agro-card p-5 rounded-2xl border border-agro-border">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-agro-muted">{t('dashboard.card_total')}</span>
            <div className="p-2 rounded-xl bg-agro-primary/10 text-agro-primary border border-agro-primary/25">
              <Activity className="w-4 h-4" aria-hidden="true" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-agro-cream">{analytics.total_predictions}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-mono text-agro-highlight font-semibold">
                Avg: {Math.round(analytics.average_confidence * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Healthy Crops Card */}
        <div className="agro-panel bg-agro-card p-5 rounded-2xl border border-agro-border">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-agro-muted">{t('dashboard.card_healthy')}</span>
            <div className="p-2 rounded-xl bg-agro-accent/15 text-agro-accent border border-agro-accent/30">
              <ShieldCheck className="w-4 h-4" aria-hidden="true" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-agro-accent">{analytics.healthy_count}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-semibold text-agro-accent">
                {Math.round((analytics.healthy_count / analytics.total_predictions) * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Diseased Crops Card */}
        <div className="agro-panel bg-agro-card p-5 rounded-2xl border border-agro-border">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-agro-muted">{t('dashboard.card_diseased')}</span>
            <div className="p-2 rounded-xl bg-agro-primary/15 text-agro-primary border border-agro-primary/30">
              <AlertTriangle className="w-4 h-4" aria-hidden="true" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-agro-primary">{analytics.diseased_count}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-semibold text-agro-primary">
                {Math.round((analytics.diseased_count / analytics.total_predictions) * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Outbreak Risk Card */}
        <div className="agro-panel bg-agro-card p-5 rounded-2xl border border-agro-border">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-agro-muted">{t('dashboard.card_risk')}</span>
            <div className="p-2 rounded-xl bg-agro-highlight/15 text-agro-highlight border border-agro-highlight/30">
              <TrendingUp className="w-4 h-4" aria-hidden="true" />
            </div>
          </div>
          <div className="mt-3 flex items-center">
            {isBlank ? (
              <span className="px-2.5 py-1 rounded-lg bg-agro-surface border border-agro-border text-agro-muted text-xs font-semibold">
                No Outbreak Active
              </span>
            ) : (
              <WeatherRiskBadge level={analytics.weather_risk_summary?.overall_risk_level || 'Low'} />
            )}
          </div>
        </div>

      </div>

      {/* If Blank: Show Hero Blank State Banner */}
      {isBlank && (
        <div className="agro-panel p-8 rounded-3xl border border-agro-primary/30 bg-agro-card shadow-xl relative overflow-hidden">
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-3 text-center md:text-left max-w-xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-agro-primary/10 border border-agro-primary/30 text-agro-primary text-xs font-bold">
                <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
                <span>Ready for Crop Diagnosis</span>
              </div>
              <h2 className="text-xl sm:text-2xl font-extrabold text-agro-cream font-heading">
                Protect your crops with real-time AI pathology
              </h2>
              <p className="text-xs sm:text-sm text-agro-muted leading-relaxed">
                {analytics.weather_risk_summary?.alert}
              </p>
            </div>

            <Link
              to="/scan"
              className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-2xl bg-agro-primary hover:bg-agro-primaryHover text-white font-extrabold text-sm transition shadow-lg shadow-orange-glow shrink-0 active:scale-[0.98]"
            >
              <Leaf className="w-4 h-4" aria-hidden="true" />
              <span>{t('dashboard.blank_cta')}</span>
              <ArrowRight className="w-4 h-4" aria-hidden="true" />
            </Link>
          </div>
        </div>
      )}

      {/* Main Grid: Weather Risk & Recent Scans */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Weather Risk Card */}
        <div className="agro-panel bg-agro-card p-6 rounded-3xl lg:col-span-1 flex flex-col justify-between border border-agro-border">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <CloudSun className="w-5 h-5 text-agro-highlight" aria-hidden="true" />
                <h3 className="text-base font-bold text-agro-cream font-heading">{t('nav.weather')}</h3>
              </div>
              <WeatherRiskBadge level={analytics.weather_risk_summary?.overall_risk_level || 'Low'} />
            </div>

            {/* Local Farm Weather Location */}
            {localWeather && (
              <div className="mb-3 px-3 py-2 rounded-xl bg-agro-surface border border-agro-border flex items-center justify-between">
                <div className="flex items-center gap-2 text-xs">
                  <MapPin className="w-3.5 h-3.5 text-agro-primary shrink-0" aria-hidden="true" />
                  <span className="font-bold text-agro-cream truncate max-w-[140px]">
                    {localWeather.location}
                  </span>
                </div>
                <span className="inline-flex items-center text-[10px] text-agro-primary font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-agro-primary animate-pulse mr-1" />
                  {localWeather.isGpsDetected ? 'Live GPS' : 'District'}
                </span>
              </div>
            )}

            <div className="bg-agro-surface p-4 rounded-xl border border-agro-border space-y-3 mb-4">
              <div className="flex justify-between text-xs text-agro-muted">
                <span>{t('dashboard.temperature') || 'Temperature'}</span>
                <span className="font-bold text-agro-cream">{localWeather?.temperature_c ?? analytics.weather_risk_summary?.current_temp ?? 26.5}°C</span>
              </div>
              <div className="flex justify-between text-xs text-agro-muted">
                <span>{t('dashboard.humidity') || 'Humidity'}</span>
                <span className="font-bold text-agro-cream">{localWeather?.humidity_pct ?? analytics.weather_risk_summary?.current_humidity ?? 65.0}%</span>
              </div>
              {localWeather?.condition && (
                <div className="flex justify-between text-xs text-agro-muted pt-1 border-t border-agro-border">
                  <span>Conditions</span>
                  <span className="text-agro-highlight font-semibold">{localWeather.condition}</span>
                </div>
              )}
            </div>

            <p className="text-xs text-agro-muted leading-relaxed bg-agro-surface p-3 rounded-xl border border-agro-border">
              {analytics.weather_risk_summary?.alert || t('dashboard.empty_msg')}
            </p>
          </div>

          <Link
            to="/weather"
            className="mt-6 inline-flex items-center justify-center gap-2 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-xs font-semibold text-agro-cream transition"
          >
            <span>{t('history.view_report') || 'Full Risk Forecast'}</span>
            <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
          </Link>
        </div>

        {/* Recent Scans Table */}
        <div className="agro-panel bg-agro-card p-6 rounded-3xl lg:col-span-2 border border-agro-border">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-agro-cream font-heading">{t('dashboard.recent_scans') || t('nav.history')}</h3>
            {recentScans.length > 0 && (
              <Link to="/history" className="text-xs text-agro-primary hover:underline inline-flex items-center gap-1 font-semibold">
                <span>{t('dashboard.view_all') || 'View All'}</span>
                <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
              </Link>
            )}
          </div>

          {recentScans.length === 0 ? (
            <div className="text-center py-12 px-4 space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-agro-surface border border-agro-border text-agro-muted flex items-center justify-center mx-auto">
                <ScanLine className="w-6 h-6" aria-hidden="true" />
              </div>
              <p className="text-agro-cream text-xs font-bold">
                {t('dashboard.empty_title') || 'No scans recorded yet'}
              </p>
              <p className="text-agro-muted text-[11px] max-w-sm mx-auto">
                {t('dashboard.empty_msg') || 'Scan a plant leaf to start tracking disease outbreak risk and health metrics.'}
              </p>
              <Link
                to="/scan"
                className="inline-flex items-center gap-2 mt-2 px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-sm"
              >
                <Leaf className="w-3.5 h-3.5" aria-hidden="true" />
                <span>{t('dashboard.blank_cta')}</span>
              </Link>
            </div>
          ) : (
            <>
              {/* Mobile Stacked Cards for Recent Scans (< sm) */}
              <div className="block sm:hidden space-y-3">
                {recentScans.map((scan) => (
                  <div
                    key={scan.id}
                    className="p-3.5 rounded-xl bg-agro-surface border border-agro-border space-y-2 transition-all shadow-sm"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-agro-cream text-xs">
                        {translateCrop(scan.crop_detected || scan.plant)}
                      </span>
                      <SeverityBadge level={scan.severity_level || scan.severity} />
                    </div>
                    <div className="text-xs text-agro-muted">
                      {translateDisease(scan.disease_name || scan.disease)}
                    </div>
                    <div className="flex items-center justify-between pt-1.5 border-t border-agro-border text-xs">
                      <span className="font-mono text-agro-primary font-bold">
                        {(((Number(scan.confidence_score ?? scan.confidence)) || 0.9) * 100).toFixed(1)}%
                      </span>
                      <Link
                        to={`/results/${scan.id}`}
                        className="text-xs font-bold text-agro-primary hover:underline inline-flex items-center gap-1"
                      >
                        <span>{t('history.view_report') || 'View Report'}</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>

              {/* Desktop Table (>= sm) */}
              <div className="hidden sm:block overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-agro-border text-agro-muted font-bold">
                      <th className="py-2.5 px-3">{t('history.col_crop') || 'Crop'}</th>
                      <th className="py-2.5 px-3">{t('history.col_disease') || 'Detected Disease'}</th>
                      <th className="py-2.5 px-3">{t('history.col_severity') || 'Severity'}</th>
                      <th className="py-2.5 px-3">{t('history.col_confidence') || 'Confidence'}</th>
                      <th className="py-2.5 px-3 text-right">{t('history.col_report') || 'Action'}</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-agro-border">
                    {recentScans.map((scan) => (
                      <tr key={scan.id} className="hover:bg-agro-surface/60 transition-colors">
                        <td className="py-3 px-3 font-bold text-agro-cream">
                          {translateCrop(scan.crop_detected || scan.plant)}
                        </td>
                        <td className="py-3 px-3 text-agro-muted">
                          {translateDisease(scan.disease_name || scan.disease)}
                        </td>
                        <td className="py-3 px-3">
                          <SeverityBadge level={scan.severity_level || scan.severity} />
                        </td>
                        <td className="py-3 px-3 font-mono text-agro-primary font-bold">
                          {(((Number(scan.confidence_score ?? scan.confidence)) || 0.9) * 100).toFixed(1)}%
                        </td>
                        <td className="py-3 px-3 text-right">
                          <Link
                            to={`/results/${scan.id}`}
                            className="text-xs font-bold text-agro-primary hover:underline"
                          >
                            {t('history.view_report') || 'View Report'}
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>

      </div>

      {/* Reset Confirmation Modal */}
      {showResetModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-agro-bg/80 backdrop-blur-sm">
          <div className="agro-panel bg-agro-card max-w-md w-full p-6 sm:p-7 rounded-3xl border border-agro-primary/40 space-y-4 shadow-2xl">
            <div className="flex items-center gap-3 text-agro-primary">
              <div className="p-2.5 rounded-xl bg-agro-primary/15 border border-agro-primary/30">
                <AlertTriangle className="w-5 h-5" aria-hidden="true" />
              </div>
              <h3 className="text-base font-bold text-agro-cream font-heading">{t('dashboard.reset_data')}</h3>
            </div>
            <p className="text-xs text-agro-muted leading-relaxed">
              {t('dashboard.reset_confirm') || 'Are you sure you want to clear scan records? The dashboard will return to a fresh blank state.'}
            </p>
            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowResetModal(false)}
                className="px-4 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-xs font-semibold text-agro-muted hover:text-agro-cream transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleResetData}
                className="px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-xs font-bold text-white transition shadow-md shadow-orange-glow"
              >
                Confirm Reset (Clear)
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
