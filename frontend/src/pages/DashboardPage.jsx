import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { 
  Scan, 
  CheckCircle2, 
  AlertTriangle, 
  CloudSun, 
  TrendingUp, 
  ArrowRight,
  Activity,
  RotateCcw,
  Sparkles,
  Leaf,
  ShieldCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

const STORAGE_KEY = 'agroscan_scans_v1';

export const DashboardPage = () => {
  const { user } = useAuth();
  const { t, translateCrop, translateDisease } = useLanguage();
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
      let backendAnalytics = null;
      try {
        const [anRes, scRes] = await Promise.all([
          api.get('/analytics/dashboard').catch(() => ({ data: null })),
          api.get('/predictions/history?limit=20').catch(() => ({ data: [] }))
        ]);
        backendAnalytics = anRes?.data || null;
        backendScans = Array.isArray(scRes?.data) ? scRes.data : [];
      } catch (err) {
        console.warn('Backend dashboard fetch notice:', err);
      }

      // 3. Deduplicate and merge scans (localStorage takes precedence for newly analyzed offline/client items)
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

        // Determine overall risk
        const risks = allScans.map(s => s.weather_risk_level || s.risk || 'Low');
        let topRisk = 'Low';
        if (risks.includes('High') || risks.includes('high')) topRisk = 'High';
        else if (risks.includes('Moderate') || risks.includes('moderate')) topRisk = 'Moderate';

        const latestScan = allScans[0];
        const latestCrop = latestScan.crop_detected || latestScan.plant || 'Crop';
        const latestDisease = latestScan.disease_name || latestScan.disease || 'Analyzed';

        setAnalytics({
          total_predictions: total,
          healthy_count: healthy,
          diseased_count: diseased,
          average_confidence: avgConf,
          weather_risk_summary: {
            overall_risk_level: topRisk,
            current_temp: latestScan.ambient_temp_c || 26.5,
            current_humidity: latestScan.humidity_pct || 75.0,
            alert: `Latest scan: ${latestCrop} (${latestDisease}) — Risk evaluated based on farm microclimate.`
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

    // Listen to custom scan completion and storage events
    const handleScanEvent = () => refreshDashboardData();
    window.addEventListener('agroscan_scan_completed', handleScanEvent);
    window.addEventListener('storage', handleScanEvent);

    return () => {
      window.removeEventListener('agroscan_scan_completed', handleScanEvent);
      window.removeEventListener('storage', handleScanEvent);
    };
  }, [refreshDashboardData]);

  const handleResetData = () => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      window.dispatchEvent(new Event('agroscan_scan_completed'));
      setShowResetModal(false);
      refreshDashboardData();
    } catch (e) {
      console.error('Failed to reset dashboard data:', e);
    }
  };

  const isBlank = (analytics.total_predictions === 0);

  return (
    <div className="space-y-6">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            {t('dashboard.title')} — {user?.full_name || user?.email?.split('@')[0] || t('header.role_farmer')} 👋
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 flex items-center space-x-2">
            <span className="text-emerald-400 font-semibold">{user?.email || 'farmer@agroscan.ai'}</span>
            <span>•</span>
            <span>{t('dashboard.subtitle')}</span>
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {!isBlank && (
            <button
              onClick={() => setShowResetModal(true)}
              className="inline-flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-slate-800/80 hover:bg-red-500/20 text-slate-300 hover:text-red-400 border border-slate-700/60 hover:border-red-500/30 text-xs font-semibold transition"
              title={t('dashboard.reset_data')}
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>{t('dashboard.reset_data')}</span>
            </button>
          )}

          <Link
            to="/scan"
            className="inline-flex items-center justify-center space-x-2 px-5 py-2.5 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-sm transition shadow-lg shadow-agri-500/20 shrink-0"
          >
            <Scan className="w-4 h-4" />
            <span>{t('dashboard.quick_scan')}</span>
          </Link>
        </div>
      </div>

      {/* Summary Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Total Scans Card */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.card_total')}</span>
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-white">{analytics.total_predictions}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-mono text-slate-400">
                Avg: {Math.round(analytics.average_confidence * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Healthy Crops Card */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.card_healthy')}</span>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-emerald-400">{analytics.healthy_count}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-semibold text-emerald-400/80">
                {Math.round((analytics.healthy_count / analytics.total_predictions) * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Diseased Crops Card */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.card_diseased')}</span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-baseline justify-between">
            <span className="text-3xl font-extrabold text-amber-400">{analytics.diseased_count}</span>
            {analytics.total_predictions > 0 && (
              <span className="text-[11px] font-semibold text-amber-400/80">
                {Math.round((analytics.diseased_count / analytics.total_predictions) * 100)}%
              </span>
            )}
          </div>
        </div>

        {/* Outbreak Risk Card */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.card_risk')}</span>
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3 flex items-center">
            {isBlank ? (
              <span className="px-2.5 py-1 rounded-lg bg-slate-800 border border-slate-700 text-slate-400 text-xs font-semibold">
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
        <div className="glass-panel p-8 rounded-3xl border border-emerald-500/20 bg-gradient-to-r from-emerald-950/30 via-slate-900 to-slate-900 shadow-xl relative overflow-hidden">
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-3 text-center md:text-left max-w-xl">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Real-time Local Storage & Diagnostics Active</span>
              </div>
              <h2 className="text-xl sm:text-2xl font-black text-white">
                {t('dashboard.empty_title') || 'Dashboard is Blank — Ready for Your First Scan'}
              </h2>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                {t('dashboard.blank_desc')}
              </p>
            </div>

            <Link
              to="/scan"
              className="inline-flex items-center space-x-2.5 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-500 to-agri-400 text-slate-950 font-black text-sm transition hover:scale-105 shadow-xl shadow-emerald-500/20 shrink-0"
            >
              <Leaf className="w-4 h-4" />
              <span>{t('dashboard.blank_cta')}</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}

      {/* Main Grid: Weather Risk & Recent Scans */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Weather Risk Card */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-1 flex flex-col justify-between border border-slate-800/80">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <CloudSun className="w-5 h-5 text-agri-400" />
                <h3 className="text-base font-bold text-white">{t('nav.weather')}</h3>
              </div>
              <WeatherRiskBadge level={analytics.weather_risk_summary?.overall_risk_level || 'Low'} />
            </div>

            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-3 mb-4">
              <div className="flex justify-between text-xs text-slate-300">
                <span>{t('dashboard.temperature') || 'Temperature'}</span>
                <span className="font-semibold">{analytics.weather_risk_summary?.current_temp || 26.5}°C</span>
              </div>
              <div className="flex justify-between text-xs text-slate-300">
                <span>{t('dashboard.humidity') || 'Humidity'}</span>
                <span className="font-semibold">{analytics.weather_risk_summary?.current_humidity || 65.0}%</span>
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed bg-slate-900/40 p-3 rounded-xl border border-slate-800">
              {analytics.weather_risk_summary?.alert || t('dashboard.empty_msg')}
            </p>
          </div>

          <Link
            to="/weather"
            className="mt-6 flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition"
          >
            <span>{t('history.view_report') || 'Full Risk Forecast'}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Recent Scans Table */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2 border border-slate-800/80">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-white">{t('dashboard.recent_scans') || t('nav.history')}</h3>
            {recentScans.length > 0 && (
              <Link to="/history" className="text-xs text-agri-400 hover:underline flex items-center space-x-1">
                <span>{t('dashboard.view_all') || 'View All'}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            )}
          </div>

          {recentScans.length === 0 ? (
            <div className="text-center py-12 px-4 space-y-3">
              <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-500 flex items-center justify-center mx-auto">
                <Scan className="w-6 h-6" />
              </div>
              <p className="text-slate-400 text-xs font-semibold">
                {t('dashboard.empty_title') || 'No scans recorded yet'}
              </p>
              <p className="text-slate-500 text-[11px] max-w-sm mx-auto">
                {t('dashboard.empty_msg') || 'Scan a plant leaf to start tracking disease outbreak risk and health metrics.'}
              </p>
              <Link
                to="/scan"
                className="inline-flex items-center space-x-2 mt-2 px-4 py-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold transition"
              >
                <Leaf className="w-3.5 h-3.5" />
                <span>{t('dashboard.blank_cta')}</span>
              </Link>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                    <th className="py-2.5 px-3">{t('history.col_crop') || 'Crop'}</th>
                    <th className="py-2.5 px-3">{t('history.col_disease') || 'Detected Disease'}</th>
                    <th className="py-2.5 px-3">{t('history.col_severity') || 'Severity'}</th>
                    <th className="py-2.5 px-3">{t('history.col_confidence') || 'Confidence'}</th>
                    <th className="py-2.5 px-3 text-right">{t('history.col_report') || 'Action'}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {recentScans.map((scan) => (
                    <tr key={scan.id} className="hover:bg-slate-800/30 transition">
                      <td className="py-3 px-3 font-semibold text-white">
                        {translateCrop(scan.crop_detected || scan.plant)}
                      </td>
                      <td className="py-3 px-3 text-slate-300">
                        {translateDisease(scan.disease_name || scan.disease)}
                      </td>
                      <td className="py-3 px-3">
                        <SeverityBadge level={scan.severity_level || scan.severity} />
                      </td>
                      <td className="py-3 px-3 font-mono text-agri-400">
                        {(((Number(scan.confidence_score ?? scan.confidence)) || 0.9) * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right">
                        <Link
                          to={`/results/${scan.id}`}
                          className="text-xs font-semibold text-agri-400 hover:underline"
                        >
                          {t('history.view_report') || 'View Report'}
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>

      {/* Reset Confirmation Modal */}
      {showResetModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="glass-panel max-w-md w-full p-6 rounded-3xl border border-red-500/30 space-y-4 shadow-2xl">
            <div className="flex items-center space-x-3 text-red-400">
              <div className="p-2 rounded-xl bg-red-500/10 border border-red-500/20">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">{t('dashboard.reset_data')}</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {t('dashboard.reset_confirm')}
            </p>
            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowResetModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleResetData}
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-xs font-bold text-white transition shadow-lg shadow-red-600/20"
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
