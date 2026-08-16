import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Scan, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  CloudSun, 
  TrendingUp, 
  ArrowRight,
  Activity
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

export const DashboardPage = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [analytics, setAnalytics] = useState(null);
  const [recentScans, setRecentScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [anRes, scRes] = await Promise.all([
          api.get('/analytics/dashboard'),
          api.get('/predictions/history?limit=5')
        ]);
        setAnalytics(anRes.data);
        setRecentScans(scRes.data);
      } catch (err) {
        console.error('Failed to load dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="space-y-6">
      
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            {t('dashboard.welcome')} {user?.full_name || user?.email?.split('@')[0] || 'Farmer'} 👋
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1 flex items-center space-x-2">
            <span className="text-emerald-400 font-semibold">{user?.email || 'user@gmail.com'}</span>
            <span>•</span>
            <span>Real-time crop disease diagnostics & weather outbreak monitoring</span>
          </p>
        </div>

        <Link
          to="/scan"
          className="inline-flex items-center justify-center space-x-2 px-5 py-3 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-sm transition shadow-lg shadow-agri-500/20 shrink-0"
        >
          <Scan className="w-4 h-4" />
          <span>{t('dashboard.quick_scan')}</span>
        </Link>
      </div>

      {/* Summary Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.total_scans')}</span>
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-white">{analytics?.total_predictions ?? 0}</span>
            <span className="text-xs text-slate-400 ml-2">recorded</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.healthy_scans')}</span>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-emerald-400">{analytics?.healthy_count ?? 0}</span>
            <span className="text-xs text-slate-400 ml-2">crops clean</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.diseased_scans')}</span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-amber-400">{analytics?.diseased_count ?? 0}</span>
            <span className="text-xs text-slate-400 ml-2">detected</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">{t('dashboard.avg_confidence')}</span>
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
              <TrendingUp className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-bold text-white">
              {((analytics?.average_confidence ?? 0) * 100).toFixed(1)}%
            </span>
            <span className="text-xs text-slate-400 ml-2">accuracy</span>
          </div>
        </div>

      </div>

      {/* Main Grid: Weather Risk & Recent Scans */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Weather Risk Card */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-1 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <CloudSun className="w-5 h-5 text-agri-400" />
                <h3 className="text-base font-bold text-white">Weather Disease Risk</h3>
              </div>
              <WeatherRiskBadge level={analytics?.weather_risk_summary?.overall_risk_level || 'High'} />
            </div>

            <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-3 mb-4">
              <div className="flex justify-between text-xs text-slate-300">
                <span>Temperature</span>
                <span className="font-semibold">{analytics?.weather_risk_summary?.current_temp || 26.5}°C</span>
              </div>
              <div className="flex justify-between text-xs text-slate-300">
                <span>Humidity</span>
                <span className="font-semibold">{analytics?.weather_risk_summary?.current_humidity || 82.0}%</span>
              </div>
            </div>

            <p className="text-xs text-amber-300/90 leading-relaxed bg-amber-500/10 p-3 rounded-xl border border-amber-500/20">
              {analytics?.weather_risk_summary?.alert || 'High relative humidity and warm temp promote fungal spore growth.'}
            </p>
          </div>

          <Link
            to="/weather"
            className="mt-6 flex items-center justify-center space-x-2 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 transition"
          >
            <span>Full Risk Forecast</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Recent Scans Table */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-white">{t('dashboard.recent_scans')}</h3>
            <Link to="/history" className="text-xs text-agri-400 hover:underline flex items-center space-x-1">
              <span>{t('dashboard.view_all')}</span>
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          {(!Array.isArray(recentScans) || recentScans.length === 0) ? (
            <div className="text-center py-10 text-slate-500 text-xs">
              No leaf scans recorded yet. Click "Quick Leaf Scan" to start your first analysis.
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400">
                    <th className="py-2.5 px-3">Crop</th>
                    <th className="py-2.5 px-3">Detected Disease</th>
                    <th className="py-2.5 px-3">Severity</th>
                    <th className="py-2.5 px-3">Confidence</th>
                    <th className="py-2.5 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {recentScans.map((scan) => (
                    <tr key={scan.id} className="hover:bg-slate-800/30 transition">
                      <td className="py-3 px-3 font-semibold text-white">{scan.crop_detected}</td>
                      <td className="py-3 px-3 text-slate-300">{scan.disease_name}</td>
                      <td className="py-3 px-3">
                        <SeverityBadge level={scan.severity_level} />
                      </td>
                      <td className="py-3 px-3 font-mono text-agri-400">
                        {(scan.confidence_score * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right">
                        <Link
                          to={`/results/${scan.id}`}
                          className="text-xs font-semibold text-agri-400 hover:underline"
                        >
                          View Report
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

    </div>
  );
};
